import pygame, random

pygame.init()

WIDTH, HEIGHT = 800, 400

# Here we define the constants for the colors
OBJECT_COLOR = 83, 83, 83
BG_COLOR = 247, 247, 247

# Here we define some constants for the differents sounds
JUMP_SOUND = pygame.mixer.Sound('audio/Jump.wav')
DIE_SOUND = pygame.mixer.Sound('audio/Die.wav')
POINT_SOUND = pygame.mixer.Sound('audio/Point.wav')

INIT_VEL = 7
GROUND_POS = HEIGHT - 160

score = 0
press_enter_counter = 0
press_enter_time = 20

die_sound = True
draw_bird = False
init_game = True
stop_game = False

display = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('Dino')

clock = pygame.time.Clock()

font = pygame.font.Font("font\ARCADEPI.TTF", 22)


class Background:
    def __init__(self, y, vel, img, width = None):
        self.WIDTH = img.get_width()
        self.IMG = img

        if width:
            self.WIDTH = width

        self.y = y
        self.x1 = 0
        self.x2 = self.WIDTH
        self.vel = vel

    def move(self):
        self.x1 -= self.vel
        self.x2 -= self.vel

        if self.x1 + self.WIDTH < 0:
            self.x1 = self.WIDTH

        if self.x2 + self.WIDTH < 0:
            self.x2 = self.WIDTH

    def draw(self, win):
        win.blit(self.IMG, (self.x1, self.y))
        win.blit(self.IMG, (self.x2, self.y))

class Dino:
    def __init__(self, x, y, imgs, sound):
        self.JUMP_SOUND = sound
        self.IMG_COUNTER = 5
        self.JUMP_COUNT = 10
        self.Y = y
        
        self.imgs = imgs
        self.img = self.imgs[0]
        self.jump_count = 10

        self.x = x
        self.y = y
        self.counter = 0
        self.is_jumping = False

    def run(self):
        self.counter += 1

        if self.counter <= self.IMG_COUNTER:
            self.img = self.imgs[0]

        elif self.counter <= self.IMG_COUNTER * 2:
            self.img = self.imgs[1]

        elif self.counter == self.IMG_COUNTER * 3 + 1:
            self.counter = 0

    def jump(self):
        self.img = self.imgs[2]

        if self.y == self.Y:
            pygame.mixer.Sound.play(self.JUMP_SOUND)

        if self.is_jumping:
            self.y -= self.jump_count * 2
            self.jump_count -= .6

        if self.jump_count <= -self.JUMP_COUNT:
            self.is_jumping = False
            self.jump_count = self.JUMP_COUNT

        if not self.is_jumping:
            self.y = self.Y
            self.is_jumping = False

    def get_mask(self):
        return pygame.mask.from_surface(self.img)

    def draw(self, win):
        win.blit(self.img, (self.x, self.y))

class Obstacle:
    def __init__(self, y, vel, img):
        self.img = img

        self.y = y
        self.x = WIDTH
        self.vel = vel

    def collision(self, dino):
        dino_mask = dino.get_mask()
        obstacle_mask = pygame.mask.from_surface(self.img)

        offset = (int(dino.x - self.x), int(dino.y - self.y))

        collision = obstacle_mask.overlap(dino_mask, offset)
        
        return collision

    def draw(self, win):
        win.blit(self.img, (self.x, self.y))

class Cactus(Obstacle):
    def __init__(self, y, vel, imgs):
        self.imgs = imgs
        self.index = 0

        super().__init__(y, vel, imgs[self.index])

        print(GROUND_POS - self.img.get_height())

    def move(self, bird):
        self.x -= self.vel

        if self.x + self.img.get_width() < 0:
            self.index = random.randint(0, len(self.imgs) - 1)
            self.img = self.imgs[self.index]

            self.x = WIDTH + 100 + bird.x
            self.y = HEIGHT - self.imgs[self.index].get_height() - 65

class Bird(Obstacle):
    def __init__(self, y, y_pos, vel, imgs):
        self.IMG_COUNTER = 10

        self.imgs = imgs
        self.index = 0
        self.counter = 0

        super().__init__(y, vel, imgs[self.index])
        
        self.x = 0
        self.y_pos = y_pos # It's a list containing the differents "y" positions the bird can have
        self.y_copy = y

    def move(self):
        global draw_bird

        self.x -= self.vel
        self.counter += 1

        if self.counter <= self.IMG_COUNTER:
            self.index = 0
            self.y = self.y_copy

        elif self.counter <= self.IMG_COUNTER * 2:
            self.index = 1
            self.y = self.y_copy - 13

        elif self.counter <= self.IMG_COUNTER * 3 + 1:
            self.counter = 0
        
        if self.x + self.img.get_width() < 0:
            self.x = 0
            self.y_copy = self.y = random.choice(self.y_pos)

            draw_bird = False

        self.img = self.imgs[self.index]

def draw_all(win, track, dino, cloud, cactus, bird):
    track.draw(win)
    dino.draw(win)
    cloud.draw(win)
    cactus.draw(win)

    if draw_bird:
        bird.draw(win)

DINO_IMGS = [pygame.image.load('imgs/DinoRun1.png'), pygame.image.load('imgs/DinoRun2.png'), pygame.image.load('imgs/DinoJump.png')]
dino = Dino(50, GROUND_POS, DINO_IMGS, JUMP_SOUND)

TRACK_IMG = pygame.image.load('imgs/Track.png')
track = Background(HEIGHT - 100, INIT_VEL, TRACK_IMG)

CLOUD_IMG = pygame.image.load('imgs/Cloud.png')
cloud = Background(40, 2, CLOUD_IMG, WIDTH)

CACTUS_IMGS = [pygame.image.load('imgs/LCactus1.png'), pygame.image.load('imgs/LCactus2.png'), pygame.image.load('imgs/LCactus3.png'), pygame.image.load('imgs/SCactus1.png'), pygame.image.load('imgs/SCactus2.png'), pygame.image.load('imgs/SCactus3.png')]
cactus = Cactus(GROUND_POS, INIT_VEL, CACTUS_IMGS)

BIRD_IMGS = [pygame.image.load('imgs/Bird1.png'), pygame.image.load('imgs/Bird2.png')]
BIRD_POS = [GROUND_POS, GROUND_POS - BIRD_IMGS[0].get_height() - 10]
bird = Bird(BIRD_POS[0], BIRD_POS, INIT_VEL, BIRD_IMGS)

RESETBT_IMG = pygame.image.load('imgs/Reset.png')
GAMEOVER_IMG = pygame.image.load('imgs/GameOver.png')
PRESSENTER_IMG = pygame.image.load('imgs/PressEnter.png')

while True:
    display.fill(BG_COLOR)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            exit()

    # We enter if we have just initialize the game
    if init_game:
        press_enter_counter += 1

        if press_enter_counter <= press_enter_time:
            display.blit(PRESSENTER_IMG, (
                WIDTH / 2 - PRESSENTER_IMG.get_width() / 2,
                HEIGHT / 2 - PRESSENTER_IMG.get_height() / 2 - 60
            ))
            
        elif press_enter_time * 2 < press_enter_counter <= press_enter_time * 3 + 1:
            press_enter_counter = 0

        keys = pygame.key.get_pressed()

        # We start the game when the user press those keys
        if keys[pygame.K_SPACE] or keys[pygame.K_UP] or keys[pygame.K_RETURN]:
            init_game = False

        track.move()
        cloud.move()
        dino.run()

    else:
        txt_render = font.render("Score: " + str(int(score)), True, OBJECT_COLOR)

        display.blit(txt_render, (
            WIDTH - txt_render.get_width() - 20,
            txt_render.get_height() - 10
        ))

        if not stop_game:
            keys = pygame.key.get_pressed()
            if keys[pygame.K_UP] or keys[pygame.K_SPACE]:
                dino.is_jumping = True

            if not dino.is_jumping:
                dino.run()

            else:
                dino.jump()

            score += .2

            if int(score) != 0:
                if int(score) % 100 == 0:
                    pygame.mixer.Sound.play(POINT_SOUND)

                if int(score) % 500 == 0:
                    bird.x = WIDTH + 100 + cactus.x
                    draw_bird = True

            cactus.move(bird)
            track.move()
            cloud.move()

            if draw_bird:
                bird.move()

            if cactus.vel <= 26:
                cactus.vel += .002
                track.vel += .002
                bird.vel += .002

        else:
            if pygame.mouse.get_pressed()[0]:
                x_reset_button = WIDTH / 2 - RESETBT_IMG.get_width() / 2
                y_reset_button = HEIGHT / 2 - RESETBT_IMG.get_height() / 2

                if x_reset_button < pygame.mouse.get_pos()[0] < x_reset_button + RESETBT_IMG.get_width():
                    if y_reset_button < pygame.mouse.get_pos()[1] < y_reset_button + RESETBT_IMG.get_width():
                        track.x1, track.x2 = 0, track.WIDTH
                        cloud.x1, cloud.x2 = 0, cloud.WIDTH

                        cactus.x = WIDTH
                        cactus.vel = track.vel = INIT_VEL

                        score = 0
                        stop_game = False
                        die_sound = True

        if cactus.collision(dino) or (bird.collision(dino) and draw_bird):
            if die_sound:
                pygame.mixer.Sound.play(DIE_SOUND)
                die_sound = False

            display.blit(RESETBT_IMG, (
                WIDTH / 2 - RESETBT_IMG.get_width() / 2,
                HEIGHT / 2 - RESETBT_IMG.get_height() / 2
            ))

            display.blit(GAMEOVER_IMG, (
                WIDTH / 2 - GAMEOVER_IMG.get_width() / 2,
                HEIGHT / 2 - GAMEOVER_IMG.get_height() / 2 - RESETBT_IMG.get_height()
            ))

            stop_game = True

    draw_all(display, track, dino, cloud, cactus, bird)

    pygame.display.flip()
    clock.tick(60)
