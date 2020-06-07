# Pycom-webthing. 

It allows to convert a pycom-pysense module into a webthing in line with W3C 
standard on Web of Things. 

It uses libraries from 
https://github.com/mozilla-iot/webthing-upy
and
https://github.com/loboris/MicroPython_ESP32_psRAM_LoBo/wiki/microWebSrv

To run it

1. Configure the WiFi password in config.py
2. Upload the files to pycom-pysense module
3. Find the ip address obtained
4. Connect to the webthing on your browser http://ip address//
5. You can interact with it using curl tool (in case ip address was as follows)

For example to change the color of RGB LED to any color (color = 13209 here) :

`curl -d '{"color": 13209}' -X PUT http://192.168.0.17/0/properties/color`

If you want to make the LED OFF

`curl -d '{"color": 0}' -X PUT http://192.168.0.17/0/properties/color`

TODO :
 - actions are not working as the code is incomplete.
