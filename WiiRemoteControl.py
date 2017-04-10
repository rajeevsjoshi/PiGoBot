import cwiid, time, math
import PiGoBot

#Create delay variable that we can use (Seconds)
Delay = 0.2
Counter = 9999

stickCenterX = 125
stickCenterY = 125

#Establish a connection with the wiimote
print ' '
print 'Press 1 and 2 on the wiimote at the same time.'
#Connect to mote and if it doesn't connect then it tells us and tries again
time.sleep(3)
print ''
print 'Establishing Connection... 5'
time.sleep(1)
print 'Establishing Connection... 4'
time.sleep(1)
print 'Establishing Connection... 3'
Wii = None
while (Wii==None):
    try:
        Wii = cwiid.Wiimote()
    except RuntimeError:
        print 'Error connecting to the wiimote, press 1 and 2.'
print 'Establishing Connection... 2'
time.sleep(1)
print 'Establishing Connection... 1'
time.sleep(1)
print ''

#Once a connection has been established with the wiimote the rest of the program will continue; otherwise, it will keep on trying to connect

#Rumble to indicate connection and turn on the LED
Wii.rumble = 1 #1 = on, 0 = off
PiGoBot.init() # Initialize PiGoBot
print 'Connection Established.'
print 'PiGoBot initialized and ready...'
print 'Press + & - buttons together to quit'
print ''

''' Each number turns on different leds on the wiimote
    ex) if Wii.led = 1, then LED 1 is on
    2  = LED 2          3  = LED 3          4  = LED 4
    5  = LED 1, 3       6  = LED 2, 3       7  = LED 1,2,3
    8  = LED 4          9  = LED 1, 4       10 = LED 2,4
    11 = LED 1,2,4      12 = LED 3,4        13 = LED 1,3,4
    14 = LED 2,3,4      15 = LED 1,2,3,4
    It counts up in binary to 15'''
time.sleep(1)
Wii.rumble = 0
Wii.led = 15

def readStickNormalized(x,y):
    xNorm = clamp(int((x-stickCenterX)/10),-9,9)
    yNorm = clamp(int((y-stickCenterY)/10),-9,9)

    return xNorm, yNorm

def clamp(val, minval, maxval):
    return min(maxval, max(minval,val))

def calibrateStick():
    global stickCenterX, stickCenterY
    stickCenterX = (Wii.state['nunchuk']['stick'][cwiid.X])
    stickCenterY = (Wii.state['nunchuk']['stick'][cwiid.Y])

# Set it so that we can tell when and what buttons are pushed, and make it so that the accelerometer input can be read
Wii.rpt_mode = cwiid.RPT_BTN | cwiid.RPT_ACC | cwiid.RPT_EXT
Wii.state

#calibrateStick()
#print 'X Center = ' + str(stickCenterX) + ', Y Center = ' + str(stickCenterY)

while True:

    #This deals with the accelerometer
    '''create a variable containing the x accelerometer value
    (changes if mote is turned or flicked left or right)
    flat or upside down = 120, if turned: 90 degrees cc = 95, 90 degrees c = 145'''
    Accx = (Wii.state['acc'][cwiid.X])

    '''create a variable containing the y accelerometer value
    (changes when mote is pointed or flicked up or down)
    flat = 120, IR pointing up = 95, IR pointing down = 145'''
    Accy = (Wii.state['acc'][cwiid.Y])

    '''create a variable containing the z accelerometer value
    (Changes with the motes rotation, or when pulled back or flicked up/down)
    flat = 145, 90 degrees cc or c, or 90 degrees up and down = 120, upside down = 95'''
    Accz = (Wii.state['acc'][cwiid.Z])


    #This deals with the buttons, we tell every button what we want it to do
    buttons = Wii.state['buttons']
    #Get battery life (as a percent of 100):
    #Just delete the nunber sign inn front
    #print Wii.state['battery']*100/cwiid.BATTERY_MAX

    # If the Plus and Minus buttons are pressed then rumble and quit, plus close program
    if (buttons - cwiid.BTN_PLUS - cwiid.BTN_MINUS == 0):
        print ''
        print 'Shutting down PiGoBot...'
        PiGoBot.cleanup()
        print 'Closing Connection...'
        Wii.rumble = 1
        time.sleep(.5)
        Wii.rumble = 0
        Wii.led = 0
        exit(Wii)

    #Here we handle the nunchuk, along with the joystick and the buttons
    while(1):
        if Wii.state.has_key('nunchuk'):
            try:
                #Here is the data for the nunchuk stick:
                #X axis:LeftMax = 22, Middle = 125, RightMax = 220
                NunchukStickX = (Wii.state['nunchuk']['stick'][cwiid.X])
                #Y axis:DownMax = 30, Middle = 125, UpMax = 228
                NunchukStickY = (Wii.state['nunchuk']['stick'][cwiid.Y])
                #The 'NunchukStickX' and the 'NunchukStickY' variables now store the stick values

                #Here we take care of all of our data for the accelerometer
              
                #The nunchuk has an accelerometer that records in a similar manner to the wiimote, but the number range is different
                #The X range is: 70 if tilted 90 degrees to the left and 175 if tilted 90 degrees to the right
                NAccx = Wii.state['nunchuk']['acc'][cwiid.X]
                #The Y range is: 70 if tilted 90 degrees down (the buttons pointing down), and 175 if tilted 90 degrees up (buttons pointing up)
                NAccy = Wii.state['nunchuk']['acc'][cwiid.Y]
                #I still don't understand the z axis completely (on the wiimote and nunchuk), but as far as I can tell it's main change comes from directly pulling up the mote without tilting it
                NAccz = Wii.state['nunchuk']['acc'][cwiid.Z]

                x, y = readStickNormalized(NunchukStickX, NunchukStickY)
                r = clamp(math.sqrt(x*x + y*y), -9, 9)

                if x == 0:
                    PiGoBot.go(y*10, y*10)
                elif x < 0:
                    if y >= 0:
                        PiGoBot.go((y-4)*10, r*10)
                    elif y < 0:
                        PiGoBot.go(-r*10, (y+4)*10)
                elif x > 0:
                    if y >= 0:
                        PiGoBot.go(r*10, (y-4)*10)
                    elif y < 0:
                        PiGoBot.go((y+4)*10, -r*10) 
                        
                '''
                #Make it so that we can control the arm with tilt Functions
                #Left to Right
                if (Accx < 100 and NAccx < 90 ):
                    #print 'Moving Left'
                if (Accx > 135 and NAccx > 150):
                    #print 'Moving Right'

                #Up and Down
                if (Accy < 100 and NAccy < 90):
                    #print 'Moving Up'
                if (Accy > 135 and NAccy > 150):
                    #print 'Moving Down'

                #Here we create a variable to store the nunchuck button data
                #0 = no buttons pressed
                #1 = Z is pressed
                #2 = C is pressed
                #3 = Both C and Z are pressed

                ChukBtn = Wii.state['nunchuk']['buttons']
                if (ChukBtn == 1):
                    #print 'Z pressed'
                    time.sleep(Delay)
                if (ChukBtn == 2):
                    #print 'C pressed'
                    time.sleep(Delay)
                #If both are pressed the led blinks
                if (ChukBtn == 3):
                    #print 'C and Z pressed'
                    time.sleep(Delay)
                '''
                
                #Any other actions that require the use of the nunchuk in any way must be put here for the error handling to function properly
                break

            #This part down below is the part that tells us if no nunchuk is connected to the wiimote
            except KeyError:
                print 'No nunchuk detected.'
