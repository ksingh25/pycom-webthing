SSID = 'freebox_kd'
PASSWORD = 'bird206206'

if SSID == '':
    print('Please edit config.py and set the SSID and password')
    raise ValueError('SSID not set')