import cwiid, time, math

# Nunchuck Paramters
# Left Max  =  22
# Right Max = 222
# Fwd Max   = 229
# Bwd Max   =  30
joy_x_center = 126
joy_y_center = 131


def setup():

    # Global variables
    global Wii
    
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
    print 'Press + & - buttons together to quit'
    print ''

    time.sleep(1)
    Wii.rumble = 0
    Wii.led = 15
    
    # Set it so that we can tell when and what buttons are pushed, and make it so that the accelerometer input can be read
    Wii.rpt_mode = cwiid.RPT_BTN | cwiid.RPT_ACC | cwiid.RPT_EXT
    Wii.state

    print 'Calibrating nunchuck...'
    time.sleep(2)
    calibrate_nunchuck()
    print 'Nunchuck calibrated.'
    


def cleanup():
        print ''
        print 'Closing Connection...'
        Wii.rumble = 1
        time.sleep(.5)
        Wii.rumble = 0
        Wii.led = 0
        exit(Wii)

def calibrate_nunchuck():
    global joy_x_center, joy_y_center
    joy_x_center = (Wii.state['nunchuk']['stick'][cwiid.X])
    joy_y_center = (Wii.state['nunchuk']['stick'][cwiid.Y])


def clamp(val, minval, maxval):
    return min(maxval, max(minval, val))


def read_nunchuck_normalized():
    x = (Wii.state['nunchuk']['stick'][cwiid.X])
    y = (Wii.state['nunchuk']['stick'][cwiid.Y])
    norm_x = clamp(round((x - joy_x_center)/10,0), -8, 8)
    norm_y = clamp(round((y - joy_y_center)/10,0), -8, 8)
    return norm_x, norm_y
    
def main():

   Delay = 0.2
    
   setup()
   while True:
        #This deals with the buttons, we tell every button what we want it to do
        buttons = Wii.state['buttons']

        # If the Plus and Minus buttons are pressed then rumble and quit, plus close program
        if (buttons - cwiid.BTN_PLUS - cwiid.BTN_MINUS == 0):
           cleanup()

        #Here we handle the nunchuk, along with the joystick and the buttons
        while(1):
            if Wii.state.has_key('nunchuk'):
                try:
                      x, y = read_nunchuck_normalized()

                      r = clamp(math.sqrt(x*x + y*y), -8, 8)

                      if (x == 0):
                          lm = y*10
                          rm = y*10
                      elif x < 0:
                          if y >= 0:
                              lm = (y-4)*20
                              rm = r*10
                          elif y < 0:
                              lm = -r*10
                              rm = (y+4)*20
                      elif x > 0:
                          if y >= 0:
                              lm = r*10
                              rm = (y-4)*20
                          elif y < 0:
                              lm = (y+4)*20
                              rm = -r*10

                      print 'LM = ' + str(lm) + ', RM = ' + str(rm)
                      time.sleep(Delay)
                      
                      #Any other actions that require the use of the nunchuk in any way must be put here for the error handling to function properly
                      break

                #This part down below is the part that tells us if no nunchuk is connected to the wiimote
                except KeyError:
                    print 'No nunchuk detected.'

  
if __name__=="__main__":
   main()
