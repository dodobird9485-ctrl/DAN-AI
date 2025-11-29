#include <Arduino.h>
#include <WiFi.h>
#include <HTTPClient.h>

// WiFi credentials - REPLACE WITH YOUR ACTUAL CREDENTIALS
const char* ssid = "YOUR_WIFI_SSID";
const char* password = "YOUR_WIFI_PASSWORD";

// Server details - REPLACE WITH YOUR SERVER DETAILS
const char* serverName = "http://your-server-ip/data"; // Example: "http://192.168.1.100/data"

// Game data structure (example) - ADJUST BASED ON ENLISTED'S DATA STRUCTURE
struct GameData {
  float playerX;
  float playerY;
  float playerZ;
  float enemyX;
  float enemyY;
  float enemyZ;
};

GameData gameData;

// Function to connect to WiFi
void connectWiFi() {
  Serial.print("Connecting to WiFi...");
  WiFi.begin(ssid, password);

  while (WiFi.status() != WL_CONNECTED) {
    delay(500);
    Serial.print(".");
  }

  Serial.println("Connected to WiFi");
  Serial.print("IP address: ");
  Serial.println(WiFi.localIP());
}

// Function to fetch game data from the server
bool fetchGameData() {
  HTTPClient http;

  // Specify the URL
  http.begin(serverName);

  // Start connection and send HTTP request
  int httpCode = http.GET();

  // Check HTTP return code
  if (httpCode > 0) {
    Serial.printf("[HTTP] GET... code: %d\n", httpCode);

    // HTTP header has been send and Server response header has been read
    if (httpCode == HTTP_CODE_OK) {
      String payload = http.getString();
      Serial.println(payload);

      // Parse the JSON payload - REPLACE WITH YOUR ACTUAL PARSING LOGIC
      // This is a VERY basic example, you'll need a proper JSON library
      // and error checking.  Assumes data is comma separated: px,py,pz,ex,ey,ez
      int commaIndex1 = payload.indexOf(',');
      int commaIndex2 = payload.indexOf(',', commaIndex1 + 1);
      int commaIndex3 = payload.indexOf(',', commaIndex2 + 1);
      int commaIndex4 = payload.indexOf(',', commaIndex3 + 1);
      int commaIndex5 = payload.indexOf(',', commaIndex4 + 1);

      if (commaIndex1 > 0 && commaIndex2 > 0 && commaIndex3 > 0 && commaIndex4 > 0 && commaIndex5 > 0) {
        try {
          gameData.playerX = payload.substring(0, commaIndex1).toFloat();
          gameData.playerY = payload.substring(commaIndex1 + 1, commaIndex2).toFloat();
          gameData.playerZ = payload.substring(commaIndex2 + 1, commaIndex3).toFloat();
          gameData.enemyX = payload.substring(commaIndex3 + 1, commaIndex4).toFloat();
          gameData.enemyY = payload.substring(commaIndex4 + 1, commaIndex5).toFloat();
          gameData.enemyZ = payload.substring(commaIndex5 + 1).toFloat();

          Serial.print("Player X: "); Serial.println(gameData.playerX);
          Serial.print("Enemy Z: "); Serial.println(gameData.enemyZ);
          return true;
        } catch (...) {
          Serial.println("Error parsing data");
          return false;
        }
      } else {
        Serial.println("Invalid data format");
        return false;
      }
    }
  } else {
    Serial.printf("[HTTP] GET... failed, error: %s\n", http.errorToString(httpCode).c_str());
    return false;
  }

  http.end();
  return false;
}

void setup() {
  Serial.begin(115200);
  connectWiFi();
}

void loop() {
  // Fetch game data
  if (fetchGameData()) {
    // Process game data and display ESP information (e.g., on a small screen)
    // This is where you would use the gameData to drive your ESP features.
    // Example: Display enemy distance on a small OLED screen.
    Serial.println("Data fetched successfully");
  } else {
    Serial.println("Failed to fetch data");
  }

  delay(100); // Adjust delay as needed
}