import sys
import pygame


class Pong:
    """Larger class to manage the game."""

    def __init__(self):
        pygame.init()
        self.clock = pygame.time.Clock()
        screen_dim = (800, 600)
        self.screen = pygame.display.set_mode(screen_dim)
        pygame.display.set_caption("Pong")

        self.screen_rect = self.screen.get_rect()
        screen_center = self.screen_rect.center

        self.player_bumper = pygame.Rect(20, screen_center[1] - 50, 15, 100)
        self.base0 = (131, 148, 150)

    def run_game(self):
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    sys.exit()

            base03 = (0, 43, 54)
            self.screen.fill(base03)

            pygame.draw.rect(self.screen, self.base0, self.player_bumper)

            keys = pygame.key.get_pressed()

            if keys[pygame.K_UP]:
                self.player_bumper.y -= 5
            if keys[pygame.K_DOWN]:
                self.player_bumper.y += 5

            pygame.display.flip()
            self.clock.tick(60)


if __name__ == "__main__":
    pong = Pong()
    pong.run_game()
