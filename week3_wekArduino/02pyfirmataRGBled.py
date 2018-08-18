"""
Control LED Color with Wekinator output

"""

import pyglet
from pyfirmata import Arduino, util

import argparse
import math
from threading import Thread

from pythonosc import dispatcher
from pythonosc import osc_server
from pyglet.window import key


##create window
window = pyglet.window.Window()

##change this Arduino port to your setting.
#board = Arduino('/dev/cu.usbmodem1411') ##for Mac
board = Arduino('COM68')  ##for Windows
#iter8 = util.Iterator(board)
#iter8.start()


rgbLedPins = [9,10,11] #red, green, blue

##setup RGB led pins 
rgbLed = []
rgbLed.append(board.get_pin('d:9:p')) ## set "d"igital pin "9" as "p"wm output
rgbLed.append(board.get_pin('d:10:p')) ## set "d"igital pin "9" as "p"wm output
rgbLed.append(board.get_pin('d:11:p')) ## set "d"igital pin "9" as "p"wm output

rgbLedValues = [0,0,0]




dispatcher = dispatcher.Dispatcher()

"""
  this function is called(dispatched) when the program received 
  message from wekinator.
  addr: contains OSC address such as "/wek/outputs"
  *args: list of values sent by OSC message
"""
def wek_message_handler(addr, *args):
	global rgbLedValues
	## print out incoming message
	print("Address: {} {}".format(addr,",".join(str(x) for x in args)))

	## assign first value as a hand indexes (0:rock 1:paper 2:scissors 3:none)
	## hand_idx variable is a global variable, changes made here will be applied 
	## to the entire program.
	if(len(args) == 3):
		rgbLedValues = [args[0],args[1],args[2]]

	## print out received hand.
	print("RGB: ({},{},{})".format(rgbLedValues[0],rgbLedValues[1],rgbLedValues[2]))
	


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
  set text  to the label in the pyglet window. 
"""  
def set_label_text(label,message):

    label.text = message


def update(dt,):
	global rgbLedValues,label


	rgbLed[0].write(rgbLedValues[0]) #change LED status on ledPin
	rgbLed[1].write(rgbLedValues[1]) #change LED status on ledPin
	rgbLed[2].write(rgbLedValues[2]) #change LED status on ledPin

	pyglet.gl.glClearColor(rgbLedValues[0],rgbLedValues[1],rgbLedValues[2],1.)
	label.text = "({:.2f},{:.2f},{:.2f})".format(rgbLedValues[0],rgbLedValues[1],rgbLedValues[2])



"""
pyglet drawing function 

pyglet calls this function everytime refreshing the pyglet window.
write drawing function and frame-by-frame actions here.

"""
@window.event
def on_draw():
    window.clear() # clear the window. you can set different background color by pyglet.gl.glClearColor(R,G,B,alpha) 
    label.draw() # draw the label


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
	label = pyglet.text.Label('OFF',  font_name='Times New Roman',
	                  font_size=36,
	                  x=window.width//2, y=window.height//2,
	                  anchor_x='center', anchor_y='center')

	### initialize an OSC server to receive messages from Wekinator.
	server = init_OSC_server(args.ip,args.port,wek_message_handler)
	### set an update function at an interval of 1/60 sec
	pyglet.clock.schedule_interval(update, 1./10)

	### keep the app running
	### type escape to quit
	pyglet.app.run()

	server.shutdown()
