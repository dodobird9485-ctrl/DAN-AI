# main.py
import cv2
import numpy as np
import dxcam
import time
import threading
import configparser

# Configuration
config = configparser.ConfigParser()
config.read('config/config.ini')

# Read configurations
TARGET_WINDOW_NAME = config['Settings']['TARGET_WINDOW_NAME']
BOX_COLOR = tuple(map(int, config['Settings']['BOX_COLOR'].split(',')))
BOX_THICKNESS = int(config['Settings']['BOX_THICKNESS'])
CONFIDENCE_THRESHOLD = float(config['Settings']['CONFIDENCE_THRESHOLD'])

# Global variables
boxes = []
confidences = []
classes = []

# Initialize DXcam
camera = dxcam.create(output_idx=0, output_color="BGR", max_buffer_len=10)

def load_yolo():
    """Loads the YOLOv3 model."""
    net = cv2.dnn.readNet('config/yolov3.weights', 'config/yolov3.cfg')
    classes = []
    with open('config/coco.names', 'r') as f:
        classes = [line.strip() for line in f.readlines()]
    layers_names = net.getLayerNames()
    output_layers = [layers_names[i - 1] for i in net.getUnconnectedOutLayers()]
    return net, classes, output_layers


def detect_objects(img, net, output_layers):
    """Detects objects in the given image using YOLOv3."""
    global boxes, confidences, classes
    height, width, channels = img.shape

    blob = cv2.dnn.blobFromImage(img, 0.00392, (416, 416), (0, 0, 0), True, crop=False)
    net.setInput(blob)
    outs = net.forward(output_layers)

    boxes = []
    confidences = []
    classes = []

    for out in outs:
        for detection in out:
            scores = detection[5:]
            class_id = np.argmax(scores)
            confidence = scores[class_id]
            if confidence > CONFIDENCE_THRESHOLD:
                center_x = int(detection[0] * width)
                center_y = int(detection[1] * height)
                w = int(detection[2] * width)
                h = int(detection[3] * height)

                x = int(center_x - w / 2)
                y = int(center_y - h / 2)

                boxes.append([x, y, w, h])
                confidences.append(float(confidence))
                classes.append(class_id)


def draw_boxes(img, classes, boxes, confidences, class_names):
    """Draws bounding boxes around detected objects."""
    indexes = cv2.dnn.NMSBoxes(boxes, confidences, CONFIDENCE_THRESHOLD, 0.4)

    if len(indexes) > 0:
        for i in indexes.flatten():
            x, y, w, h = boxes[i]
            label = str(class_names[classes[i]])
            confidence = str(round(confidences[i], 2))
            color = BOX_COLOR  # Use configured color
            cv2.rectangle(img, (x, y), (x + w, y + h), color, BOX_THICKNESS) # Use configured thickness
            cv2.putText(img, label + " " + confidence, (x, y - 5), cv2.FONT_HERSHEY_SIMPLEX, 0.5, color, 2)


def capture_and_process():
    """Captures the screen, detects objects, and draws bounding boxes."""
    global boxes, confidences, classes
    while True:
        try:
            image = camera.grab()
            if image is not None:
                detect_objects(image, net, output_layers)
                draw_boxes(image, classes, boxes, confidences, class_names)
                cv2.imshow("Enlisted ESP", image)
                if cv2.waitKey(1) & 0xFF == ord('q'):
                    break
            else:
                time.sleep(0.01) # Prevent busy-waiting
        except Exception as e:
            print(f"Error in capture and process loop: {e}")
            time.sleep(1) # Wait before retrying


if __name__ == "__main__":
    try:
        net, class_names, output_layers = load_yolo()
        camera.start(target_fps=30, region=None) # Capture full screen

        capture_thread = threading.Thread(target=capture_and_process)
        capture_thread.daemon = True  # Allow main thread to exit
        capture_thread.start()

        capture_thread.join()  # Wait for the capture thread to finish (or be interrupted)

    except Exception as e:
        print(f"An error occurred: {e}")
    finally:
        camera.stop()
        cv2.destroyAllWindows()
