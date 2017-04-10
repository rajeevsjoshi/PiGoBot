import RPi.GPIO as GPIO # Import the GPIO Library
import time             # Import the Time library
import PiGoBot

# Distance Variables
HowNear = 20.0
ReverseTime = 0.5
TurnTime = 0.3

# Return True if the ultrasonic sensor sees an obstacle
def IsNearObstacle(localHowNear):
    Distance = PiGoBot.getDistance()

    print("IsNearObstacle: "+str(Distance))
    if Distance < localHowNear:
        return True
    else:
        return False

# Move back a little, then turn right
def AvoidObstacle():
    # Back off a little
    print("Backwards")
    PiGoBot.reverse(30)
    time.sleep(ReverseTime)
    PiGoBot.stop()

    # Turn right
    print("Right")
    PiGoBot.spinRight(30)
    time.sleep(TurnTime)
    PiGoBot.stop()

try:
    PiGoBot.init()
    #repeat the next indented block forever
    while True:
        PiGoBot.forward(50)
        time.sleep(0.1)
        if IsNearObstacle(HowNear):
            PiGoBot.stop()
            AvoidObstacle()

# If you press CTRL+C, cleanup and stop
except KeyboardInterrupt:
    PiGoBot.cleanup()
