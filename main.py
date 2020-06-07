import sys
import logging
import connect

logging.basicConfig(logging.DEBUG)
log = logging.getLogger(__name__)

connect.connect_to_ap()


def pycom_pysense():
    print('importing pysense_thing...')
    import pysense_thing
    print('Starting pysense server...')
    pysense_thing.run_server()


pycom_pysense()