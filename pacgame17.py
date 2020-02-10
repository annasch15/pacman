import pygame
import os
from random import choice



pygame.init()

size = width, height = 1050 , 800
screen = pygame.display.set_mode(size)
screen.fill((0, 0, 0))
clock = pygame.time.Clock()
v = 3
fps = 30
score = 0

def draw():
    font = pygame.font.Font(None, 50)
    text = font.render(f'Score: {score}', 1, (248, 243, 43))
    text_x = 10
    text_y = 10
    screen.blit(text, (text_x, text_y))
   
def draw_life():
    font2 = pygame.font.Font(None, 50)
    life = font2.render('Lives left:', 1, (248, 243, 43))
    life_x = 730
    life_y = 10
    screen.blit(life, (life_x, life_y))
   
def square(x, y):
    pygame.draw.rect(screen, (0, 0, 0), (x * 50, y * 50, 50, 50))
   
def load_image(name, colorkey=None):
    fullname = os.path.join('data', name)
    image = pygame.image.load(fullname).convert_alpha()
    return image

FPS = 50

def terminate():
    pygame.quit()

def start_screen():
    intro_text = ['PACMAN']

    fon = pygame.transform.scale(load_image('pacfon.jpg'), (width, height))
    screen.blit(fon, (0, 0))
    font = pygame.font.Font(None, 250)
    text_coord = 50
    for line in intro_text:
        string_rendered = font.render(line, 1, pygame.Color('yellow'))
        intro_rect = string_rendered.get_rect()
        text_coord += 10
        intro_rect.top = text_coord
        intro_rect.x = 140
        text_coord += intro_rect.height
        screen.blit(string_rendered, intro_rect)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            elif event.type == pygame.KEYDOWN or event.type == pygame.MOUSEBUTTONDOWN:
                return  # начинаем игру
        pygame.display.flip()
        clock.tick(FPS)

start_screen()

def load_level(filename):
    filename = "data/" + filename
    with open(filename, 'r') as mapFile:
        level_map = [line.strip() for line in mapFile]

    max_width = max(map(len, level_map))
 
    return list(map(lambda x: x.ljust(max_width, '.'), level_map))


dot1 = load_image('dot.png')
dot = pygame.transform.scale(dot1, (50, 50))
life1 = load_image('pacman_life.png')
life = pygame.transform.scale(life1, (50, 50))


black_square1 = load_image('black.png')
black_square = pygame.transform.scale(black_square1, (50, 50))
blue_square1 = load_image('square.png')
blue_square = pygame.transform.scale(blue_square1, (50, 50))
cherry1 = load_image('cherry.png')
cherry = pygame.transform.scale(cherry1, (30, 30))

tile_images = {'wall': blue_square, 'empty': black_square, 'dot': dot,
               'life': life, 'cherry': cherry}

player_image1 = load_image('pacman.png')
player_image = pygame.transform.scale(player_image1, (30, 30))
image1 = pygame.transform.rotate(player_image, 90)
image2 = pygame.transform.rotate(player_image, -90)
image3 = pygame.transform.flip(player_image, 1, 0)
image4 = player_image

red1 = load_image('red2.png')
red = pygame.transform.scale(red1, (30, 30))
blue1 = load_image('blue2.png')
blue = pygame.transform.scale(blue1, (30, 30))


ghost_images = {'bghost': blue, 'rghost': red}

tile_width = tile_height = 50

all_walls = []

class Tile(pygame.sprite.Sprite):
    def __init__(self, tile_type, pos_x, pos_y):
        super().__init__(tiles_group, all_sprites)
        self.image = tile_images[tile_type]
        self.rect = self.image.get_rect().move(tile_width * pos_x, tile_height * pos_y)


class Player(pygame.sprite.Sprite):
    def __init__(self, pos_x, pos_y):
        super().__init__(player_group, all_sprites)
        self.image = player_image
        self.rect = self.image.get_rect().move(tile_width * pos_x + 10, tile_height * pos_y + 10)
        self._layer = self.rect.bottom
        self.vx = 0
        self.vy = 0
        self.up = False
        self.down = False
        self.left = False
        self.right = False
        self.score = 0
        self.lives = 3
        self.life = False
        self.n = 0
        self.win = False

       
    def update(self):
        self.rect = self.rect.move(self.vx, self.vy)
        if self.up:
            self.image = image1
            self.vx = 0
            self.vy = -2
        elif self.down:
            self.image = image2
            self.vx = 0
            self.vy = 2
        elif self.left:
            self.image = image3
            self.vx = -2
            self.vy = 0
        elif self.right:
            self.image = image4
            self.vx = 2
            self.vy = 0
        if pygame.sprite.spritecollideany(self, cherries):
            self.win = True    
        if pygame.sprite.spritecollideany(self, walls):
            self.vx = 0
            self.vy = 0
        x = pygame.sprite.spritecollide(self, dots, True)
        if x:
            self.score += 100
        if pygame.sprite.spritecollideany(self, ghosts):
            self.image = player_image
            self.rect.x = 160
            self.rect.y = 710
            self.vx = 0
            self.vy = 0
            self.up = False
            self.down = False
            self.left = False
            self.right = False            
            self.life = True    


class Ghost(pygame.sprite.Sprite):
    def __init__(self, ghost_color, pos_x, pos_y, direction):
        super().__init__(all_sprites, ghosts)
        self.add(ghosts)
        self.image = ghost_images[ghost_color]
        self.rect = self.image.get_rect().move(tile_width * pos_x + 10, tile_height * pos_y + 10)
        self._layer = self.rect.bottom
        self.vx = 0
        self.vy = 0
        self.up = False
        self.down = False
        self.left = False
        self.right = False
        self.direction = direction


    def update(self):
        self.rect = self.rect.move(self.vx, self.vy)
        if self.direction == 1 or self.direction == 5:
            if self.rect.y + 40 == 550:
                self.down = False
                self.up = True
                self.vx = 0
                self.vy = -2
            if self.rect.y - 10 == 300:
                self.up = False
                self.down = True
                self.vx = 0
                self.vy = 2
        elif self.direction == 2:
            if self.rect.x - 10 == 250:
                self.right = True
                self.vx = 2
                self.vy = 0
            if self.rect.x + 40 == 700:
                self.right = False
                self.down = True
                self.vx = 0
                self.vy = 2
            if self.rect.y - 10 == 200 and self.rect.x + 40 == 700:
                self.down = False
                self.left = True
                self.vx = -2
                self.vy = 0
            if self.rect.x - 10 == 550 and self.rect.y - 10 == 200:
                self.left = False
                self.down = True
                self.vx = 0
                self.vy = 2
            if self.rect.y + 40 == 350 and self.rect.x - 10 == 550:
                self.down = False
                self.left = True
                self.vx = -2
                self.vy = 0
            if self.rect.x - 10 == 450 and self.rect.y - 10 == 300:
                self.left = False
                self.up = True
                self.vx = 0
                self.vy = -2
            if self.rect.y - 10 == 200 and self.rect.x - 10 == 450:
                self.up = False
                self.left = True
                self.vx = -2
                self.vy = 0
            if self.rect.x - 10 == 350 and self.rect.y - 10 == 200:
                self.left = False
                self.up = True
                self.vx = 0
                self.vy = -2
            if self.rect.y - 10 == 100 and self.rect.x - 10 == 350:
                self.up = False
                self.right = True
                self.vx = 2
                self.vy = 0
        elif self.direction == 3 or self.direction == 4:
            if self.rect.y - 10 == 300:
                self.up = False
                self.down = True
                self.vx = 0
                self.vy = 2
            if self.rect.y + 40 == 550:
                self.down = False
                self.up = True
                self.vx = 0
                self.vy = -2      
                   

class Wall(pygame.sprite.Sprite):
    def __init__(self, tile_type, pos_x, pos_y):
        super().__init__(all_sprites, walls)
        self.add(walls)
        self.image = tile_images[tile_type]
        self.rect = self.image.get_rect().move(tile_width * pos_x, tile_height * pos_y)
       
       
class Dots(pygame.sprite.Sprite):
    def __init__(self, tile_type, pos_x, pos_y):
        super().__init__(all_sprites, dots)
        self.add(dots)
        self.image = tile_images[tile_type]
        self.rect = self.image.get_rect().move(tile_width * pos_x, tile_height * pos_y)
       

class Cherry(pygame.sprite.Sprite):
    def __init__(self, tile_type, pos_x, pos_y):
        super().__init__(all_sprites, cherries)
        self.add(cherries)
        self.image = tile_images[tile_type]
        self.rect = self.image.get_rect().move(tile_width * pos_x + 10, tile_height * pos_y + 10)
       
       
GRAVITY = 0.1


class Particle(pygame.sprite.Sprite):
    fire = [load_image("star.png")]
    for scale in (5, 10, 20):
        fire.append(pygame.transform.scale(fire[0], (scale, scale)))

    def __init__(self, pos, dx, dy):
        super().__init__(all_sprites, stars)
        self.image = choice(self.fire)
        self.rect = self.image.get_rect()
       
        self.velocity = [dx, dy]
        self.rect.x, self.rect.y = pos

        self.gravity = GRAVITY

    def update(self):

        self.velocity[1] += self.gravity
   
        self.rect.x += self.velocity[0]
        self.rect.y += self.velocity[1]
       

def create_particles(position):
    particle_count = 20
    numbers = range(-5, 6)
    for _ in range(particle_count):
        Particle(position, choice(numbers), choice(numbers))
       
all_sprites = pygame.sprite.LayeredUpdates()
tiles_group = pygame.sprite.LayeredUpdates()
player_group = pygame.sprite.LayeredUpdates()
walls = pygame.sprite.LayeredUpdates()
dots = pygame.sprite.LayeredUpdates()
ghosts = pygame.sprite.LayeredUpdates()
stars = pygame.sprite.LayeredUpdates()
cherries = pygame.sprite.LayeredUpdates()


player = None

def generate_level(level):
    new_player, x, y = None, None, None
    for y in range(len(level)):
        for x in range(len(level[y])):
            if level[y][x] == '.':
                Tile('empty', x, y)
                Dots('dot', x, y)
            elif level[y][x] == '-':
                Wall('wall', x, y)
            elif level[y][x] == 'v':
                Cherry('cherry', x, y)
            elif level[y][x] == '+':
                villian = choice(['bghost', 'rghost'])
                Tile('empty', x, y)
                Dots('dot', x, y)
                if x == 1:
                    ghost1 = Ghost(villian, x, y, 1)
                elif x == 5:
                    ghost2 = Ghost(villian, x, y, 2)
                elif x == 7:
                    ghost3 = Ghost(villian, x, y, 3)
                elif x == 13:
                    ghost4 = Ghost(villian, x, y, 4)
                elif x == 19:
                    ghost5 = Ghost(villian, x, y, 5)
            elif level[y][x] == '?':
                Tile('life', x, y)            
    for y in range(len(level)):
        for x in range(len(level[y])):
            if level[y][x] == '@':
                Tile('empty', x, y)
                new_player = Player(x, y)
                player_x = x
                player_y = y          
    return new_player, x, y, ghost1, ghost2, ghost3, ghost4, ghost5

player, level_x, level_y, ghost1, ghost2, ghost3, ghost4, ghost5 = generate_level(load_level('pacmap.txt'))

n = 0
x = 0
y = -5
running = True
while running:
    if player.lives > 0 and player.win is False:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                if event.key == 273:
                    player.up = True
                    player.down = False
                    player.left = False
                    player.right = False                
                    player.vx = 0
                    player.vy = -2
                if event.key == 274:
                    player.up = False
                    player.down = True
                    player.left = False
                    player.right = False
                    player.vx = 0
                    player.vy = 2
                if event.key == 276:
                    player.left = True
                    player.right = False
                    player.up = False
                    player.down = False
                    player.vx = -2
                    player.vy = 0
                if event.key == 275:
                    player.up = False
                    player.down = False
                    player.left = False
                    player.right = True
                    player.vx = 2
                    player.vy = 0
        if player.life == True:
            player.life = False
            player.lives -= 1
            if player.n == 0:
                Tile('empty', 20, 0)
            elif player.n == 1:
                Tile('empty', 19, 0)
            elif player.n == 2:
                screen.fill((0, 0, 0))
                Tile('empty', 18, 0)
            player.n += 1

               
        screen.fill((0, 0, 0))

        all_sprites.change_layer(player, player.rect.bottom)
        all_sprites.change_layer(ghost1, player.rect.bottom)
        all_sprites.change_layer(ghost2, player.rect.bottom)
        all_sprites.change_layer(ghost3, player.rect.bottom)
        all_sprites.change_layer(ghost4, player.rect.bottom)
        all_sprites.change_layer(ghost5, player.rect.bottom)
       
        score = player.score
       
        draw()
        draw_life()
        all_sprites.update()  
        all_sprites.draw(screen)
        clock.tick(fps)
    else:
        screen.fill((0, 0, 0))
        if player.win:
            intro_text = ['YOU ARE A WINNER', f'YOUR SCORE IS {player.score}',
                          'CONGRATULATIONS']
            if len(stars) <= 1000:
                x = choice([i for i in range(1, 1000)])
                y = choice([i for i in range(1, 700)])
                create_particles((x, y))
                stars.update()
                stars.draw(screen)                
        else:
            intro_text = [f'YOUR SCORE IS {player.score}', 'YOU HAVE LOST']
        font = pygame.font.Font(None, 80)
        text_coord = 300
        for line in intro_text:
            string_rendered = font.render(line, 1, pygame.Color('yellow'))
            intro_rect = string_rendered.get_rect()
            text_coord += 10
            intro_rect.top = text_coord
            intro_rect.x = 250
            text_coord += intro_rect.height
            screen.blit(string_rendered, intro_rect)        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

    pygame.display.flip()
pygame.quit()