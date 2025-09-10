#include <WiFi.h>
#include <Firebase_ESP_Client.h>
#include <TinyGPS++.h>
#include <Adafruit_MPU6050.h>
#include <Adafruit_Sensor.h>
#include <Wire.h>
#include <FirebaseJson.h>

// Edge Impulse includes placeholder (add your code here)
#include "addons/TokenHelper.h"

#define WIFI_SSID "Wifi has left the chat"
#define WIFI_PASSWORD "Jaguar08"

#define API_KEY "AIzaSyBZodTPYfYuDJdmP06Y-BfcDox1dONJ_GU"
#define DATABASE_URL "https://toddletrack-fd848-default-rtdb.asia-southeast1.firebasedatabase.app"

#define USER_EMAIL "subhalakshmibalakrishnan88@gmail.com"
#define USER_PASSWORD "jaguar08"

HardwareSerial gpsSerial(2);
TinyGPSPlus gps;
Adafruit_MPU6050 mpu;

FirebaseData fbdo;
FirebaseAuth auth;
FirebaseConfig config;

bool alert = false;

void setup() {
  Serial.begin(115200);
  while (!Serial) delay(10);

  // Initialize MPU6050
  if (!mpu.begin()) {
    Serial.println("Failed to find MPU6050 chip");
    while (1) { delay(10); }
  }
  mpu.setAccelerometerRange(MPU6050_RANGE_8_G);
  mpu.setGyroRange(MPU6050_RANGE_500_DEG);
  mpu.setFilterBandwidth(MPU6050_BAND_21_HZ);

  // Initialize GPS serial (pins RX=16, TX=17)
  gpsSerial.begin(9600, SERIAL_8N1, 16, 17);

  // Wi-Fi connect
  WiFi.begin(WIFI_SSID, WIFI_PASSWORD);
  Serial.print("Connecting to Wi-Fi");
  while (WiFi.status() != WL_CONNECTED) {
    delay(500);
    Serial.print(".");
  }
  Serial.println("\nWiFi connected");

  // Firebase init
  config.api_key = API_KEY;
  config.database_url = DATABASE_URL;
  auth.user.email = USER_EMAIL;
  auth.user.password = USER_PASSWORD;
  Firebase.begin(&config, &auth);
  Firebase.reconnectWiFi(true);
}

void loop() {
  // Read GPS data
  while (gpsSerial.available() > 0) {
    gps.encode(gpsSerial.read());
  }

  // Read MPU6050 data
  sensors_event_t a, g, temp;
  mpu.getEvent(&a, &g, &temp);

  // Simple threshold check for abnormal movement (modify thresholds based on your EI model)
  // Example: if acceleration on any axis exceeds 15 m/s^2 (~1.5g), trigger alert
  alert = (abs(a.acceleration.x) > 15.0 || abs(a.acceleration.y) > 15.0 || abs(a.acceleration.z) > 15.0);

  if (gps.location.isValid()) {
    float latitude = gps.location.lat();
    float longitude = gps.location.lng();

    Serial.printf("Lat: %f, Lon: %f, Alert: %s\n", latitude, longitude, alert ? "YES" : "NO");

    FirebaseJson json;
    json.set("latitude", latitude);
    json.set("longitude", longitude);
    json.set("accel_x", a.acceleration.x);
    json.set("accel_y", a.acceleration.y);
    json.set("accel_z", a.acceleration.z);
    json.set("gyro_x", g.gyro.x);
    json.set("gyro_y", g.gyro.y);
    json.set("gyro_z", g.gyro.z);
    json.set("alert", alert);

    if (Firebase.RTDB.updateNode(&fbdo, "/child_id_001/data", json)) {
      Serial.println("Data uploaded successfully");
    } else {
      Serial.printf("Firebase upload failed: %s\n", fbdo.errorReason().c_str());
    }

    delay(5000);
  }
}

