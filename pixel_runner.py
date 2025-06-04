import pygame
import sys

WIDTH, HEIGHT = 640, 480
GRAVITY = 0.5

class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.Surface((20, 20))
        self.image.fill((255, 0, 0))
        self.rect = self.image.get_rect()
        self.rect.x = 50
        self.rect.bottom = HEIGHT - 40
        self.vel_y = 0

    def update(self, pressed, platforms):
        if pressed[pygame.K_LEFT]:
            self.rect.x -= 3
        if pressed[pygame.K_RIGHT]:
            self.rect.x += 3

        self.vel_y += GRAVITY
        self.rect.y += self.vel_y

        for platform in platforms:
            if self.rect.colliderect(platform.rect) and self.vel_y >= 0:
                self.rect.bottom = platform.rect.top
                self.vel_y = 0

        if self.rect.left < 0:
            self.rect.left = 0
        if self.rect.right > WIDTH:
            self.rect.right = WIDTH

    def jump(self):
        if self.vel_y == 0:
            self.vel_y = -10

class Platform(pygame.sprite.Sprite):
    def __init__(self, x, y, w, h):
        super().__init__()
        self.image = pygame.Surface((w, h))
        self.image.fill((0, 255, 0))
        self.rect = self.image.get_rect(topleft=(x, y))

class Goal(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.Surface((20, 20))
        self.image.fill((0, 0, 255))
        self.rect = self.image.get_rect(topleft=(x, y))

def draw_text_center(screen, text, font):
    lines = text.split('\n')
    for i, line in enumerate(lines):
        img = font.render(line, True, (255, 255, 255))
        rect = img.get_rect(center=(WIDTH // 2, HEIGHT // 2 + i * 30))
        screen.blit(img, rect)

def build_level(defn):
    plats = pygame.sprite.Group()
    for spec in defn['platforms']:
        plats.add(Platform(*spec))
    goal = Goal(*defn['goal'])
    return plats, goal

def main():
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption('Pixel Runner')
    font = pygame.font.Font(None, 32)
    clock = pygame.time.Clock()

    levels = [
        {
            'platforms': [
                (0, HEIGHT - 20, WIDTH, 20),
                (200, HEIGHT - 120, 120, 20)
            ],
            'goal': (WIDTH - 40, HEIGHT - 40),
            'complete': 'You found the first crystal!'
        },
        {
            'platforms': [
                (0, HEIGHT - 20, WIDTH, 20),
                (150, HEIGHT - 160, 80, 20),
                (350, HEIGHT - 200, 120, 20)
            ],
            'goal': (20, 40),
            'complete': 'You recovered all the color!'
        }
    ]
    intro = (
        'Pixel Runner\n\n'
        'The sorcerer has stolen all the color.\n'
        'Collect the blue crystals to restore it.\n'
        'Press any key to start.'
    )

    state = 'intro'
    level_index = 0
    player = Player()
    platforms, goal = build_level(levels[level_index])

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if state == 'intro' and event.type == pygame.KEYDOWN:
                state = 'playing'
            elif state == 'level_complete' and event.type == pygame.KEYDOWN:
                level_index += 1
                if level_index >= len(levels):
                    state = 'game_complete'
                else:
                    platforms, goal = build_level(levels[level_index])
                    player.rect.x = 50
                    player.rect.bottom = HEIGHT - 40
                    player.vel_y = 0
                    state = 'playing'
            elif state == 'game_complete' and event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                running = False
            elif state == 'playing' and event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                player.jump()

        screen.fill((0, 0, 0))
        if state == 'intro':
            draw_text_center(screen, intro, font)
        elif state == 'playing':
            pressed = pygame.key.get_pressed()
            player.update(pressed, platforms)
            for p in platforms:
                screen.blit(p.image, p.rect)
            screen.blit(goal.image, goal.rect)
            screen.blit(player.image, player.rect)
            if player.rect.colliderect(goal.rect):
                state = 'level_complete'
        elif state == 'level_complete':
            msg = levels[level_index]['complete'] + '\nPress any key to continue.'
            draw_text_center(screen, msg, font)
        elif state == 'game_complete':
            draw_text_center(
                screen,
                'Congratulations!\nYou saved the world.\nPress ESC to quit.',
                font
            )
        pygame.display.flip()
        clock.tick(60)

    pygame.quit()
    sys.exit()

if __name__ == '__main__':
    main()
