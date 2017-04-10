#!/usr/bin/python
#
# Python Module to externalise all AlphaBot specific hardware
#
#===========================================================================

#===========================================================================
# General Functions
#
# init()    - Initialize GPIO pins, switches motors and LEDs Off, etc.
# cleanup() - Sets all motors and LEDs off and sets GPIO to standard values
#===========================================================================

# Import all necessary libraries
import sys, threading, time, os
import RPi.GPIO as GPIO, sys, threading, time, os

# Pins  9, 10   - Right Motor
# Pins  7, 8    - Left Motor
pinMotorA_1 = 10
pinMotorA_2 = 9
pinMotorB_1 = 8
pinMotorB_2 = 7

# UltraSonic Sensor pins
pinTrigger = 17
pinEcho = 18

# IR Sensor pin
pinLineSensorLeft = 23
pinLineSensorCenter = 24
pinLineSensorRight = 25

#===========================================================================
# General Functions
#
#===========================================================================

# init()    - Initialize GPIO pins, switches motors and LEDs Off, etc.
def init():

    # Global variables
    global rf, rb, lf, lb
    
    GPIO.setwarnings(False)
    
    # Use physical pin numbering
    GPIO.setmode(GPIO.BCM)

    # Use pwm on inputs so motors don't go too fast
    GPIO.setup(pinMotorA_1, GPIO.OUT)
    rf = GPIO.PWM(pinMotorA_1, 20)
    rf.start(0)

    GPIO.setup(pinMotorA_2, GPIO.OUT)
    rb = GPIO.PWM(pinMotorA_2, 20)
    rb.start(0)

    GPIO.setup(pinMotorB_1, GPIO.OUT)
    lf = GPIO.PWM(pinMotorB_1, 20)
    lf.start(0)

    GPIO.setup(pinMotorB_2, GPIO.OUT)
    lb = GPIO.PWM(pinMotorB_2, 20)
    lb.start(0)

    # Set UltraSonic sensor pins as output and input
    GPIO.setup(pinTrigger, GPIO.OUT)  # Trigger
    GPIO.setup(pinEcho, GPIO.IN)      # Echo

    #set up digital IR detectors as inputs
    GPIO.setup(pinLineSensorLeft, GPIO.IN) 	# Left line sensor
    GPIO.setup(pinLineSensorCenter, GPIO.IN) 	# Center line sensor
    GPIO.setup(pinLineSensorRight, GPIO.IN) 	# Right line sensor

    print("PiGoBot initialized.")
    

# cleanup() - Sets all motors and LEDs off and sets GPIO to standard values
def cleanup():
    stop()
    time.sleep(1)
    GPIO.cleanup()
    print("PiGoBot cleanup complete.")

# End of General Functions
#===========================================================================


#===========================================================================
# Motor Functions
#===========================================================================

# stop(): Stops both motors
def stop():
    rf.ChangeDutyCycle(0)
    rb.ChangeDutyCycle(0)
    lf.ChangeDutyCycle(0)
    lb.ChangeDutyCycle(0)
    
# forward(speed): Sets both motors to move forward at speed. 0 <= speed <= 100
def forward(speed):
    rf.ChangeDutyCycle(speed)
    rb.ChangeDutyCycle(0)
    lf.ChangeDutyCycle(speed)
    lb.ChangeDutyCycle(0)
    rf.ChangeFrequency(speed + 5)
    lf.ChangeFrequency(speed + 5)
    
# reverse(speed): Sets both motors to reverse at speed. 0 <= speed <= 100
def reverse(speed):
    rf.ChangeDutyCycle(0)
    rb.ChangeDutyCycle(speed)
    lf.ChangeDutyCycle(0)
    lb.ChangeDutyCycle(speed)
    rb.ChangeFrequency(speed + 5)
    lb.ChangeFrequency(speed + 5)

# spinLeft(speed): Sets motors to turn opposite directions at speed. 0 <= speed <= 100
def spinLeft(speed):
    rf.ChangeDutyCycle(speed)
    rb.ChangeDutyCycle(0)
    lf.ChangeDutyCycle(0)
    lb.ChangeDutyCycle(speed)
    rf.ChangeFrequency(speed + 5)
    lb.ChangeFrequency(speed + 5)
    
# spinRight(speed): Sets motors to turn opposite directions at speed. 0 <= speed <= 100
def spinRight(speed):
    rf.ChangeDutyCycle(0)
    rb.ChangeDutyCycle(speed)
    lf.ChangeDutyCycle(speed)
    lb.ChangeDutyCycle(0)
    rb.ChangeFrequency(speed + 5)
    lf.ChangeFrequency(speed + 5)
    
# turnForward(leftSpeed, rightSpeed): Moves forwards in an arc by setting different speeds. 0 <= leftSpeed,rightSpeed <= 100
def turnForward(leftSpeed, rightSpeed):
    rf.ChangeDutyCycle(rightSpeed)
    rb.ChangeDutyCycle(0)
    lf.ChangeDutyCycle(leftSpeed)
    rb.ChangeDutyCycle(0)
    rf.ChangeFrequency(rightSpeed + 5)
    lf.ChangeFrequency(leftSpeed + 5)
    
# turnReverse(leftSpeed, rightSpeed): Moves backwards in an arc by setting different speeds. 0 <= leftSpeed,rightSpeed <= 100
def turnReverse(leftSpeed, rightSpeed):
    rf.ChangeDutyCycle(0)
    rb.ChangeDutyCycle(rightSpeed)
    lf.ChangeDutyCycle(0)
    lb.ChangeDutyCycle(leftSpeed)
    rb.ChangeFrequency(rightSpeed + 5)
    lb.ChangeFrequency(leftSpeed + 5)

# go(leftSpeed, rightSpeed): controls motors in both directions independently using different positive/negative speeds. -100<= leftSpeed,rightSpeed <= 100
def go(leftSpeed, rightSpeed):
    if rightSpeed<0:
        rf.ChangeDutyCycle(0)
        rb.ChangeDutyCycle(abs(rightSpeed))
        rb.ChangeFrequency(abs(rightSpeed) + 5)
    else:
        rb.ChangeDutyCycle(0)
        rf.ChangeDutyCycle(rightSpeed)
        rf.ChangeFrequency(rightSpeed + 5)
    if leftSpeed<0:
        lf.ChangeDutyCycle(0)
        lb.ChangeDutyCycle(abs(leftSpeed))
        lb.ChangeFrequency(abs(leftSpeed) + 5)
    else:
        lb.ChangeDutyCycle(0)
        lf.ChangeDutyCycle(leftSpeed)
        lf.ChangeFrequency(leftSpeed + 5)

# go(speed): controls motors in both directions together with positive/negative speed parameter. -100<= speed <= 100
def goBoth(speed):
    if speed<0:
        reverse(abs(speed))
    else:
        forward(speed)


# End of Motor Functions
#======================================================================


#===========================================================================
# UltraSonic Sensor Functions
#===========================================================================

# getDistance(): Returns the distance in cm to the nearest reflecting object. 0 == no object
def getDistance():
    GPIO.output(pinTrigger, True)
    time.sleep(0.00001)
    GPIO.output(pinTrigger, False)
    StartTime = time.time()
    StopTime = StartTime

    while GPIO.input(pinEcho)==0:
        StartTime = time.time()
        StopTime = StartTime

    while GPIO.input(pinEcho)==1:
        StopTime = time.time()
        # If the sensor is too close to an object, the Pi cannot
        # see the echo quickly enough, so we have to detect that
        # problem and say what has happened.
        if StopTime-StartTime >= 0.04:
            print("Hold on there!  You're too close for me to see.")
            StopTime = StartTime
            break

    ElapsedTime = StopTime - StartTime
    Distance = (ElapsedTime * 34300)/2

    return Distance

# End of UltraSonic Sensor Functions
#===========================================================================


#===========================================================================
# IR Sensor Functions
#===========================================================================

# isLeftOverBlack(): Return True if the left line detector is over a black line
def isLeftOverBlack():
    if GPIO.input(pinLineSensorLeft) == 0:
        return True
    else:
        return False

# isCenterOverBlack(): Return True if the center line detector is over a black line
def isCenterOverBlack():
    if GPIO.input(pinLineSensorCenter) == 0:
        return True
    else:
        return False

# isRightOverBlack(): Return True if the right line detector is over a black line
def isRightOverBlack():
    if GPIO.input(pinLineSensorRight) == 0:
        return True
    else:
        return False


# End of IR Sensor Functions
#===========================================================================
