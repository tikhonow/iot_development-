#include <WiFi.h>
#include <ArduinoJson.h>
#include <JC_Button.h>
#include "EspMQTTClient.h"

#define BUTTON_PIN (26)

#define PUB_DELAY (3 * 1000)
#define MQTT_SERVER_HOST  "dev.rightech.io"
#define MQTT_CLIENT_ID    ""
#define WIFI_SSID  ""
#define WIFI_PASSWORD ""

long last = 0;

EspMQTTClient client(
  WIFI_SSID,
  WIFI_PASSWORD,
  MQTT_SERVER_HOST,
  "",
  "",
  MQTT_CLIENT_ID
);

Button mainButton(BUTTON_PIN, 50);

extern uint32_t volume_db;
extern uint32_t speed;

void wifi_init()
{
  // WiFi.mode(WIFI_STA);
  // WiFi.begin(ssid, password);
  // Serial.print("Connecting to WiFi ..");
  // while (WiFi.status() != WL_CONNECTED) {
  //   Serial.print('.');
  //   delay(1000);
  // }
  // Serial.println(WiFi.localIP());
}

void wifi_update()
{
  StaticJsonDocument<200> doc;
  doc["sensor"] = "noise";
  doc["volume"] = volume_db;
  doc["speed"] = speed;
  // serializeJsonPretty(doc, Serial);
}

void publishVolume() {
  long now = millis();
  if (client.isConnected() && (now - last > PUB_DELAY)) {
    client.publish("base/state/noise", String(volume_db));
    client.publish("base/state/speed", String(speed));
    last = now;
  }
}

void setup() {
  Serial.begin(115200);
  mainButton.begin();
  microphone_init();
  screen_init();
  // wifi_init();
}

void loop() {
  mainButton.read();
  screen_update();
  // wifi_update();
  client.loop();
  publishVolume();

  if (mainButton.wasPressed())
  {
    Serial.println("yoooo");
  }
}