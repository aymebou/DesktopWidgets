#! /usr/bin/env python

"""
    This file creates sow on your desktop, it is used for 1920x1080 sized screens
    It works by creating a tkinter window, with low alpha, and white circles with snow-like behavior.

    Two important things to notice : - it uses the deskop type given by tkinter to remain in the desktop, but if your window envirronment is not familiar with this,
                                       it might not work
                                     - there is a lign of non-used pixels to make you able to click on your desktop on the left side, so that you can unselect the window.

    """



from random import randint, uniform
from signal import signal, SIGINT
from sys import exit, stdout
from Tkinter import *

def main():
    sm = SnowMachine()
    sm.play()

class SnowMachine():

    def __init__(self):
        # handle ctrl+c from terminal
        signal(SIGINT, self.signal_handler)

        # create Tk panel
        self.root = Tk()
        self.root.wm_title("snowflakes")
        self.root.wm_attributes("-type",'desktop')
        self.root.geometry("1919x1080+1+0")  ##Adjust with your screen size.
        self.root.wm_attributes("-alpha", 0.1)

        width = self.root.winfo_screenwidth()
        height = self.root.winfo_screenheight()

        # create drawing canvas
        self.canv = Canvas(self.root, width=width, height=height)
        self.canv.pack()
        self.canv.configure(bg="black")


        # make snowflaks
        self.snowflakes = []
        for i in range(650 ):
            self.snowflakes.append(snowflake(self.canv, randint(0, width), randint(0, height / 16), length=uniform(4, 8)))

    def play(self):
        self.root.after(50, self.run)
        self.root.mainloop()

    def run(self):
        for snowflake in self.snowflakes:
            snowflake.next()
        self.root.update_idletasks()
        self.root.after(15, self.run)

    def signal_handler(self, signal, frame):
        stdout.write("\x1B[2D") # moves cursor back 2 so that when user enter ^c to quit, these characters don't appear
        self.root.quit() # close tkinter frame/panel


class snowflake():

    def __init__(self, canvas, x, y, **kwargs):
        self.canv = canvas
        self.x = x
        self.y = y
        self.vx = kwargs.get("x_velocity", uniform(1, 4))
        self.vy = kwargs.get("y_velcity", uniform(-4, 1))
        self.ax = None
        self.ay = None

        self.len = kwargs.get("length", 3)

        self.circ = self.canv.create_oval(self.x, self.y, self.x + self.len, self.y + self.len, outline="grey98", fill="grey98")

    def nextAccelerations(self):
        self.ax = uniform(-.5, .5)
        self.ay = uniform(-.5, .5)

    def nextVelocities(self):
        self.nextAccelerations()

        self.vx = max(-4, min(4, self.vx + self.ax))
        self.vy = max(-.5, min(6, self.vy + self.ay))


    def nextPositions(self):
        width = self.canv.winfo_width() - 15
        height = self.canv.winfo_height() + 3

        self.nextVelocities()

        self.x += self.vx
        self.y += self.vy

        if self.x + self.vx + self.len < 0:
            self.x = width - 2 + self.len
        if self.x + self.vx > width:
            self.x = 2 - self.len
        if self.y + self.vy - self.len > height:
            self.y = -self.len
            self.x = randint(0, width)
            self.vy = uniform(.5, 2)



    def next(self):
        v = self.nextPositions()
        self.canv.coords(self.circ, self.x, self.y, self.x + self.len, self.y + self.len)


if __name__ == "__main__":
    main()
