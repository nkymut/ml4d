"""
0. hello world to pyglet

"""

import pyglet

class Window(pyglet.window.Window):
    #initialize method
    def __init__(self,*args, **kwargs):

        super().__init__(width=512, height=512,caption="01HelloWorld.py",
                             fullscreen=False,visible=True,resizable=False)
        ## initialize a label with text
        ## https://pyglet.readthedocs.io/en/pyglet-1.2-maintenance/api/pyglet/text/pyglet.text.Label.html
        self.label = pyglet.text.Label('HOWDY',  font_name='Times New Roman',
                                font_size=36,
                                x=self.width//2, y=self.height//2,
                                anchor_x='center', anchor_y='center')
    
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