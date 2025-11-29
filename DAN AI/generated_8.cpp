#include <WiFi.h>

void setup() {
  Serial.begin(115200);

  WiFi.mode(WIFI_STA); // Set WiFi to station mode to scan networks
  WiFi.disconnect();    // Disconnect from any previous WiFi connection
  delay(100);

  Serial.println("Scanning available networks...");
}

void loop() {
  try {
    int n = WiFi.scanNetworks(); // Scan for available WiFi networks

    if (n == 0) {
      Serial.println("No networks found");
    } else {
      Serial.print(n);
      Serial.println(" networks found:");
      for (int i = 0; i < n; ++i) {
        // Print network information
        Serial.print(i + 1);
        Serial.print(": ");
        Serial.print(WiFi.SSID(i)); // Network name
        Serial.print(" (");
        Serial.print(WiFi.RSSI(i)); // Signal strength
        Serial.print("dBm)");
        Serial.print(" ");
        Serial.println((WiFi.encryptionType(i) == WIFI_AUTH_OPEN) ? "Open" : "Secured"); // Encryption type
        delay(10);
      }
    }
    WiFi.scanDelete(); // Delete the scan result to free memory
  } catch (...) {
    Serial.println("An error occurred during WiFi scanning.");
  }
  delay(5000); // Wait 5 seconds before scanning again
}