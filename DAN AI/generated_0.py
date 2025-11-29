```cpp
#include <WiFi.h>

void setup() {
  Serial.begin(115200);

  WiFi.mode(WIFI_STA);  // Set WiFi to station mode (scan only)
  WiFi.disconnect();    // Disconnect from any previous network
  delay(100);

  Serial.println("Setup done");
}

void loop() {
  Serial.println("Scanning WiFi networks...");

  int n = WiFi.scanNetworks();  // Scan for available networks

  if (n == 0) {
    Serial.println("No networks found");
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
      Serial.print(" Channel: ");
      Serial.print(WiFi.channel(i));
      Serial.print(" Encryption: ");
      Serial.println(WiFi.encryptionType(i));
      delay(10);
    }
  }
  Serial.println("Scan done");

  delay(10000); // Wait 10 seconds before scanning again
}
```