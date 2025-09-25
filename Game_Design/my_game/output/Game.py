import pygame

class Paddle:
    def __init__(self, x, y, width, height, speed):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.speed = speed

    def move_left(self):
        self.x -= self.speed

    def move_right(self):
        self.x += self.speed

    def draw(self, screen):
        pygame.draw.rect(screen, (0, 0, 255), (self.x, self.y, self.width, self.height))


class Ball:
    def __init__(self, x, y, radius, speed_x, speed_y):
        self.x = x
        self.y = y
        self.radius = radius
        self.speed_x = speed_x
        self.speed_y = speed_y

    def move(self):
        self.x += self.speed_x
        self.y += self.speed_y

    def draw(self, screen):
        pygame.draw.circle(screen, (255, 0, 0), (self.x, self.y), self.radius)

    def bounce_x(self):
        self.speed_x *= -1

    def bounce_y(self):
        self.speed_y *= -1

class Obstacle:
    def __init__(self, x, y, width, height):
        self.x = x
        self.y = y
        self.width = width
        self.height = height

    def draw(self, screen):
        pygame.draw.rect(screen, (0, 255, 0), (self.x, self.y, self.width, self.height))


class Game:
    def __init__(self, width=800, height=600):
        pygame.init()
        self.screen_width = width
        self.screen_height = height
        self.screen = pygame.display.set_mode((self.screen_width, self.screen_height))
        pygame.display.set_caption("Bouncing Ball")

        paddle_width = 100
        paddle_height = 15
        paddle_x = (self.screen_width - paddle_width) // 2
        paddle_y = self.screen_height - paddle_height - 10
        paddle_speed = 5
        self.paddle = Paddle(paddle_x, paddle_y, paddle_width, paddle_height, paddle_speed)

        ball_radius = 10
        ball_x = self.screen_width // 2
        ball_y = self.screen_height // 2
        ball_speed_x = 3
        ball_speed_y = 3
        self.ball = Ball(ball_x, ball_y, ball_radius, ball_speed_x, ball_speed_y)

        self.score = 0
        self.game_over = False
        self.font = pygame.font.Font(None, 36)
        self.paused = False
        self.clock = pygame.time.Clock()

        self.obstacles = [
            Obstacle(100, 150, 50, 20),
            Obstacle(300, 250, 75, 20),
            Obstacle(500, 100, 60, 20)
        ]

        self.start_game = False  # Flag to indicate if the game has started

    def run(self):
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_p:
                        self.paused = not self.paused
                    if event.key == pygame.K_SPACE and not self.start_game:
                        self.start_game = True
                        self.reset()

            if self.start_game:
                if not self.paused and not self.game_over:
                    self.handle_input()
                    self.update()
                    self.render(self.screen)
                elif self.paused:
                    self.display_pause_screen(self.screen)
                elif self.game_over:
                    self.game_over_screen(self.screen)
            else:
                self.display_start_screen(self.screen)

            pygame.display.flip()
            self.clock.tick(60)

        pygame.quit()

    def handle_input(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            self.paddle.move_left()
            if self.paddle.x < 0:
                self.paddle.x = 0
        if keys[pygame.K_RIGHT]:
            self.paddle.move_right()
            if self.paddle.x > self.screen_width - self.paddle.width:
                self.paddle.x = self.screen_width - self.paddle.width

    def update(self):
        self.ball.move()
        self.check_collision()

        if self.ball.y > self.screen_height:
            self.game_over = True

    def render(self, screen):
        screen.fill((0, 0, 0))
        self.paddle.draw(screen)
        self.ball.draw(screen)

        for obstacle in self.obstacles:
            obstacle.draw(screen)

        score_text = self.font.render(f"Score: {self.score}", True, (255, 255, 255))
        screen.blit(score_text, (10, 10))

    def check_collision(self):
        # Ball and Paddle collision
        if (self.ball.x + self.ball.radius > self.paddle.x and
            self.ball.x - self.ball.radius < self.paddle.x + self.paddle.width and
            self.ball.y + self.ball.radius > self.paddle.y and
            self.ball.y - self.ball.radius < self.paddle.y + self.paddle.height):
            self.ball.bounce_y()
            self.score += 10

        # Ball and Walls collision
        if self.ball.x - self.ball.radius < 0 or self.ball.x + self.ball.radius > self.screen_width:
            self.ball.bounce_x()
        if self.ball.y - self.ball.radius < 0:
            self.ball.bounce_y()

        # Ball and Obstacles collision
        for obstacle in self.obstacles:
            if (self.ball.x + self.ball.radius > obstacle.x and
                self.ball.x - self.ball.radius < obstacle.x + obstacle.width and
                self.ball.y + self.ball.radius > obstacle.y and
                self.ball.y - self.ball.radius < obstacle.y + obstacle.height):
                self.ball.bounce_y()
                self.score += 20 # More points for obstacle bounce

    def game_over_screen(self, screen):
          screen.fill((0, 0, 0))
          game_over_text = self.font.render("Game Over", True, (255, 255, 255))
          score_text = self.font.render(f"Final Score: {self.score}", True, (255, 255, 255))
          #restart_text = self.font.render("Press SPACE to Restart", True, (255,255,255))


          game_over_rect = game_over_text.get_rect(center=(self.screen_width // 2, self.screen_height // 2 - 50))
          score_rect = score_text.get_rect(center=(self.screen_width // 2, self.screen_height // 2))
          #restart_rect = restart_text.get_rect(center=(self.screen_width // 2, self.screen_height // 2 + 50))

          screen.blit(game_over_text, game_over_rect)
          screen.blit(score_text, score_rect)
          #screen.blit(restart_text, restart_rect)

    def display_pause_screen(self, screen):
        pause_text = self.font.render("Paused", True, (255, 255, 255))
        pause_rect = pause_text.get_rect(center=(self.screen_width // 2, self.screen_height // 2))
        screen.blit(pause_text, pause_rect)

    def display_start_screen(self, screen):
        screen.fill((0, 0, 0))
        start_text = self.font.render("Press SPACE to Start", True, (255, 255, 255))
        start_rect = start_text.get_rect(center=(self.screen_width // 2, self.screen_height // 2))
        screen.blit(start_text, start_rect)

    def reset(self):
        self.score = 0
        self.game_over = False
        self.ball.x = self.screen_width // 2
        self.ball.y = self.screen_height // 2
        self.ball.speed_x = 3
        self.ball.speed_y = 3
        paddle_width = 100
        paddle_x = (self.screen_width - paddle_width) // 2
        self.paddle.x = paddle_x


if __name__ == "__main__":
    game = Game()
    game.run()