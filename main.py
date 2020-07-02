import pygame
import os
import math
import random
pygame.init()

WIDTH = 1200
HEIGHT = 700

WIN = pygame.display.set_mode((WIDTH, HEIGHT))


P1_UP = pygame.transform.scale(pygame.image.load(
    os.path.join('assets', 'player1_up.png')), (20, 50))
P1_DOWN = pygame.transform.scale(pygame.image.load(
    os.path.join('assets', 'player1_down.png')), (20, 50))
P2_UP = pygame.transform.scale(pygame.image.load(
    os.path.join('assets', 'player2_up.png')), (20, 50))
P2_DOWN = pygame.transform.scale(pygame.image.load(
    os.path.join('assets', 'player2_down.png')), (20, 50))

BALL = pygame.transform.scale(pygame.image.load(
    os.path.join('assets', 'ball.png')), (30, 30))


ICON = pygame.image.load(os.path.join('assets', 'icon.png'))
BG = pygame.transform.scale(pygame.image.load(
    os.path.join('assets', 'background.png')), (WIDTH, HEIGHT))

HIT_SOUND1 = pygame.mixer.Sound('assets/hit1.wav')
HIT_SOUND2 = pygame.mixer.Sound('assets/hit2.wav')


pygame.display.set_caption('Pong')
pygame.display.set_icon(ICON)

class Player():

    def __init__(self, x, y, img_up, img_down):
        self.x = x
        self.y = y
        self.img_up = img_up
        self.img_down = img_down
        self.mask_up = pygame.mask.from_surface(self.img_up)
        self.mask_down = pygame.mask.from_surface(self.img_down)
        self.score = 0
        self.vel = 4

    def draw(self, WIN):
        WIN.blit(self.img_up, (self.x, self.y))
        WIN.blit(self.img_down, (self.x, self.y + self.img_down.get_height()))


class Ball():
    def __init__(self, img):
        self.img = img
        self.x = WIDTH/2 - (self.img.get_width()/2)
        self.y = HEIGHT/2 - (self.img.get_height()/2)
        self.x_vel = random.choice([5,-5])
        self.y_vel = random.randrange(-5,5)
        self.mask = pygame.mask.from_surface(self.img)

    def draw(self, WIN,HEIGHT):
        if self.y <= 0 or self.y + self.img.get_height() >= HEIGHT:
            self.y_vel *= -1
        self.x += self.x_vel
        self.y += self.y_vel
        # pygame.draw.rect(WIN,(0,0,0),(self.x,self.y,50,50))
        WIN.blit(self.img, (self.x, self.y))

    def mis_vel(self):
        if self.y_vel == 0:
            self.y_vel = 1

sound_count = 0
player1 = Player(P1_UP.get_width()+30, HEIGHT/2 -P1_UP.get_height(), P1_UP, P1_DOWN)
player2 = Player(WIDTH - P2_UP.get_width() - 30, HEIGHT /2 - P2_UP.get_height(), P2_UP, P2_DOWN)
def main():
    run = True
    FPS = 60
    
    clock = pygame.time.Clock()
    ball = Ball(BALL)
    player1.vel = 4
    score_text_color1 = (56, 148, 235)
    score_text_color2 = (255, 100, 100)
    score_font = pygame.font.SysFont('arial', int(WIDTH/6), True)
    score1 = score_font.render(str(player1.score), 1, score_text_color1)
    score2 = score_font.render(str(player2.score), 1, score_text_color2)
    text_y = HEIGHT/2 - (score1.get_height()/2)
    text_x1 = WIDTH/5 - (score1.get_width()/2)
    text_x2 =WIDTH - WIDTH/5 - (score1.get_width()/2)


    def redraw_window(WIN):
        WIN.blit(BG, (0, 0))
        WIN.blit(score1,(text_x1, text_y))
        WIN.blit(score2, (text_x2, text_y))
        #pygame.draw.rect(WIN, (0, 0, 0), (0, HEIGHT/2, WIDTH, 1))
        player1.draw(WIN)
        player2.draw(WIN)
        ball.draw(WIN,HEIGHT)
        pygame.display.update()

    def collision():
        if ball.x + ball.img.get_width() >= player2.x:
            if ball.y + ball.img.get_height() >= player2.y and ball.y < player2.y + player2.img_up.get_height():
                ball.x_vel *= -1
                if ball.y_vel >= 0:
                    ball.y_vel *= -1
                    sound()
                else:
                    ball.y -= 1
                    sound()
            elif ball.y + ball.img.get_height() >= player2.y + player2.img_down.get_height() and ball.y <= player2.y + (2*player2.img_down.get_height()):
                ball.x_vel *= -1
                if ball.y_vel <= 0:
                    ball.y_vel *= -1
                    sound()
                else:
                    ball.y += 1
                    sound()



        elif ball.x == player1.x + player1.img_up.get_width():
            if ball.y + ball.img.get_height() >= player1.y and ball.y < player1.y + player1.img_up.get_height():
                ball.x_vel *= -1
                if ball.y_vel >= 0:
                    ball.y_vel *= -1
                    sound()
                else:
                    ball.y -= 1
                    sound()
            elif ball.y + ball.img.get_height() >= player1.y + player1.img_down.get_height() and ball.y <= player1.y + (2*player1.img_down.get_height()):
                ball.x_vel *= -1
                if ball.y_vel <= 0:
                    ball.y_vel *= -1
                    sound()
                else:
                    ball.y += 1
                    sound()
        ball.mis_vel()


    def sound():
        global sound_count
        sound_count += 1
        if sound_count % 2 == 0:
            HIT_SOUND1.play()
            
        else:
            HIT_SOUND2.play()
            
        
    def point():
        if ball.x <= 0:
            player2.score += 1
            print(player2.score)
            run = False
            main()
        if ball.x + ball.img.get_width() >= WIDTH:
            player1.score += 1
            print(player1.score)
            run = False
            main()

    def controls():
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                quit()

        if keys[pygame.K_w] and player1.y > 10:
            player1.y -= player1.vel
        if keys[pygame.K_s] and player1.y + (2 * player1.img_down.get_height()) < HEIGHT - 10:
            player1.y += player1.vel

        if keys[pygame.K_UP] and player2.y > 10:
            player2.y -= player1.vel
        if keys[pygame.K_DOWN] and player2.y + (2 * player2.img_down.get_height()) < HEIGHT - 10:
            player2.y += player1.vel
        if keys[pygame.K_r]:
            player1.score = 0
            player2.score = 0
            run = False
            main()

    while run:
        clock.tick(FPS)
        keys = pygame.key.get_pressed()
        point()
        collision()
        controls()
        redraw_window(WIN)


main()
