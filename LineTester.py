import RPi.GPIO as GPIO # Import the GPIO Library
import time # Import the Time library
import PiGoBot

try:
    PiGoBot.init()
    #repeat the next indented block forever
    print("Following the line")
    while True:
        # If the sensor is low (=0), it is above the black line
        if PiGoBot.isLeftOverBlack():
            print("0: The left sensor is over the line")
            time.sleep(0.5)
        elif PiGoBot.isCenterOverBlack():
	    print("0: The center sensor is over the line")
            time.sleep(0.5)
        elif PiGoBot.isRightOverBlack():
	    print("0: The right sensor is over the line")
            time.sleep(0.5)
	# If not (else), print the following
        else:
            print("1: The robot has lost the line")
            time.sleep(0.5)

# If you press CTRL+C, cleanup and stop
except KeyboardInterrupt:
    PiGoBot.cleanup()
