"""Blinks the ESP32 LED depending on wifi and internet availability

permanent led = internet access is working
slow blinking = wifi access but no internet access
fast blinking = neither internet nor wifi
"""

import network
import time
import urequests
from machine import Pin

pin_22 = Pin(22, Pin.OUT)


def led_on():
    pin_22.value(0)


def led_off():
    pin_22.value(1)


# todo multithread / async
def led_blink(duration=30, blink_duration=1):
    if blink_duration == 0:
        led_on()
        time.sleep(duration)
        led_off()
    else:
        loop_until = time.time() + duration
        while time.time() < loop_until:
            led_on()
            time.sleep(blink_duration)
            led_off()
            time.sleep(blink_duration)


def has_internet():
    try:
        urequests.get('http://www.httpbin.org/ip')
    except Exception as e:
        # Should catch the correct exceptions but it is not clear
        # what might be thrown here
        print(e)
        return False
    else:
        return True


def read_wifi_credentials():
    """Reads wifi ssid and its password from the file wifi_credentials

    Assumes that the content of the file is the ssid on the first line
    and password on the second line with no other content
    """
    with open('wifi_credentials') as f:
        return f.read().strip().splitlines()


def wlan_connect():
    wlan.connect(ssid, password)


def wlan_reconnect():
    # I have seen a case where wifi is up but there is no internet
    # access until the wifi connection is reset
    wlan.disconnect()
    # No idea if this is needed
    time.sleep(1)
    wlan_connect()


ssid, password = read_wifi_credentials()
print(ssid, password)

wlan = network.WLAN(network.STA_IF)
wlan.active(True)

while True:
    # if not wlan.isconnected():
    #     wlan_connect()
    #     led_blink(duration=1,blink_duration=0.04)
    #     print('connecting')
    #     # give some time to the ESP32 to connect
    #     time.sleep(5)

    if not wlan.isconnected():
        print('no wifi')
        wlan_reconnect()
        led_blink(duration=9, blink_duration=0.4)
    elif not has_internet():
        print('wifi no internet')
        wlan_reconnect()
        led_blink(duration=9)
    else:
        print('internet OK')
        led_blink(blink_duration=0)
