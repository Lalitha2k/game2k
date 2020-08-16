# Gain access to the pygame library
import pygame
 
# Size of the screen
SCREEN_TITLE = 'Crossy RPG'
SCREEN_WIDTH = 700
SCREEN_HEIGHT = 700
# Colors according to RGB codes
WHITE_COLOR = (255, 255, 255)
BLACK_COLOR = (0, 0, 0)
# Clock used to update game events and frames
clock = pygame.time.Clock()
pygame.font.init()
font = pygame.font.SysFont('comicsans', 75)
 
class Game:
 
    # Typical rate of 60, equivalent to FPS
    TICK_RATE = 60
 
    # Initializer for the game class to set up the width, height, and title
    def __init__(self, image_path,title, width, height):
        self.title = title
        self.width = width
        self.height = height
 
        # Create the window of specified size in white to display the game
        self.game_screen = pygame.display.set_mode((width, height))
        # Set the game window color to white
        self.game_screen.fill(WHITE_COLOR)
        pygame.display.set_caption(title)
        backgroungimage = pygame.image.load(image_path)
        self.image = pygame.transform.scale(backgroungimage,(width,height))
 
    def run_game_loop(self , levelspeed):
        is_game_over = False
        did_win = False
        direction = 0
 
        player_character = PlayerCharacter('player1.jpg', 375, 700, 50, 50)
        enemy_0 = NonPlayerCharacter('enemy.jpg',20,600,50,50)
        enemy_0.SPEED *= levelspeed

        enemy_1 = NonPlayerCharacter('enemy.jpg',self.width -40,400,50,50)
        enemy_1.SPEED *= levelspeed

        enemy_2 = NonPlayerCharacter('enemy.jpg',20,200,50,50)
        enemy_2.SPEED *= levelspeed
        treasure = GameObject('treasure.jpg',348,60,60,60 )
   
        # Main game loop, used to update all gameplay such as movement, checks, and graphics
        # Runs until is_game_over = True
        while not is_game_over:
 
            # A loop to get all of the events occuring at any given time
            # Events are most often mouse movement, mouse and button clicks, or exit events
            for event in pygame.event.get():
                # If we have a quite type event (exit out) then exit out of the game loop
                if event.type == pygame.QUIT:
                    is_game_over = True
                # Detect when key is pressed down
                elif event.type == pygame.KEYDOWN:
                    # Move up if up key pressed
                    if event.key == pygame.K_UP:
                        direction = 1
                    # Move down if down key pressed
                    elif event.key == pygame.K_DOWN:
                        direction = -1
                # Detect when key is released
                elif event.type == pygame.KEYUP:
                    # Stop movement when key no longer pressed
                    if event.key == pygame.K_UP or event.key == pygame.K_DOWN:
                        direction = 0
                
                print(event)
 
            # Redraw the screen to be a blank white window
            self.game_screen.fill(WHITE_COLOR)
            self.game_screen.blit(self.image,(0,0))

            treasure.draw(self.game_screen)
            # Update the player position
            player_character.move(direction,self.height )
            # Draw the player at the new position
            player_character.draw(self.game_screen)

            enemy_0.move(self.width)
            enemy_0.draw(self.game_screen)

            if levelspeed > 2:
                enemy_1.move(self.width)
                enemy_1.draw(self.game_screen)
            if levelspeed >3:
                enemy_2.move(self.width)
                enemy_2.draw(self.game_screen)


            if player_character.detect_collision(enemy_0):
                is_game_over = True
                did_win= False
                text = font.render('you suck yuk :/',True,BLACK_COLOR)
                self.game_screen.blit(text,(300,350))
                pygame.display.update()
                clock.tick(1)
                break
            elif player_character.detect_collision(treasure):
                is_game_over = True
                did_win = True
                text = font.render('you win :)))',True,BLACK_COLOR)
                self.game_screen.blit(text,(300,350))
                pygame.display.update()
                clock.tick(1)
                break
 
            # Update all game graphics
            pygame.display.update()
            # Tick the clock to update everything within the game
            clock.tick(self.TICK_RATE)
        if did_win:
            self.run_game_loop(levelspeed + 0.5)   
        else:
                return

 
# Generic game object class to be subclassed by other objects in the game
class GameObject:
 
    def __init__(self, image_path, x, y, width, height):
        object_image = pygame.image.load(image_path)
        # Scale the image up
        self.image = pygame.transform.scale(object_image, (width, height))
        
        self.x_pos = x
        self.y_pos = y
 
        self.width = width
        self.height = height
 
    # Draw the object by blitting it onto the background (game screen)
    def draw(self, background):
        background.blit(self.image, (self.x_pos, self.y_pos))
 
# Class to represent the character contolled by the player
class PlayerCharacter(GameObject):
 
    # How many tiles the character moves per second
    SPEED = 10
 
    def __init__(self, image_path, x, y, width, height):
        super().__init__(image_path, x, y, width, height)
 
# Move function will move character up if direction > 0 and down if < 0
    def move(self, direction,max_height):
        if direction > 0:
            self.y_pos -= self.SPEED
        elif direction < 0:
            self.y_pos += self.SPEED
        if self.y_pos >= max_height - 40:
            self.y_pos = max_height - 40

    def detect_collision(self,otherbody):
        if self.y_pos > otherbody.y_pos + otherbody.height:
                   return False
        elif self.y_pos + self.height < otherbody.y_pos:
            return False 
        if self.x_pos > otherbody.x_pos + otherbody.width:
            return False
        elif self.x_pos + self.width < otherbody.x_pos:
            return False

        return True 


            # Class to represent the enemies moving left to right and right to left
class NonPlayerCharacter(GameObject):
 
    # How many tiles the character moves per second
    SPEED = 5
 
    def __init__(self, image_path, x, y, width, height):
        super().__init__(image_path, x, y, width, height)
 
    # Move function will move character right once it hits the far left of the
    # screen and left once it hits the far right of the screen
    def move(self, max_width):
        if self.x_pos <= 20:
            self.SPEED = abs(self.SPEED)
        elif self.x_pos >=  max_width - 40:
            self.SPEED = -abs(self.SPEED)
        self.x_pos += self.SPEED
       
pygame.init()
 
new_game = Game('background.png',SCREEN_TITLE, SCREEN_WIDTH, SCREEN_HEIGHT)
new_game.run_game_loop(1)
 
# Load the player image from the file directory
# player_image = pygame.image.load('player.png')
# Scale the image up
# player_image = pygame.transform.scale(player_image, (50, 50))
 
# Quit pygame and the program
pygame.quit()
quit()