import pygame
import random
import sys

pygame.init()
WIDTH = 336
HEIGHT = 540
window = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()
moving = True
class Background():
    def __init__(self):
        self.image = pygame.image.load('background.png')
        self.x_1 = 0
        self.x_2 = WIDTH
    
    def draw(self):
        window.blit(self.image, (self.x_1, 0))
        window.blit(self.image, (self.x_2, 0))
    
    def update(self):
        self.x_1 -= 0.3
        self.x_2 -= 0.3
        if self.x_1 <= -WIDTH:
            self.x_1 = WIDTH
        if self.x_2 <= -WIDTH:
            self.x_2 = WIDTH
class Ground():
    def __init__(self):
        self.image = pygame.image.load('ground.png')
        self.x_1 = 0
        self.x_2 = WIDTH
    
    def draw(self):
        window.blit(self.image, (self.x_1, 428))
        window.blit(self.image, (self.x_2, 428))
    
    def update(self):
        self.x_1 -= 2
        self.x_2 -= 2
        if self.x_1 <= -WIDTH:
            self.x_1 = WIDTH
        if self.x_2 <= -WIDTH:
            self.x_2 = WIDTH
class Pipes():
    def __init__(self):
        self.gate = random.randint(100, HEIGHT-200)
        self.gap = random.randint(35, 50)
        self.top_image = pygame.image.load('top-pipe.png')
        self.top_rect = self.top_image.get_rect()
        self.top_rect.bottomleft = (WIDTH, self.gate - self.gap)
        self.bot_image = pygame.image.load('bot-pipe.png')
        self.bot_rect = self.bot_image.get_rect()
        self.bot_rect.topleft = (WIDTH, self.gate + self.gap)
    def draw(self):
        window.blit(self.top_image, self.top_rect)
        window.blit(self.bot_image, self.bot_rect)
    def update(self):
        self.top_rect.x -= 2
        self.bot_rect.x -= 2
        if self.top_rect.right < 0:
            self.gate = random.randint(100, HEIGHT-200)
            print(self.gate)
            self.gap =random.randint(35, 50)
            print(self.gap)
            self.top_rect.bottomleft = (WIDTH, self.gate - self.gap)
            self.bot_rect.topleft = (WIDTH, self.gate + self.gap)
            game.score += 1
            game.update_score()
class Bird():
    def __init__(self):
        self.image_default = pygame.image.load('bird.png')
        self.image = self.image_default
        self.rect = self.image.get_rect(center = (
            WIDTH // 3,
            HEIGHT // 2
        ))
        self.base_speed = -2
        self.speed = self.base_speed
        self.angle = 0
    def draw(self):
        window.blit(self.image, self.rect)
    def update(self):
        self.rect.y -= self.speed
        if self.speed> self.base_speed:
            self.speed -= 1
        if self.rect.top < 0:
            self.rect.top = 1
        if self.rect.bottom > 429:
            self.rect.bottom = 428
        if self.speed > 0:
            self.angle += 3
            if self.angle >50:
                self.angle = 50
        if self.speed < 0:
            self.angle -= 1
            if self.angle <-50:
                self.angle = -50
        self.image = pygame.transform.rotate(self.image_default, self.angle)


        for e in events:
            if game.state == 'play':
                if e.type == pygame.KEYDOWN or e.type == pygame.MOUSEBUTTONDOWN:
                    self.speed = 8
        if self.rect.collidelistall([pipes.bot_rect, pipes.top_rect]):
            game.state = 'over'
class Gamemanager():
    def __init__(self):
        self.state = 'play'
        self.score = 0
        self.font = pygame.font.Font('Flappy-Bird.ttf', 30)
        self.score_text = self.font.render('0', True, (255, 255, 255))
        self.restart_text = self.font.render('Press any key to restart', True, (255, 255, 255))  
    def centerx(self, surf):
        return (WIDTH // 2) - (surf.get_width() // 2)
    def centery(self, surf):
        return (HEIGHT // 2) - (surf.get_height() // 2)
    def draw_score(self):
        window.blit(self.score_text, (self.centerx(self.score_text), 10))
    def update_score(self):
        self.score_text = self.font.render(str(self.score), True, (255, 255, 255))
    def draw_restart(self):
        window.blit(self.restart_text, (self.centerx(self.restart_text), self.centery(self.restart_text)))            
    def restart(self):
        self.state = 'play'
        self.score = 0
        self.update_score()
        bird.rect.center = (WIDTH // 3, HEIGHT // 2)
        bird.speed = bird.base_speed
        bird.angle = 0
        pipes.gate = random.randint(100, HEIGHT-200)
        pipes.gap =random.randint(35, 50)
        pipes.top_rect.bottomleft = (WIDTH, pipes.gate - pipes.gap)
        pipes.bot_rect.topleft = (WIDTH, pipes.gate + pipes.gap)


bg = Background()
gr = Ground()
pipes = Pipes()
bird = Bird()
game = Gamemanager()

while True:
    events = pygame.event.get()
    for e in events:
        if e.type == pygame.QUIT:
            sys.exit()
        if e.type == pygame.KEYDOWN or pygame.MOUSEBUTTONDOWN:
            if game.state == 'over':
                game.restart()
    if game.state == 'play':
        bg.update()
        pipes.update()
        gr.update()         
    bird.update()

    bg.draw()
    pipes.draw()
    gr.draw()
    bird.draw()
    game.draw_score()
    if game.state == 'over':
        game.draw_restart()

    pygame.display.flip()
    clock.tick(60)