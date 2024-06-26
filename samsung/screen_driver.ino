#include <Adafruit_GFX.h>    // Core graphics library
#include <Adafruit_ST7789.h> // Hardware-specific library for ST7735
#include <SPI.h>

#define TFT_CS        (14)
#define TFT_RST        (15)
#define TFT_DC         (32)

#define DISPLAY_BL (5)

Adafruit_ST7789 tft = Adafruit_ST7789(TFT_CS, TFT_DC, TFT_RST);

static const uint8_t SCREEN_WIDTH = 280;
static const uint8_t SCREEN_HEIGHT = 240;

static const uint8_t MIN_RADIUS = 12;
static const uint8_t MAX_RADIUS = 36;
static uint8_t current_radius = MIN_RADIUS;

static uint8_t current_height = 0;

static uint32_t change_radius_last_time = millis();
static const uint32_t CHANGE_RADIUS_TIME = 1000;

static const uint16_t GRADIENT_STEP = 100;

uint32_t volume_db = 0;
char volume_str[16];

extern float raw_volume;
uint32_t speed = 0;

void screen_init()
{
  pinMode(DISPLAY_BL, OUTPUT);
  digitalWrite(DISPLAY_BL, HIGH);

  tft.init(240, 280);
  tft.setRotation(45);
  tft.fillScreen(ST77XX_WHITE);
}

void screen_update()
{
  volume_db = microphone_get_volume();
  if (millis() - change_radius_last_time >= CHANGE_RADIUS_TIME)
  {
    itoa(volume_db, volume_str, 10);
    draw_text(volume_str, ST77XX_BLACK);
    change_radius_last_time = millis();

    tft.setRotation(90);
    if (0 <= raw_volume && raw_volume < 500)
    {
      draw_emoji(":)", ST77XX_BLACK);
      speed = 1;
    }
    else if (500 <= raw_volume && raw_volume < 1000)
    {
      draw_emoji(":l", ST77XX_BLACK);
      speed = 2;
    }
    else if (1000 <= raw_volume && raw_volume < 4000)
    {
      draw_emoji(":(", ST77XX_BLACK);
      speed = 3;
    }
    tft.setRotation(45);
  }
}

void draw_text(char *text, uint16_t color) {
  tft.fillRect(30, 30, 300, 60, ST77XX_WHITE);
  tft.setCursor(30, 30);
  tft.setTextColor(color);
  tft.setTextWrap(false);
  tft.setTextSize(8);
  tft.print(text);
}

void draw_emoji(char *text, uint16_t color) {
  tft.fillRect(120, 120, 100, 60, ST77XX_WHITE);
  tft.setCursor(120, 120);
  tft.setTextColor(color);
  tft.setTextWrap(false);
  tft.setTextSize(8);
  tft.print(text);
}