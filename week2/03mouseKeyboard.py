"""
3. handle mouse and keyboard

"""

import pyglet

class Window(pyglet.window.Window):
    # initialize method
    def __init__(self, *args, **kwargs):

        super().__init__(width=800, height=512,caption="03mouseKeyboard.py",
                             fullscreen=False,visible=True,resizable=True)
    
        # add label here to display mouse and key events!
        self.label1 = pyglet.text.Label('Key:',  font_name='Times New Roman',
                                font_size=36,
                                x=self.width//10, y=self.height//2+80,
                                anchor_x='left', anchor_y='center')

        self.label2 = pyglet.text.Label('Mouse Button:',  font_name='Times New Roman',
                                font_size=36,
                                x=self.width//10, y=self.height//2+20,
                                anchor_x='left', anchor_y='center')

        self.label3 = pyglet.text.Label('Mouse Pos:()',  font_name='Times New Roman',
                                font_size=36,
                                x=self.width//10, y=self.height//2-40,
                                anchor_x='left', anchor_y='center')
            
    # drawing method 
    def on_draw(self):
        self.clear()

        self.label1.draw() # draw label1 "Key: symbol(character)"
        self.label2.draw() # draw label2 "Mouse Button: button id"
        self.label3.draw() # draw label3 "Mouse Pos(x(dx),y(dy))"


    # handle key event  
    # http://pyglet.readthedocs.io/en/pyglet-1.3-maintenance/programming_guide/keyboard.html
    def on_key_press(self, symbol, modifiers):
       ## do something here 
        print("%s key pressed" % chr(symbol))
        ## formatting text sting and assign text to the label
        ## more detail about format string, read here https://pyformat.info/
        self.label1.text = "Key: {1} ({0})".format(symbol,chr(symbol))
    
    # handle mouse button event
    # on_mouse_press is called when any mouse button is pressed.
    def on_mouse_press(self, x, y, button, modifiers):
        print("mouse %s pressed at %d,%d" % (button,x,y))
        ## formatting text sting and assign text to the label
        ## detail about string, read here https://pyformat.info/
        self.label2.text = "Mouse Button:{0}".format(button)
        ## set background color to Red
        pyglet.gl.glClearColor(1,0,0,1.)
       
    # on_mouse_release is called when mouse button is released.
    def on_mouse_release(self, x, y, button, modifiers):
        self.label2.text = "Mouse Button:{0}".format(0)
        ## set background color to black
        pyglet.gl.glClearColor(0,0,0,1.) 

    # handle mouse motion event
    # on_mouse_motion(x, y, dx, dy):
    # x,y : x,y coordinate of the mosue
    # dx,dy : movement of the mouse since the last frame. 
    def on_mouse_motion(self, x, y, dx, dy):
        print("mouse motion at %d,%d (%d,%d)" % (x,y,dx,dy))
        self.label3.text = "Mouse Pos:({0}({2}),{1}({3}))".format(x,y,dx,dy)


#main function
def main():
    ##create window
    window = Window(width=300, height=300)

    ### keep the app running
    ### type escape to quit
    pyglet.app.run()


if __name__ == '__main__':
    main()

