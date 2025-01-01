import sys
import pygame
import random


class Pong:
    """Larger class to manage the game."""

    """
    TODO:
    Helper functions for:
    - collisions
    - end game
    """

    def __init__(self):
        pygame.init()
        self.clock = pygame.time.Clock()
        screen_dim = (800, 600)
        self.screen = pygame.display.set_mode(screen_dim)
        pygame.display.set_caption("Pong")

        self.screen_rect = self.screen.get_rect()
        screen_center = self.screen_rect.center

        self.PADDING = 15

        self.player_bumper = pygame.Rect(self.PADDING, screen_center[1] - 50, self.PADDING, 100)
        self.enemy_bumper = pygame.Rect(800 - self.PADDING * 2, screen_center[1] - 50, self.PADDING, 100)
        self.ball = pygame.Rect(screen_center[0] - 5, screen_center[1] - 5, 10, 10)

        self.player_score = 0
        self.enemy_score = 0

        self.ball_velocity = [5,5]
        if random.randint(0, 1) == 0:
            self.ball_velocity[0] *= -1
        if random.randint(0, 1) == 0:
            self.ball_velocity[1] *= -1

        self.BASE0 = (131, 148, 150)
        self.BASE01 = (88, 110, 117)
        self.BASE03 = (0, 43, 54)

    def run_game(self):
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    sys.exit()

            self.screen.fill(self.BASE03)

            top_wall = (0, 0, 800, self.PADDING)
            pygame.draw.rect(self.screen, self.BASE0, top_wall)

            bottom_wall = (0, 600 - self.PADDING, 800, self.PADDING)
            pygame.draw.rect(self.screen, self.BASE0, bottom_wall)

            for n in range(1, 20):
                divider = (self.screen_rect.center[0] - (self.PADDING // 2), 30 * n, self.PADDING, self.PADDING)
                pygame.draw.rect(self.screen, self.BASE01, divider)

            pygame.draw.rect(self.screen, self.BASE0, self.player_bumper)
            pygame.draw.rect(self.screen, self.BASE0, self.enemy_bumper)

            keys = pygame.key.get_pressed()
            VELOCITY = 5

            if keys[pygame.K_w] and self.player_bumper.y > self.PADDING:
                self.player_bumper.y -= VELOCITY
            if keys[pygame.K_s] and self.player_bumper.y < 600 - self.PADDING - self.player_bumper.height:
                self.player_bumper.y += VELOCITY

            if keys[pygame.K_UP] and self.enemy_bumper.y > self.PADDING:
                self.enemy_bumper.y -= VELOCITY
            if keys[pygame.K_DOWN] and self.enemy_bumper.y < 600 - self.PADDING - self.enemy_bumper.height:
                self.enemy_bumper.y += VELOCITY

            if self.ball.y < 0 + self.PADDING or self.ball.y > 600 - self.PADDING * 2:
                self.ball_velocity[1] *= -1

            if self.PADDING < self.ball.x < self.PADDING * 2 and \
                    self.player_bumper.y < self.ball.y < self.player_bumper.y + 100:
                self.ball_velocity[0] = 5

            if self.ball.x + self.PADDING > 800 - self.PADDING * 2 and \
                    self.enemy_bumper.y < self.ball.y < self.enemy_bumper.y + 100:
                self.ball_velocity[0] = -5

            if self.ball.x < 0:
                self.enemy_score += 1
                self.ball.x = self.screen_rect.centerx
                self.ball.y = self.screen_rect.centery
                self.ball_velocity = [0,0]

                print("enemy scored")

            if self.ball.x > 800 - self.PADDING:
                self.player_score += 1
                self.ball.x = self.screen_rect.centerx
                self.ball.y = self.screen_rect.centery
                self.ball_velocity = [0,0]
                print("player scored")

            self.ball.x += self.ball_velocity[0]
            self.ball.y += self.ball_velocity[1]

            f = pygame.font.SysFont('IBM Plex Mono', 50)
            player_score_image = f.render(str(self.player_score), True, self.BASE0, self.BASE03)
            self.screen.blit(player_score_image, [self.screen_rect.centerx - 100, 50])

            enemy_score_image = f.render(str(self.enemy_score), True, self.BASE0, self.BASE03)
            self.screen.blit(enemy_score_image, [self.screen_rect.centerx + 65, 50])

            pygame.draw.rect(self.screen, self.BASE0, self.ball)


            pygame.display.flip()
            self.clock.tick(60)


if __name__ == "__main__":
    pong = Pong()
    pong.run_game()
