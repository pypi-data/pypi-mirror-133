import os, sys, inspect, logging, time

lib_folder = os.path.join(os.path.split(inspect.getfile( inspect.currentframe() ))[0], '..')
lib_load = os.path.realpath(os.path.abspath(lib_folder))

if lib_load not in sys.path:
    sys.path.insert(0, lib_load)

import capablerobot_usbhub

count = 0
while True:
    
    hub = capablerobot_usbhub.USBHub()

    print("Count : {}".format(count))

    for idx, key in enumerate(hub.devices):
        hub.activate(key)
        device = hub.device
    
        print("Hub Key  : {} ({})".format(device.key, idx))
        print("Revision : {}".format(device.sku))
        print("Serial   : {}".format(device.serial))
        print("USB Path : {}".format(device.usb_path))

    print()
    count += 1

        