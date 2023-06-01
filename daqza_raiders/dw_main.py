#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat May 27 20:29:52 2023

@author: Daedallu!
"""

import pygame
from pygame.locals import *
pygame.font.init()
import sys
import random
from pygame import mixer



pygame.mixer.pre_init(44100, -16, 2, 512, None, 5)
mixer.init()
#pygame.init()


#definindo os FPS:
Clock = pygame.time.Clock()
fps = 60

#defnindo sons:
explosion_fx = pygame.mixer.Sound("/home/glorto86b/py_games/daqza_raiders/images/xplod2.mp3")
explosion_fx.set_volume(0.5)

laser_fx = pygame.mixer.Sound("/home/glorto86b/py_games/daqza_raiders/images/shot.mp3")
laser_fx.set_volume(0.5)

#enemyFire_fx = pygame.mixer.Sound("/home/glorto86b/daqa_wars/images/enemyShot.mp3")
#enemyFire_fx.set_volume(0.2)

#bgMusic = pygame.mixer.Sound("/home/glorto86b/daqa_wars/images/flight3.mp3")
#bgMusic.set_volume(0.05)

screen_width = 600
screen_height = 800

#definindo as var de jogo:
rows = 5
cols = 5
enemy_cooldown = 200 #disparos em milissegundos
last_enemy_shot = pygame.time.get_ticks()
countdown = 3
last_count = pygame.time.get_ticks()
game_over = 0 #naõ é fim de jogo; 1 = jogador venceu; -1 = jogador perdeu


screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("DAQZA RAID(version beta)","/home/glorto86b/py_games/daqza_raiders/images/shipp.bmp ")

font30 = pygame.font.SysFont('uroob', 30)
font40 = pygame.font.SysFont('uroob', 40)
font50 = pygame.font.SysFont('uroob', 50)

#define as cores:
ftalo= (204, 0, 157)
blue_green = (42, 212, 255)
white = (255, 255, 255)
lilac = (234, 0, 234)

#texto

def draw_text(text, font, text_col, x, y):
    img = font.render(text, True, text_col)
    screen.blit(img,(x,y))


bg = pygame.image.load("/home/glorto86b/py_games/daqza_raiders/images/bg2.png")

def draw_bg():
    #screen.blit((45, 0 , 55))
    screen.blit(bg, (0,0))
    
class Spaceship(pygame.sprite.Sprite):
    
    def __init__(self, x, y, health):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load("/home/glorto86b/py_games/daqza_raiders/images/ship.png")
        self.rect = self.image.get_rect()
        self.rect.center = [x,y]
        self.health_start = health
        self.health_remains = health
        self.last_shot = pygame.time.get_ticks()
       # bgMusic.play(-1)
        
        
    #definindo a vel. do veículo:
    def update(self):
        speed = 8
        #var cooldown:
        cooldown = 500 #milissegundos
        
        game_over = 0
        
        
        key = pygame.key.get_pressed()
        if key[pygame.K_LEFT] and self.rect.left>0:
            self.rect.x -= speed
        if key[pygame.K_RIGHT] and self.rect.right<screen_width:
            self.rect.x += speed
        #if key[pygame.K_UP] and self.rect.y>int(screen_height)/2:
         #   self.rect.y -= speed
        #if key[pygame.K_DOWN] and self.rect.y>=int(screen_height)/2 or self.rect.y>screen_height - 50:
         #   self.rect.y += speed
         #disparo
         #grava tempo corrente:
        time_now = pygame.time.get_ticks()
        if key[pygame.K_SPACE] and time_now - self.last_shot > cooldown:
           bullet = Bullets(self.rect.centerx, self.rect.top)
           bullet_group.add(bullet)
           self.last_shot = time_now
           laser_fx.play()

        if key[pygame.K_DOWN] and key[pygame.K_x]:
           self.image = pygame.image.load("/home/glorto86b/py_games/daqza_raiders/images/enemy" + str(random.randint(1,5)) + ".png")
        if key[pygame.K_UP] :
           self.image = pygame.image.load("/home/glorto86b/py_games/daqza_raiders/images/ship.png")
        if key[pygame.K_DOWN] and key[pygame.K_g] and key[pygame.K_h]:
           self.image = pygame.image.load("/home/glorto86b/py_games/daqza_raiders/images/phantom_ghost.png")
           speed = 20
        if key[pygame.K_DOWN] and key[pygame.K_0] and key[pygame.K_n] and key[pygame.K_l]  :
           self.image = pygame.image.load("/home/glorto86b/py_games/daqza_raiders/images/invisible.png")
           
           
           
           
         #atualiza máscara:
        self.mask = pygame.mask.from_surface(self.image)
         
         #desenha a barra de energia
        pygame.draw.rect(screen, ftalo, (self.rect.x, (self.rect.bottom + 10), self.rect.width, 15))
        if self.health_remains > 0:
            pygame.draw.rect(screen, blue_green, (self.rect.x, (self.rect.bottom + 10), int(self.rect.width * (self.health_remains/self.health_start)), 15))
        elif self.health_remains <= 0:
            xplod = Xplodit(self.rect.centerx, self.rect.centery, 3)
            xplodit_group.add(xplod)
            self.kill()
            game_over = -1
        return game_over
    
        
        
        
#cria uma classe pra munição da espaçonave/jogador    
class Bullets(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load("/home/glorto86b/py_games/daqza_raiders/images/Bullet.png")
        self.rect = self.image.get_rect()
        self.rect.center = [x,y]
    def update(self):
        self.rect.y -= 5
        if self.rect.bottom < 200:
            self.image = pygame.image.load("/home/glorto86b/py_games/daqza_raiders/images/Bullet2.png")
        if self.rect.bottom < 400 and self.rect.bottom > 200:
            self.image = pygame.image.load("/home/glorto86b/py_games/daqza_raiders/images/Bullet3.png")    
        if self.rect.bottom < 100:
            self.kill()
        

        
        if pygame.sprite.spritecollide(self, enemies_group, True):
           self.kill()
           explosion_fx.play()
           xplod = Xplodit(self.rect.centerx, self.rect.centery, 2)
           xplodit_group.add(xplod)
           
        


#cria uma classe pra munição da espaçonave/jogador    
class Enemies(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load ("/home/glorto86b/py_games/daqza_raiders/images/enemy" + str(random.randint(1,5)) + ".png")
        self.rect = self.image.get_rect()
        self.rect.center = [x,y]
        self.move_counter = 0
        self.move_direction = 1
    def update(self):
        self.rect.x += self.move_direction
        self.move_counter +=5
        if abs(self.move_counter) > 75:
            self.move_direction *= -1
            self.move_counter *= self.move_direction

        

#criando classe de munição inimiga

class Enemy_Bullets(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load("/home/glorto86b/py_games/daqza_raiders/images/enemyBullet.png")
        self.rect = self.image.get_rect()
        self.rect.center = [x,y]
    def update(self):
        self.rect.y += 10
        if self.rect.top > screen_height:
            self.kill()
        if pygame.sprite.spritecollide(self, spaceship_group, False, pygame.sprite.collide_mask):
           self.kill()
           explosion_fx.play()
           #decrementa a saúde da espaçonave/jogador
           spaceship.health_remains -= 1
           xplod = Xplodit(self.rect.centerx, self.rect.centery, 1)
           xplodit_group.add(xplod)

#criando classe de explosoes:

class Xplodit(pygame.sprite.Sprite):
        def __init__(self, x, y, size):
            pygame.sprite.Sprite.__init__(self)
            self.images = []
            for num in range(1,5):
                img = pygame.image.load(f"/home/glorto86b/py_games/daqza_raiders/images/xplod{num}.png")
                if size == 1:
                    img = pygame.transform.scale(img,(40, 40))
                if size == 2:
                    img = pygame.transform.scale(img,(60, 60))
                if size == 3:
                    img = pygame.transform.scale(img,(180, 180))
                #add the image to the list
                self.images.append(img)
            self.index = 0    
            self.image = self.images[self.index]
            self.rect = self.image.get_rect()
            self.rect.center = [x,y]
            self.counter = 0
        
        def update(self):
            xplodit_speed = 3
            #atualiza a animação da explosão
            self.counter += 1
            
            if self.counter >= xplodit_speed and self.index < len(self.images) - 1:
               self.counter = 0
               self.index += 1
               self.image = self.images[self.index]
            #se a animação está completa, apaga a explosão  
            if self.index >= len(self.images) - 1 and self.counter >= xplodit_speed:
                self.kill()
    

        
#criando grupos de sprites:

spaceship_group = pygame.sprite.Group()
bullet_group = pygame.sprite.Group()
enemies_group = pygame.sprite.Group()
enemy_bullets_group = pygame.sprite.Group()
xplodit_group = pygame.sprite.Group()


def create_enemies():
    for row in range(rows):
        for item in range(cols):
            enemy = Enemies(100 + item * 100, 100 + row * 70)
            enemies_group.add(enemy)
            
create_enemies()


#criando o jogador:
    
spaceship = Spaceship(int(screen_width/2), screen_height - 190, 3)
spaceship_group.add(spaceship)

run = True

while run:
    
    Clock.tick(fps)
    
    #desenha a tela
    draw_bg()
    
    

    if countdown == 0:

        #cria disparos inimigos aleatórios:
        
        #grava tempo atual
        time_now = pygame.time.get_ticks()
        #disparo
        if time_now - last_enemy_shot > enemy_cooldown and len(enemy_bullets_group) < 5 and len(enemies_group) > 0:
            attacking_enemy = random.choice(enemies_group.sprites()) 
            enemy_bullet = Enemy_Bullets(attacking_enemy.rect.centerx, attacking_enemy.rect.bottom)
            enemy_bullets_group.add(enemy_bullet)
            last_enemy_shot = time_now
        
        #checa se todos os inimigos foram eliminados
        if len(enemies_group) == 0:
            game_over = 1
            
        if game_over == 0:
            #atualiza a nave:        
            game_over = spaceship.update()
        
            #atualiza munição
            bullet_group.update()
            #atualiza inimigos
            enemies_group.update()
            #atualiza munição inimiga:
            enemy_bullets_group.update()
            
        else:    
            if game_over == -1:
                draw_text('GAME OVER', font50, lilac, int(screen_width/2 - 90), int(screen_height/2 + 50 ))
            if game_over == 1:
                draw_text('CONGRATS. YOU WIN.', font50, lilac, int(screen_width/2 - 150), int(screen_height/2 + 50 ))
            
            
    
    if countdown > 0:
        draw_text('GET READY', font40, white, int(screen_width/2 - 90), int(screen_height/2 + 50 ))
        draw_text(str(countdown), font40, white, int(screen_width/2 - 10), int(screen_height/2 + 100))
        count_timer = pygame.time.get_ticks()
        if count_timer - last_count > 1000:
            countdown -= 1
            last_count = count_timer
        
        
    #atualiza xplodit_group
    xplodit_group.update()
    
    
    #atualiza grupos de sprites:
    spaceship_group.draw(screen)
    bullet_group.draw(screen)
    enemies_group.draw(screen)
    enemy_bullets_group.draw(screen)
    xplodit_group.draw(screen)
    
    pygame.display.update()
    
    
   #laço principal do jogo
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False #pára o jogo
            
#mostra as atualizações de tela
pygame.quit()
            #sys.exit()
            
    
    
