"""
Firmata Servo Control with Wekinator continuous output

"""

import pyglet
from pyfirmata import Arduino, util

import argparse
import math
from threading import Thread

from pythonosc import dispatcher
from pythonosc import osc_server
from pyglet.window import key

from wekinator import Wekinator 

class Window(pyglet.window.Window):	


	##Arduino Serial port setting.
	#board = Arduino('/dev/cu.usbmodem1411') ##for Mac
	board = Arduino('COM93')  ##for Windows
	#board = Arduino('/dev/ttyACM0')  ##for Raspberry Pi
	
	##setup Servo pin
	## refer pyFirmata Documentation for details
	## https://media.readthedocs.org/pdf/pyfirmata/latest/pyfirmata.pdf
	servo = board.get_pin('d:4:s')

	servoAngle = 90

	#initialize method
	def __init__(self,*args, **kwargs):
		super().__init__(width=512, height=512,caption="04pyfirmataServoClassifier.py",
								fullscreen=False,visible=True,resizable=False)
		## initialize a label with text
		## https://pyglet.readthedocs.io/en/pyglet-1.2-maintenance/api/pyglet/text/pyglet.text.Label.html
		self.label = pyglet.text.Label('HOWDY',  font_name='Times New Roman',
								font_size=36,
								x=self.width//2, y=self.height//2,
								anchor_x='center', anchor_y='center')

		### initialize an OSC server to receive messages from Wekinator.
		self.wek_output = Wekinator(args[0].ip,args[0].port,self.on_wekinator_message)

		### set an update function at an interval of 1/60 sec
		pyglet.clock.schedule_interval(self.update, 1/60.0)
	
	def update(self,dt,):
		self.label.text = "ServoAngle:({})".format(self.servoAngle)
		self.servo.write(self.servoAngle)

	#drawing method 
	def on_draw(self):
		self.clear()
		self.label.draw() # draw the label


	
	
	"""
	this function is called(dispatched) when the program received 
	message from wekinator.
	addr: contains OSC address such as "/wek/outputs"
	*args: list of values sent by OSC message
	"""
	def on_wekinator_message(self,addr, *args):
		## print out incoming message
		print("Address: {} {}".format(addr,",".join(str(x) for x in args)))

		## assign servo angle value
		if(len(args) == 1):
				self.servoAngle = int(args[0] * 180.0)

				## print out received hand.
				print("ServoAngle: ({})".format(self.servoAngle))



"""
  main routine to initialize the program

"""
if __name__ == "__main__":
  """
   checking command line options here.
   you can specify ip address and port number from 
   command line by adding "arguments" 

   python ****.py --ip "127.0.0.1" --port 12000 

  """ 
  parser = argparse.ArgumentParser()
  parser.add_argument("--ip",
      default="127.0.0.1", help="The ip to listen on")
  parser.add_argument("--port",
      type=int, default=12000, help="The port to listen on")
  args = parser.parse_args()


  ### initialize an OSC server to receive messages from Wekinator.
  #server = Wekinator(args.ip,args.port,wek_message_handler)
  ##create window
  window = Window(args, width=640, height=480)

  ### start pyglet app
  pyglet.app.run()