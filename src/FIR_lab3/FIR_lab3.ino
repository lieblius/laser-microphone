#include <Audio.h>
#include <Wire.h>
#include <SD.h>
#include <SPI.h>
#include <SerialFlash.h>
#include "band_pass.h"

#define LED 13

const int myInput = AUDIO_INPUT_LINEIN;


AudioInputI2S         audioInput;         // audio shield: mic or line-in
AudioFilterFIR        myFilter;
AudioOutputI2S        audioOutput;        // audio shield: headphones & line-out

// Create Audio connections between the components
AudioConnection f_in(audioInput, 0, myFilter, 0);
AudioConnection f_out(myFilter, 0, audioOutput, 0);
AudioControlSGTL5000 audioShield;

struct fir_filter {
  short *coeffs;
  short num_coeffs;    // num_coeffs must be an even number, 4 or higher
};

struct fir_filter filt = {BP, 224};


void setup() {
  Serial.begin(9600);
  delay(300);
  pinMode(LED, OUTPUT);

  // allocate memory for the audio library
  AudioMemory(8);
  audioShield.enable();
  audioShield.volume(0.6);

  // Initialize the filter
  myFilter.begin(filt.coeffs, filt.num_coeffs);
}


void loop()
{
}
