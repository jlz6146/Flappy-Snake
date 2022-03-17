import pygame
from pygame.locals import *
import random
import time


class Python(pygame.sprite.Sprite):
    def __init__(self, position):
        pygame.sprite.Sprite.__init__(self)
        self.position = position
        self.fly = pygame.image.load('snak2.png')
        self.fly = pygame.transform.scale(self.fly,[120,80])
        self.normal = pygame.image.load('snak1.png')
        self.normal = pygame.transform.scale(self.normal,[120,80])
        self.k_left = self.k_right = self.k_up = self.k_down = 0
        self.image = self.normal
        self.rect = pygame.rect.Rect(self.position, self.image.get_size())

    def move(self, t0):
        self.rect.y += 5
        key_dict = pygame.key.get_pressed()
        if key_dict[K_SPACE]:
            self.image = self.fly
            self.rect.y -= 30
        else:
            self.image = self.normal

        return float(t0)

class Pipe(pygame.sprite.Sprite):
    def __init__(self, position):
        pygame.sprite.Sprite.__init__(self)

        self.image = pygame.image.load('pipe.jpg')
        self.position = position
        self.rect = pygame.rect.Rect(self.position, self.image.get_size())
        self.speed = 10

    def create_pipe(self, pipe_group):
        if not pipe_group:
            for i in range(1):
                rand_x = random.randint(width, width * 5 // 3)
                n = random.randint(-600,-300)
                pipe_group.add(Pipe((rand_x, n)))
                pipe_group.add(Pipe((rand_x, n+900)))

    def update(self):
        self.rect.x -= self.speed

class Game1():
    def gameover():
        clock = pygame.time.Clock()
        waiting = True
        while waiting:
            clock.tick(FPS)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    exit()
                elif event.type == pygame.KEYDOWN:
                    waiting = False

    def starting():
        start = pygame.image.load("snik.png")
        start = pygame.transform.scale(start,[480,700])
        screen.blit(start,(0,0))
        waiting = True
        pygame.display.update()
        while waiting:
            
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    exit()
                elif event.type == pygame.KEYDOWN:
                    waiting = False

    def main(self, screen):
        score = 0
        pygame.mixer.music.load("starting.wav")
        pygame.mixer.music.play(-1)
        Game1.starting()

        clock = pygame.time.Clock()
        python = Python((100, height / 2))
        pipe = Pipe((width, height/2))

        python_group = pygame.sprite.Group()
        python_group.add(python)

        pipe_group = pygame.sprite.Group()

        t0 = 0

        pygame.mixer.music.load("middle.wav")
        pygame.mixer.music.play(-1)

        while 1:
            t = time.time()
            clock.tick(FPS)

            pipe.create_pipe(pipe_group)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    exit()

            #bg = pygame.image.load("background.jpg")
            bg = pygame.image.load("bg.png")
            bg = pygame.transform.scale(bg,[480,700])
            screen.blit(bg,(0,0))

            t0 += (time.time()-t)
            t0 = python.move(t0)

            pipe_group.update()

            for pipe in pipe_group:
                if pipe.rect.x < -100:
                    pipe_group.remove(pipe)
                    score = score + 0.5
            font = pygame.font.SysFont(None,55)
            text = font.render("Score: " + str(int(score)),True,(0,0,0))
            screen.blit(text, [0,0])

            collision = pygame.sprite.spritecollide(python, pipe_group, False)

            if len(collision) > 0:
                score = 0
                pygame.mixer.music.load("end.wav")
                pygame.mixer.music.play(0)
                gameover = pygame.image.load('gameover.png')
                screen.blit(gameover, (0, 60))
                font = pygame.font.SysFont(None,55)
                text = font.render("press any key to restart",True,(24,50,154))
                screen.blit(text, [25,500])
                pygame.display.update()
                Game1.gameover()
                clock = pygame.time.Clock()
                python = Python((100, height / 2))
                pipe = Pipe((width, height/2))
                pygame.mixer.music.load("middle.wav")
                pygame.mixer.music.play(-1)

                python_group = pygame.sprite.Group()
                python_group.add(python)

                pipe_group = pygame.sprite.Group()

                t0 = 0
                

            screen.blit(python.image, (python.rect.x, python.rect.y))
            pipe_group.draw(screen)

            pygame.display.update()


pygame.init()

width = 480
height = 700
FPS = 30

screen = pygame.display.set_mode((width, height))
Game1().main(screen)