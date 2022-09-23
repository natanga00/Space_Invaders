import pygame
import random
import math
from pygame import mixer

# initializing pygame
pygame.init()

# creating screen
screen_width = 800
screen_height = 600
screen = pygame.display.set_mode((screen_width, screen_height))

# caption and icon
pygame.display.set_caption("Space Invaders")

# Score
score_val = 0
score_acumulo = 1
scoreX = 5
scoreY = 5
font = pygame.font.Font('freesansbold.ttf', 20)
win_game_font = pygame.font.Font('freesansbold.ttf', 40)

# Game Over
game_over_font = pygame.font.Font('freesansbold.ttf', 64)

phase = 1
game_endend = False
enabled_explosion = True


def show_score(x, y):
    score = font.render("Points: " + str(score_val) + " - Phase: " + str(phase), True, (255, 255, 255))
    screen.blit(score, (x, y))


def game_over():
    game_over_text = game_over_font.render("GAME OVER",
                                           True, (255, 255, 255))
    screen.blit(game_over_text, (190, 250))

def won_game():
    global game_endend
    invaderImage.clear()
    invader_X.clear()
    invader_Y.clear()
    invader_Xchange.clear()
    invader_Ychange.clear()
    game_endend = True

    won_game_text = win_game_font.render("Parabéns você salvou a galáxia Anima", True, (255, 255, 255))
    screen.blit(won_game_text, (20, 300))

class Background(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.bgimage = pygame.image.load("data/" + background_image)
        self.bgY = 0
        self.bgX = 0
        self.rectBGimg = self.bgimage.get_rect()

    def render(self):
        screen.blit(self.bgimage, (self.bgX, self.bgY))


# Background Sound
mixer.music.load('data/background.wav')
mixer.music.play(-1)

# player
playerImage = pygame.image.load('data/nave.png')
player_X = 370
player_Y = 523
player_Xchange = 0

# Invader
invaderImage = []
invader_X = []
invader_Y = []
invader_Xchange = []
invader_Ychange = []
no_of_invaders = 10
image_invader = 'alien1.png'

background_image = 'bk1.png'



# Bullet
# rest - bullet is not moving
# fire - bullet is moving
bulletImage = pygame.image.load('data/bullet.png')
bullet_X = 0
bullet_Y = 500
bullet_Xchange = 0
bullet_Ychange = 12
bullet_state = "rest"
background = Background()


# Collision Concept
def isCollision(x1, x2, y1, y2):
    distance = math.sqrt((math.pow(x1 - x2, 2)) +
                         (math.pow(y1 - y2, 2)))
    if distance <= 50:
        return True
    else:
        return False


def player(x, y):
    screen.blit(playerImage, (x - 16, y + 10))


def invader(x, y, i):
    screen.blit(invaderImage[i], (x, y))


def bullet(x, y):
    global bullet_state
    screen.blit(bulletImage, (x, y))
    bullet_state = "fire"

def createNewEnemies():
    for num in range(no_of_invaders):
        invaderImage[num] = pygame.image.load('data/' + image_invader)


for num in range(no_of_invaders):
    invaderImage.append(pygame.image.load('data/' + image_invader))
    invader_X.append(random.randint(64, 737))
    invader_Y.append(random.randint(30, 180))
    invader_Xchange.append(1.2)
    invader_Ychange.append(50)

# game loop
running = True
while running:

    # RGB
    screen.fill((0, 0, 0))
    background.render()

    if score_val <= 25:
        phase = 1
    elif 26 <= score_val <= 80:
        image_invader = 'alien2.png'
        createNewEnemies()
        background_image = 'bk2.png'
        background = Background()
        background.render()
        phase = 2
    elif 81 <= score_val <= 150:
        image_invader = 'alien3.png'
        createNewEnemies()
        background_image = 'bk3.png'
        background = Background()
        background.render()
        bulletImage = pygame.image.load('data/missile.png')
        phase = 3
        score_acumulo = 4
    elif 151 <= score_val < 200:
        image_invader = 'alien4.png'
        createNewEnemies()
        background_image = 'bk4.png'
        background = Background()
        background.render()
        bulletImage = pygame.image.load('data/bullet2.png')
        phase = 4
        score_acumulo = 8
    else:
        won_game()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        # Controlling the player movement
        # from the arrow keys
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                player_Xchange = -1.7
            if event.key == pygame.K_RIGHT:
                player_Xchange = 1.7
            if event.key == pygame.K_SPACE:

                # Fixing the change of direction of bullet
                if bullet_state == "rest" and not game_endend:
                    bullet_X = player_X
                    bullet(bullet_X, bullet_Y)
                    bullet_sound = mixer.Sound('data/bullet.wav')
                    bullet_sound.play()
            if event.key == pygame.K_e:
                if (151 <= score_val < 200) and enabled_explosion:
                    explosion_galatical_sound = mixer.Sound('data/kaboom.wav')
                    explosion_galatical_sound.play()
                    enabled_explosion = False
                    score_val += 80

        if event.type == pygame.KEYUP:
            player_Xchange = 0

    if not game_endend:

        # adding the change in the player position
        player_X += player_Xchange
        for i in range(no_of_invaders):
            invader_X[i] += invader_Xchange[i]

        # bullet movement
        if bullet_Y <= 0:
            bullet_Y = 600
            bullet_state = "rest"
        if bullet_state == "fire":
            bullet(bullet_X, bullet_Y)
            bullet_Y -= bullet_Ychange

        # movement of the invader
        for i in range(no_of_invaders):

            if invader_Y[i] >= 450:
                if abs(player_X - invader_X[i]) < 80:
                    for j in range(no_of_invaders):
                        invader_Y[j] = 2000
                        explosion_sound = mixer.Sound('data/explosion.wav')
                        explosion_sound.play()
                    game_over()
                    break

            if invader_X[i] >= 735 or invader_X[i] <= 0:
                invader_Xchange[i] *= -1
                invader_Y[i] += invader_Ychange[i]
            # Collision
            collision = isCollision(bullet_X, invader_X[i],
                                    bullet_Y, invader_Y[i])
            if collision:
                score_val += score_acumulo
                bullet_Y = 600
                bullet_state = "rest"
                invader_X[i] = random.randint(64, 736)
                invader_Y[i] = random.randint(30, 200)
                invader_Xchange[i] *= -1

            invader(invader_X[i], invader_Y[i], i)

        # restricting the spaceship so that
        # it doesn't go out of screen
        if player_X <= 16:
            player_X = 16
        elif player_X >= 750:
            player_X = 750

    player(player_X, player_Y)
    show_score(scoreX, scoreY)
    pygame.display.update()