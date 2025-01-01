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
        self.enemy_bumper = pygame.Rect(780, screen_center[1] - 50, 15, 100)
        self.base0 = (131, 148, 150)
        self.base01 = (88, 110, 117)

    def run_game(self):
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    sys.exit()

            base03 = (0, 43, 54)
            self.screen.fill(base03)

            top_wall = (0, 0, 800, 15)
            pygame.draw.rect(self.screen, self.base0, top_wall)

            bottom_wall = (0, 585, 800, 15)
            pygame.draw.rect(self.screen, self.base0, bottom_wall)

            for n in range(1, 20):
                divider = (self.screen_rect.center[0] - 15, 30 * n, 15, 15)
                pygame.draw.rect(self.screen, self.base01, divider)

            pygame.draw.rect(self.screen, self.base0, self.player_bumper)
            pygame.draw.rect(self.screen, self.base0, self.enemy_bumper)

            keys = pygame.key.get_pressed()

            if keys[pygame.K_w]:
                self.player_bumper.y -= 5
            if keys[pygame.K_s]:
                self.player_bumper.y += 5

            if keys[pygame.K_UP]:
                self.enemy_bumper.y -= 5
            if keys[pygame.K_DOWN]:
                self.enemy_bumper.y += 5

            pygame.display.flip()
            self.clock.tick(60)


if __name__ == "__main__":
    pong = Pong()
    pong.run_game()
