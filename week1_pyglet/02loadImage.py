"""
2. load image to pyglet

"""

import pyglet


class Window(pyglet.window.Window):
    #initialize method
    def __init__(self,*args, **kwargs):

        super().__init__(width=850, height=512,caption="02loadImage.py",
                             fullscreen=False,visible=True,resizable=True)
    
        """
        Example 1: loading image from the known resource directory
        by default it loads files from current directory '.'
        you can add more directories to the resource seeach path by defining 

        pyglet.resource.path = ['.','folder1','folder2'] 
        pyglet.resource.reindex()

        more detail
        https://pyglet.readthedocs.io/en/pyglet-1.2-maintenance/api/pyglet/pyglet.resource.html#module-pyglet.resource
        """
        self.image = pyglet.resource.image('image/kitten.jpg')

        """
        Example2: loading image from any directory path
        To load from current directory you must add './' (mac) or '.\' before the filename.
        Otherwise, you have to provide the full path to the image file, 
        for example

        image1 = pyglet.image.load("c:\week2\image\kitten.jpg") #Windows
        image1 = pyglet.image.load("/User/username/week2/image/kitten.jpg") #Mac

        more detail
        https://pyglet.readthedocs.io/en/pyglet-1.2-maintenance/api/pyglet/pyglet.image.html
        ##pyglet.resource.image 
        """
        self.image1 = pyglet.image.load('./image/kitten.jpg')
    
    #drawing method 
    def on_draw(self):
        self.clear()

        self.image.blit(100, 50) ## draw the image on the screen image.blit(X, Y)
        self.image1.blit(450, 50) ## draw the image on the screen image.blit(X, Y)



#main function
def main():
    ##create window
    window = Window(width=300, height=300)

    ### keep the app running
    ### type escape to quit
    pyglet.app.run()


if __name__ == '__main__':
    main()