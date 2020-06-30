# Pycom-webthing. 

It allows to convert a pycom-pysense module (https://pycom.io/) into a webthing in line with W3C 
standard on Web of Things. The code was tested with Lopy4 + PySense sensor module.

It uses  
https://github.com/mozilla-iot/webthing-upy
and
https://github.com/loboris/MicroPython_ESP32_psRAM_LoBo/wiki/microWebSrv

To run it

1. Configure your WiFi SSID and password in config.py
2. Upload the files to pycom-pysense module using Atom or VScode (see http://docs.pycom.io)
3. Find the ip address obtained by pycom. For example scanning for IP addresses in your network using nmap and testing with ping. Another way is to stop the pycom program with Ctrl+C and 

`>>> from network import WLAN`

`>>> WLAN.ifconfig()`

4. To check the Things Description (TD), connect to the webthing on your browser http://ip address//
5. You can interact with it using curl tool (assuming that the ip address was 192.168.0.17)

For example to change the color of RGB LED to any color (color = 13209 here) :

`curl -d '{"color": 13209}' -X PUT http://192.168.0.17/0/properties/color`
(on windows the command is slightly different:)
`curl -d "{"color": 13209}" -H "Content-Type: application/json" -X PUT http://192.168.0.17/0/properties/color`

If you want to make the LED OFF

`curl -d '{"color": 0}' -X PUT http://192.168.0.17/0/properties/color`
(on windows the command is slightly different:)
`curl -d "{"color": 0}" -H "Content-Type: application/json" -X PUT http://192.168.0.17/0/properties/color`

You can read the temperature using your browser or using curl

`curl -X GET http://192.168.0.17/0/properties/temperature`

TODO :
 - actions are not working as the code is incomplete.
