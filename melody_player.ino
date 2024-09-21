// Statements prefixed with "#" are known as precompiler directives, and they modify the source code before
// compilation. This particular one, #include, will insert the contents of the header file on the right into
// the location of the #include directive.
#include "melody.hpp"
#include "songs.hpp"

// Indicates the pin on the Arduino to which the buzzer is connected.
const int BUZZER_PIN = 8;

// Ensures the melody plays only once
bool shouldPlayMelody = true;

void setup() {
  // Where was Serial.begin #included from, you may ask? The answer is the header file declaring it is automatically
  // #included at the top as a feature of the Arduino system.
  // Serial allows a device connected to the USB port to communicate with the Arduino. Serial.begin() opens that
  // connection and sets the number of bits per second (baud) data will be sent. 9600 baud is usually good.
  Serial.begin(9600);
}

void loop() {
  if (shouldPlayMelody) { // If we haven't played the melody yet...
    // The playMelody function was #included from melody.hpp. If the implementation is changed down the road, we don't
    // need to do anything in this file unless the signature changed.
    playMelody(BUZZER_PIN, GOOD_OLD_SONG_EXTENDED);  // ...play it...
    // 
    shouldPlayMelody = false;  // ...and then indicate we've already played it.
  }
}
