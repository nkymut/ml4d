"""
Wekinator Rock Paper Scissors Game (2 player version)


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

hands : list of hands
hand_idx: index value of the current hand selection

"""
hands = ["Rock","Paper","Scissors"," "]
hands_dict = {"Rock":0,"Paper":1, "Scissors":2}
hand_idx = 0
enemy_hand_idx = 0

results = ["Player A wins","Player B wins","draw" ] 

window = pyglet.window.Window(640,480)
window.on_close = lambda:window.close()

label = pyglet.text.Label("",
                          font_size=72,
                          x=window.width//2, y=window.height//2,
                          anchor_x='center', anchor_y='center')


dispatcher0 = dispatcher.Dispatcher()
dispatcher1 = dispatcher.Dispatcher()

def init_OSC_server(ip,port,dispatcher,osc_message_handler):
    dispatcher.map("/wek/outputs", osc_message_handler)

    server = osc_server.ThreadingOSCUDPServer(
        (ip, port), dispatcher)
    print("Serving on {}".format(server.server_address))

    server_thread = Thread(target=server.serve_forever)
    server_thread.daemon = True
    server_thread.start()

    return server

"""
  this function is called when the program received 
  message from wekinator.
"""
def wek_my_message_handler(addr, *args):
    global hand_idx,enemy_hand_idx
    print("My Hand: {} {}".format(addr,",".join(str(x) for x in args)))
    
    if(args[0] < 4):
      hand_idx = int(args[0]) - 1
      print("Hand: {}".format(hands[hand_idx]))

def wek_enemy_message_handler(addr, *args):
    global hand_idx,enemy_hand_idx
    print("Enemy Hand: {} {}".format(addr,",".join(str(x) for x in args)))
    
    if(args[0] < 4):
      enemy_hand_idx = int(args[0]) - 1
      print("Hand: {}".format(hands[enemy_hand_idx]))

def game_logic(hand_idx,enemy_hand_idx):
    truth_table = [ [ 2, 1, 0 ] , [0 , 2, 1] , [1, 0, 2 ] ]
    result_idx = truth_table[hand_idx][enemy_hand_idx]

    #print("my_hand:{}, enemy_hand:{}".format(hands[hand_idx],hands[enemy_hand_idx]))
    result = results[result_idx]

    return hand_idx, enemy_hand_idx, result 



def update(dTime, ):
    global hand_idx, enemy_hand_idx
    hand_idx, enemy_hand_idx, result = game_logic(hand_idx,enemy_hand_idx)

    set_label_text(my_hand_label,hands[hand_idx])
    set_label_text(enemy_hand_label,hands[enemy_hand_idx])
    set_label_text(game_label,result)


"""
  set text  to the label in the pyglet window. 
"""  
def set_label_text(label,message):

    label.text = message


"""
This function is called everytime pyglet window 
refresh the screen.

Write code to draw something here.

"""
@window.event
def on_draw():
    global hand_idx,enemy_hand_idx,status,server
    #enemy_hand_idx = game_logic(hand_idx,enemy_hand_idx)
    window.clear()
    hand_images[hand_idx].blit(0,0) 
    enemy_hand_images[enemy_hand_idx].blit(window.width,0)

    game_label.draw()
    my_hand_label.draw()
    enemy_hand_label.draw()


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
    global hand_idx,enemy_hand_idx 

    if symbol == key._1:
      hand_idx = 0
    elif symbol == key._2:
      hand_idx = 1
    elif symbol == key._3:
      hand_idx = 2  
    elif symbol == key._4:
      hand_idx = 3  
    elif symbol == key._8:
      enemy_hand_idx = 0
    elif symbol == key._9:
      enemy_hand_idx = 1  
    elif symbol == key._0:
      enemy_hand_idx = 2  
    


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
  my_hand_label = pyglet.text.Label("Me",
                          font_size=36,
                          x=window.width/4, y=window.height/4,
                          anchor_x='center', anchor_y='center')
  my_hand_label.color = (255,255,255,255)

  enemy_hand_label = pyglet.text.Label("Enemy",
                          font_size=36,
                          x=window.width/4*3, y=window.height/4,
                          anchor_x='center', anchor_y='center')
  enemy_hand_label.color = (255,255,255,255)


  game_label = pyglet.text.Label("Enemy",
                          font_size=36,
                          x=window.width/2, y=window.height/4*3,
                          anchor_x='center', anchor_y='center')
  game_label.color = (255,255,255,255)
  
  ### loading images
  ###  images are stored under "image" folder
  rock_image = pyglet.resource.image('image/rock.png')
  paper_image = pyglet.resource.image('image/paper.png')
  scissors_image = pyglet.resource.image('image/scissors.png')

  enemy_rock_image = pyglet.resource.image('image/rock.png', flip_x=True)
  enemy_paper_image = pyglet.resource.image('image/paper.png',flip_x=True)
  enemy_scissors_image = pyglet.resource.image('image/scissors.png',flip_x=True)
  
  ### create a list of images and set a default image
  hand_images = [rock_image,paper_image,scissors_image]
  enemy_hand_images =  [enemy_rock_image,enemy_paper_image,enemy_scissors_image]

  ### initialize an OSC server to receive messages from Wekinator.
  server = init_OSC_server("127.0.0.1",12000,dispatcher0,wek_my_message_handler)

  server1 = init_OSC_server(args.ip,12001,dispatcher1,wek_enemy_message_handler)

  ### set an update function at an interval of 1/60 sec (60 times per sec)
  pyglet.clock.schedule_interval(update, 1/60.0)

  pyglet.app.run()

  server.shutdown()
