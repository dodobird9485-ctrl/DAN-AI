#include <Arduino.h>
#include <WiFi.h>

// Define a function to scan for WiFi networks
void scanNetworks() {
  Serial.println("** WiFi Network Scan **");

  // WiFi.scanNetworks will return the number of networks found
  int numNetworks = WiFi.scanNetworks();

  if (numNetworks == 0) {
    Serial.println("No networks found.");
  } else {
    Serial.print("Found ");
    Serial.print(numNetworks);
    Serial.println(" networks.");

    // Print the SSID and RSSI for each network found
    for (int i = 0; i < numNetworks; i++) {
      Serial.print(i + 1);
      Serial.print(": ");
      Serial.print(WiFi.SSID(i));
      Serial.print(" (");
      Serial.print(WiFi.RSSI(i));
      Serial.print("dBm)");
      Serial.println((WiFi.encryptionType(i) == WIFI_AUTH_OPEN)?" ":"*"); // Indicate if network is open or secured
      delay(10); // Add a small delay to avoid overwhelming the serial output
    }
  }
}

void setup() {
  Serial.begin(115200); // Initialize serial communication
  delay(1000); // Wait for serial monitor to open

  WiFi.mode(WIFI_STA); // Set WiFi to station mode (client mode)
  WiFi.disconnect(); // Disconnect from any previous WiFi connection
  delay(100); // Wait for disconnection
}

void loop() {
  scanNetworks(); // Call the scanNetworks function
  delay(10000); // Wait 10 seconds before scanning again
}