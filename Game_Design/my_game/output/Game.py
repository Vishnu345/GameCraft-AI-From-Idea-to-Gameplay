
import pygame
import random

class Game:
    """
    Encapsulates the core logic of the Snake game.
    """

    def __init__(self, width, height):
        """
        Initializes the game with the specified grid dimensions.

        Args:
            width (int): The width of the game grid.
            height (int): The height of the game grid.
        """
        self.grid_width = width
        self.grid_height = height
        self.snake = [(width // 2, height // 2), (width // 2 - 1, height // 2), (width // 2 - 2, height // 2)]  # Initial snake at the center
        self.food = self.generate_food()
        self.direction = 'right'
        self.score = 0
        self.game_over = False
        self.speed = 10  # Adjust for desired game speed. Higher values mean faster game.


    def reset(self):
        """
        Resets the game state to its initial configuration.
        """
        self.snake = [(self.grid_width // 2, self.grid_height // 2), (self.grid_width // 2 - 1, self.grid_height // 2), (self.grid_width // 2 - 2, self.grid_height // 2)]
        self.food = self.generate_food()
        self.direction = 'right'
        self.score = 0
        self.game_over = False

    def update(self):
        """
        Updates the game state based on the current direction.
        Moves the snake, checks for collisions, and handles food consumption.
        """
        if not self.game_over:
            self.move_snake()
            if self.check_collisions():
                self.game_over = True
            if self.snake[0] == self.food:
                self.eat_food()

    def move_snake(self):
        """
        Moves the snake one step in the current direction.
        """
        head_x, head_y = self.snake[0]
        if self.direction == 'up':
            new_head = (head_x, head_y - 1)
        elif self.direction == 'down':
            new_head = (head_x, head_y + 1)
        elif self.direction == 'left':
            new_head = (head_x - 1, head_y)
        elif self.direction == 'right':
            new_head = (head_x + 1, head_y)

        self.snake.insert(0, new_head)  # Add new head
        self.snake.pop()  # Remove tail

    def check_collisions(self):
        """
        Checks for collisions with the walls or the snake's own body.

        Returns:
            bool: True if a collision occurs, False otherwise.
        """
        head_x, head_y = self.snake[0]

        # Wall collision
        if head_x < 0 or head_x >= self.grid_width or head_y < 0 or head_y >= self.grid_height:
            return True

        # Self-collision
        if self.snake[0] in self.snake[1:]:
            return True

        return False

    def eat_food(self):
        """
        Handles the logic for when the snake eats food.
        Increases the snake's length, updates the score, and generates new food.
        """
        self.score += 10
        self.snake.insert(0, self.food) # Add the food as a new head - effectively lengthening the snake
        self.food = self.generate_food()


    def generate_food(self):
        """
        Generates a new food item at a random location on the grid,
        ensuring it does not overlap with the snake.

        Returns:
            tuple: The (x, y) coordinate of the new food item.
        """
        while True:
            x = random.randint(0, self.grid_width - 1)
            y = random.randint(0, self.grid_height - 1)
            if (x, y) not in self.snake:
                return (x, y)

    def change_direction(self, new_direction):
        """
        Changes the snake's direction, validating that the new direction is not
        directly opposite the current direction.

        Args:
            new_direction (str): The new direction for the snake ('up', 'down', 'left', 'right').
        """
        if new_direction == 'up' and self.direction != 'down':
            self.direction = 'up'
        elif new_direction == 'down' and self.direction != 'up':
            self.direction = 'down'
        elif new_direction == 'left' and self.direction != 'right':
            self.direction = 'left'
        elif new_direction == 'right' and self.direction != 'left':
            self.direction = 'right'

    def get_state(self):
         """
         Returns the current state of the game.

         Returns:
             dict: A dictionary containing the snake's position, food position,
                   score, and game over status.
         """
         return {
             'snake': self.snake,
             'food': self.food,
             'score': self.score,
             'game_over': self.game_over
         }