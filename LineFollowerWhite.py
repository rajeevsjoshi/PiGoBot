import RPi.GPIO as GPIO # Import the GPIO Library
import time # Import the Time library
import PiGoBot

# Search for the black line
def SeekLine():
    print("Seeking the line")
    # The direction the robot will turn - True = Left
    Direction = True

    SeekSize = 0.20 # Turn for 0.20s
    SeekCount = 1 # A count of times the robot has looked for the line
    MaxSeekCount = 10 # The maximum time to seek the line in one direction

    # Turn the robot left and right until it finds the line
    # Or we have looked long enough
    while SeekCount <= MaxSeekCount:
        # Set the seek time
        SeekTime = SeekSize * SeekCount

        # Start the motors turning in a direction
        if Direction:
            print("Looking left")
            PiGoBot.spinLeft(20)
        else:
            print("Looking Right")
            PiGoBot.spinRight(20)

        # Save the time it is now
        StartTime = time.time()
        
        # While the robot is turning for SeekTime seconds,
        # check to see whether the line detector is over black
        while time.time()-StartTime <= SeekTime:
            if not PiGoBot.isOverBlack():
                PiGoBot.stop()
                # Exit the SeekLine() function returning 
                # True - the line was found
                return True

        # The robot has not found the black line yet, so stop
        PiGoBot.stop()

        # Increase the seek count
        SeekCount += 1

        # Change direction
        Direction = not Direction

    # The line wasn't found, so return False
    return False

try:
    PiGoBot.init()
    #repeat the next indented block forever
    print("Following the line")
    while True:
        # If the seson is low (=0), it is above the black line
        if not PiGoBot.isOverBlack():
            PiGoBot.forward(20)
        # If not (else), print the following
        else:
            PiGoBot.stop()
            if SeekLine() == False:
                PiGoBot.stop()
                print("The robot has lost the line")
                exit()
            else:
                print("Following the line")

# If you press CTRL+C, cleanup and stop
except KeyboardInterrupt:
    PiGoBot.cleanup()
