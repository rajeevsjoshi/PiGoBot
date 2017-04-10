# AlphaBot Motor Speed Test
#----------------------------------
from Tkinter import *
import Lib.Motor as Motor        # Import Motor library

class App:

    def __init__(self, master):
        frame = Frame(master)
        frame.pack()
        scale = Scale(frame, from_=0, to=100,
              orient=HORIZONTAL, command=self.update)
        scale.grid(row=0)


    def update(self, speed):
        Motor.Forwards(float(speed),float(speed))

root = Tk()
root.wm_title('Motor Speed ontrol')
app = App(root)
root.geometry("200x50+0+0")

try:
    root.mainloop()

finally:
    GPIO.cleanup()
