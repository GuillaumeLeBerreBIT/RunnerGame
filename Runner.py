import pygame
# Now closing pygame will cause an error, because we stil keep the while loop open >> Most secure to close pygame == sys module
# One of the commands lets you close any kind of code you have opened entirely
from sys import exit
from random import randint, choice

############ FUNCTIONS ############
# Can add all of the code for the player
class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()      # This is to initialize the sprite class inside this class as well. 
    
        # Surface of the player both images to create animation
        player_walk_1 = pygame.image.load('graphics/Player/player_walk_1.png').convert_alpha()
        player_walk_2 = pygame.image.load('graphics/Player/player_walk_2.png').convert_alpha()
        # Surface when the player is walking between 2 images (animation)
        self.player_walk = [player_walk_1, player_walk_2]       # -- > Need self to acces it outside the __init__
        # Use to pick the different surfaces of player walk
        self.player_index = 0
        # Surface when the player jumps
        self.player_jump = pygame.image.load('graphics/Player/jump.png').convert_alpha()
        
        # self.image is the surface that is going to be dispayed by default
        self.image = self.player_walk[self.player_index]
        # self.rect is to figure where the ectangle is going to go
        self.rect = self.image.get_rect(midbottom = (80,300))
        # Need a gravity for all of this
        self.gravity = 0 
        
        self.jump_sound = pygame.mixer.Sound('audio/jump.mp3')
        self.jump_sound.set_volume(0.2) # Can set a value from 1 to 0 to either mute it or be louder
    
    def player_input(self):
        # Will give all possible key inputs
        keys = pygame.key.get_pressed()                           # -- > KEYBOARD BUTTON COLLISION OPTION 1
        if keys[pygame.K_SPACE] and self.rect.bottom >= 300:
            self.gravity = -20
            # To play the jump sound
            self.jump_sound.play()
        
    def apply_gravity(self):
        self.gravity += 1
        # Selecting the rectangle to move it & apply the gravity towards it
        self.rect.y += self.gravity
        # This will make sure the player does not keep falling -- > When dropping below will keep setting it on the ground 
        if self.rect.bottom >= 300:
            self.rect.bottom = 300
            
    def animation_state(self):
        # First want to check if the player is on the floor or in the air
        if self.rect.bottom < 300: 
            # Draw the jump animation
            self.image = self.player_jump
        else: 
            # Keep increasing the index value
            self.player_index += 0.1 
            # Set the index to 0 if it is bigger then the length of the list images player_walk
            if self.player_index >= len(self.player_walk): self.player_index = 0
            # The image to draw
            self.image = self.player_walk[int(self.player_index)]
        
    # This is a function to update all of its sprites
    def update(self):
        self.player_input()
        self.apply_gravity()
        self.animation_state()
        

class Obstacle(pygame.sprite.Sprite):
    
    def __init__(self, type) :
        super().__init__()
        
        # If statement to import different type of images depending on what I get. 
        # When creating the obstacle can type in what kind of obstacle u want by defining the "TYPE" 
        # -- > Then get a list with all of frames & y_pos -- > Get the image to get a rectangle
        if type == 'flye':
            # Fly imgages
            fly_1 = pygame.image.load('graphics/Fly/Fly1.png').convert_alpha()
            fly_2 = pygame.image.load('graphics/Fly/Fly2.png').convert_alpha()
            self.frames = [fly_1, fly_2]
            y_pos = 210
        else:
            # SNAIL IMAGES
            snail_1 = pygame.image.load('graphics/snail/snail1.png').convert_alpha() # Removing alpha values
            snail_2 = pygame.image.load('graphics/snail/snail2.png').convert_alpha() # Removing alpha values
            # List to change over the surface animations. 
            self.frames = [snail_1, snail_2]
            y_pos = 300
        # Index of the frame list    
        self.animation_index = 0
        # The frame to draw (surface from the list)
        self.image = self.frames[self.animation_index]
        # The position of the image to spawn/draw
        self.rect = self.image.get_rect(midbottom = (randint(900,1100), y_pos))
        
    def animation_state(self):
        # Keep increasing the index value
        self.animation_index += 0.1 
        # Set the index to 0 if it is bigger then the length of the list images player_walk
        if self.animation_index >= len(self.frames): self.animation_index = 0
        # The image to draw
        self.image = self.frames[int(self.animation_index)]
    
    def update(self):
        self.animation_state()
        # To move fly/snail to the left every cycle of the game loop by substracting couple of pixels every game loop updates
        self.rect.x -= 6
        self.destroy()
        
    def destroy(self):
        # If the obstacle is far outside the screen want to destroy it >> To remove OBJECTS from the list to save space and spare computational resources. 
        if self.rect.x <= -100:
            self.kill()
        
def display_score():    # Do not need any arguments
    # Convert to seconds 
    current_time = int(pygame.time.get_ticks() / 1000) - start_time     # Will from the time since pygame.init() subtract the time since RESTARTING the game (current iteration)
    # Change the integer to string OTHERWISE ERROR
    score_surf = test_font.render(f'Score: {current_time}', False, (64,64,64))      # TEXT SURFACE == RENDER(text, Anti-Aliase, color) 
    score_rect = score_surf.get_rect(center = (400,50))      # Place the SCORE on the center of the screen.
    screen.blit(score_surf,score_rect)      # The score TEXT -- > 300 from LEFT & 50 from the top
    return current_time     # To access the variable everywhere

#def obstacle_movement(obstacle_list):
#    #If the list is empty will not do it
#    if obstacle_list:
#        # Each rectangle iterated from the list >> Due to random adding Snails and Fly's in get_rect. 
#        for obstacle_rect in obstacle_list:
#            obstacle_rect.x -= 5    # Define the speed, every single obstacle will be moved towards the left on every cycle of the game loop.
#            
#            # Draw on the screen the apropriate surface based on the position of the snail
#            if obstacle_rect.bottom == 300:
#                screen.blit(snail_surface, obstacle_rect) # Draw snail 
#            else:
#                screen.blit(fly_surface, obstacle_rect) # Draw the fly 
#                
#                
#        # Want to remove the object from the lsit to far to the left >> Checks every object in the list and if they are of the screen do not add to list
#        obstacle_list = [obstacle for obstacle in obstacle_list if obstacle.x > -100]
#        
#        return obstacle_list
#    # First time obstacle will be empty due to timer not been triggered. Need to return a list since the above returns 'None' which is non appended. 
#    else:
#        return []

# End the game of player and object collide. 
def collisions(player, obstacles):
    # Want to check if there are obstacles in the first palce. 
    if obstacles:
        for obstacle_rect in obstacles:
            # Check if any of the obstacles colliding with the player
            if player.colliderect(obstacle_rect): 
                return False # If there is collision set to false == GLOBAL SCOPE NOW
    #If all runs without doing anything return True
    return True

def collision_sprite():
    # Needs 3 arguments: (sprite, group, bool) -- > Can acces sprite by using .sprite && Group single only access specific one
    if pygame.sprite.spritecollide(player.sprite, obstacle_group,  False):       # True == player and snail collide then snail deleted, False == The snail will not be deleted upon collision
        # This will delete all sprites so the game has a fresh start
        obstacle_group.empty()
        return False
    
    else: return True
    
#def player_animation():
#    # Play walking animation if the player is on the floor
#    # Display the jump surface when the player is not on the floor
#    global player_surface, player_index
#    #If the player is above the y position show the jump animation in the player surface. 
#    if player_rectangle.bottom < 300:
#        player_surface = player_jump
#    else:
#        # By slowly increamenting will reach index 1 which is then 2nd surface to call.
#        player_index += 0.1
#        # If the value greater then the list length set back to 0. len(list): [0,1] == 2
#        if player_index >= len(player_walk): player_index = 0
#        # Use the index to call the surface walk player to draw
#        player_surface = player_walk[int(player_index)]
    
# This will start Pygame and all sub parts needed to make a game, run images, plays sound, ...
# Always need to call first 
pygame.init()

# Display surface == window players will see in the end
# Requires on argument -- > tuple(width,height) in pixels
screen = pygame.display.set_mode((800,400))
# Changes display title
pygame.display.set_caption('Runner')
# Very import issue is the FRAME RATE >> Want to keep it constant so game can be run consistently on any platform == 60 fps constant
# Really want to create a clock object >> Handle Time & Frame Rate
clock = pygame.time.Clock()

# FONT == Display the score == Font(font type, font size)
# Folder containing a 'TTF' file == Specifies FONT 
test_font = pygame.font.Font('font/Pixeltype.ttf',50)

# VARIABLES
# As long True keep the game active. 
game_active = False     # Set to FALSE to work on the get over screen
# A variable for setting the timer to 0 each time restarting the game. 
start_time = 0
# Can set a score 
score = 0 

# Play the background music
bg_Music = pygame.mixer.Sound('audio/music.wav')
bg_Music.set_volume(0.1) # Mute the volume 
bg_Music.play(loops = -1) #The -1 will make it to play this sound forever

################# GROUPS #################
# Add the player to a group
player = pygame.sprite.GroupSingle() # This is the group set up
player.add(Player()) # This is the sprite will contain all from the class Player
# Add the obstacle group
obstacle_group = pygame.sprite.Group()
#obstacle_group.add(Obstacle(type = 'fly'))


# Every time import image into pygame -- > Put this image on its separet surface. 
sky_surface = pygame.image.load('graphics/Sky.png').convert()   # Convert image that pygame can work with == RUN FASTER   
# Calling the ground image
ground_surface = pygame.image.load('graphics/ground.png').convert()
"""
# OBSTACLES 
# Calling the ground image
# SNAIL IMAGES
snail_frame_1 = pygame.image.load('graphics/snail/snail1.png').convert_alpha() # Removing alpha values
snail_frame_2 = pygame.image.load('graphics/snail/snail2.png').convert_alpha() # Removing alpha values
# List to change over the surface animations. 
snail_frames = [snail_frame_1, snail_frame_2]
# Call index from list
snail_frame_index = 0
# The surface that will be drawn
snail_surface = snail_frames[snail_frame_index]
# snail_rectangle = snail_surface.get_rect(bottomright = (600, 300)) # Important to put the snake on top of the ground = 300 

# Fly imgages
fly_frame_1 = pygame.image.load('graphics/Fly/Fly1.png').convert_alpha()
fly_frame_2 = pygame.image.load('graphics/Fly/Fly2.png').convert_alpha()
fly_frames = [fly_frame_1, fly_frame_2]
fly_frame_index = 0
fly_surface = fly_frames[fly_frame_index]

# List with all obstacles present in anamitions/blitted. Used to spawn multiple objects on random times. 
obstacle_rect_list = []

# PLAYER
# Surface of the player both images to create animation
player_walk_1 = pygame.image.load('graphics/Player/player_walk_1.png').convert_alpha()
player_walk_2 = pygame.image.load('graphics/Player/player_walk_2.png').convert_alpha()
# Surface when the player is walking between 2 images (animation)
player_walk = [player_walk_1, player_walk_2]
# Use to pick the different surfaces of player walk
player_index = 0
# Surface when the player jumps
player_jump = pygame.image.load('graphics/Player/jump.png').convert_alpha()
# Going to pick the first player walk service
player_surface = player_walk[player_index]
"""
# Takes a surface -- > Draws a Rectangle around it -- > Define specific position to place it e.g. midleft 
#player_rectangle = player_surface.get_rect(midbottom = (80,300)) # -- > Know position of the Ground! 
# Start with a default gravity of == 0 
#player_gravity = 0
# Create a new player -- > GAME OVER SCREEN
player_stand = pygame.image.load('graphics/Player/player_stand.png').convert_alpha()
# Transform.scale can increase or decrease the size of the player -- > SCALE(SURF,(WIDTH,HEIGHT))
# OR USE SCALE2X -- > Automatically increase dubble without parsing tuple of size. 
# OR OR USE ROTOZOOM(SURF, ANGLE, SCALE)
player_stand = pygame.transform.rotozoom(player_stand,0,2)
# Draw the player in the center of the screen. Use the new scaled surface to draw rectangle. 
player_stand_rect = player_stand.get_rect(center = (400,200))

# TEXT SURFACE == RENDER(text, Anti-Aliase, color) -- > AA = Smooth the edges of the text -- > If using Pixel art == False 
game_name = test_font.render('Pixel Runner', False, (111,196,169))
# Want to place the SCORE on the center of the screen. 
game_name_rect = game_name.get_rect(center = (400,80))

# Have the surface of the text message
game_message = test_font.render('Press space to run', False,(111,196,169))
game_message_rect = game_message.get_rect(center = (400,320))


# TIMER
obstacle_timer = pygame.USEREVENT + 1 # Some events are already preserved with Pygame so need to add one more to it create new one
# Now need to trigger the events in certain intervals (Event to trigger, How often in Miliseconds)
pygame.time.set_timer(obstacle_timer, 1500)

snail_animation_timer = pygame.USEREVENT + 2 # Here as well create a new timer by incrementing with 2. 
# To set how fast the animation/surface will change
pygame.time.set_timer(snail_animation_timer, 500)

fly_animation_timer = pygame.USEREVENT + 3
# Set the animation of a fly bit faster
pygame.time.set_timer(fly_animation_timer, 200)


# Window to not close >> Need to run code forever
# Inside this loops the entire game will run, have to break it from the inside 
while True:
    # Event loop == check for all possile types of player input. 
    # event loops through all the events
    # pygame.event.get() >> Would get all the events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:       # QUIT == constant equal to X from the window (close window)
            pygame.quit()                   # Polar opposite to pygame.init()
            exit()                          # Closes while loop

        # To check if the game is active
        if game_active:
            # Timer in the event loop >> Snail will move differently due to different starting position
            if event.type == obstacle_timer:
                # Want to have obstacle group -- > Add one instance of Obstacle
                # Using the choice it will either select snail 75 % or fly 25 % 
                obstacle_group.add(Obstacle(choice(['flye','snail','snail','snail'])))
                
                ########### Obstacle list append stuff in it ###########
                # Statement to randomly give True(1) or False(0). 
                # if randint(0,2):
                #     # This will spawn the snail on the right of the screen and move it slightly towards the left. 
                #     obstacle_rect_list.append(snail_surface.get_rect(bottomright = (randint(900,1100), 300)))
                # else:    
                #     # Now need to add the fly using the same logic, need to adjust the Y-pos cause its higher placed
                #     obstacle_rect_list.append(fly_surface.get_rect(bottomright = (randint(900,1000), 210)))
            """
            # This will update all of the snail surfaces >> Depending on how fast the timer is set, will update the surface absed on it
            if event.type == snail_animation_timer:
                # Change the snail frame index from 0 to 1 and back to 0
                if snail_frame_index == 0: snail_frame_index = 1
                else: snail_frame_index = 0
                snail_surface = snail_frames[snail_frame_index]
            
            # Statement to update all the fly surfaces    
            if event.type == fly_animation_timer:
                # The if-statements to change the surfaces of the objects. 
                if fly_frame_index == 0: fly_frame_index = 1
                else: fly_frame_index = 0
                fly_surface = fly_frames[fly_frame_index]
                
        
        # ONLY CHECK THIS IF THE GAME IS RUNNING
        if game_active:
            ############ MOUSE BUTTON COLLISION OPTION 1 ############
            # Check a MOUSE BOTTUM is pressed. -- > Spacebar pressed && Only can JUMP when player is in contact with the ground again. 
            if event.type == pygame.MOUSEBUTTONDOWN and player_rectangle.bottom == 300:        
                # event.type -- > Moving mouse triggers (X,Y) POS -- > Can use in collidepoint when the mouse hits the player surface for instance. 
                if player_rectangle.collidepoint(event.pos):
                    # Upon presseing on the player -- > Will make it jump. 
                    player_gravity = -20
            
            ############ KEYBOARD BUTTON COLLISION OPTION 1 ############
            # Using the event type to check if any key is pressed 
            if event.type == pygame.KEYDOWN:
                # Check a specific key is pressed. -- > Spacebar pressed && Only can JUMP when player is in contact with the ground again. 
                if event.key == pygame.K_SPACE and player_rectangle.bottom == 300:
                    # Since origin 0 == y is at top, decreasing it makes the player jump. 
                    player_gravity = -20
            # Using the event type to check if any key is released 
            #if event.type == pygame.KEYUP:
            #    print('key up')
        """
        # RESTARTING THE GAME
        else:
            # Checking if a key is pressed down && They key pressed is spacebar. 
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                # Restart GAME itself
                game_active = True
                # Set the snail on the right, so it does not keep overlapping with player until frames of collision are passed. 
                #snail_rectangle.left = 800 >> REPLACED BY COLLISION
                # This will get the time when RESTARTING -- > Substractin the time of the TOTAL time to make sure the SCORE/TIMER starts from ZERO. && HAS TO BE SAME AS IN FUNCTION 
                start_time = int(pygame.time.get_ticks() / 1000)
        
        
    # As long it is true will keep playing the game. -- > GAME SCREEEN 
    if game_active:
        # BACKGROUND IMAGES
        # Call the display surface + Block Image Transfer
        screen.blit(sky_surface,(0,0))          # 1)
        # Putting the ground image on top of the SKY_SURFACE
        screen.blit(ground_surface,(0,300))     # 2)
        # Can draw other shapes polygon, circle, ellipse, line, arc, ...
        # Snce defining border, doesnt color inside -- > Add dubble
        #pygame.draw.rect(screen, '#c0e8ec', score_rect)
        # Need surface want to draw on == DP surf + Color + Actual rectangle to draw (Optional + border width + Border radius)
        #pygame.draw.rect(screen, '#c0e8ec', score_rect, 10)
        
        # The score TEXT -- > 300 from LEFT & 50 from the top
        #screen.blit(score_surface,score_rect)      # 3)
        # Calling the function for the SCORE && Everytime the display_score is run, score will be the value of whatever reutrned by display_score == Actual score
        score = display_score()

        # SNAIL IMAGE >> Replaced by OBSTACLE TIMER
        # By deacreasing the x value the image looks like it is moving towards the character
        #snail_rectangle.x -= 4
        # MEASURE SNAIL LEAVES SCREEN == Want to check when the RIGHT side of snail smaller then 0 -- > Set the LEFT side of the image at 800, just outside the Display surface. 
        #if snail_rectangle.right <= 0: snail_rectangle.left = 800
        # This will keep drawing images WITHOUT REMOVING PREVIOUS IMAGE -- > Set a proper Background
        #screen.blit(snail_surface,snail_rectangle)

        # PLAYER IMAGE
        # Using the gravity to move the player downwards. 
        # player_gravity += 1
        # # To make the player go downards -- > use vertical attribute. 
        # player_rectangle.y += player_gravity
        # # This will make sure the player does not keep falling -- > When dropping below will keep setting it on the ground 
        # if player_rectangle.bottom >= 300: 
        #     player_rectangle.bottom = 300
        # # player_rectangle.left += 1  # This is how to move something in Pygame -- > Move rectangle that contains the surface. & Can print the position for measurements. 
        
        #  # Function to show the player animation BEFORE BLITTING THE PLAYER!!!!
        # player_animation()
        # screen.blit(player_surface, player_rectangle) #Taking the player surface and place it in the position of the rectangle. 
        
        ############## SPRITES ##############
        # Call the Groupsingle and use the draw method togheter with the surface wanting to draw (screen)
        player.draw(screen)
        # This is to update all of the sprites -- > Calling the funtion out our class
        player.update()
        # Call the obstalce Group
        obstacle_group.draw(screen)
        # Update all of the sprite animations
        obstacle_group.update()
        
        
        # OBSTACLE MOVE
        # First the function is ran >> Move every rectangle in the list bit further left
        # Take the new list and overwrite previously list annd thus continously update list. 
        #obstacle_rect_list = obstacle_movement(obstacle_rect_list)
        #print(obstacle_rect_list)   >>>> [Rect(-2938, 264, 72, 36), Rect(-2367, 264, 72, 36), Rect(-1903, 264, 72, 36), Rect(-1445, 264, 72, 36)] 
        
        # COLLISION
        game_active = collision_sprite()
        #Using the player and all surfaces in the obstacle list to look fort collisions. 
        #game_active = collisions(player_rectangle, obstacle_rect_list)
        
        # COLLISION >> REPLACED ^^^^
        # Want to check if the player rect is colliding with the snail_rect, which is the one want to check against
        # NO Collision == 0 (False) & COLLISION == 1 (True) -- > If True: 
        # This will trigger multiple times & when having health or heart system == Problem!
        #if snail_rectangle.colliderect(player_rectangle):    
        #    # When setting to False -- > Do not update this & Dont draw anything on top of it == See last frame. 
        #    game_active = False
            

        ############ MOUSE BUTTON COLLISION OPTION 2 ############
        # This is to get the position of the mouse
        #mouse_pos = pygame.mouse.get_pos()
        # Check if the mouse is colliding with the player. 
        #if player_rectangle.collidepoint(mouse_pos):
        #    print(pygame.mouse.get_pressed()) # This returns a tuple (False, False, False) == For the Three mouse buttons (LMB, SWM, RMB) == If any pressed RETURNS TRUE. 
        
        ############ KEYBOARD COLLISION OPTION 2 ############
        # This will return a tuple with either buttom not pressed == False OR pressed == True
        # Saving in a varibale, can be used kind of like a dictionary
        #keys = pygame.key.get_pressed()
        # Using key word arguments to search for specific key: https://www.pygame.org/docs/ref/key.html#pygame.key.get_pressed
        #if keys[pygame.K_SPACE]:
        #    print('jump')
    
    # When the game_active FALSE == Then show this screen -- > INTRO && MENU SCREEN
    else:
        # The background of the game over screen. RGB == (Red, Green, Blue) 0-255
        screen.fill((94,129,162))
        # Draw the player in the center of the screen using new TRANSFORMED SURFACE 
        screen.blit(player_stand,player_stand_rect)
        ## When the game is over need to clear the obstacle_rect_list (otherwise start up with some pos of objects)
        #obstacle_rect_list.clear()
        ## Want to add the player to the bottom again >> If jumped against flye restart at bottom
        #player_rectangle.midbottom = (80,300)
        ## Set the graity again to zero so do not fall any further
        #player_gravity = 0
        
        
        # Creating text surface for the score
        score_message = test_font.render(f'Your score: {score}',False,(111,196,169))
        # Draw a rectangle of the score message
        score_message_rect = score_message.get_rect(center = (400,320))
        # Draw the score on the screen
        screen.blit(game_name,game_name_rect)
        
        # When starting up the game for the first time
        if score == 0:
            # Draw message on the screen
            screen.blit(game_message,game_message_rect)
        else:
            # Drawing the score on the screen of the game
            screen.blit(score_message,score_message_rect)

    # Draw all our elements & update everything
    pygame.display.update()         # Updates display surface of everything drawn inside the while loop
    # Telling the while loop to run not faster then 60 times per second
    clock.tick(60)




##################### BASICS OF IMAGE #####################
# To Draw any kind of image == SURFACE 
# Display surface == Game window anything displayed goes on here. 
# Regular Surface == Essantially an image (imported, rendered, text or plain color) -- > Needs to be put on display surface to be visible & flexible amount

# Display surface == (width,height)
#test_surface = pygame.Surface((100,200))
#test_surface.fill('Red')

#while True:
#    for event in pygame.event.get():
#        if event.type == pygame.QUIT:       
#            pygame.quit()                   
#            exit()                         
#            
#    # Call the display surface + Block Image Transfer == Put one surface on another one
#    # -- > blit(SURFACE,(POS)) -- > POS of screen is the ORIGIN POINT
#    # POS == (0,0) -- > Top-left -- > Increase x (width) move to right & Increase y (height) move to bottom (away from top). 
#    # POS == (0,0) want the TOP-LEFT of this (regular) surface put it on the TOP-LEFT of the Display surface 
#    screen.blit(test_surface,(200,100))
#
#    pygame.display.update() 
#    clock.tick(60)
#
##################### CREATE TEXT #####################
# If you want to create a text -- > Create an Image of the text & Place that on the surface -- > Place that surface on the screen. 
# 1) Need to create a FONT (text size & style)
# 2) WRITE text on a surface
# 3) BLIT the text surface 
#
##################### BASIC ANIMATIONS #####################
# Now creating 3 images == Sky, Ground, Text
# Always place them in the same position
# ! These are not static images -- > Updating this image over and over again 60 times per second. 
# They are always in the same positions and thus why they are static to us. 
# BUT updating the position of each of the surfaces -- > Get a moving image.  
# -- >> SCREEN.BLIT = USE A VARIABLE THAT WE CONTINOUSLY UPDATE == MOVING IMAGE
# Try with snail image
#
# WITHOUT USING RECTANGLES
# snail_x_pos = 600
#    # The snail position will be decreased by 4 == MOVING IMAGE
#    snail_x_pos -= 4 # This will now move the position by X towards the left running each loop 
#    # When, the value is below -100 == RESET THE VALUE AGAIN! Otherwise will never return/be kept out of the image position. 
#    if snail_x_pos < -100: snail_x_pos = 800    # If the SNAIL POS below -100 set the POS at 800 aka furthest left in Display == Looks like LOOP == BUT RESETTING THE IMAGE
#    # This will keep drawing images WITHOUT REMOVING PREVIOUS IMAGE -- > Set a proper Background
#    screen.blit(snail_surface,(snail_x_pos,270))
#
# CONVERT() == Converts the image that pygame can work easily with & RUN FASTER 
#              & The returned Surface will contain the same color format, colorkey and alpha transparency as the file it came from
# CONVERT_ALPHA() == Convert improve performance & for pixel perfect collision == For alpha transparency, like in .png images. 
#
##################### RECTANGLES #####################
# 1) Help place the surface much more efficiently and much more precisely
# 2) HELP DETECT COLLISIONS
# Rectangles will make it so you can take another point e.g. grab the bottom of the snail image and place that point. 
# The ACTUAL IMAGE information placed on SURFACE & POSITION in a RECTANGLE -- > Splitting image in TWO DIFFERENT VARIABLES HAVE TO CONTROL TOGHETER (Later SPRITE class)
# 
# Tuple(x,y) -- > POS == Topleft - midtop - topright - midleft - center - midright - bottomleft - midbottom - bottomright
# Individual values == x,y - top - left - right - bottom - centerx,centery == Objects -- > Rect.y, Rect.bottom
# ALSO size, width, height, pygame.Rect(left,top,width,height) BUT want an rectangle with the exact size of the surface SO this wont see often.
#
# Move any individual points in a rectangle == Move all other points as well, stay relative to each other
# Can use a rectangle to place a surface right in the middle of a rectangle 
# Can use a rectangle to detect collisions
# 
# Surface always takes the TOPLEFT as ORIGIN 
# Rectangle GRAB ANY OF THE POINTS AROUND IT
#
# Later see SPRITE class == Surface + Rectangle 
#
##################### COLLISIONS + RECTANGLES #####################
# Want to check if there is a collision between player & Snail == Rectangles that contain them 
# -- > rect1.colliderect(rect2)
# Checks if one point collides with a rectangle. Extremely important when using a mouse to click on something
# Need a rectangle & then calling this as a method. As an argument into collidepoint pass a TUPLE(x,y)
# then pygame checks if this one position is inside the rectangle or not -- > Value returned used in IF-statement. 
# -- > rect1.collidepoint((x,y))
#
# Can also use rectangles to place the text/score on the screen. 
##################### MOUSE POSITION #####################
#
# Getting the mouse position?  
# 1) pygame.mouse  == Information about position & buttoms pressed & visibility, ... -- > Can set POS of mouse or if the mouse is visible in the first place, ... 
# 2) event loop, check events that check the mouse position. -- > Work with the mouse position. 
#
# MOUSEBUTTONDOWN & MOUSEBOTTUNUP -- > To check wheter clicking down or up (For LMB, SW, RMB). 
# MOUSEMOTION == Gives the mouse position & Only triggers when moving the mouse.
##################### DRAWING RECTANGLES #####################
# -- > pygame.draw to draw rectangles, circles, lines draw inside the boundary box of that rectangle. 
# Can be used to add some background to score/text
# EXERCISE: Draw straight line from top to bottom diagonally 
#    pygame.draw.line(screen, 'Gold', (0,0), (800,400))
#    pygame.draw.line(screen, 'Gold', (0,0), pygame.mouse.get_pos()) -- > Line that follows the mouse. 
#
# Draw an ellipse -- > Can generate a surface from scratch pygame.Rect(left,top,width,height)
#    pygame.draw.ellipse(screen, 'Brown', pygame.Rect(50,200,100,100))
#
##################### COLORS #####################
# RGB -- > Red, Green, Blue -- > Specify a value from 0 == No color to 255 == To full color
# rgb_color(red,green,blue)
# Hexadecimals -- > hex_color = #rrgbb -- > 00 == No color to ff == full color
#
##################### PLAYER CHARACTER #####################
# 1) Keyboard input -- > pygame.key OR event loop
#                        In the event loop: 1) Check if any button was pressed 2) work with a specific key
#                        When using classes you want the control inside of the relevant class -- > pygame.mouse & pygame.key
# 2) Jump & Gravity     
#
# The longer you fall, the faster you fall == Exponentially. 
# gravity += some value
# player.y += gravity
# Dont care about physics BUT for ease of programming and fun. 
#
# Jumping the character by using MOUSE CLICK
# Check for mouse pos/collision -- > buttom press -- > jump
# OR
# Buttom press -- > Mouse collision -- > Jump == More efficient (Checking the collision on every frame wastefull)
#
# 3) Creating a floor -- > Check the collision between the player and the floor. Move player up if collision. 
#  -- > Here only need on point 300, If player going below that will set player at 300. 
#
##################### CREATING DIFFERENT STATES #####################
# state manegement in pygame -- > Now in the loop drawing & checking certain things. -- > Set all of this inside an if statement. 
# if game_active: 
#    current_game -- > Drawing all stuff seen. 
# else:           -- > Colliding 
#    game_over    -- > Draw something else. 
#
##################### DISPLAYING SCORE #####################
# Want to display how lon the player has been alive. -- > Measure time
# pygame.time.get_ticks() == Gives us the time since we started pygame aka pygame.init() in milliseconds. 
#
# 1) Update score on every frame 
# 2) Put that on the surface
# 3) Display the surface -- > Everytime creating new frame == Creating to some new text. 
#
##################### TRANSFORM SURFACES #####################
# With transform can do all sorts of things. Can scale surfaces, rotate surfaces, flip surfaces, ...
#
# Displaying score in game over screen
#   1) Store score in a function
#   2) current_time needs to be global or be retunred
#   3) Place the reutrned score on a surface and blit it 
#
##################### BETTER ENEMY LOGIC #####################
# WIll use a timer to run certain type of code on certain timer. >> Custom user event
# 1) Create a custom event
# 2) Tell pygame to trigger that event continously 
# 3) Add code in the event loop
# New logic
# 1) Create a list of obstacle rectangles
# 2) Everytime the timer triggers we add a new rectangle to that list
# 3) We move every rectangle in that list to the very left on every frame
# 4) Delete rectangles too far left
# >> PROBLEMS
# 1) Collision does not work anymore
# 2) We dont delete rectangles when leaving the screen. 
# 3) We only havce snails
#
#####################   FIXING THE COLLISION LOGIC #####################
# Cycle through the obstacle rect list >> If player collides with any of the rectangles == END GAME
#
#####################   ANIMATE PLAYER, FLY, SNAIL #####################
# Update the surface that we are putting on the screen every few miliseconds
# By doing this it looks like it is animated. 
# PLayer animation creaet a random timer that updates on every random cycle of the loop
# For the obstacles create a new timer, inbuild timer. -- > Everytime it triggers we update all the surfaces for all flies or all snails (each have their own timer)
#
#####################   SPRITE CLASSES #####################
#
# The player is organised with 4 code snippets, in a much complex game this would be much more. 
# Ideally want to put all this into a single class. 
#
# A sprite class contains a surface and a rectangle; it can be drawn an updated very easily. 
# -- > Create a sorite class for the player an d a sprite class for each obstacle. 
#
# Pygame does not draw sprites automatically --- > basically a surface and a rectangle combined && can not use screen.blit 
# Create sprite -- > place sprites in a Group ir GroupSingle -- > Draw/update all sprites in that group
#
# Group == A group for multiple sprites (flies & snails) 
# GroupSingle == A group with a single sprite (player)
# -- > Checking for collision need in different groups
#
# Adding sprite collisions 
# -- > spritecollide(sprite,group,dokill) == takes a sprite and checks if this sprite collides with any other sprite in another group
# returns a list of all collided sprites -- > Can work with in a function