"""
Blink LED with pyfirmata

"""

import pyglet
from pyfirmata import Arduino, util

##create window
window = pyglet.window.Window()

##change this Arduino port to your setting.
board = Arduino('/dev/cu.usbmodem1411') ##for Mac
#board = Arduino('COM7')  ##for Windows


ledState = 0
ledPin = 10

def update(dt,):
	global ledState,ledPin
	if(ledState == 0):
		ledState = 1
		label.text = "ON"
		pyglet.gl.glClearColor(255,0,0,255)
	else:
		ledState = 0
		label.text = "OFF"
		pyglet.gl.glClearColor(0,0,0,0)

	board.digital[ledPin].write(ledState)



## initialize a label with text
## https://pyglet.readthedocs.io/en/pyglet-1.2-maintenance/api/pyglet/text/pyglet.text.Label.html
label = pyglet.text.Label('OFF',  font_name='Times New Roman',
                          font_size=36,
                          x=window.width//2, y=window.height//2,
                          anchor_x='center', anchor_y='center')


"""
pyglet drawing function 

pyglet calls this function everytime refreshing the pyglet window.
write drawing function and frame-by-frame actions here.

"""
@window.event
def on_draw():
    window.clear() # clear the window. you can set different background color by pyglet.gl.glClearColor(R,G,B,alpha) 
    label.draw() # draw the label


### set an update function at an interval of 1 sec
pyglet.clock.schedule_interval(update, 1)

### keep the app running
### type escape to quit
pyglet.app.run()
