"""
Firmata Servo Control with Wekinator output

"""

import pyglet
from pyfirmata import Arduino, util

import argparse
import math
from threading import Thread

## pythonosc modules for receiving OSC message
from pythonosc import dispatcher
from pythonosc import osc_server

## pythonosc modules for sending OSC message
from pythonosc import osc_bundle_builder
from pythonosc import osc_message_builder
from pythonosc import udp_client
from pyglet.window import key


##create window
window = pyglet.window.Window()

##change this Arduino port to your setting.
#board = Arduino('/dev/cu.usbmodem1411') ##for Mac
board = Arduino('COM40')  ##for Windows
iter8 = util.Iterator(board)
iter8.start()

##setup Servo pins 
## refer pyFirmata Documentation for details
## https://media.readthedocs.org/pdf/pyfirmata/latest/pyfirmata.pdf
servo = board.get_pin('d:4:s')

# list of predefined servo angles
servoAngleList = [90,20,50,120,150]
servoAngleIdx = 0


"""  
  sending message to wekinator input.
  addr: contains OSC address such as "/wek/outputs"
  args: a value or list of values to be sent by OSC message
"""

def wek_send_message(addr, args):
	print("Address: {} {}".format(len(args),",".join(str(x) for x in args)))
	# msg = osc_message_builder.OscMessageBuilder(address="/wek/inputs")
	# # Add 3 messages in the bundle, each with more arguments.

	client.send_message("/wek/inputs", args)


dispatcher = dispatcher.Dispatcher()

"""
  this function is called(dispatched) when the program received 
  message from wekinator.
  addr: contains OSC address such as "/wek/outputs"
  *args: list of values sent by OSC message
"""
def wek_message_handler(addr, *args):
	global servoAngle,servoAngleIdx
	## print out incoming message
	print("Address: {} {}".format(addr,",".join(str(x) for x in args)))

	## assign first value as a hand indexes (0:rock 1:paper 2:scissors 3:none)
	## hand_idx variable is a global variable, changes made here will be applied 
	## to the entire program.
	if(len(args) == 1):
		if args[0] - 1 < len(servoAngleList):
			servoAngleIdx = int(args[0]) - 1
			servoAngle = servoAngleList[servoAngleIdx]

			## print out received hand.
			print("ServoAngle: ({},{})".format(servoAngleIdx,servoAngleList[servoAngleIdx]))
	

"""
initialise OSC Server
This function creates a thread of listening incoming OSC message at  
"""
def init_OSC_server(ip,port,osc_message_handler):

    ## create an event dispatcher for "/wek/outputs" address.
    ## set event handler "osc_message_handler"
    dispatcher.map("/wek/outputs", osc_message_handler)

    ## setup and start an osc server thread on specified ip address and port.
    server = osc_server.ThreadingOSCUDPServer(
        (ip, port), dispatcher)
    print("Serving on {}".format(server.server_address))

    server_thread = Thread(target=server.serve_forever)
    server_thread.daemon = True
    server_thread.start()

    return server


"""
  update servo angles 
"""  
def update(dt,):
	global label,servoAngle, servoAngleIdx
	
	servoAngle = servoAngleList[servoAngleIdx]
	label.text = "ServoAngle:({},{})".format(servoAngleIdx,servoAngle)
	servo.write(servoAngle)


"""
pyglet drawing function 

pyglet calls this function everytime refreshing the pyglet window.
write drawing function and frame-by-frame actions here.

"""
@window.event
def on_draw():
    window.clear() # clear the window. you can set different background color by pyglet.gl.glClearColor(R,G,B,alpha) 
    label.draw() # draw the label
    statusLabel.draw()

@window.event
def on_key_press(symbol, modifiers):
    global servoAngleIdx

    if symbol == key._1:
      servoAngleIdx = 0
    elif symbol == key._2:
      servoAngleIdx = 1
    elif symbol == key._3:
      servoAngleIdx = 2  
    elif symbol == key._4:
      servoAngleIdx = 3  
    elif symbol == key._5:
      servoAngleIdx = 4


    

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
	## initialize a label with text
	## https://pyglet.readthedocs.io/en/pyglet-1.2-maintenance/api/pyglet/text/pyglet.text.Label.html
	label = pyglet.text.Label('Servo',  font_name='Times New Roman',
	                  font_size=36,
	                  x=window.width//2, y=window.height//2,
	                  anchor_x='center', anchor_y='center')

	statusMessage

	statusLabel = pyglet.text.Label('Servo',  font_name='Times New Roman',
                  font_size=36,
                  x=0, y=window.height//2,
                  anchor_x='center', anchor_y='center')

	client = udp_client.SimpleUDPClient(args.ip, 6448) ## setup OSC client to Wekinator localhost port 6448

	### initialize an OSC server to receive messages from Wekinator.
	server = init_OSC_server(args.ip,args.port,wek_message_handler)
	### set an update function at an interval of 1/60 sec
	pyglet.clock.schedule_interval(update, 1./10)

	### keep the app running
	### type escape to quit
	pyglet.app.run()

	server.shutdown()
