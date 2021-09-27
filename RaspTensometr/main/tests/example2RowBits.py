#! /usr/bin/python2
from datetime import datetime
import time
import sys

EMULATE_HX711 = False

print("Start!!")
referenceUnit = 1

if not EMULATE_HX711:
    import RPi.GPIO as GPIO
    from hx711 import HX711
else:
    from emulated_hx711 import HX711


def cleanAndExit():
    print("Cleaning...")

    if not EMULATE_HX711:
        GPIO.cleanup()

    print("Bye!")
    sys.exit()


hx = HX711(5, 6)

hx.set_reading_format("MSB", "MSB")

hx.set_reference_unit(91)

hx.reset()
hx.tare_A()
print("Tare done! Add weight now...")

print("Start!! Run loop:")
timeAllApp = datetime.now()
print("Start app TIME: ", timeAllApp)

end = 0

while True:
    try:

        #print("==================================================\n")
        tStart = datetime.now()
        #print(tStart)
        val = hx.get_weight_A(1)

       # print("Tens value: ", val," Mensure iteration: ", end)

        # hx.power_down()
        # hx.power_up()

        time.sleep(0.00001)
        tStop = datetime.now()
        #print(tStop, "\n")
        tDiference = tStop - tStart
        print("Time mesurment: ", tDiference)
        end = end + 1
       # print("--------------------------------------------------\n")
        if (end == 100):
            timeEndApp = datetime.now()
            difTimeApp = timeEndApp - timeAllApp
            print("Lenght time app: ", difTimeApp)
            print("End example.py")

            break
    except (KeyboardInterrupt, SystemExit):
        cleanAndExit()
