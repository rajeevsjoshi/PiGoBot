
import cwiid, time

#Create delay variable that we can use (Seconds)
Delay = 0.2
Counter = 9999

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
print 'Connection Established.'
print 'Press any button to continue...'
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

# Set it so that we can tell when and what buttons are pushed, and make it so that the accelerometer input can be read
Wii.rpt_mode = cwiid.RPT_BTN | cwiid.RPT_ACC | cwiid.RPT_EXT
Wii.state

while True:

    #This deals with the buttons, we tell every button what we want it to do
    buttons = Wii.state['buttons']

    # If the Plus and Minus buttons are pressed then rumble and quit, plus close program
    if (buttons - cwiid.BTN_PLUS - cwiid.BTN_MINUS == 0):
        print ''
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
                #X axis:LeftMax = 25, Middle = 125, RightMax = 225
                NunchukStickX = (Wii.state['nunchuk']['stick'][cwiid.X])
                #Y axis:DownMax = 30, Middle = 125, UpMax = 225
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
            
                #Make it so that we can control the arm with the joystick
                if (NunchukStickX <= 0):
                    print 'Moving Left      - ' + str(NunchukStickX)
                    time.sleep(Delay)
                if (NunchukStickX > 0):
                    print 'Moving Right     - ' + str(NunchukStickX)
                    time.sleep(Delay)
                if (NunchukStickY <= 0):
                    print 'Moving Backward  - ' + str(NunchukStickY)
                    time.sleep(Delay)
                if (NunchukStickY > 0):
                    print 'Moving Forward   - ' + str(NunchukStickY)
                    time.sleep(Delay)
              
            #This part down below is the part that tells us if no nunchuk is connected to the wiimote
            except KeyError:
                print 'No nunchuk detected.'
