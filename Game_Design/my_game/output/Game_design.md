```markdown
# Game Design Document: Simple Snake Game

## 1. Introduction

This document outlines the design for a simple Snake game. The game involves controlling a snake to eat food items, growing longer with each item consumed. The player must avoid colliding with the walls or the snake's own body. This GDD aims to provide a clear and comprehensive guide for developers to implement the game efficiently.

### 1.1. Game Title: Snake

### 1.2. Genre: Arcade, Puzzle

### 1.3. Target Audience: Casual gamers, all age groups

## 2. Game Overview

### 2.1. Core Gameplay Loop

The player controls a snake within a defined game board. The snake moves continuously in a direction chosen by the player. The player can change the snake's direction using controls (e.g., arrow keys). The goal is to eat food items that appear randomly on the board. Each time the snake eats food, it grows in length. The game ends if the snake collides with the walls of the game board or with its own body.

### 2.2. Gameplay Objectives

*   Primary Objective: Achieve the highest possible score by eating as much food as possible without colliding with the wall or itself.
*   Secondary Objectives: Unlock achievements (e.g., reach a certain score, eat a specific number of food items).

## 3. Game Mechanics

### 3.1. Movement

*   The snake moves continuously in one of four directions: up, down, left, or right.
*   The player changes the direction using directional input (e.g., arrow keys).
*   Movement is tile-based; the snake moves one cell at a time.

### 3.2. Food

*   Food items appear randomly on the game board.
*   When the snake's head occupies the same cell as a food item, the snake "eats" the food.
*   Eating food increases the snake's length by one segment.
*   A new food item appears after the previous one is eaten.

### 3.3. Collision Detection

*   Wall Collision: If the snake's head collides with any of the game board's walls, the game ends.
*   Self-Collision: If the snake's head collides with any part of its body, the game ends.

### 3.4. Game Over

*   The game ends when either a wall collision or self-collision occurs.
*   The final score is displayed.
*   The player is given the option to restart the game.

### 3.5. Special Gameplay Instructions

*   The game starts with the snake having a length of 3 segments.
*   The initial direction of the snake is randomly chosen.
*   The initial food item is placed randomly, ensuring it does not overlap with the initial snake position.

## 4. User Interactions and User Experience (UX)

### 4.1. Controls

*   **Up Arrow Key:** Move the snake upwards.
*   **Down Arrow Key:** Move the snake downwards.
*   **Left Arrow Key:** Move the snake leftwards.
*   **Right Arrow Key:** Move the snake rightwards.
*   **[Optional: Spacebar/Enter]:** Pause/Resume the game.

### 4.2. User Interface (UI)

*   **Score Display:** Shows the current score. Located at the top-left or top-right of the screen.
*   **Game Board:** Clearly displays the snake, food, and boundaries.
*   **Game Over Screen:** Displays the final score and an option to restart the game.
*   **Pause Screen (Optional):** Displays a "Paused" message and options to resume or restart.

### 4.3. User Experience (UX) Guidelines

*   **Responsiveness:** The game should respond instantly to user input.
*   **Clarity:** The game board and UI elements should be clear and easy to understand.
*   **Feedback:** Provide visual feedback when the snake eats food (e.g., a slight animation or sound effect).
*   **Accessibility:** Use clear and contrasting colors for the snake, food, and background.

## 5. Scoring System and Level Progression

### 5.1. Scoring

*   Each food item eaten increases the score by a fixed amount (e.g., 10 points).
*   The score is continuously updated and displayed on the screen.

### 5.2. Level Progression (Optional)

*   The game's difficulty could increase over time by:
    *   Increasing the speed of the snake.
    *   Introducing obstacles on the game board.
    *   Decreasing the size of the game board.
*   These difficulty adjustments could be triggered based on the score or time elapsed.

## 6. Game Layout

### 6.1. Game Board Dimensions

*   The game board is a grid of cells (e.g., 20x20, 30x20). The specific dimensions can be adjusted.

### 6.2. Cell Size

*   Each cell has a fixed size (e.g., 20x20 pixels, 30x30 pixels).

### 6.3. Visual Representation

*   **Snake:** A series of connected cells, each representing a segment of the snake's body.
*   **Food:** A single cell with a distinct color or shape to differentiate it from the snake and background.
*   **Walls:** The boundaries of the game board, visually distinct from the playable area.

## 7. Game Over Logic

### 7.1. Trigger Conditions

*   The game over sequence is triggered when the snake collides with a wall or its own body.

### 7.2. Game Over Sequence

1.  Stop the snake's movement.
2.  Display a "Game Over" message on the screen.
3.  Display the player's final score.
4.  Provide options:
    *   Restart the game.
    *   Return to the main menu (if applicable).

## 8. Python Implementation Details

### 8.1. Module Name: `Game`

### 8.2. Primary Class Name: `Game`

### 8.3. Key Classes and Methods

```python
# Game.py

class Game:
    def __init__(self, width, height):
        """
        Initializes the game environment.
        :param width: Width of the game board in cells.
        :param height: Height of the game board in cells.
        """
        self.width = width
        self.height = height
        self.snake = Snake(self)
        self.food = Food(self)
        self.score = 0
        self.game_over = False

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
                self.food.generate_food() #generate new food

    def draw(self, screen):
        """
        Draws the game elements (snake, food, board) on the screen.
        :param screen: The display surface.
        """
        # Implementation details for drawing the game elements

    def handle_input(self, key):
        """
        Handles user input (arrow keys) to change the snake's direction.
        :param key: The key pressed by the user.
        """
        self.snake.change_direction(key)

    def restart(self):
        """
        Restarts the game (resets snake, food, score, game_over flag).
        """
        self.snake = Snake(self)
        self.food = Food(self)
        self.score = 0
        self.game_over = False

class Snake:
    def __init__(self, game):
        """
        Initializes the snake object.
        :param game: A reference to the Game object.
        """
        self.game = game
        self.body = [(game.width // 2, game.height // 2), (game.width // 2 - 1, game.height // 2), (game.width // 2 - 2, game.height // 2)] # Initial snake position
        self.direction = "RIGHT"  # Initial direction

    def move(self):
        """
        Moves the snake one cell in the current direction.
        """
        # Implementation details for moving the snake and updating the body

    def change_direction(self, key):
        """
        Changes the direction of the snake based on user input.
        :param key: The key pressed by the user.
        """
        # Implementation details for changing direction

    def check_collision(self):
        """
        Checks for collisions with walls or the snake's own body.
        :return: True if a collision occurs, False otherwise.
        """
        # Implementation details for collision detection

    def eat(self, food):
        """
        Checks if the snake has eaten the food.
        :param food: The Food object.
        :return: True if the snake has eaten the food, False otherwise.
        """
        # Implementation details for eating food

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
         # Implementation details for generating food at a random valid location
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
        # Implementation details for drawing the food

```

### 8.4. Functionalities

*   **Game Initialization:** Sets up the game board, snake, and initial food item.
*   **Game Update:** Updates the game state in each frame (movement, collision, score).
*   **Input Handling:** Processes user input to control the snake's direction.
*   **Rendering:** Draws the game elements on the screen.
*   **Collision Detection:** Checks for collisions between the snake, walls, and itself.
*   **Scoring:** Calculates and updates the player's score.
*   **Game Over Handling:** Ends the game and displays the final score.

## 9. Assets

### 9.1. Visual Assets

*   **Snake:** Simple colored blocks or sprites.
*   **Food:** A distinct colored block or sprite.
*   **Background:** A simple, neutral color.
*   **Walls:** Visually distinct borders.

### 9.2. Audio Assets (Optional)

*   **Eating Sound:** A short sound effect when the snake eats food.
*   **Game Over Sound:** A sound effect when the game ends.

## 10. Development Notes

*   Use a modular approach to separate game logic from rendering.
*   Implement collision detection efficiently to maintain performance.
*   Prioritize responsiveness to user input.
*   Consider using a game engine or library (e.g., Pygame) to simplify development.
*   Adhere to coding standards for readability and maintainability.

## 11. Future Enhancements (Optional)

*   Add multiple levels with increasing difficulty.
*   Implement power-ups (e.g., speed boost, temporary invincibility).
*   Introduce different types of food with varying score values.
*   Implement a high score leaderboard.
*   Add visual effects and animations to enhance the user experience.
```