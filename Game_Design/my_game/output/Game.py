
import pygame
import random

# Define some colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)


class Game:
    def __init__(self, width, height, cell_size):
        """
        Initializes the game environment.
        :param width: Width of the game board in cells.
        :param height: Height of the game board in cells.
        """
        pygame.init()
        self.width = width
        self.height = height
        self.cell_size = cell_size
        self.screen_width = width * cell_size
        self.screen_height = height * cell_size
        self.screen = pygame.display.set_mode((self.screen_width, self.screen_height))
        pygame.display.set_caption("Snake Game")
        self.clock = pygame.time.Clock()
        self.snake = Snake(self)
        self.food = Food(self)
        self.score = 0
        self.game_over = False
        self.running = True # Added running flag for the main loop
        self.font = pygame.font.Font(None, 36)  # Initialize font


    def update(self):
        """
        Updates the game state (snake movement, food consumption, collision detection).
        """
        if not self.game_over:
            self.snake.move()
            if self.snake.check_collision():
                self.game_over = True
            if self.snake.eat(self.food):
                self.score += 10
                self.food.generate_food()  # generate new food

    def draw(self):
        """
        Draws the game elements (snake, food, board) on the screen.
        :param screen: The display surface.
        """
        self.screen.fill(BLACK)  # Clear the screen

        # Draw the snake
        for segment in self.snake.body:
            pygame.draw.rect(self.screen, GREEN, (segment[0] * self.cell_size, segment[1] * self.cell_size, self.cell_size, self.cell_size))

        # Draw the food
        pygame.draw.rect(self.screen, RED, (self.food.position[0] * self.cell_size, self.food.position[1] * self.cell_size, self.cell_size, self.cell_size))

        # Draw the score
        score_text = self.font.render(f"Score: {self.score}", True, WHITE)
        self.screen.blit(score_text, (5, 5))

        if self.game_over:
            game_over_text = self.font.render("Game Over! Press R to restart", True, WHITE)
            score_text = self.font.render(f"Final Score: {self.score}", True, WHITE)
            text_rect = game_over_text.get_rect(center=(self.screen_width // 2, self.screen_height // 2 - 20))
            score_rect = score_text.get_rect(center=(self.screen_width // 2, self.screen_height // 2 + 20))
            self.screen.blit(game_over_text, text_rect)
            self.screen.blit(score_text, score_rect)

        pygame.display.flip()  # Update the full display Surface to the screen

    def handle_input(self, event):
        """
        Handles user input (arrow keys) to change the snake's direction.
        :param key: The key pressed by the user.
        """
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP and self.snake.direction != "DOWN":
                self.snake.direction = "UP"
            elif event.key == pygame.K_DOWN and self.snake.direction != "UP":
                self.snake.direction = "DOWN"
            elif event.key == pygame.K_LEFT and self.snake.direction != "RIGHT":
                self.snake.direction = "LEFT"
            elif event.key == pygame.K_RIGHT and self.snake.direction != "LEFT":
                self.snake.direction = "RIGHT"
            elif self.game_over and event.key == pygame.K_r:
                self.restart()

    def restart(self):
        """
        Restarts the game (resets snake, food, score, game_over flag).
        """
        self.snake = Snake(self)
        self.food = Food(self)
        self.score = 0
        self.game_over = False

    def run(self):
        """
        Main game loop.
        """
        while self.running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                self.handle_input(event)

            self.update()
            self.draw()
            self.clock.tick(10)  # Control game speed (frames per second)

        pygame.quit()


class Snake:
    def __init__(self, game):
        """
        Initializes the snake object.
        :param game: A reference to the Game object.
        """
        self.game = game
        self.body = [(game.width // 2, game.height // 2), (game.width // 2 - 1, game.height // 2),
                     (game.width // 2 - 2, game.height // 2)]  # Initial snake position
        self.direction = "RIGHT"  # Initial direction

    def move(self):
        """
        Moves the snake one cell in the current direction.
        """
        head_x, head_y = self.body[0]
        if self.direction == "UP":
            new_head = (head_x, head_y - 1)
        elif self.direction == "DOWN":
            new_head = (head_x, head_y + 1)
        elif self.direction == "LEFT":
            new_head = (head_x - 1, head_y)
        elif self.direction == "RIGHT":
            new_head = (head_x + 1, head_y)

        self.body.insert(0, new_head)
        self.body.pop()  # Remove the last segment


    def change_direction(self, key):
        """
        Changes the direction of the snake based on user input.
        :param key: The key pressed by the user.
        """
        pass # Direction change handled in Game class


    def check_collision(self):
        """
        Checks for collisions with walls or the snake's own body.
        :return: True if a collision occurs, False otherwise.
        """
        head_x, head_y = self.body[0]
        if head_x < 0 or head_x >= self.game.width or head_y < 0 or head_y >= self.game.height:
            return True  # Wall collision
        if (head_x, head_y) in self.body[1:]:
            return True  # Self-collision
        return False

    def eat(self, food):
        """
        Checks if the snake has eaten the food.
        :param food: The Food object.
        :return: True if the snake has eaten the food, False otherwise.
        """
        if self.body[0] == food.position:
            head_x, head_y = self.body[0]
            if self.direction == "UP":
                new_head = (head_x, head_y - 1)
            elif self.direction == "DOWN":
                new_head = (head_x, head_y + 1)
            elif self.direction == "LEFT":
                new_head = (head_x - 1, head_y)
            elif self.direction == "RIGHT":
                new_head = (head_x + 1, head_y)
            self.body.insert(0, new_head)

            return True
        return False


class Food:
    def __init__(self, game):
        """
        Initializes the food object.
        :param game: A reference to the Game object.
        """
        self.game = game
        self.position = self.generate_food()  # Initial food position

    def generate_food(self):
        """
        Generates a new random position for the food item.
        """
        import random
        while True:
            x = random.randint(0, self.game.width - 1)
            y = random.randint(0, self.game.height - 1)
            if (x, y) not in self.game.snake.body:
                return (x, y)

    def draw(self, screen):
        """
        Draws the food on the screen.
        :param screen: The display surface.
        """
        pass # Drawing is handled in Game class


if __name__ == '__main__':
    game = Game(20, 15, 20)  # width, height, cell_size
    game.run()