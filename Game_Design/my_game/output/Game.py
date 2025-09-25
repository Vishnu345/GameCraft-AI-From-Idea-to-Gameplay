import random


class Game:
    def __init__(self, grid_width, grid_height, initial_speed):
        """
        Initializes the game with the given grid dimensions and initial speed.

        Args:
            grid_width (int): Width of the game grid.
            grid_height (int): Height of the game grid.
            initial_speed (int): Initial speed of the snake.
        """
        self.grid_width = grid_width
        self.grid_height = grid_height
        self.initial_speed = initial_speed
        self.reset()  # Initialize/reset the game state.

    def reset(self):
        """Resets the game to its initial state."""
        self.snake = [(self.grid_width // 2, self.grid_height // 2)]  # Snake starts at the center.
        self.food = self._spawn_food()
        self.direction = random.choice(['up', 'down', 'left', 'right'])
        self.score = 0
        self.speed = self.initial_speed
        self.game_over = False

    def _spawn_food(self):
        """Generates food at a random position not occupied by the snake."""
        while True:
            x, y = random.randint(0, self.grid_width - 1), random.randint(0, self.grid_height - 1)
            if (x, y) not in self.snake:
                return (x, y)

    def move(self):
        """
        Moves the snake one step in the current direction. Checks for collisions,
        food consumption, and updates the game state accordingly.
        """
        head_x, head_y = self.snake[0]
        new_head = {
            'up': (head_x, head_y - 1),
            'down': (head_x, head_y + 1),
            'left': (head_x - 1, head_y),
            'right': (head_x + 1, head_y)
        }.get(self.direction)

        # Collision detection
        if not self._is_valid_move(new_head[0], new_head[1]) or self._is_collision(new_head):
            self.game_over = True
            return

        self.snake.insert(0, new_head)  # Add new head to the snake.

        # Check if food is eaten
        if new_head == self.food:
            self.score += 10
            self.food = self._spawn_food()
            self.speed = max(1, self.speed - 0.2)  # Increase speed as snake grows.
        else:
            self.snake.pop()  # Remove the tail if food not eaten.

    def change_direction(self, new_direction):
        """
        Changes the direction of the snake and prevents 180-degree turns.

        Args:
            new_direction (str): New direction ('up', 'down', 'left', 'right').
        """
        opposite_directions = {'up': 'down', 'down': 'up', 'left': 'right', 'right': 'left'}
        if new_direction != opposite_directions.get(self.direction):
            self.direction = new_direction

    def _is_valid_move(self, x, y):
        """Checks if a given position is within grid boundaries."""
        return 0 <= x < self.grid_width and 0 <= y < self.grid_height

    def _is_collision(self, head):
        """Checks if the snake's head collides with its body."""
        return head in self.snake[1:]

    def update(self):
        """Updates the game (moves the snake if it's not game over)."""
        if not self.game_over:
            self.move()

    def get_state(self):
        """
        Returns the current state of the game.

        Returns:
            dict: Game state including grid dimensions, snake position, food position,
                  score, speed, and game-over status.
        """
        return {
            'grid_width': self.grid_width,
            'grid_height': self.grid_height,
            'snake': self.snake,
            'food': self.food,
            'score': self.score,
            'game_over': self.game_over,
            'speed': self.speed
        }

    def get_score(self):
        """Returns the player's current score."""
        return self.score