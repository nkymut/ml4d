"""Wekinator Input Receiver

This program listens to "/wek/outputs", and prints out received packets.
"""
import pyglet
from pyglet.gl import *
import argparse
import math
from threading import Thread

from pythonosc import dispatcher
from pythonosc import osc_server
from pyglet.window import key


"""
global variables

hands : list of hand's name
hand_idx: index value of the current hand selection

"""
hands = ["Rock","Paper","Scissors"," "]
hand_idx = 0


window = pyglet.window.Window(640,480)
window.on_close = lambda:window.close()

label = pyglet.text.Label("My Hand",
                          font_size=72,
                          x=window.width//2, y=window.height//2,
                          anchor_x='center', anchor_y='center')


dispatcher = dispatcher.Dispatcher()

"""
  this function is called(dispatched) when the program received 
  message from wekinator.
  addr: contains OSC address such as "/wek/outputs"
  *args: list of values sent by OSC message
"""
def wek_message_handler(addr, *args):
    global hand_idx,label
    ## print out incoming message
    print("Address: {} {}".format(addr,",".join(str(x) for x in args)))

    ## assign first value as a hand indexes (0:rock 1:paper 2:scissors 3:none)
    ## hand_idx variable is a global variable, changes made here will be applied 
    ## to the entire program.
    if(args[0] < 5):
      hand_idx = int(args[0]) - 1
    
    ## print out received hand.
    print("Hand: {}".format(hands[hand_idx]))


"""
update function
called at the interval set by pyglet.clock.schedule_interval(update, 1/60.0)

The first argument "dTime" stores exact inteval time passed from the last  

dTime: interval time

"""
def update(dTime, ):
    global hand_idx,label
    set_label_text(label,hands[hand_idx])
    pass


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
def set_label_text(label, message):
    label.text = message


"""
This function is called everytime pyglet window 
refreshes its window.

Write code to draw something here.

"""
@window.event
def on_draw():
    global hand_idx,status,server

    window.clear()

    hand_images[hand_idx].blit(0,0)
     
    label.draw()


"""
This function is called when anykey is pressd.

if you import key objects: from pyglet.window import key

you can check incoming key type with key variable
key.a for "a" 
key._1 for "1"

Write code to draw something here.

"""

@window.event
def on_key_press(symbol, modifiers):
    global hand_idx 

    if symbol == key._1:
      hand_idx = 0
    elif symbol == key._2:
      hand_idx = 1
    elif symbol == key._3:
      hand_idx = 2  
    elif symbol == key._4:
      hand_idx = 3  

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

  ### initializing text label
  label = pyglet.text.Label("My hand",
                          font_size=72,
                          x=window.width//2, y=window.height//2,
                          anchor_x='center', anchor_y='center')
  label.color = (255,255,255,255)
  
  ### loading images
  ###  images are stored under "image" folder
  rock_image = pyglet.resource.image('image/rock_s.png')
  paper_image = pyglet.resource.image('image/paper_s.png')
  scissors_image = pyglet.resource.image('image/scissors_s.png')
  none_image = pyglet.resource.image('image/Empty.png')
  ### create a list of images and set a default image
  hand_images = [rock_image,paper_image,scissors_image,none_image]

  ### initialize an OSC server to receive messages from Wekinator.
  server = init_OSC_server(args.ip,args.port,wek_message_handler)
  
  ### set an update function at an interval of 1/60 sec (60 times per sec)
  pyglet.clock.schedule_interval(update, 1/60.0)

  ### start pyglet app
  pyglet.app.run()

  ### stop OSC Server
  server.shutdown()
