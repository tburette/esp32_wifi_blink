ESP32 wifi blink
================

Blinks the ESP32 LED depending on wifi and internet availability.

Permanent led = internet access is working
Slow blinking = wifi access but no internet access
Fast blinking = neither internet nor wifi


Usage
=====
Create a wifi_credentials file with the ssid on the first line and password on the second line (nothing else).


Put the python files along with wifi_credentials on the ESP32 (with ampy for instance).

Restart the ESP32.
