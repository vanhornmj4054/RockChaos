import pygame
import random
from pygame.locals import *
import sys
import math
import os
from os import path


img_dir = path.join(path.dirname(__file__), 'images')
snd_dir = path.join(path.dirname(__file__), 'snd')


WIDTH = 1000
HEIGHT = 570
FPS = 60

# define colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)


# initialize pygame and create window
pygame.init()
pygame.mixer.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Enemies test")
clock = pygame.time.Clock()
pygame.display.set_mode((0, 0), pygame.FULLSCREEN)







#------------- Load Music and sound effects-------------------
opening_music = pygame.mixer.music.load('bgm_maoudamashii_healing08.ogg')
pygame.mixer.music.set_volume(0.3)
pygame.mixer.music.play(-1)
laser_shot = pygame.mixer.Sound(path.join(snd_dir, "pulse_gun.wav"))
explosion = pygame.mixer.Sound(path.join(snd_dir, "explosion.wav"))
death_explosion = pygame.mixer.Sound(path.join(snd_dir, "ground_explosion.wav"))
ground_explosion = pygame.mixer.Sound(path.join(snd_dir, "explosion1.wav"))


# -----------------------------------------SCROLLING EXPERIMENT---------------------------------------------

# bg = pygame.image.load(path.join(img_dir, "bg4.png")).convert()
# bgWidth, bgHeight = bg.get_rect().size

# stageWidth = bgWidth*2
# stagePosX = 0

# startScrollingPosX = HW
# --------------------------------------------------------------------------------------------------------

font_name = pygame.font.match_font("ariel")
def draw_text(surf, text, size, x, y):
    font = pygame.font.Font(font_name, size)
    text_surface = font.render(text, True, WHITE)
    text_rect = text_surface.get_rect()
    text_rect = (850,20)
    surf.blit(text_surface, text_rect)

# def draw_instruction(surf, text, size, x, y, game_start):
#     start = pygame.time.get_ticks()
#     while game_start == True:
#         now = pygame.time.get_ticks()
#         if now - start < 10000:
#             font = pygame.font.Font(font_name, size)
#             text_surface = font.render(text, True, WHITE)
#             text_rect = text_surface.get_rect()
#             text_rect = (WIDTH/2,HEIGHT/4)
#             surf.blit(text_surface, text_rect)
#             now = pygame.time.get_ticks()
#         else:


def game_over_screen():
    bg = pygame.image.load(path.join(img_dir, "game_over.png"))
    bg_rect = bg.get_rect()
    bg_rect.centerx = WIDTH / 2
    bg_rect.centery = HEIGHT / 2
    player.kill()
    music = pygame.mixer.music.load('game_over.mp3')
    pygame.mixer.music.set_volume(0.3)
    pygame.mixer.music.play(-1)
    waiting = True
    all_sprites.draw(screen)
    screen.fill(BLACK)
    screen.blit(bg, bg_rect)
    draw_text(screen, ("Score: " + str(score)), 35, WIDTH / 2, 10)
    # draw_text(screen, ("Level: " + level, 35, WIDTH / 2, 10)
    # *after* drawing everything, flip the display

    pygame.display.flip()
    while waiting:
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:
                    print("r")
                    pygame.quit()


def new_mob():
    m = Mob()
    all_sprites.add(m)
    mobs.add(m)

# ------health bar: note "pct" is percentage of health points
def draw_shield_bar(surf, x,y,pct):
    if pct < 0:
        pct = 0
    BAR_LENGTH = 100
    BAR_HEIGHT = 10
    fill = (pct / 100) * BAR_LENGTH
    outline_rect = pygame.Rect(x,y,BAR_LENGTH, BAR_HEIGHT)
    fill_rect = pygame.Rect(x,y,fill, BAR_HEIGHT)
    pygame.draw.rect(surf, GREEN, fill_rect)
    pygame.draw.rect(surf, BLACK, outline_rect, 2)

class Player(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        # player rectangle height and width
        self.image = pygame.Surface((50,40))
        self.images = []
        img = pygame.image.load(os.path.join('images', 'stand_left.png'))
        self.images.append(img)
        self.image = self.images[0]
        self.rect = self.image.get_rect()
        self.image = pygame.transform.scale(img, (60,60))
        self.radius = 15
        # draw a circle around player to see where a collision would be 
        # pygame.draw.circle(self.image, RED, self.rect.center, self.radius)
        self.rect.centerx = WIDTH / 2
        self.rect.bottom = HEIGHT - 35
        self.speedx = 0
        self.speedy = 0
        self.shoot_delay = 200
        self.last_shot = pygame.time.get_ticks()
        self.shield = 100


    def update(self):
        self.speedx = 0
        self.speedy = 0
        keystate = pygame.key.get_pressed()
        if keystate[pygame.K_LEFT]:
            self.speedx = -5
        if keystate[pygame.K_RIGHT]:
            self.speedx = 5
        if keystate[pygame.K_SPACE]:
            self.shoot()

        self.rect.x += self.speedx
        self.rect.y += self.speedy
        if self.rect.right > WIDTH:
            self.rect.right = WIDTH
        if self.rect.left < 0:
            self.rect.left = 0

    def shoot(self):
        now = pygame.time.get_ticks()
        if now - self.last_shot > self.shoot_delay:
            self.last_shot = now
        # put the bottom of the bullet at the top of the player in the center of its 'x' width
            bullet = Bullet(self.rect.centerx, self.rect.top)
            all_sprites.add(bullet)
            bullets.add(bullet)
            laser_shot.play()
    
    # def death(self):
    #     print("death")
    #     death_explosion.play(0)
    #     self.kill()



class Mob(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image_orig = random.choice(meteor_images)
        self.image_orig.set_colorkey(BLACK)
        self.image = self.image_orig.copy()
        # img = pygame.image.load(os.path.join('images', 'enemy.png'))
        # self.images.append(img)
        # self.image = self.images[0]
        self.rect = self.image.get_rect()
        self.radius = int(self.rect.width * .85 /2)
        # draw a circle around player to see where a collision would be 
        # pygame.draw.circle(self.image, RED, self.rect.center, self.radius)
        self.rect.x = random.randrange(WIDTH - self.rect.width)
        self.rect.y = random.randrange(-70,-60)
        self.speedx = random.randrange(-3,3)
        self.speedy = random.randrange(1,8)
        # set meteors to spin
        self.rot = 0
        self.rot_speed = random.randrange(-8, 8)
        self.last_update = pygame.time.get_ticks()
    
    def rotate(self):
        now = pygame.time.get_ticks()
        if now - self.last_update > 50:
            self.last_update = now
            self.rot = (self.rot + self.rot_speed) % 360
            new_image = pygame.transform.rotate(self.image_orig, self.rot)
            old_center = self.rect.center
            self.image = new_image
            self.rect = self.image.get_rect()
            self.rect.center = old_center



    def update(self):
        self.rotate()
        self.rect.x += self.speedx
        self.rect.y += self.speedy
        if self.rect.top > HEIGHT + 10:
            self.rect.x = random.randrange(WIDTH - self.rect.width)
            self.rect.y = random.randrange(-70, -60)
            self.speedy = random.randrange(1,8)
        if self.rect.bottom > 580:
            ground_explosion.play(0)
            explode = Explosion(self.rect.center, 'lg')
            all_sprites.add(explode)
            self.kill()
            
            m = Mob()
            all_sprites.add(m)
            mobs.add(m)
        

class Bullet(pygame.sprite.Sprite):
    # the 'x' and 'y' to spawn bullet at a certain location 
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface((10, 20))
        self.images = []
        img = pygame.image.load(os.path.join('images', 'shot3.png'))
        self.images.append(img)
        self.image = self.images[0]
        self.rect = self.image.get_rect()
        self.radius = 15
        # draw a circle around player to see where a collision would be 
        # pygame.draw.circle(self.image, RED, self.rect.center, self.radius)
        self.rect.bottom = y
        self.rect.centerx = x + 12
        self.speedy = -20

    def update(self):
        self.rect.y += self.speedy
        # kill if it moves off the screen (bullet didn't hit anything)
        if self.rect.bottom < 0:
            self.kill()

class Explosion(pygame.sprite.Sprite):
    def __init__(self, center, size):
        pygame.sprite.Sprite.__init__(self)
        self.size = size
        self.image = explosion_anim[self.size][0]
        self.rect = self.image.get_rect()
        self.rect.center = center
        self.frame = 0
        self.last_update = pygame.time.get_ticks()
        self.frame_rate = 50

    def update(self):
        now = pygame.time.get_ticks()
        if now - self.last_update > self.frame_rate:
            self.last_update = now
            self.frame += 1
            if self.frame == len(explosion_anim[self.size]):
                self.kill()
            else:
                center = self.rect.center
                self.image = explosion_anim[self.size][self.frame]
                self.rect = self.image.get_rect()
                self.rect.center = center




#---------------SPLASH PAGE----------------------------------------------
game_start = False
while game_start == False:
    logo = pygame.image.load(path.join(img_dir, "opening-logo.png"))
    logo_rect = logo.get_rect()
    screen.blit(logo, logo_rect)
    logo_rect.centerx = WIDTH / 2
    logo_rect.centery = HEIGHT / 2

    bg = pygame.image.load(path.join(img_dir, "bg4.png")).convert()
    bg_rect = bg.get_rect()
    screen.blit(bg, bg_rect)
    for event in pygame.event.get():
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                print("space")
                game_start = True


    screen.fill(WHITE)
    screen.blit(bg, bg_rect)
    screen.blit(logo, logo_rect)
    
    # *after* drawing everything, flip the display
    pygame.display.flip()


if game_start == True:
    music = pygame.mixer.music.load('bgm_maoudamashii_fantasy15.ogg')
    pygame.mixer.music.set_volume(0.3)
    pygame.mixer.music.play(-1)


    meteor_images = []
    meteor_list = ['meteorBrown_big1.png', 'meteorBrown_big2.png','meteorBrown_med1.png','meteorBrown_med3.png','meteorBrown_small1.png','meteorBrown_small2.png', 'meteorBrown_tiny1.png', 'meteorBrown_tiny2.png']

    for img in meteor_list:
        meteor_images.append(pygame.image.load(path.join(img_dir, img)).convert())



    explosion_anim = {}
    explosion_anim["lg"] = []
    explosion_anim["sm"] = []
    for i in range(9):
        filename = 'regularExplosion{}.png'.format(i)
        img = pygame.image.load(path.join(img_dir, filename)).convert()
        img.set_colorkey(BLACK)
        img_lg = pygame.transform.scale(img, (100,100))
        explosion_anim['lg'].append(img_lg)
        img_sm = pygame.transform.scale(img, (32,32))
        explosion_anim['sm'].append(img_sm)
        # filename = "sonicExplosion{}.png".format(i)
        # img = pygame.image.load(path.join(img_dir, filename)).convert()
        # explosion_anim["player"].append(img)

# -----------Adding sprites------------------------------------

    all_sprites = pygame.sprite.Group()
    mobs = pygame.sprite.Group()
    bullets = pygame.sprite.Group()
    player = Player()
    all_sprites.add(player)
    
# -----------Keeping Score--------------
 
# Game loop
running = True
game_over = False
level = 2
start = pygame.time.get_ticks()
score = 0
while running:
    clock.tick(FPS)
    if game_over:
        now = pygame.time.get_ticks()
        if now - start > 3000:
            start = now
            game_over_screen()
    # keep loop running at the right speed
    
    # Process input (events)
    for event in pygame.event.get():
        # check for closing window
        if event.type == pygame.QUIT:
            running = False


    # Update sprites
    all_sprites.update()


    now = pygame.time.get_ticks()
    
    if now - start > 10000:
        start = now
        level += 1
    
        for i in range(level):
            new_mob()


    # check to see if bullet hit mob. True1 = delete mob if hit by bullet, True2 if bullet get hit then delete
    hits = pygame.sprite.groupcollide(mobs, bullets, True, True)
    # when you kill of an enemy, make sure to spawn more
    for hit in hits:
        score += hit.radius // 4
   
        explosion.play()
        explode = Explosion(hit.rect.center, 'lg')
        explode_sm = Explosion(hit.rect.center, 'sm')
        all_sprites.add(explode)
        new_mob()


    # check to see if a mob hit the player
    hits = pygame.sprite.spritecollide(player, mobs, True)
    for hit in hits:
        player.shield -= hit.radius * 2
        new_mob()
        explosion.play()
        # death_explosion = Explosion(player.rect.center, 'player')
        explode = Explosion(player.rect.center, 'lg')
        explode_sm = Explosion(player.rect.center, 'sm')
        all_sprites.add(explode)

        # player.death()
        if player.shield <= 0:
            game_over = True


    screen.fill(BLACK)
    screen.blit(bg, bg_rect)
    all_sprites.draw(screen)
    draw_text(screen, ("Score: " + str(score)), 40, WIDTH / 2, 10)
    draw_shield_bar(screen, 5,5,player.shield)

    # *after* drawing everything, flip the display
    pygame.display.flip()


pygame.quit()