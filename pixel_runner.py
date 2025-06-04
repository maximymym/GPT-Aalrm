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


def main():
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Pixel Runner")
    clock = pygame.time.Clock()

    player = Player()
    ground = Platform(0, HEIGHT - 20, WIDTH, 20)
    platform1 = Platform(200, HEIGHT - 120, 120, 20)
    platforms = pygame.sprite.Group(ground, platform1)

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                player.jump()

        pressed = pygame.key.get_pressed()
        player.update(pressed, platforms)

        screen.fill((0, 0, 0))
        for p in platforms:
            screen.blit(p.image, p.rect)
        screen.blit(player.image, player.rect)
        pygame.display.flip()
        clock.tick(60)

    pygame.quit()
    sys.exit()


if __name__ == "__main__":
    main()
