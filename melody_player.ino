// Statements prefixed with "#" are known as precompiler directives, and they modify the source code before
// compilation. This particular one, #include, will insert the contents of the header file on the right into
// the location of the #include directive.
#include "melody.hpp"
#include "songs.hpp"

// Indicates the pin on the Arduino to which the buzzer is connected.
constexpr uint8_t BUZZER_PIN = 8;

constexpr uint8_t FORCE_SENSOR_PIN = A0;

constexpr int FORCE_THRESHOLD = 200;
constexpr unsigned long DEBOUNCE_DELAY_MILLIS = 200;

bool shouldPlayMelody = false;
bool lastState = false;
unsigned long lastDebounceTime = 0;

void setup() {
  // Where was Serial.begin #included from, you may ask? The answer is the header file declaring it is automatically
  // #included at the top as a feature of the Arduino system.
  // Serial allows a device connected to the USB port to communicate with the Arduino. Serial.begin() opens that
  // connection and sets the number of bits per second (baud) data will be sent. 9600 baud is usually good.
  Serial.begin(9600);
}

void loop() {
  // Read values from the force sensor
  int force = analogRead(FORCE_SENSOR_PIN);
  bool currentState = force > 500;
  // Debounce the state. This ensures that small fluctuations in the force on the
  // sensor don't cause erratic behavior.
  // See https://docs.arduino.cc/built-in-examples/digital/Debounce/ for more info.
  if (currentState == lastState) {
    if ((millis() - lastDebounceTime) > DEBOUNCE_DELAY_MILLIS) {
      shouldPlayMelody = currentState;
      lastState = shouldPlayMelody;
    }
  } else {
    lastDebounceTime = millis();
    lastState = currentState;
  }

  if (shouldPlayMelody) {
    playMelody(BUZZER_PIN, THRILLER);
    shouldPlayMelody = false;
  }
}
