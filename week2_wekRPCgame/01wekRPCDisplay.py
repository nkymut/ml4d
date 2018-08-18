"""
Wekinator Rock Paper Scissors Game

This program listens to "/wek/outputs", and displays the corresponding image.
/wek/outputs/0 rock.png
/wek/outputs/1 paper.png
/wek/outputs/2 scissors.png
/wek/outputs/3 empty.png

"""
import pyglet
from pyglet.gl import *
import argparse
import math


from pythonosc import dispatcher
from pythonosc import osc_server
from pyglet.window import key
from wekinator import Wekinator 


class RPCApp(pyglet.window.Window):
    """
    hands : list of hand's name
    self.hand_idx: index value of the current hand selection
    """
    hands = ["Rock","Paper","Scissors"," "]
    hand_idx = 0
    #initialize method
    def __init__(self,*args, **kwargs):

        super().__init__(width=kwargs["width"], height=kwargs["height"],caption="RPCGame",
                             fullscreen=False,visible=True,resizable=False)
        ## initialize a label with text
        ## https://pyglet.readthedocs.io/en/pyglet-1.2-maintenance/api/pyglet/text/pyglet.text.Label.html
        self.label = pyglet.text.Label("My Hand",
                          font_size=72,
                          x=self.width//2, y=self.height//2,
                          anchor_x='center', anchor_y='center')
        self.label.color = (255,255,255,255)
        

        ### loading images
        ###  images are stored under "image" folder
        rock_image = pyglet.resource.image('image/rock.png')
        paper_image = pyglet.resource.image('image/paper.png')
        scissors_image = pyglet.resource.image('image/scissors.png')
        none_image = pyglet.resource.image('image/empty.png')
        ### create a list of images and set a default image
        self.hand_images = [rock_image,paper_image,scissors_image,none_image]

        ### initialize an OSC server to receive messages from Wekinator.
        self.wek_output = Wekinator(args[0].ip,args[0].port,self.on_wekinator_message)
        

        ### set an update function at an interval of 1/60 sec (60 times per sec)
        pyglet.clock.schedule_interval(self.update, 1/60.0)


    """
    update function
    called at the interval set by pyglet.clock.schedule_interval(update, 1/60.0)

    The first argument "dTime" stores exact inteval time passed from the last  

    dTime: interval time

    """
    def update(self,dTime, ):
        self.set_label_text(self.label,self.hands[self.hand_idx])
    
    """
    set text  to the label in the pyglet window. 
    """  
    def set_label_text(self,label, message):
        self.label.text = message

    """
    This function is called when anykey is pressd.

    if you import key objects: from pyglet.window import key

    you can check incoming key type with key variable
    key.a for "a" 
    key._1 for "1"

    Write code to draw something here.

    """

    def on_key_press(self, symbol, modifiers):

        if symbol == key._1:
            self.hand_idx = 0
        elif symbol == key._2:
            self.hand_idx = 1
        elif symbol == key._3:
            self.hand_idx = 2  
        elif symbol == key._4:
            self.hand_idx = 3  
    """
    this function is called(dispatched) when the program received 
    message from wekinator.
    addr: contains OSC address such as "/wek/outputs"
    *args: list of values sent by OSC message
    """
    def on_wekinator_message(self, addr, *args):

        ## print out incoming message
        print("Address: {} {}".format(addr,",".join(str(x) for x in args)))

        ## assign first value as a hand indexes (0:rock 1:paper 2:scissors 3:none)
        ## self.hand_idx variable is a global variable, changes made here will be applied 
        ## to the entire program.
        if(args[0] < 5):
            self.hand_idx = int(args[0]) - 1
        
        ## print out received hand.
        print("Hand: {}".format(self.hands[self.hand_idx]))

    """
    This function is called everytime pyglet window 
    refreshes its window.

    Write code to draw something here.
    """
    def on_draw(self):

        self.clear()

        self.hand_images[self.hand_idx].blit(0,0)
        self.label.draw()
    
    def on_close(self):
         ### stop OSC Server
        self.wek_output.close()
        super().on_close()
        

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

  ##create RPCApp window
  window = RPCApp(args, width=640, height=480)

  ### start pyglet app
  pyglet.app.run()

