from random import randint
from pygame import *
from time import sleep
win_width = 700
win_height = 500
window = display.set_mode((700, 500))
display.set_caption("Shooter")
background = transform.scale(image.load("galaxy.jpg"), (700, 500))
mixer.init()
clock = time.Clock()
FPS = 60


class GameSprite(sprite.Sprite):
    def __init__(self, player_image, player_x, player_y, player_speed, w=65, h=65):
        super().__init__()
        self.image = transform.scale(image.load(player_image), (w, h))
        self.speed = player_speed
        self.rect = self.image.get_rect()
        self.rect.x = player_x
        self.rect.y = player_y

    def reset(self):
        window.blit(self.image, (self.rect.x, self.rect.y))


class Player(GameSprite):
    def update(self):
        keys = key.get_pressed()
        if keys[K_LEFT] and self.rect.x > 0:
            self.rect.x -= self.speed
        if keys[K_RIGHT] and self.rect.x < win_width - 70:
            self.rect.x += self.speed

    def fire(self):
        bullet = Bullet("bullet.png", self.rect.centerx, self.rect.top, 10, w=30, h=40)
        bullets.add(bullet)


class Bullet(GameSprite):
    def update(self):
        self.rect.y -= self.speed
        if self.rect.y < 0:
            self.kill()


lost = 0
score = 0


class Enemy(GameSprite):
    def update(self):
        global lost
        self.rect.y += self.speed
        if self.rect.y > win_height:
            self.rect.x = randint(80, win_width - 80)
            self.rect.y = 0
            lost = lost + 1


font.init()
font1 = font.SysFont("Arial", 40)
font2 = font.SysFont("Arial",80)

player = Player("rocket.png", 300, 430, 10)
monsters = sprite.Group()
bullets = sprite.Group()

asteroids = sprite.Group()

def start_game():
    global player, monsters, bullets, lost, score, finish, result_text
    global num_fire, reload, reload_start_time


    lost = 0
    score = 0
    finish = False
    result_text = font1.render("", True, (255, 255, 255))

    num_fire = 0
    reload = False
    reload_start_time = 0

    player.rect.x = 300
    player.rect.y = 430

    bullets.empty()
    monsters.empty()
    asteroids.empty()

    for i in range(5):
        enemy = Enemy("ufo.png", randint(0, win_width - 65), randint(-150, -40), 2)
        monsters.add(enemy)

    for i in range(3):
        asteroid = Enemy("car.png", randint(0, win_width - 65), randint(-150, -40), 2)
        asteroids.add(asteroid)


start_game()

game = True
while game:
    window.blit(background, (0, 0))

    for e in event.get():
        if e.type == QUIT:
            game = False

        if e.type == KEYDOWN:
            if e.key == K_SPACE and not finish and not reload:
                mixer.music.load("fire.ogg")
                mixer.music.play()
                player.fire()
                num_fire += 1
                if num_fire >= 5:
                    reload = True
                    reload_start_time = time.get_ticks()
            if e.key == K_r:
                start_game()

    if not finish:
        player.update()
        monsters.update()
        bullets.update()
        asteroids.update()

        if reload:
            now_time = time.get_ticks()
            if now_time - reload_start_time >= 4000:
                reload = False
                num_fire = 0

        hits_monsters = sprite.groupcollide(monsters, bullets, True, True)
        for i in hits_monsters:
            score += 1
            enemy = Enemy("ufo.png", randint(0, win_width - 65), randint(-150, -40), 2)
            monsters.add(enemy)

        if sprite.spritecollide(player, monsters, True) or sprite.spritecollide(player, asteroids, True):
            finish = True
            result_text = font2.render("You Lose", True, (222, 24, 24))

        if score >= 10:
            finish = True
            result_text = font2.render("You Win", True, (43,143,43))
        elif lost > 10:
            finish = True
            result_text = font2.render("You Lose", True, (222, 24, 24))

        player.reset()
        monsters.draw(window)
        bullets.draw(window)
        asteroids.draw(window)

        text_score = font1.render("Destroyed: " + str(score), True, (255, 255, 255))
        text_lose = font1.render("Missed: " + str(lost), True, (255, 255, 255))
        window.blit(text_score, (10, 10))
        window.blit(text_lose, (10, 40))

    if finish:
        window.blit(result_text, (win_width // 2-100, win_height // 2-50))
        restart_text = font1.render("Press R to restart", True, (255, 255, 255))
        window.blit(restart_text, (win_width // 2 - 110, win_height // 2 + 40))
    if reload:
        text_reload = font1.render("Reloading...", True, (255, 0, 0))
        window.blit(text_reload, (280, 450))

    clock.tick(FPS)
    display.update()
