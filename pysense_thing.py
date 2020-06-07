from action import Action
from event import Event
from property import Property
from thing import Thing
from value import Value
from server import SingleThing, MultipleThings, WebThingServer
import logging
import time
import machine
import pycom
import gc
from machine import Timer

from pysense import Pysense
from LIS2HH12 import LIS2HH12
from SI7006A20 import SI7006A20
from LTR329ALS01 import LTR329ALS01
from MPL3115A2 import MPL3115A2, ALTITUDE, PRESSURE

py = Pysense()
si = SI7006A20(py)
lt = LTR329ALS01(py)
li = LIS2HH12(py)

class SetRGBColor(Action):

    def __init__(self, thing, input_):
        Action.__init__(self, uuid.uuid4().hex, thing, 'setrgbcolor', input_=input_)

    def perform_action(self):
        self.thing.set_property('color', self.input['color'])
        print('SetRGBColor: color =', color)

class PycomThing(Thing):

    def __init__(self):
        Thing.__init__(
            self,
            'urn:dev:ops:my-pycom-pysense',
            'My Pycom',
            ['RGBLed', 'memory'],
            'A web connected Pycom'
        )

        self.color = 0 #0 is no light, 20 is very light blue #0xff00 #green
        self.updateLeds()
        self.mempycom = Value(0.0)
        self.seconds = 0
        
        self.__alarm = Timer.Alarm(self._seconds_handler, s=10, periodic=True)
        #self._alarm = Timer.Alarm(updateMemPycom, 1, arg=None, periodic=True)
        
        
        self.add_property(
            Property(self,
                    'mempycom',
                    self.mempycom,
                    metadata={
                        '@type': 'SystemParameter',
                         'title': 'Memory',
                         'type': 'number',
                         'description': 'The free RAM of the system',
                     }
            )
                    
        )
        self.add_property(
            Property(self,
                     'color',
                     Value(self.color, self.setcolor),
                     metadata={
                         '@type': 'ColorProperty',
                         'title': 'Color',
                         'type': 'integar',
                         'description': 'The color of the LED',
                     }))
  

        self.add_available_action(
            'setrgbcolor',
            {
                'title': 'Change Color',
                'description': 'Change the color of LED',
                'input': {
                    'type': 'object',
                    'required': [
                        'color',
                    ],
                    'properties': {
                        'color': {
                            'type': 'integer',
                            'minimum': 0,
                            'maximum': 0xFFFFFF,
                            #'unit': 'percent',
                        },
                    },
                },
            },
            SetRGBColor)

    def setcolor(self, color):
        print('setcolor: color =', color)
        self.color = color
        self.updateLeds()


    def updateLeds(self):
        print('color', self.color)
        pycom.heartbeat(False) 
        pycom.rgbled(self.color)

    def updateMemPycom(self):
        self.mempycom = gc.mem_free()
        print('mem', self.mempycom)
     
    #TODO : should not need to run timer to update values!
    def _seconds_handler(self, alarm):
        self.seconds += 1
        new_mem = float(gc.mem_free())
        self.mempycom.notify_of_external_update(new_mem)
        self.updateLeds()
        #print("%02d iterations" % self.seconds)
        #print(si.temperature())
        if self.seconds < 0:
            alarm.cancel() # never stop 


class PySenseThing(Thing):

    def __init__(self):
        Thing.__init__(
            self,
            'urn:dev:ops:my-pysense',
            'My PySense',
            ['Temperature', 'Humidity', 'Pressure', 'Luminance', 'Accelerometer'],
            'A Sensor Shield'
        )

        self.seconds = 0
        self.temperature = Value(0.0)
        self.humidity = Value(0.0)
        self.light=lt.light()[0]
        self.accelaration_0=li.acceleration()[0]
        self.accelaration_1=li.acceleration()[1]
        self.accelaration_2=li.acceleration()[2]
        self.roll = li.roll()
        self.pitch = li.pitch()
        
        self.__alarm = Timer.Alarm(self._seconds_handler, s=10, periodic=True)
        #self._alarm = Timer.Alarm(updateMemPycom, 1, arg=None, periodic=True)

        self.add_property(
            Property(self,
                     'temperature',
                     self.temperature, #, self.updateTemperature),
                     metadata={
                         '@type': 'Temperature',
                         'title': 'Temperature',
                         'type': 'number',
                         'description': 'The temperature sensor value',
                     }))
        self.add_property(
            Property(self,
                     'humidity',
                     self.humidity,
                     metadata={
                         '@type': 'Humidity',
                         'title': 'Humidity',
                         'type': 'number',
                         'description': 'The humidity sensor value',
                     }))
       
    def updateTemperature(self):
        self.temperature = si.temperature()
        print('temperature', self.temperature)
        
    def updateHumidity(self):
        self.humidity = si.humidity()
        print('humidity', self.humidity)

    #TODO : should not need to run timer to get temperature value!
    def _seconds_handler(self, alarm):
        self.seconds += 1
        new_temperature = si.temperature()
        new_humidity = si.humidity()
        self.temperature.notify_of_external_update(new_temperature)
        self.humidity.notify_of_external_update(new_humidity)
        #print("%02d iterations" % self.seconds)
        #print(si.temperature())
        if self.seconds < 0:
            alarm.cancel() # never stop 


def run_server():
    print('run_server')

    # Create a thing that represents a pycom
    pycom = PycomThing()

    # Create a thing that represents a pysense
    pysense = PySenseThing()

    # If adding more than one thing, use MultipleThings() with a name.
    # In the single thing case, the thing's name will be broadcast.
    server = WebThingServer(MultipleThings([pycom, pysense], 'PycomAndPySense'), port=80)
    try:
        print('starting the server')
        server.start()
    except KeyboardInterrupt:
        print('stopping the server')
        server.stop()
        print('done')

if __name__ == '__main__':

    run_server()



