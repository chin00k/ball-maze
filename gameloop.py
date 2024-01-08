
#This file contains the main pygame game loop

#Function called by the game manager
def main(userseed, px, py):

    import pygame
    import random
    from objects import Ball, Block, Brickwall, Spike, cchev
    from objects import Bluechevron, getdir, Greenchevron, Portal
    from objectmap import setup
    
    #gets the seed for the map
    string = userseed
    
    
    pygame.init() #starts pygame
    
    """
    SETUP section - preparing everything before the main loop runs
    """
    
    
    #Shorter way of calling randint
    def cr(lb, ub):
        return random.randint(lb, ub)
    
    #Makes sure that we know what to print as a final score before it is wiped
    def keepscore(score):
        global printscore
        printscore = score
    
    #Function to check if you are trying to commit into another block or out
    #of the map. It would require 4 paramters if it was in the objects file
    def objhit(orient):
        
        '''
        The function uses a hidden red chevron to do the checking.
        When you commit, it puts the chevron where you want to go
        and checks if the hidden chevron collides against anything
        '''
        
        #Puts the chevron inside the focusblock
        cc1.rect.x = focusblock[0] + 7
        cc1.rect.y = focusblock[1] + 10
        
        #Moves to chevron in the direction of the requested commit
        #Basically it puts it where the block will spit you out
        if orient == 0:
            cc1.rect.y -= 50
        if orient == 2:
            cc1.rect.y += 50
        if orient == 1:
            cc1.rect.x -= 50
        if orient == 3:
            cc1.rect.x += 50
        
        #Checks if the chevron is outside of the map
        if cc1.rect.x <= 100 or cc1.rect.x >= 900:
            return True
        if cc1.rect.y <= 0 or cc1.rect.y >= 800:
            return True
        
        #Checks if the chevron is inside another block
        for block in blocks:
            if pygame.sprite.collide_mask(cc1, block):
                return True
            
        
    # Global constants
    SCREEN_WIDTH = 1000
    SCREEN_HEIGHT = 800
    FRAME_RATE = 120
    
    # Useful colors 
    BLACK = (0, 0, 0)
    WHITE = (25, 155, 255)
    BROWN = (168, 119, 50)
    fblue = (124, 193, 206)
    
    # Creating the screen and the clock
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    screen.set_alpha(0)  # Make alpha bits transparent
    clock = pygame.time.Clock()
       
    #Adding the ball 
    b1 = Ball(105, 410, 37, 30, 0, 0)
    ball = pygame.sprite.Group()
    ball.add(b1)
    b1.xv = 1
    b1.yv = 0
    
    #creting group for blocks and portal and spikes
    blocks = pygame.sprite.Group()
    
    portals = pygame.sprite.Group()
    
    spikes = pygame.sprite.Group()
    
    #defining fonts for labels
    myfont = pygame.font.Font("fonts/ESSTIX13.TTF", 30)
    sysfont = pygame.font.SysFont("", 50)
    
    #Function to generate the map
    #Takes the seed from the manager
    #and the portal xy if it is given
    def setupmap(string, px, py):
        #Clearing group of blocks and portals
        blocks.empty()
        portals.empty()
        spikes.empty()
        
        #Takes arguments from the game manager
        #px is never actaully -1
        #So when it is seen, it puts it in manual generation mode
        if px != -1:
            manualset = True
        else:
            manualset = False
        
        #Generating an array to represent the map
        objectsarray = setup(string, manualset, px, py)
        
        #Clearing a path in front for the ball
        objectsarray[8][0] = 0
        objectsarray[8][1] = 0
        objectsarray[8][2] = 0
        
        #Adding the blocks and portals
        for i in range(16):
            for j in range(16):
                #Adding entities to correspond to the values in the map array
                #that was generated based on the seed in a funtion in objectmap.py
                if objectsarray[i][j] == 1:
                    
                    blocks.add(Block(100 + 50*j, 50*i, 50, 50, 0, 0))
                    
                if objectsarray[i][j] == 9:
                    #there will only be 1 portal
                    p1 = Portal(100 + 50*j, 50*i, 10, 10, 0, 0)
                    portals.add(p1)
                    
                if objectsarray[i][j] == 5:
                    spikes.add(Spike(100 + 50*j, 50*i, 50, 50, 0, 0))
                    
    
    #adding the walls
    br1 = Brickwall(0, 0, 100, 800, 0, 0)
    br2 = Brickwall(900, 0, 100, 800, 0, 0)
    walls = pygame.sprite.Group()
    walls.add(br1, br2)
    
    
    #intializing the focusblock. Putting it outside so that it is invisible
    #until the first collision
    focusblock = [-1000, 0]
    
    #Creating the blue and green chevron
    bc1 = Bluechevron(0, 0, 20, 20, 0, 0, 0)
    bc = pygame.sprite.Group()
    bc.add(bc1)
    
    gc1 = Greenchevron(0, 0, 20, 20, 0, 0, 0)
    gc = pygame.sprite.Group()
    gc.add(gc1)
    
    cc1 = cchev(-200, 0, 20, 20, 0, 0, 0)
    cc = pygame.sprite.Group()
    cc.add(cc1)
    
    
    #Setting up some important variables
    
    bouncecounter = 0 #Prevents glitching when bouncing against the walls
    keycooldown = 0
    
    #all these are to handle when you win/lose and when to draw the banner
    committed = False
    winstate = False
    losestate = False
    
    drawvic = 0
    drawvicflag = False
    
    drawdef = 0
    drawdefflag = False
    
    commitcount = 0
    
    #calls setupmap and finally loads the map
    setupmap(string, px, py)
    
    while True:
        """
        EVENTS section - how the code reacts when users do things
        """

        for event in pygame.event.get():
            if event.type == pygame.QUIT:  # When user clicks the 'x' on the window, close our game
                pygame.quit()
                return
    
        # Keyboard events
        keys_pressed = pygame.key.get_pressed()

        # option to quit from the keyboard
        if keys_pressed[pygame.K_q]:
            pygame.quit()
            return
        
        keycooldown += 1
        
        if committed == False:
            #Spins the chevron if not committed
            if keys_pressed[pygame.K_LEFT] and keycooldown > 15:
                
                #Actually rotates the chevrons
                bc1.rotate(-90)
                gc1.rotate(-90)
                
                #Keeps orientation between 0 and 3
                if bc1.orient == 0:
                    bc1.orient = 3
                else:
                    bc1.orient -= 1
                
                    
                if gc1.orient == 0:
                    gc1.orient = 3
                else:
                    gc1.orient -= 1
                
                
                keycooldown = 0 #resets the key cooldown
                
        #Commits
        if keys_pressed[pygame.K_DOWN] and keycooldown > 15:
            
            #Fixes sequential incrementation error when a
            #winstate is activated
            if committed == False:
                commitcount += 1
            
            #Checks that a commit is legal
            if objhit(bc1.orient):
                commitcount -= 1 #makes sure that bad commits aren't counted
            else:
                committed = True
            
            
            keycooldown = 0
            
        #Reset the map   
        if keys_pressed[pygame.K_r] and keycooldown > 15:
            b1.rect.x = 105 #Moves the ball to start pos
            b1.rect.y = 410
            b1.xv = 1 #resets movement
            b1.yv = 0
            setupmap(string, px, py) #resets map
            focusblock = [-1000, 0] #resets the focusblock
            commitcount = 0
            winstate = False
            
            keycooldown = 0
        
        #Keeping orientation in check
        if bc1.orient == 4 or bc1.orient == -4:
            bc1.orient = 0
        if gc1.orient == 4 or gc1.orient == -4:
            gc1.orient = 0
        
    
    
        """
        UPDATE section - manipulate everything on the screen
        """
        
        #Code to update the victory banner
        if drawvicflag and drawvic <= 300:
            #2 different labels had to be used because of
            #font rendering issues
            victory = myfont.render("Victory with a commit score of" , 20, (255,255,255))
            scorelabel =  sysfont.render(str(printscore), 20, (255,255,255))
            drawvic += 1 #makes sure we display for 300 frames
            b1.rect.x -= 1
        else:
            #does nothing otherwise
            victory = myfont.render("" , 20, (255,255,255))
            scorelabel =  sysfont.render("", 20, (255,255,255))
            
        #same as above but for defeat banner
        if drawdefflag == True and drawdef <= 300:
            defeat = myfont.render("Defeat" , 20, (255,255,255))
            drawdef += 1
            b1.rect.x -= 1
        else:       
            defeat = myfont.render("" , 20, (255,255,0))
        
        #What to do if we have lost
        #see key_r event for details
        if losestate == True:
            drawdef = 0
            drawdefflag = True
            b1.rect.x = 105
            b1.rect.y = 410
            b1.xv = 1
            b1.yv = 0
            #Reset the map
            setupmap(string, px, py)
            focusblock = [-1000, 0]
            commitcount = 0
            losestate = False
        
        #What to do if you have won
        if winstate == True:
            keepscore(commitcount)
            drawvic = 0
            drawvicflag = True
            b1.rect.x = 105
            b1.rect.y = 410
            b1.xv = 1
            b1.yv = 0
            #Reset the map
            setupmap(string, px, py)
            focusblock = [-1000, 0]
            commitcount = 0
            winstate = False
            
        #Collsion against walls section
        bouncecounter += 1
        
        #Makes sure that we can't glitch out while bouncing
        #off the wall
        if bouncecounter >= 1:
            if b1.rect.x >= 870 or b1.rect.x <= 95:
                b1.xv *= -1
                            
            elif b1.rect.y >= 770 or b1.rect.y <= 0:
                b1.yv *= -1
                
        
        #Collision against blocks section
        
        for block in blocks:
            
            #Collide_mask worked batter than collide_rect
            if pygame.sprite.collide_mask(b1, block):
                
                #If ball is coming from below or above
                if b1.rect.left >= block.rect.left and b1.rect.right >= block.rect.right:                                    
                    
                    # makes sure to only switch the chevron if not committed
                    if committed == False:
                        focusblock = [block.rect.x, block.rect.y]
                    
                    
                    #Makes sure that bounce is against committed block
                    if committed == True and getdir(b1) == 2 and pygame.sprite.collide_rect(block, bc1) == True:
                        
                        #Moving up
                        
                        
                        if bc1.orient == 3: #Chevron pointing right
                            b1.yv = 0
                            b1.rect.y -= 40
                            b1.rect.x += 40
                            b1.xv = -1
                        elif bc1.orient == 1: #Chevron pointing left
                            b1.yv = 0
                            b1.rect.y -= 40
                            b1.rect.x -= 40
                            b1.xv = 1
                        elif bc1.orient == 0: #Chevron pointing up
                            b1.rect.y -= 80
                        else:
                            b1.yv *= -1 #Just bounce off
                            
                        committed = False
                    
                    
                    elif committed == True and getdir(b1) == 0 and pygame.sprite.collide_rect(block, bc1) == True:
                        
                        #Moving down
                        
                        if bc1.orient == 3: #Chevron pointing right
                            b1.yv = 0
                            b1.rect.y += 40
                            b1.rect.x += 40
                            b1.xv = -1
                        elif bc1.orient == 1: #Chevron pointing left
                            b1.yv = 0
                            b1.rect.y += 40
                            b1.rect.x -= 40
                            b1.xv = 1
                        elif bc1.orient == 2: #Chevron pointing down
                            b1.rect.y += 80
                        else:
                            b1.yv *= -1 #Just bounce off
                            
                        committed = False
                        
                    else:
                        b1.yv *= -1
                    
                    
                    
                
                #if ball is coming from left or right    
                if b1.rect.bottom >= block.rect.top and b1.rect.top <= block.rect.bottom:
                    
                    #switch chevron only if not committed
                    if committed == False:
                        focusblock = [block.rect.x, block.rect.y]
                    
                    if committed == True and getdir(b1) == 3 and pygame.sprite.collide_rect(block, bc1) == True:
                        
                        #Moving right
                        
                        if bc1.orient == 0: #Chevron point up
                            b1.xv = 0
                            b1.rect.x += 40
                            b1.rect.y -= 40
                            b1.yv = -1
                        elif bc1.orient == 2: #Chevron pointing down
                            b1.xv = 0
                            b1.rect.x += 40
                            b1.rect.y += 40
                            b1.yv = 1
                        elif bc1.orient == 3: #Chevron pointing right
                            b1.rect.x += 80
                        else:
                            b1.xv *= -1 #Just bounce
                            
    
                        committed = False
                    
                    elif committed == True and getdir(b1) == 1 and pygame.sprite.collide_rect(block, bc1) == True:
                        
                        #Moving left
                        
                        if bc1.orient == 0: #Chevron pointing up
                            b1.yv = -1
                            b1.rect.y -= 40
                            b1.rect.x -= 40
                            b1.xv = 0
                        elif bc1.orient == 2: #Chevron pointing down
                            b1.yv = 1
                            b1.rect.y += 40
                            b1.rect.x -= 40
                            b1.xv = 0
                        elif bc1.orient == 1:
                            b1.rect.x -= 80 #Chevron Pointing Left
                        else:
                            b1.xv *= -1 #Just bounce
                            
                        committed = False
                    else:
                        b1.xv *= -1
            
        #If hitting the portal, you win
        for portal in portals:
            if pygame.sprite.collide_rect(b1, portal):
                winstate = True
        
        #if you hit the spikes, you lose        
        for spike in spikes:
            if pygame.sprite.collide_rect(b1, spike):
                losestate = True
    
        #Movement of ball
           
        b1.rect.x += b1.xv
        b1.rect.y += b1.yv      
        
        #Changing where the chevrons will be
        bc1.rect.x = focusblock[0] + 7
        bc1.rect.y = focusblock[1] + 10
        gc1.rect.x = focusblock[0] + 7
        gc1.rect.y = focusblock[1] + 10
        
        
        
        """
        DRAW section - make everything show up on screen
        """
        
        
        
        screen.fill(fblue)  # Fill the screen with one colour
        
        #draw sprites in proper order
        
        walls.draw(screen)
        if winstate == False: #only draw the ball if still in the game
            ball.draw(screen)
        blocks.draw(screen)
        portals.draw(screen)
        
        spikes.draw(screen)
        
        #Draw one chevron, hide the other
        if winstate == False:
            if committed == False:
                bc.draw(screen)
            elif committed == True:
                gc.draw(screen)
        
        #draws victory banner if needed
        if drawvicflag and drawvic <= 300:
            pygame.draw.rect(screen, BLACK, (0, 390, 1000, 50))
            screen.blit(victory, (300,400))
            screen.blit(scorelabel, (695, 399))
        
        #draws defeat banner if needed
        if drawdefflag and drawdef <= 300:
            pygame.draw.rect(screen, BLACK, (0, 390, 1000, 50))
            screen.blit(defeat, (450,400))   
        
       #cc.draw(screen) #Uncomment this to see the anti-glitch chevron
        
        pygame.display.flip()  # Pygame uses a double-buffer, without this we see half-completed frames
        clock.tick(100)  # Pause the clock to always maintain FRAME_RATE frames per second

