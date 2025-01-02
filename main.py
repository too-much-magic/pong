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

        self.ball_velocity = [0,0]
        self.start_game()

        self.bumper_hit_sound = pygame.mixer.Sound("sounds/bumper_hit.wav")
        self.wall_hit_sound = pygame.mixer.Sound("sounds/wall_hit.wav")
        self.game_over_sound = pygame.mixer.Sound("sounds/game_over.wav")

        self.AI_mode = True
        self.direction = "DOWN"
        self.game_over_state = False

        self.BASE0 = (131, 148, 150)
        self.BASE01 = (88, 110, 117)
        self.BASE02  = (7, 54, 66)
        self.BASE03 = (0, 43, 54)

    def game_over(self, enemy_won: bool):
        self.ball.x = self.screen_rect.centerx
        self.ball.y = self.screen_rect.centery
        self.ball_velocity = [0, 0]
        pygame.mixer.Sound.play(self.game_over_sound)
        if enemy_won:
            self.enemy_score += 1
        else:
            self.player_score += 1
        self.game_over_state = True

    def start_game(self):
        self.ball_velocity = [5,5]
        if random.randint(0, 1) == 0:
            self.ball_velocity[0] *= -1
        if random.randint(0, 1) == 0:
            self.ball_velocity[1] *= -1

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

            if not self.AI_mode:
                if keys[pygame.K_UP] and self.enemy_bumper.y > self.PADDING:
                    self.enemy_bumper.y -= VELOCITY
                if keys[pygame.K_DOWN] and self.enemy_bumper.y < 600 - self.PADDING - self.enemy_bumper.height:
                    self.enemy_bumper.y += VELOCITY

            elif not self.game_over_state:
                if self.direction == "DOWN":
                    self.enemy_bumper.y += VELOCITY

                if self.direction == "UP":
                    self.enemy_bumper.y -= VELOCITY

                if self.enemy_bumper.y > self.PADDING and self.enemy_bumper.y + 50 > self.ball.y \
                        and pygame.time.get_ticks() % 500 > 150:
                    self.direction = "UP"

                if self.enemy_bumper.y < 600 - self.PADDING - self.enemy_bumper.height and self.enemy_bumper.y + 50 < self.ball.y \
                        and pygame.time.get_ticks() % 500 > 150:
                    self.direction = "DOWN"

            if self.ball.y < 0 + self.PADDING or self.ball.y > 600 - self.PADDING * 2:
                self.ball_velocity[1] *= -1
                pygame.mixer.Sound.play(self.wall_hit_sound)

            if self.PADDING < self.ball.x < self.PADDING * 2 and \
                    self.player_bumper.y < self.ball.y < self.player_bumper.y + 100:
                self.ball_velocity[0] = 5
                pygame.mixer.Sound.play(self.bumper_hit_sound)

            if self.ball.x + self.PADDING > 800 - self.PADDING * 2 and \
                    self.enemy_bumper.y < self.ball.y < self.enemy_bumper.y + 100:
                self.ball_velocity[0] = -5
                pygame.mixer.Sound.play(self.bumper_hit_sound)


            if self.ball.x < 0:
                self.game_over(enemy_won=True)

            if self.ball.x > 800 - self.PADDING:
                self.game_over(enemy_won=False)

            self.ball.x += self.ball_velocity[0]
            self.ball.y += self.ball_velocity[1]

            f = pygame.font.Font('fonts/IBMPlexMono-Text.ttf', 50)
            player_score_image = f.render(str(self.player_score), True, self.BASE0, self.BASE03)
            self.screen.blit(player_score_image, [self.screen_rect.centerx - 100, 50])

            enemy_score_image = f.render(str(self.enemy_score), True, self.BASE0, self.BASE03)
            self.screen.blit(enemy_score_image, [self.screen_rect.centerx + 65, 50])

            pygame.draw.rect(self.screen, self.BASE0, self.ball)

            if self.game_over_state:
                game_over_screen_width = 400
                game_over_screen_height = 100
                game_over_screen = pygame.Rect(self.screen_rect.centerx - game_over_screen_width // 2,
                                               self.screen_rect.centery - game_over_screen_height // 2,
                                               game_over_screen_width,
                                               game_over_screen_height)

                f = pygame.font.Font('fonts/IBMPlexMono-Text.ttf', 30)
                pygame.draw.rect(self.screen, self.BASE02, game_over_screen)
                play_again_image = f.render("Play again?", True, self.BASE0, self.BASE02)
                self.screen.blit(play_again_image, [game_over_screen.x + self.PADDING, game_over_screen.y])
                play_again_options = f.render("[y] yes, [n] no", True, self.BASE0, self.BASE02)
                self.screen.blit(play_again_options, [game_over_screen.x + self.PADDING, game_over_screen.y + 45])

                if keys[pygame.K_n]:
                    quit(0)
                if keys[pygame.K_y]:
                    self.game_over_state = False
                    self.start_game()

            pygame.display.flip()
            self.clock.tick(60)


if __name__ == "__main__":
    pong = Pong()
    pong.run_game()
