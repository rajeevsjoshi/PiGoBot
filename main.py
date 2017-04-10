import time, math
import cwiid
import WiiRemote
import PiGoBot

#Create delay variable that we can use (Seconds)
Delay = 0.2
WiiRemote.setup()   # Initialize Wii Remote
PiGoBot.init()      # Initialize PiGoBot
    
mode = 0            # Initial mode = Wii Control Mode

# Distance Variables for Abstacle Avoidance Mode
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

# Avoid Obstace - Move back a little, then turn right
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
            PiGoBot.spinLeft(40)
        else:
            print("Looking Right")
            PiGoBot.spinRight(40)

        # Save the time it is now
        StartTime = time.time()
        
        # While the robot is turning for SeekTime seconds,
        # check to see whether the line detector is over black
        while time.time()-StartTime <= SeekTime:
            if (PiGoBot.isLeftOverBlack() or PiGoBot.isCenterOverBlack() or PiGoBot.isRightOverBlack()):
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

   
while True:

    #This deals with the buttons, we tell every button what we want it to do
    buttons = WiiRemote.Wii.state['buttons']

    # If the Plus and Minus buttons are pressed then rumble and quit, plus close program
    if (buttons - cwiid.BTN_PLUS - cwiid.BTN_MINUS == 0):
        PiGoBot.cleanup()
        WiiRemote.cleanup()

    if (buttons & cwiid.BTN_HOME):
        mode = 0           # Wii Remote Control Mode
        WiiRemote.Wii.led = 15
        print 'Home pressed'

    if (buttons & cwiid.BTN_1):
        mode = 1           # Obstacle Avoidance Mode
        WiiRemote.Wii.led = 9
        print '1 pressed'

    if (buttons & cwiid.BTN_2):
        mode = 2           # Line Fllowing Mode
        WiiRemote.Wii.led = 6
        print '2 pressed'
        
    while(mode == 0):
        if WiiRemote.Wii.state.has_key('nunchuk'):
            try:
                x, y = WiiRemote.read_nunchuck_normalized()
                r = WiiRemote.clamp(math.sqrt(x*x + y*y), -8, 8)
                
                if x == 0:
                    PiGoBot.go(y*10, y*10)
                elif x < 0:
                    if y >= 0:
                        PiGoBot.go((y-4)*20, r*10)
                    elif y < 0:
                        PiGoBot.go(-r*10, (y+4)*20)
                elif x > 0:
                    if y >= 0:
                        PiGoBot.go(r*10, (y-4)*20)
                    elif y < 0:
                        PiGoBot.go((y+4)*20, -r*10)

                #Break for any other actions that require the use of the nunchuk in any way
                break

            #This part down below is the part that tells us if no nunchuk is connected to the wiimote
            except KeyError:
                print 'No nunchuk detected.'
                    
    while(mode == 1):
        PiGoBot.forward(50)
        time.sleep(0.1)

        if IsNearObstacle(HowNear):
            PiGoBot.stop()
            AvoidObstacle()
                
        #Break for any other actions that require the use of the nunchuk in any way
        break

    while(mode == 2):
        # If the sensor is low (=0), it is above the black line
        if (PiGoBot.isCenterOverBlack() and PiGoBot.isRightOverBlack()):
            PiGoBot.spinRight(30)
	if (PiGoBot.isCenterOverBlack() and PiGoBot.isLeftOverBlack()):
            PiGoBot.spinLeft(30)
	elif PiGoBot.isCenterOverBlack():
            PiGoBot.forward(30)
	elif PiGoBot.isRightOverBlack():
	    while not (PiGoBot.isCenterOverBlack()):
		PiGoBot.spinRight(20)
	elif PiGoBot.isLeftOverBlack():
	    while not (PiGoBot.isCenterOverBlack()):
		PiGoBot.spinLeft(20)
	elif (PiGoBot.isLeftOverBlack() and PiGoBot.isCenterOverBlack() and PiGoBot.isRightOverBlack()):
            PiGoBot.stop()
	# If not (else), print the following
        else:
            PiGoBot.stop()
            if SeekLine() == False:
                PiGoBot.stop()
                print("The robot has lost the line")
                exit()
            else:
                print("Following the line")

        #Break for any other actions that require the use of the nunchuk in any way
        break
                
