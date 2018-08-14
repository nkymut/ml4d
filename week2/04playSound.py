"""
4. play sound 

Install AVbin before executing the sample
http://avbin.github.io/AVbin/Download.html
"""

import pyglet
## import key symbols
## more details http://pyglet.readthedocs.io/en/pyglet-1.3-maintenance/programming_guide/keyboard.html
from pyglet.window import key

"""
0. hello world to pyglet

"""

import pyglet


class Window(pyglet.window.Window):
    #initialize method
    def __init__(self,*args, **kwargs):

        super().__init__(width=800, height=512,caption="04playSound.py",
                             fullscreen=False,visible=True,resizable=False)
        self.label1 = pyglet.text.Label('Press Key 1:Rock 2:Paper 3:Scissors',  font_name='Times New Roman',
                          font_size=24,
                          x=self.width//10, y=self.height//2+80,
                          anchor_x='left', anchor_y='center')
        ##loadsound from resource folder
        self.sound1 = pyglet.resource.media('rock.mp3', streaming=False)
        self.sound2 = pyglet.resource.media('paper.mp3', streaming=False)
        self.sound3 = pyglet.resource.media('scissors.mp3', streaming=False)
        self.soundlist = [self.sound1,self.sound2,self.sound3]
            
    #drawing method 
    def on_draw(self):
        self.clear()
        self.label1.draw()

    # handle key event  
    def on_key_press(self,symbol, modifiers):
      ## do something here
        print("{} pressed".format(chr(symbol)))
        #print(symbol)
        if symbol == key._1:
          self.soundlist[0].play()
        elif symbol == key._2:
          self.soundlist[1].play()
        elif symbol == key._3:
          self.soundlist[2].play()

    # handle mouse event
    def on_mouse_press(self,x, y, button, modifiers):
      global sound
      print("mouse pressed!")
      #play scissors sound
      soundlist[2].play()


#main function
def main():
    ##add "./sound" folder to the resource search path
    pyglet.resource.path = ['sound']
    pyglet.resource.reindex()
    ##create window
    window = Window(width=300, height=300)

    ### keep the app running
    ### type escape to quit
    pyglet.app.run()


if __name__ == '__main__':
    main()
