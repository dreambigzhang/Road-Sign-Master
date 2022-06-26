# Road Sign Master
import pygame, random

def main():
    pygame.init() # initialize all pygame modules
    pygame.display.set_mode((500, 400))# create a pygame display window
    pygame.display.set_caption('Road Sign Master')
    w_surface = pygame.display.get_surface()
    game = Game(w_surface) # create a game object
    # start the main game loop by calling the play method on the game object
    game.play()
    # quit pygame and clean up the pygame window
    pygame.quit()

# User-defined classes

class Game:
    # An object in this class represents a complete game.

    def __init__(self, surface):
        # Initialize a Game.
        # - self is the Game to initialize
        # - surface is the display window surface object
        self.surface = surface
        self.bg_color = pygame.Color('black')

        self.FPS = 60
        self.game_Clock = pygame.time.Clock()
        self.close_clicked = False
        self.continue_game = True
    
        self.load_images()
        self.board_size = 4
        self.board=[]
        self.create_board()
        
        self.two_clicked = 0
        self.two_tiles = []
        self.score = 0
        self.image_found = 0
        
    def load_images(self):
        self.image_list=[]
        image_number_list = random.sample(range(1, 19), 8)
        #print(image_number_list)
        for number in image_number_list:
            image = str(number)+'o'+'.jpg'
            self.image_list.append(image)
            image_i = str(number)+'i'+'.jpg'
            self.image_list.append(image_i)
        random.shuffle(self.image_list)
        #print(self.image_list)
        
    def create_board(self):
        index=0
        for row_index in range(0,self.board_size):
            new_row=[]
            for col_index in range(0,self.board_size):
                name = self.image_list[index]
                index+=1
                image = pygame.image.load(name)
                width = image.get_width()
                height = image.get_height()
                x= col_index*width
                y= row_index*height
                tile = Tile(x,y,width,height,image, name, self.surface)
                new_row.append(tile)
            self.board.append(new_row)
        
    def play(self):
        # Play the game until the player presses the close box.
        # - self is the Game that should be continued or not.

        while not self.close_clicked:  # until player clicks close box
            # play frame
            self.handle_events()
            self.draw()            
            if self.continue_game:
                self.update()
                self.decide_continue()
            else:
                self.is_win()
            self.game_Clock.tick(self.FPS) # run at most with FPS Frames Per Second 

    def handle_events(self):
        # Handle each user event by changing the game state appropriately.
        # - self is the Game whose events will be handled
        events = pygame.event.get()
        for event in events:
            if event.type == pygame.QUIT:
                self.close_clicked = True
            if event.type == pygame.MOUSEBUTTONUP and self.continue_game:
                self.handle_mouse_up(event.pos)   # event.pos is a (x,y) tuple --> position of the click
                
    def handle_mouse_up(self, position):
        for row in self.board:
            for tile in row:
                if tile.select(position) and tile.is_hidden() and self.two_clicked < 2:  # select method is in the Tile class
                    self.two_tiles.append(tile)
                    tile.reveal()
                    self.two_clicked += 1
    
    def two_clicked_tiles(self):
        if self.two_clicked >= 2:
            
            if self.two_tiles[0].compare(self.two_tiles[1]):
                self.image_found += 2
            else:
                pygame.time.wait(400)
                self.two_tiles[0].hide()
                self.two_tiles[1].hide()
            self.two_clicked = 0
            self.two_tiles = []
            
    def draw(self):
        # Draw all game objects.
        # - self is the Game to draw
        # clear the display surface first
        # draw the boards
        if self.continue_game:
            self.surface.fill(self.bg_color)
            for row in self.board:
                for tile in row:
                    tile.draw()
        self.draw_score()
        pygame.display.update() # make the updated surface appear on the display
    
    def draw_score(self):
        score_string = str(self.score)
        font_size = 63
        fg_color = pygame.Color('white')
        bg_color = self.bg_color
        font=pygame.font.SysFont('TimesNew Roman', font_size)
        text_box = font.render(score_string, True, fg_color, bg_color)
        a = self.surface.get_width()
        b = text_box.get_width()
        x = a-b
        location = (x,0)
        self.surface.blit(text_box, location)   
        
    def update(self):
        # Update the game objects for the next frame.
        # - self is the Game to update
        self.draw()
        self.two_clicked_tiles()
        self.score = pygame.time.get_ticks()//1000 - 7
        
    def decide_continue(self):
        # Check and remember if the game should continue
        # - self is the Game to check
        if self.image_found >= 16:
            self.continue_game = False
        
    def is_win(self):
        font_size = 63
        fg_color = pygame.Color('red')
        bg_color = pygame.Color('white')
        font=pygame.font.SysFont('Arial', font_size)
        text_box1 = font.render('Good Job!', True, fg_color, bg_color)
        location = (100,100)
        self.surface.blit(text_box1, location)
        
        
class Tile:
    def __init__(self, x, y, width, height, image, name, surface):
        self.rect = pygame.Rect(x,y, width,height)
        self.color = pygame.Color('black')
        self.surface = surface
        self.border_width = 3
        self.content = image
        self.hidden_image = pygame.image.load('image0.bmp')
        self.hidden = True
        self.name = name
        
    def draw(self):
        # draw the Tile object
        location = (self.rect.x, self.rect.y)
        if self.hidden == True:
            self.surface.blit(self.hidden_image, location)
        else:
            self.surface.blit(self.content, location)
        pygame.draw.rect(self.surface, self.color, self.rect, 3)
    
    def reveal(self):
        self.hidden = False
        
    def hide(self):
        self.hidden = True
            
    def select(self, position):
        selected = False
        if self.rect.collidepoint(position):  # collidepoint is a method in the rect class checking if a point is inside a rect
                selected = True
        return selected
    
    def is_hidden(self):
        return self.hidden
    
    def return_name(self):
        return self.name[:-5]
    
    def compare(self, other):
        if self.name[:-5] == other.return_name():
            return True
        else:
            return False
main()