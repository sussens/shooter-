from pygame import *
from random import randint, choice
win_width = 700
win_height = 500
window = display.set_mode((win_width, win_height))
display.set_caption('Шутер')
background = transform.scale(image.load('galaxy.jpg'), (win_width, win_height))
mixer.init()
mixer.music.load('space.ogg')
mixer.music.play()
mixer.music.set_volume(0.5)
clock = time.Clock()
FPS = 60
counter = 0


class GameSprite(sprite.Sprite):
    def __init__(self, player_image, player_x, player_y, player_speed, player_width, player_height):
        super().__init__()
        self.image = transform.scale(image.load(player_image), (player_width, player_height))
        self.speed = player_speed
        self.rect = self.image.get_rect()
        self.rect.x = player_x
        self.rect.y = player_y
    def reset(self):
        window.blit(self.image, (self.rect.x, self.rect.y))
class Player(GameSprite):
    def update(self):
        keys = key.get_pressed()
        if keys[K_LEFT] and self.rect.x >= 0:
            self.rect.x -= self.speed
        if keys[K_RIGHT] and self.rect.x <= 630:
            self.rect.x += self.speed
        if keys[K_SPACE]:
            self.fire()
    def fire(self):
        bullet = Bullet('bullet.png', self.rect.centerx, self.rect.top ,20, 15, 20)
        bullets.add(bullet)
player = Player('rocket.png', 200, 400, 10, 50, 70)
monsters = sprite.Group()
bullets = sprite.Group()

class Enemy(GameSprite):
    def update(self):
        global lost
        self.rect.y += self.speed
        if self.rect.y >= 420:
            self.rect.y = 0
            self.rect.x = randint(0, 610)
            lost += 1

class Bullet(GameSprite):
    def update(self):
        self.rect.y -= self.speed
        if self.rect.y <= 0:
            self.kill()
font.init()
font1 = font.SysFont('Arial', 36)

for i in range(5):
    monster = Enemy(choice(['asteroid.png', 'ufo.png']), randint(0, 610), -10, randint(2, 4), 80, 45)
    monsters.add(monster)
lost = 0
game = True
finish = False
while game == True:
    for e in event.get():
        if e.type == QUIT:
            game = False
    if counter >= 50:
            imagewin = transform.scale(image.load('4d9bd02d718c4909b69b2618e707f0e0.png'), (700, 500))
            window.blit(imagewin, (0, 0))
            finish = True
        
    if lost >= 10:
        imagelost = transform.scale(image.load("Без названия.png"), (700, 500))
        window.blit(imagelost, (0, 0))
        finish = True
    if finish == False:

        sprites_list = sprite.spritecollide(player, monsters, False)
        sprites_list1 = sprite.groupcollide(monsters, bullets, True, True)
        for i in sprites_list1:
            counter += 1
            monster = Enemy(choice(['asteroid.png', 'ufo.png']), randint(0, 610), -10, randint(2, 4), 80, 45)
            monsters.add(monster)
        window.blit(background, (0, 0))
        player.update()
        player.reset()
        monsters.draw(window)
        monsters.update()
        bullets.draw(window)
        bullets.update()
        text_lose = font1.render('Пропущено: ' + str(lost), 1, (255, 255, 255))
        text_counter = font1.render('Счёт: ' + str(counter), 1, (255, 255 ,255))
        window.blit(text_lose, (10, 10))
        window.blit(text_counter, (10, 50))
    display.update()
    clock.tick(FPS)     
