import pygame
import os
import math




class Ball(pygame.sprite.Sprite):
    def __init__(self, x, y, width, height, xv, yv):
        
        super().__init__()
        self.image = self.load("assets/ball2.png")
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.xv = xv #x and y velocity
        self.yv = yv

    def load(self, img): 
        #load image without bliting, this allows a transparent background        
        image = pygame.image.load(img)
        image = pygame.transform.scale(image, (35, 30)) #scale correctly
        return image
    
    def loadwithargs(self, img, x, y):
        #load function with modifiable args so classes that inherit
        #can have access
        image = pygame.image.load(img)
        image = pygame.transform.scale(image, (x, y))
        return image

#Block, spike, wall, portal all behave like ball and inherit from it    
class Block(Ball):
    def __init__(self, x, y, width, height, xv, yv):
        super().__init__(x, y, width, height, xv, yv)
        self.image = create_image(os.path.join("assets/block.jpg"),50,50)
        
class Spike(Block):
    def __init__(self, x, y, width, height, xv, yv):
        super().__init__(x, y, width, height, xv, yv)
        self.image = self.loadwithargs("assets/navalmine.png",50 ,50)
        
class Brickwall(Ball):
    def __init__(self, x, y, width, height, xv, yv):
        super().__init__(x, y, width, height, xv, yv)
        self.image = create_image(os.path.join("assets/brickwall.jpg"), width, height)

class Portal(Ball):
    def __init__(self, x, y, width, height, xv, yv):
        super().__init__(x, y, width, height, xv, yv)
        self.image = self.loadwithargs("assets/portal.png",50 ,50)

#Inherits from ball but adds orientation attribute
#And gives a way to spin the chevrons absolutley and relativley  
#based on orientation      
class Bluechevron(Ball):
    def __init__(self, x, y, width, height, xv, yv, orient):
        super().__init__(x, y, width, height, xv, yv)
        self.image = self.load("assets/bluechevron.png")  
        self.orient = 0
        
    def rotate(self, deg):
        self.image = pygame.transform.rotate(self.image, deg)
        return self.image
    
    #function takes desired chevron orientation
    def rotateto(self, orient):
        if self.orient != orient:
            #spin the chevron until it arrives into
            #the correct orientation
            for i in range(1, orient): 
                self.image = pygame.transform.rotate(self.image, 90)
            return self.image
        else:
            return self.image

#Greenchevron and anti glitch chevron inherit from the blue one
class Greenchevron(Bluechevron):
    def __init__(self, x, y, width, height, xv, yv, orient):
        super().__init__(x, y, width, height, xv, yv, orient)
        self.image = self.load("assets/greenchevron.png")
        
class cchev(Bluechevron):
    def __init__(self, x, y, width, height, xv, yv, orient):
        super().__init__(x, y, width, height, xv, yv, orient)
        self.image = self.load("assets/redchevron.png")

#global function to create a sprite the proper way
#taken from schulich ignite example code       
def create_image(image_location, width, height):

    """
    

    Args:
        image_location: A string representing the file location for the image
        width: The width of the output image in pixels
        height: The height of the output image in pixels
    
    Returns:
        A surface representing the output image.
    """
    
    pygame.display.init()
    tile_image = pygame.image.load(image_location).convert_alpha()
    # The tile is a square and the height is expected to be smaller than the width
    tile_width = height
    tile_height = height
    tile_image = pygame.transform.scale(tile_image, (tile_width, tile_height))
    #image = tile_image
    # The self.image attribute expects a Surface, so we can manually create one and "blit" the tile image onto the surface..
    image = pygame.Surface((width, height))
    
    
    blits_data = [(tile_image, (tile_width * i, 0)) for i in range(math.ceil(width / tile_width))]
    image.blits(blits_data)

    return image
    

#Global function to convert the direction that
#the ball is moving into an orientation for the chevrons 
def getdir(obj):
    if obj.xv == -1:
        return 1
    elif obj.xv == 1:
        return 3
    elif obj.yv == -1:
        return 2
    elif obj.yv == 1:
        return 0

