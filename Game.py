import pygame
from pygame import mixer

pygame.mixer.pre_init(44100, -16, 2, 512)
mixer.init()
pygame.init()


#load sounds
pygame.mixer.music.load('sounds/music.wav')
pygame.mixer.music.set_volume(0.2)              #volume set to 20% of original
pygame.mixer.music.play(-1, 0.0, 5000)

coin_fx = pygame.mixer.Sound('sounds/coin.wav')
coin_fx.set_volume(0.6)                         #volume set to 60% of original
jump_fx = pygame.mixer.Sound('sounds/jump.wav')
jump_fx.set_volume(0.6)                         #volume set to 60% of original
game_over_fx = pygame.mixer.Sound('sounds/game_over.wav')
game_over_fx.set_volume(0.6)                    #volume set to 60% of original

scr_width = 600
scr_height = 600
win = pygame.display.set_mode((scr_width, scr_height))
pygame.display.set_caption("PLATFORMER")
clk = pygame.time.Clock()

restart_button = pygame.image.load('images/restart_btn.png')
start_button = pygame.image.load('images/start_btn.png')
exit_button = pygame.image.load('images/exit_btn.png')
bg = pygame.image.load ('images/Background.png')
bg = pygame.transform.scale(bg, (600, 600))

#game variables
tile_size = 30
level = 1
score=0
gameover=0
main_menu = True
game_end = 0

#divide window into a grid
def grid():
        for i in range(0, int(scr_width/tile_size)+1):
                pygame.draw.line(win, (255, 255, 255), (0, i*tile_size ), (scr_width, i*tile_size))
                pygame.draw.line(win, (255, 255, 255), (i*tile_size, 0 ), (i*tile_size, scr_height))

#function to display text
def draw_text(text, font, colour, x, y):
              text_img = font.render(text, True, colour)
              win.blit(text_img, (x, y))

font_score = pygame.font.SysFont('Times New Roman', 20)
red = (255, 0, 0)
font_text = pygame.font.SysFont('Bauhaus 93', 90 )
font_lvl_comp = pygame.font.SysFont('Bauhaus 93', 70 )
blue = (0, 0, 255)
              
        
# drawing structure

class World:

        def __init__(self, tile_data, tile_size):
                self.tile_data = tile_data
                self.tile_size = tile_size
                self.tile_list = []
                self.coin_list = []
                self.obstacle_list = []
                self.heart_list = []
                self.monster_group = pygame.sprite.Group()

        #loading images

                dirt = pygame.image.load('images/dirt.png')
                dirt = pygame.transform.scale(dirt, (self.tile_size, self.tile_size))
                grass = pygame.image.load('images/grass.png')
                grass = pygame.transform.scale(grass, (self.tile_size, self.tile_size))
                coin = pygame.image.load('images/coin.png')
                coin = pygame.transform.scale(coin, (self.tile_size-10, self.tile_size-10))
                door = pygame.image.load('images/door.png')
                door = pygame.transform.scale(door, (self.tile_size*2, self.tile_size*2))
                heart = pygame.image.load('images/heart.png')
                heart = pygame.transform.scale(heart, (self.tile_size-10, self.tile_size-10))

                for y in range(len(self.tile_data)):
                        for x in range(len(self.tile_data[y])):
                                tile = self.tile_data[y][x]
                                if tile == 1:
                                        tile_img = dirt
                                        tile_rect = pygame.Rect(x*self.tile_size, y*self.tile_size, self.tile_size, self.tile_size)
                                        self.tile_list.append((tile_img, tile_rect))

                                elif tile == 2:
                                        tile_img = grass
                                        tile_rect = pygame.Rect(x*self.tile_size, y*self.tile_size, self.tile_size, self.tile_size)
                                        self.tile_list.append((tile_img, tile_rect))

                                elif tile == 3:
                                        tile_img = coin 
                                        tile_rect = pygame.Rect(x*self.tile_size+5, y*self.tile_size+5, self.tile_size-10, self.tile_size-10)
                                        self.coin_list.append((tile_img, tile_rect))

                                elif tile == 4:
                                        spike = pygame.image.load('images/spike0.png')
                                        spike = pygame.transform.scale(spike, (self.tile_size, self.tile_size))
                                        tile_img = spike
                                        tile_rect = pygame.Rect(x*self.tile_size, y*self.tile_size, self.tile_size, self.tile_size)
                                        self.obstacle_list.append((tile_img, tile_rect))
                                        
                                elif tile == 5:
                                        spike = pygame.image.load('images/spike1.png')
                                        spike = pygame.transform.scale(spike, (self.tile_size, self.tile_size))
                                        tile_img = spike
                                        tile_rect = pygame.Rect(x*self.tile_size, y*self.tile_size, self.tile_size, self.tile_size)
                                        self.obstacle_list.append((tile_img, tile_rect))
                                        
                                elif tile == 6:
                                        spike = pygame.image.load('images/spike2.png')
                                        spike = pygame.transform.scale(spike, (self.tile_size, self.tile_size))
                                        tile_img = spike
                                        tile_rect = pygame.Rect(x*self.tile_size, y*self.tile_size, self.tile_size, self.tile_size)
                                        self.obstacle_list.append((tile_img, tile_rect))
                                elif tile == 7:
                                        spike = pygame.image.load('images/spike3.png')
                                        spike = pygame.transform.scale(spike, (self.tile_size, self.tile_size))
                                        tile_img = spike
                                        tile_rect = pygame.Rect(x*self.tile_size, y*self.tile_size, self.tile_size, self.tile_size)
                                        self.obstacle_list.append((tile_img, tile_rect))
                                
                                elif tile == 8:
                                        spike = pygame.image.load('images/spike4.png')
                                        spike = pygame.transform.scale(spike, (self.tile_size, self.tile_size))
                                        tile_img = spike
                                        tile_rect = pygame.Rect(x*self.tile_size, y*self.tile_size, self.tile_size, self.tile_size)
                                        self.obstacle_list.append((tile_img, tile_rect))


                                elif tile == 9:
                                        monster = Enemy(x * self.tile_size, y * self.tile_size + 5)
                                        self.monster_group.add(monster)
                                        
                                elif tile == 10:
                                        self.door_img = door
                                        self.door_rect = pygame.Rect(x*self.tile_size, y*self.tile_size, 2*self.tile_size, 2*self.tile_size)
                                        
                                elif tile == 11:
                                        heart_img = heart
                                        heart_rect = pygame.Rect(x*self.tile_size+5,  y*self.tile_size+5, self.tile_size, self.tile_size)
                                        self.heart_list.append((heart_img, heart_rect))
                                
                                
        #to draw items in list
        def draw_tile(self):

                for tile in self.tile_list:
                        win.blit(tile[0], (tile[1][0], tile[1][1]))

                for coin in self.coin_list:
                         win.blit(coin[0], (coin[1][0], coin[1][1]))

                for obstacle in self.obstacle_list:
                         win.blit(obstacle[0], (obstacle[1][0], obstacle[1][1]))

                win.blit(self.door_img, (self.door_rect[0], self.door_rect[1]))

                for heart in self.heart_list:
                        win.blit(heart[0], (heart[1][0], heart[1][1]))


class Character:
        def __init__(self, x, y,  vel_x, vel_y):
                self.x = x
                self.y = y
                self.new_x = x
                self.new_y = y
                self.vel_x = vel_x
                self.vel_y = vel_y
                self.win = win
                self.walkcount = 0
                self.right = False
                self.left = False
                self.standing = True
                self.x_collision = False
                self.y_collision = True
                self.rect = pygame.Rect(self.x, self.y, 28, 52)
                self.left_img = []
                self.right_img = []
                
                for i in range(1, 5):
                        self.left_img.append(pygame.image.load(f'images/L{i}.png'))
                        self.left_img[i-1] = pygame.transform.scale(self.left_img[i-1], (28, 52))
                for i in range(1, 5):
                        self.right_img.append(pygame.image.load(f'images/R{i}.png'))
                        self.right_img[i-1] = pygame.transform.scale(self.right_img[i-1], (28, 52))
                self.standing_left = pygame.image.load('images/standing_left.png')
                self.standing_left = pygame.transform.scale(self.standing_left, (28, 52))
                self.standing_right = pygame.image.load('images/standing_right.png')
                self.standing_right = pygame.transform.scale(self.standing_right, (28, 52))
                
        #to draw the character at current position
        def draw_char(self):
                if self.standing:               #character is stationary
                        self.walkcount = 0
                        if self.left:         #not right since at beginning of game we need right facing
                                win.blit(self.standing_left, (self.x, self.y))
                        else:          
                                win.blit(self.standing_right, (self.x, self.y))
                else:
                        if self.walkcount+1 >=16:
                                self.walkcount = 0
                        #display animation of character
                        if self.right:
                                win.blit(self.right_img[self.walkcount//4], (self.x, self.y))
                                self.walkcount += 1
                        else:
                                win.blit(self.left_img[self.walkcount//4], (self.x, self.y))
                                self.walkcount += 1



#for moving enemy
class Enemy(pygame.sprite.Sprite):

        def __init__(self,x,y):
                pygame.sprite.Sprite.__init__(self)
                img = pygame.image.load('images/spike monster1.png')
                self.image = pygame.transform.scale(img, (45, 25))
                self.rect = self.image.get_rect()
                self.rect.x = x
                self.rect.y = y
                self.move_direction = 1
                self.move_counter = 0

        def update(self):
                self.rect.x += self.move_direction
                self.move_counter += 1
                if abs(self.move_counter) > 45 :
                        self.move_direction *= -1
                        self.move_counter *= -1

class Button():
        def __init__(self, x, y, button_img):
                self.button_img = button_img
                self.button_img_rect = self.button_img.get_rect()
                self.button_img_rect.x = x
                self.button_img_rect.y = y
                self.click = False
                self.action = False

        def got_clicked(self):
                pos_cur = pygame.mouse.get_pos()
                if self.button_img_rect.collidepoint(pos_cur):
                        if (pygame.mouse.get_pressed()[0] == 1 and self.click == False):
                                self.click = True
                                self.action = True
                        if pygame.mouse.get_pressed()[0] == 0 :
                                self.click = False
                win.blit(self.button_img, self.button_img_rect)
                return self.action                                  

#level data
tile_data_lvl_1 = [[11, 11, 11, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 10, 0],
               [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
               [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2, 2, 1, 1],
               [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
               [7, 3, 3, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
               [2, 2, 2, 0, 0, 0, 0, 0, 0, 0, 0, 2, 2, 0, 0, 0, 0, 0, 0, 0],
               [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
               [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
               [0, 0, 0, 0, 0, 0, 2, 2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
               [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 9, 0, 0, 5, 3, 3, 3, 3],
               [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2],
               [3, 3, 3, 6, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
               [2, 2, 2, 2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
               [0, 0, 0, 0, 0, 0, 2, 2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
               [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
               [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 3, 3, 3, 0, 0, 0, 0, 0, 0, 0],
               [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2, 2, 2, 0, 0, 0, 2, 2, 0, 0],
               [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 0, 0, 0, 0, 0, 3, 3],
               [0, 0, 0, 0, 0, 0, 0, 9, 0, 0, 1, 1, 1, 4, 4, 4, 0, 9, 0, 0],
               [2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 1, 1, 1, 2, 2, 2, 2, 2, 2, 2]]

tile_data_lvl_2 = [[11, 11, 11, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 10, 0],
                   [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                   [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2, 2, 1, 1],
                   [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 6, 0, 3, 0, 0, 0, 0, 0, 0],
                   [0, 0, 0, 0, 0, 0, 0, 0, 0, 2, 2, 2, 2, 2, 2, 0, 0, 0, 0, 0],
                   [7, 3, 3, 0, 9, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                   [2, 2, 2, 2, 2, 2, 2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                   [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 3, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                   [0, 0, 0, 0, 0, 0, 0, 0, 0, 2, 2, 0, 0, 0, 0, 0, 9, 0, 0, 3],
                   [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2, 2, 2, 2, 2, 2, 2],
                   [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                   [7, 3, 0, 6, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                   [2, 2, 2, 2, 2, 2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                   [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                   [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 3, 4, 3, 8],
                   [0, 0, 0, 0, 0, 0, 0, 0, 0, 3, 0, 0, 0, 0, 0, 2, 2, 2, 2, 2],
                   [0, 0, 0, 0, 0, 0, 0, 2, 2, 2, 2, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                   [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                   [0, 0, 0, 2, 2, 3, 0, 4, 0, 3, 0, 0, 3, 9, 0, 0, 0, 0, 3, 0],
                   [2, 2, 2, 1, 1, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2]]

tile_data_lvl_3 =[[11 , 11, 11, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 10, 0, 0],
               [0 , 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
               [0 , 0, 0, 0, 0, 0, 0, 0, 0, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2],
               [0 , 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
               [7 , 3, 0, 9, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
               [2 , 2, 2, 2, 2, 2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
               [0 , 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
               [0 , 0, 0, 0, 0, 0, 0, 0, 0, 0, 3, 0, 0, 0, 0, 0, 0, 0, 0, 0],
               [0 , 0, 0, 0, 0, 0, 0, 0, 0, 0, 2, 2, 0, 0, 0, 0, 0, 0, 0, 0],
               [7 , 3, 3, 3, 6, 0, 0, 6, 6, 6, 6, 0, 0, 0, 0, 0, 0, 0, 0, 0],
               [2 , 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 0, 0, 0, 0, 9, 0, 3, 0, 0],
               [0 , 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2, 2, 2, 2, 0, 0],
               [0 , 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
               [0 , 0, 0, 0, 0, 0, 0, 0, 0, 9, 3, 0, 0, 0, 0, 0, 0, 0, 0, 0],
               [0 , 0, 0, 0, 0, 0, 0, 0, 2, 2, 2, 2, 0, 0, 0, 0, 0, 0, 0, 0],
               [0 , 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 3, 8],
               [0 , 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2, 2, 2, 2, 2, 2],
               [0 , 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
               [0 , 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
               [2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2]]

#creating objects of each class
world_data_1 = World(tile_data_lvl_1, tile_size)
world_data_2 = World(tile_data_lvl_2, tile_size)
world_data_3 = World(tile_data_lvl_3, tile_size)
world_data_dict = {1 : world_data_1, 2 : world_data_2, 3 : world_data_3}

char = Character(0, 530, 5, 0)
restart_btn = Button(scr_width//2 - 60, scr_height//2 - 21, restart_button)
start_btn = Button(15, 270, start_button)
exit_btn = Button(310, 270, exit_button)


#function to draw everything on the window
def update_win():

        #global variables

        global score
        global run
        global gameover
        global main_menu
        global game_end
        global level

        win.blit(bg, (0, 0))
        if game_end == 1 :
              main_menu = True
              draw_text('YOU WON!', font_text, blue, 130, 90)
        if main_menu :
              if start_btn.got_clicked():
                    main_menu = False
                    start_btn.action = False
                    level = 1
                    char.__init__(0, 530, 5, 0)
                    for lvl in range(1,4):
                        world_data_dict[lvl].__init__(world_data_dict[lvl].tile_data, tile_size)  #initialize all 3 levels
                    game_end = 0
                    score = 0
              if exit_btn.got_clicked():
                    run = False
                    exit_btn.action = False
        else:     
              #grid()
              world_data_dict[level].draw_tile()
              world_data_dict[level].monster_group.draw(win)
              draw_text('SCORE: '+str(score),font_score, red, 0, tile_size +5)  
              if(gameover == 0):
                      char.draw_char()
                      world_data_dict[level].monster_group.update()
              else:
                      draw_text("GAME OVER !",font_text, red, 60, 120)
                      if restart_btn.got_clicked() :
                              char.__init__(0, 530, 5, 0)    #initialize character
                              world_data_dict[level].__init__(world_data_dict[level].tile_data, tile_size)  #initialize world
                              gameover = 0
                              score = 0
                              restart_btn.action = False
        pygame.display.update()
        
run = True

#main game loop
while run:
        clk.tick(60)
        for event in pygame.event.get():
                if event.type == pygame.QUIT:
                        run = False

        if not main_menu:

                if gameover == 0 :
                  char.new_x = char.x
                  char.new_y = char.y
                  
                  char.new_y += char.vel_y     #simulate gravity
                  char.vel_y += 1
                      
                  k = pygame.key.get_pressed()
                  if (k[pygame.K_LEFT] and char.x>0):       #left movement
                          char.left = True
                          char.right = False
                          char.standing = False
                          char.new_x -= char.vel_x
                          
                  elif (k[pygame.K_RIGHT] and char.x<scr_width -30):    #right movement
                          char.left = False
                          char.right = True
                          char.standing = False
                          char.new_x += char.vel_x
                          
                  else:
                          char.standing = True          #stationary character

                  if (k[pygame.K_SPACE] and on_platform):       #jumping
                          jump_fx.play()
                          char.vel_y = -15

                  #check collision in x direction
                  char.x_collision = False
                  char.rect = pygame.Rect(char.new_x, char.y, 28, 52)
                  
                  for p in world_data_dict[level].tile_list:
                          if p[1].colliderect(char.rect):
                                  char.x_collision = True
                                  break
                  if not(char.x_collision):
                          char.x = char.new_x

                  #check collision in y direction   
                  char.y_collision = False
                  on_platform = False
                  char.rect = pygame.Rect(char.x, char.new_y, 28, 52)

                  for p in world_data_dict[level].tile_list: 
                          if p[1].colliderect(char.rect):
                                  char.y_collision = True
                                  char.vel_y = 0
                                  if (p[1][1]>char.new_y):         #check if player is above platform
                                          char.y = p[1][1] - 52       
                                          on_platform = True
                                  break
                  if not(char.y_collision) and char.new_y>0:
                          char.y = char.new_y

                  char.rect = pygame.Rect(char.x, char.y, 28, 52)

                  for c in world_data_dict[level].coin_list:       #check collision with coin
                          if c[1].colliderect(char.rect):
                                  coin_fx.play()
                                  score+=1
                                  world_data_dict[level].coin_list.remove(c)
                  
                  for i in world_data_dict[level].obstacle_list:   #check collision with spikes
                          if i[1].colliderect(char.rect):
                                  char.y=530
                                  char.x=0
                                  try:
                                          world_data_dict[level].heart_list.pop()
                                  except IndexError:
                                          game_over_fx.play()
                                          gameover = 1
                                  break
                  
                  if pygame.sprite.spritecollide(char,  world_data_dict[level].monster_group, False):  #check collision with moving enemy
                          char.y = 530
                          char.x = 0
                          try:
                              world_data_dict[level].heart_list.pop()
                          except IndexError:
                              game_over_fx.play()
                              gameover = 1
                  
                  if world_data_dict[level].door_rect.colliderect(char.rect):           #check collision with door
                          if level == 3:
                              game_end = 1
                          else:
                              level+=1
                              char.x = 0
                              char.y = 530
                              score = 0
                              draw_text('LEVEL COMPLETE', font_lvl_comp, blue, 100, 150)
                              pygame.display.update()
                              pygame.time.delay(1000)
                    
        update_win()        
        
pygame.quit()
