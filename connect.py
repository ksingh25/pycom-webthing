import machine
import network
import config
import time
from network import WLAN


def connect_to_ap():
    station = WLAN(mode=WLAN.STA)
#    if not station.active():
  #      station.active(True)
    if not station.isconnected():
        print('Connecting....')
        station.connect(config.SSID, auth=(WLAN.WPA2, config.PASSWORD), timeout=5000)
        while not station.isconnected():
            time.sleep(1)
            print('.', end='')
        print("connected")
        print(station.ifconfig())
 #   print('ifconfig =', station.ifconfig())
