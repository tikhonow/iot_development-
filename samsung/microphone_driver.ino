#include "VolAnalyzer.h"

#define MICROPHONE_PIN (34)
#define MIN_VOLUME (0)
#define MAX_VOLUME (100)

const int sampleSize = 100;  // Количество выборок для вычисления RMS
const float V_ref = 200.0f;

VolAnalyzer analyzer(MICROPHONE_PIN);

float raw_volume = 0;

void microphone_init()
{
  pinMode(MICROPHONE_PIN, INPUT);
  analyzer.setAmpliK(10);
}

float microphone_get_volume()
{
  if (analyzer.tick())
  {
    raw_volume = analyzer.getMax();
  }
  // return raw_volume;

  // float adcValues[sampleSize];  // Массив для хранения выборок АЦП
  // float sum = 0.0;

  // for (int i = 0; i < sampleSize; i++) {
  //   adcValues[i] = analogRead(MICROPHONE_PIN);
  //   delay(1);  // Задержка для обеспечения стабильности выборок
  // }

  // for (int i = 0; i < sampleSize; i++) {
  //   raw_volume += adcValues[i];
  // }
  // raw_volume /= sampleSize;

  float SPL_dB = 20 * log10(raw_volume / V_ref) + 55;

  return SPL_dB;
}