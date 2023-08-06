import os, sys, inspect
import time
import logging

lib_folder = os.path.join(os.path.split(inspect.getfile( inspect.currentframe() ))[0], '..')
lib_load = os.path.realpath(os.path.abspath(lib_folder))

if lib_load not in sys.path:
    sys.path.insert(0, lib_load)

FORMAT = '%(levelname)-8s %(message)s'
logging.basicConfig(format=FORMAT)
logger = logging.getLogger('USB Hub Status')
logger.setLevel(logging.DEBUG)

import capablerobot_usbhub 

hub = capablerobot_usbhub.USBHub()
hub.i2c.enable()


logger.info("Port Connections : {}".format(hub.connections()))
logger.info("Port Speeds      : {}".format(hub.speeds()))

logger.info("Port Currents (mA)")
logger.info("     Measured : " + " ".join([("%.2f" % v).rjust(7) for v in hub.power.measurements()]))
logger.info("     Limit    : {}".format(hub.power.limits()))
logger.info("     Alerts   : {}".format(" ".join(hub.power.alerts())))
logger.info("     State    : {}".format(hub.power.state()))


print(hub.register_read(addr=0x30E5, print=True))

## Battery charge enable (RO)
print(hub.register_read(addr=0x30D0, print=True))

print(hub.register_read(addr=0x343C, print=True))
print(hub.register_read(addr=0x343D, print=True))
print(hub.register_read(addr=0x343E, print=True))
print(hub.register_read(addr=0x343F, print=True))