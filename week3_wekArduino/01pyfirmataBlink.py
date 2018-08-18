"""
Blink LED with pyfirmata

"""

import pyglet
from pyfirmata import Arduino, util

class Window(pyglet.window.Window):	
	ledState = 0
	ledPin = 10

	##Arduino Serial port setting.
	#board = Arduino('/dev/cu.usbmodem1411') ##for Mac
	board = Arduino('COM93')  ##for Windows
	#board = Arduino('/dev/ttyACM0')  ##for Raspberry Pi

	#initialize method
	def __init__(self,*args, **kwargs):
		super().__init__(width=512, height=512,caption="01pyfirmataBlink.py",
								fullscreen=False,visible=True,resizable=False)
		## initialize a label with text
		## https://pyglet.readthedocs.io/en/pyglet-1.2-maintenance/api/pyglet/text/pyglet.text.Label.html
		self.label = pyglet.text.Label('HOWDY',  font_name='Times New Roman',
								font_size=36,
								x=self.width//2, y=self.height//2,
								anchor_x='center', anchor_y='center')
		### set an update function at an interval of 1 sec
		pyglet.clock.schedule_interval(self.update, 1)
	
	def update(self,dt,):
		if(self.ledState == 0):
			self.ledState = 1
			self.label.text = "ON"
			pyglet.gl.glClearColor(255,0,0,255)
		else:
			self.ledState = 0
			self.label.text = "OFF"
			pyglet.gl.glClearColor(0,0,0,0)

		self.board.digital[self.ledPin].write(self.ledState)
    
	#drawing method 
	def on_draw(self):
		self.clear()
		self.label.draw() # draw the label


#main function
def main():
    ##create window
    window = Window(width=300, height=300)

    ### keep the app running
    ### type escape to quit
    pyglet.app.run()


if __name__ == '__main__':
    main()


### keep the app running
### type escape to quit
pyglet.app.run()
