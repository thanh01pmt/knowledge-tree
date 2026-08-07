/*
 * Smart Bulb ESP32-S3 Firmware
 * Điều khiển LED WS2812 qua REST API + MQTT
 */
#include <WiFi.h>
#include <WebServer.h>
#include <ArduinoJson.h>
#include <Adafruit_NeoPixel.h>
#include <PubSubClient.h>

// Cấu hình WiFi
const char* WIFI_SSID = "YOUR_WIFI";
const char* WIFI_PASS = "YOUR_PASS";

// Cấu hình MQTT
const char* MQTT_HOST = "192.168.1.100";
const int MQTT_PORT = 1883;
const char* MQTT_TOPIC_STATE = "smartbulb/state";
const char* MQTT_TOPIC_CMD = "smartbulb/cmd";

// LED WS2812
#define LED_PIN 48
#define LED_COUNT 30
Adafruit_NeoPixel strip(LED_COUNT, LED_PIN, NEO_GRB + NEO_KHZ800);

// Trạng thái đèn
bool bulbOn = false;
int brightness = 100;
uint8_t r = 255, g = 255, b = 255;
String effect = "none";

WebServer server(80);
WiFiClient wifiClient;
PubSubClient mqttClient(wifiClient);

// ============ REST API Handlers ============

void handleGetState() {
  StaticJsonDocument<256> doc;
  doc["isOn"] = bulbOn;
  doc["brightness"] = brightness;
  doc["red"] = r;
  doc["green"] = g;
  doc["blue"] = b;
  doc["effect"] = effect;
  String response;
  serializeJson(doc, response);
  server.send(200, "application/json", response);
}

void handleSetPower() {
  if (server.hasArg("plain")) {
    StaticJsonDocument<128> doc;
    deserializeJson(doc, server.arg("plain"));
    bulbOn = doc["isOn"] | false;
    updateLED();
  }
  handleGetState();
}

void handleSetBrightness() {
  if (server.hasArg("plain")) {
    StaticJsonDocument<128> doc;
    deserializeJson(doc, server.arg("plain"));
    brightness = doc["brightness"] | 100;
    updateLED();
  }
  handleGetState();
}

void handleSetColor() {
  if (server.hasArg("plain")) {
    StaticJsonDocument<128> doc;
    deserializeJson(doc, server.arg("plain"));
    r = doc["red"] | 255;
    g = doc["green"] | 255;
    b = doc["blue"] | 255;
    updateLED();
  }
  handleGetState();
}

void handleSetEffect() {
  if (server.hasArg("plain")) {
    StaticJsonDocument<128> doc;
    deserializeJson(doc, server.arg("plain"));
    effect = doc["effect"] | "none";
    updateLED();
  }
  handleGetState();
}

// ============ MQTT ============

void mqttCallback(char* topic, byte* payload, unsigned int length) {
  String message;
  for (unsigned int i = 0; i < length; i++) {
    message += (char)payload[i];
  }
  StaticJsonDocument<128> doc;
  deserializeJson(doc, message);
  if (doc.containsKey("isOn")) bulbOn = doc["isOn"];
  if (doc.containsKey("brightness")) brightness = doc["brightness"];
  if (doc.containsKey("red")) r = doc["red"];
  if (doc.containsKey("green")) g = doc["green"];
  if (doc.containsKey("blue")) b = doc["blue"];
  if (doc.containsKey("effect")) effect = doc["effect"].as<String>();
  updateLED();
  publishState();
}

void publishState() {
  StaticJsonDocument<256> doc;
  doc["isOn"] = bulbOn;
  doc["brightness"] = brightness;
  doc["red"] = r;
  doc["green"] = g;
  doc["blue"] = b;
  doc["effect"] = effect;
  char buffer[256];
  serializeJson(doc, buffer);
  mqttClient.publish(MQTT_TOPIC_STATE, buffer);
}

// ============ LED ============

void updateLED() {
  if (!bulbOn) {
    strip.clear();
    strip.show();
    return;
  }
  if (effect == "breathe") {
    // Hiệu ứng thở: tăng/giảm độ sáng
    for (int i = 0; i < LED_COUNT; i++) {
      strip.setPixelColor(i, strip.Color(r * brightness / 100, g * brightness / 100, b * brightness / 100));
    }
  } else if (effect == "rainbow") {
    // Hiệu ứng cầu vồng
    for (int i = 0; i < LED_COUNT; i++) {
      strip.setPixelColor(i, wheel((i * 256 / LED_COUNT) & 255));
    }
  } else {
    for (int i = 0; i < LED_COUNT; i++) {
      strip.setPixelColor(i, strip.Color(r * brightness / 100, g * brightness / 100, b * brightness / 100));
    }
  }
  strip.show();
}

uint32_t wheel(byte wheelPos) {
  wheelPos = 255 - wheelPos;
  if (wheelPos < 85) return strip.Color(255 - wheelPos * 3, 0, wheelPos * 3);
  if (wheelPos < 170) {
    wheelPos -= 85;
    return strip.Color(0, wheelPos * 3, 255 - wheelPos * 3);
  }
  wheelPos -= 170;
  return strip.Color(wheelPos * 3, 255 - wheelPos * 3, 0);
}

// ============ Setup ============

void setup() {
  Serial.begin(115200);
  strip.begin();
  strip.show();

  // Kết nối WiFi
  WiFi.begin(WIFI_SSID, WIFI_PASS);
  while (WiFi.status() != WL_CONNECTED) {
    delay(500);
    Serial.print(".");
  }
  Serial.println("\nWiFi connected: " + WiFi.localIP().toString());

  // REST API routes
  server.on("/api/state", HTTP_GET, handleGetState);
  server.on("/api/power", HTTP_POST, handleSetPower);
  server.on("/api/brightness", HTTP_POST, handleSetBrightness);
  server.on("/api/color", HTTP_POST, handleSetColor);
  server.on("/api/effect", HTTP_POST, handleSetEffect);
  server.begin();

  // MQTT
  mqttClient.setServer(MQTT_HOST, MQTT_PORT);
  mqttClient.setCallback(mqttCallback);
  mqttClient.connect("smartbulb-esp32");
  mqttClient.subscribe(MQTT_TOPIC_CMD);
}

void loop() {
  server.handleClient();
  if (mqttClient.connected()) {
    mqttClient.loop();
  } else {
    mqttClient.connect("smartbulb-esp32");
    mqttClient.subscribe(MQTT_TOPIC_CMD);
  }
  delay(10);
}
