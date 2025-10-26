/*
    sketch.ino
    Basic HID setup for Raspberry Pi Pico (Arduino core)

    - Uses Arduino Keyboard HID (make sure your board/core supports USB HID)
    - Initializes HID interface; optionally send a test string once after enumeration
*/

#include <Arduino.h>
#include <USBKeyboard.h>

USBKeyboard key;

void setup()
{
}
void loop()
{
    // Keep the MCU running with HID active. Do any HID actions from here.
    delay(1000);
    key.printf("Hello World\r\n");
}