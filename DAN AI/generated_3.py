```arduino
#include <WiFi.h>

void setup() {
  Serial.begin(115200);
  Serial.println("ESP32 WiFi Scanner");

  WiFi.mode(WIFI_STA); // Set WiFi to station mode (scan only)
  WiFi.disconnect();   // Disconnect from any previous network
  delay(100);

  Serial.println("Scanning WiFi networks...");
}

void loop() {
  int n = WiFi.scanNetworks(); // Scan for available networks

  if (n == 0) {
    Serial.println("No WiFi networks found.");
  } else {
    Serial.print(n);
    Serial.println(" networks found:");
    for (int i = 0; i < n; ++i) {
      // Print SSID and RSSI for each network found
      Serial.print(i + 1);
      Serial.print(": ");
      Serial.print(WiFi.SSID(i));
      Serial.print(" (");
      Serial.print(WiFi.RSSI(i));
      Serial.print("dBm)");
      Serial.println((WiFi.encryptionType(i) == WIFI_AUTH_OPEN)?" Unsecured":" Secured");
      delay(10);
    }
  }
  Serial.println("Scan complete. Waiting 10 seconds...");
  delay(10000); // Wait 10 seconds before rescanning
}
```