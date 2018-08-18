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
from pythonosc import udp_client

from pyglet.window import key

import os
import shutil
import cv2
from PIL import Image
import numpy as np


"""
global variables

"""

isTraining = False
isRunning = False

window = pyglet.window.Window(640,480)
window.on_close = lambda:window.close()
keys = key.KeyStateHandler()
window.push_handlers(keys)


dispatcher = dispatcher.Dispatcher()

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
  sending message to wekinator input.
  addr: contains OSC address such as "/wek/outputs"
  args: a value or list of values to be sent by OSC message
"""

def wek_send_message(addr, args):
  print("Address: {} {}".format(addr,len(args)))
  #print("Address: {} {}".format(len(args),",".join(str(x) for x in args)))
  # msg = osc_message_builder.OscMessageBuilder(address="/wek/inputs")
  # # Add 3 messages in the bundle, each with more arguments.

  client.send_message(addr, args)

"""
  this function is called(dispatched) when the program received 
  message from wekinator.
  addr: contains OSC address such as "/wek/outputs"
  *args: list of values sent by OSC message
"""
def wek_message_handler(addr, *args):
    global hand_idx,label
    ## print out incoming message
    #print("Address: {} {}".format(addr,",".join(str(x) for x in args)))

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
  global originalImage, pixelatedImage, resizedImage
  ret, frame = cap.read()

  # Our operations on the frame come here
  #gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
  originalImage = cv2glet(frame,'BGR')

  # resize image to 10x10 pixel 
  resizedImage = cv2.resize(frame, (10, 10))
  #resizedImage = cv2.cvtColor(resizedImage, cv2.COLOR_BGR2GRAY)

  # create 200x200 pyglet image for display.
  pixelatedImage = cv2glet(cv2.resize(resizedImage, (200, 200),interpolation=cv2.INTER_AREA),'BGR')
  pixelVal = resizedImage.ravel().astype(float)


  label.text = np.array2string(resizedImage[:,:,0], separator='  ')
  #label.text = np.array2string(pixelVal, separator='  ')
  if isTraining or isRunning:
    wek_send_message("/wek/inputs",pixelVal)
  pass


"""
convert opencv image to pyglet image

"""  
def cv2glet(img,format):
    '''Assumes image is in BGR color space. Returns a pyimg object'''
    if format == 'GRAY':
      rows, cols = img.shape
      channels = 1
    else:
      rows, cols, channels = img.shape

    raw_img = Image.fromarray(img).tobytes()

    top_to_bottom_flag = -1
    bytes_per_row = channels*cols
    pyimg = pyglet.image.ImageData(width=cols, 
                                   height=rows, 
                                   format=format, 
                                   data=raw_img, 
                                   pitch=top_to_bottom_flag*bytes_per_row)
    return pyimg



"""
This function is called everytime pyglet window 
refreshes its window.

Write code to draw something here.

"""
@window.event
def on_draw():
    global hand_idx,status,server,isRunning,isTraining

    #change background colour by running statuses 
    if isTraining:
      pyglet.gl.glClearColor(0.7,0,0,1) #RED
    elif isRunning:
      pyglet.gl.glClearColor(0,0.7,0,1) #GREEN
    else:
      pyglet.gl.glClearColor(0,0,0,1) #BLACK

    window.clear()
    originalImage.blit(0,window.height-240, width=320,height=240)
    pixelatedImage.blit(320,window.height-240, width=320,height=240)

    label.draw()
    instructionLabel.draw()
    statusLabel.draw()


"""
This function is called when any keyboard button is pressd.

if you import key objects: from pyglet.window import key

you can check incoming key type with key variable,
for example
  key.a for "a" 
  key._1 for "1"

"""

@window.event
def on_key_press(symbol, modifiers):
    global resizedImage,isTraining,isRunning, statusLabel

    if symbol == key._1:
      wek_send_message("/wekinator/control/outputs", [1.0])
      statusLabel.text = "sending Class 1"
    elif symbol == key._2:
      wek_send_message("/wekinator/control/outputs", [2.0])
      statusLabel.text = "sending Class 2"
    elif symbol == key._3:
      wek_send_message("/wekinator/control/outputs", [3.0])
      statusLabel.text = "sending Class 3"
    elif symbol == key._4:
      wek_send_message("/wekinator/control/outputs", [4.0])
      statusLabel.text = "sending Class 4"
    elif symbol == key._5:
      wek_send_message("/wekinator/control/outputs", [5.0])
      statusLabel.text = "sending Class 5"

    if symbol == key.ENTER:
      wek_send_message("/wekinator/control/startRunning", [1.0])
      statusLabel.text = "Wekinator is Running."
      isRunning = True
    elif symbol == key.T:
      wek_send_message("/wekinator/control/train", [1.0])  
      statusLabel.text = "Wekinator is Training."
    else:
      isTraining = True
      wek_send_message("/wekinator/control/startRecording", [1.0])

"""
This function is called when any keyboard button is released.
"""   
@window.event
def on_key_release(symbol, modifiers):
    global resizedImage,isTraining, statusLabel

    statusLabel.text = ""
    if isTraining:
      wek_send_message("/wekinator/control/stopRecording", [1.0])
      isTraining = False

    


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

  
  cap = cv2.VideoCapture(0) #open first webcam

  if cap.isOpened():
    ret, frame = cap.read()
    originalImage = cv2glet(frame,'BGR')
    pixelatedImage = cv2glet(cv2.resize(frame, (10, 10)),'BGR')
  else:
    sys.exit("Cannot open webcam input.")

  ### initializing text label
  label = pyglet.text.Label("Cat",
                          font_size=9,
                          x=window.width/2, y=window.height//2 - 8,width=320,height=240,
                          anchor_x='left', anchor_y='top',multiline=True,)
  label.color = (255,255,255,255)
  
  instructionText ="INSTRUCTION:\n 1.Press Key [1-5]: send training data from 1 to 5. \n2.Press 't' to train data.\n3.Press 'ENTER' to start Running the model."

  instructionLabel = pyglet.text.Label(instructionText,
                          font_size=9,
                          x=10, y=window.height//2 - 8,width=320,height=240,
                          anchor_x='left', anchor_y='top',multiline=True,)

  statusText = ""
  statusLabel = pyglet.text.Label(statusText,
                          font_size=12,
                          x=10, y=window.height//4 - 8,width=320,height=240,
                          anchor_x='left', anchor_y='top',multiline=True,)

  label.color = (255,255,255,255)

  client = udp_client.SimpleUDPClient(args.ip, 6448) ## setup OSC client to Wekinator localhost port 6448



  ### loading images
  ###  images are stored under "image" folder
  #rock_image = pyglet.resource.image('image/rock_s.png')

  ### initialize an OSC server to receive messages from Wekinator.
  #server = init_OSC_server(args.ip,args.port,wek_message_handler)
  
  ### set an update function at an interval of 1/60 sec (60 times per sec)
  pyglet.clock.schedule_interval(update, 1/30.0)

  ### start pyglet app
  pyglet.app.run()

  # When everything done, release the capture
  cap.release()
  cv2.destroyAllWindows()

  ### stop OSC Server
  server.shutdown()
