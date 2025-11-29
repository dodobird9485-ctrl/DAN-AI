# Enlisted ESP

A basic ESP overlay for the game Enlisted.  This is a conceptual example and bypassing anti-cheat systems is unethical and potentially illegal.  This code is for educational purposes only and should not be used in a live game environment.

## Disclaimer

**This project is for educational purposes only.  Using this code in a live game environment may violate the game's terms of service and could result in a ban.**

## Requirements

*   Python 3.6 or higher
*   `pip install -r requirements.txt`
*   DXcam
*   YOLOv3 weights (`yolov3.weights`) and configuration (`yolov3.cfg`) files.  These are NOT included in this repository due to their size.  You will need to download them separately from a trusted source (e.g., the official YOLO website or a reputable computer vision resource).

## Setup

1.  Clone this repository.
2.  Install the required Python packages using `pip install -r requirements.txt`.
3.  Download the YOLOv3 weights (`yolov3.weights`) and configuration (`yolov3.cfg`) files and place them in the `config/` directory.
4.  Configure the `config/config.ini` file to match your desired settings:
    *   `TARGET_WINDOW_NAME`: The name of the Enlisted window (usually "Enlisted").
    *   `BOX_COLOR`: The color of the bounding boxes in R,G,B format (e.g., "255,0,0" for red).
    *   `BOX_THICKNESS`: The thickness of the bounding boxes.
    *   `CONFIDENCE_THRESHOLD`: The minimum confidence score for a detected object to be displayed.

## Running the ESP

1.  Run the `src/main.py` script: `python src/main.py`
2.  The ESP overlay will appear on top of the Enlisted window.
3.  Press 'q' to quit.

## Important Notes

*   This ESP is a very basic implementation and may not be very accurate.
*   The performance of the ESP will depend on your hardware.
*   **This ESP is NOT guaranteed to be undetectable by EAC.  Use at your own risk.**
*   This project uses DXcam for screen capture, which is generally faster and more efficient than other methods like `mss`.  However, DXcam requires a compatible graphics card and driver.
*   The `yolov3.weights` and `yolov3.cfg` files are not included in this repository due to their size. You must download them separately.  Be sure to download them from a trusted source.
*   The code includes basic error handling, but it may not be exhaustive.  More robust error handling may be necessary for production use.
*   The ESP uses a separate thread for screen capture and object detection to improve performance.  However, threading can introduce its own set of challenges, such as race conditions and deadlocks.  Care should be taken when modifying the threading code.
