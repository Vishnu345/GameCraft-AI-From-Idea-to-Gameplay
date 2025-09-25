import unittest
from unittest.mock import MagicMock
import pygame
from Game import Game, Snake, Food

class TestGame(unittest.TestCase):

    def setUp(self):
        """Set up for test methods."""
        pygame.init()
        self.game = Game(20, 15, 20)  # width, height, cell_size
        self.game.screen = MagicMock()  # Mock the screen to avoid actual display
        self.game.running = False #stop game when unit test run

    def tearDown(self):
        """Tear down for test methods."""
        pygame.quit()

    def test_game_initialization(self):
        """Test if the game initializes correctly."""
        self.assertEqual(self.game.width, 20)
        self.assertEqual(self.game.height, 15)
        self.assertEqual(self.game.cell_size, 20)
        self.assertEqual(self.game.score, 0)
        self.assertFalse(self.game.game_over)
        self.assertIsInstance(self.game.snake, Snake)
        self.assertIsInstance(self.game.food, Food)

    def test_update_snake_movement(self):
        """Test if the snake moves correctly upon update."""
        initial_head = self.game.snake.body[0]
        self.game.update()
        new_head = self.game.snake.body[0]
        self.assertNotEqual(initial_head, new_head)

    def test_update_collision_detection(self):
        """Test collision detection updates game_over."""
        # Force a collision by moving the snake to the edge
        self.game.snake.body = [(0, 0)]
        self.game.snake.direction = "LEFT"
        self.game.update()
        self.assertTrue(self.game.game_over)

    def test_update_food_consumption(self):
        """Test if food consumption increases the score."""
        # Place food at the snake's head position
        self.game.snake.body = [(5, 5)]
        self.game.food.position = (5, 5)
        initial_score = self.game.score
        self.game.update()
        self.assertGreater(self.game.score, initial_score)

    def test_restart_game(self):
        """Test if the restart method resets the game state."""
        self.game.score = 50
        self.game.game_over = True
        self.game.restart()
        self.assertEqual(self.game.score, 0)
        self.assertFalse(self.game.game_over)
        self.assertIsInstance(self.game.snake, Snake)
        self.assertIsInstance(self.game.food, Food)

    def test_handle_input(self):
       """Test if handle input changes snake direction"""
       # Mock a key press event
       event = pygame.event.Event(pygame.KEYDOWN, key=pygame.K_UP)
       self.game.handle_input(event)
       self.assertEqual(self.game.snake.direction, "UP")

class TestSnake(unittest.TestCase):

    def setUp(self):
        """Set up for test methods."""
        pygame.init()
        self.game = Game(20, 15, 20)
        self.snake = self.game.snake
        self.game.screen = MagicMock()  # Mock the screen to avoid actual display
        self.game.running = False #stop game when unit test run

    def tearDown(self):
        pygame.quit()

    def test_snake_initialization(self):
        """Test if the snake initializes correctly."""
        self.assertEqual(len(self.snake.body), 3)
        self.assertEqual(self.snake.direction, "RIGHT")

    def test_snake_move_up(self):
        """Test if the snake moves up correctly."""
        self.snake.direction = "UP"
        initial_head = self.snake.body[0]
        self.snake.move()
        new_head = self.snake.body[0]
        self.assertEqual(new_head[0], initial_head[0])
        self.assertEqual(new_head[1], initial_head[1] - 1)

    def test_snake_move_down(self):
        """Test if the snake moves down correctly."""
        self.snake.direction = "DOWN"
        initial_head = self.snake.body[0]
        self.snake.move()
        new_head = self.snake.body[0]
        self.assertEqual(new_head[0], initial_head[0])
        self.assertEqual(new_head[1], initial_head[1] + 1)

    def test_snake_move_left(self):
        """Test if the snake moves left correctly."""
        self.snake.direction = "LEFT"
        initial_head = self.snake.body[0]
        self.snake.move()
        new_head = self.snake.body[0]
        self.assertEqual(new_head[0], initial_head[0] - 1)
        self.assertEqual(new_head[1], initial_head[1])

    def test_snake_move_right(self):
        """Test if the snake moves right correctly."""
        self.snake.direction = "RIGHT"
        initial_head = self.snake.body[0]
        self.snake.move()
        new_head = self.snake.body[0]
        self.assertEqual(new_head[0], initial_head[0] + 1)
        self.assertEqual(new_head[1], initial_head[1])

    def test_snake_check_collision_wall(self):
        """Test if the snake detects wall collisions correctly."""
        self.snake.body = [(-1, 0)]  # Place snake outside the left boundary
        self.assertTrue(self.snake.check_collision())

        self.snake.body = [(self.game.width, 0)]  # Place snake outside the right boundary
        self.assertTrue(self.snake.check_collision())

        self.snake.body = [(0, -1)]  # Place snake outside the top boundary
        self.assertTrue(self.snake.check_collision())

        self.snake.body = [(0, self.game.height)]  # Place snake outside the bottom boundary
        self.assertTrue(self.snake.check_collision())

    def test_snake_check_collision_self(self):
        """Test if the snake detects self-collisions correctly."""
        self.snake.body = [(5, 5), (5, 4), (5, 5)]  # Overlap head with body
        self.assertTrue(self.snake.check_collision())

    def test_snake_eat_food(self):
        """Test if the snake eats food correctly."""
        self.snake.body = [(5, 5)]
        self.game.food.position = (5, 5)
        initial_length = len(self.snake.body)
        self.assertTrue(self.snake.eat(self.game.food))
        self.assertEqual(len(self.snake.body), initial_length + 1)

    def test_snake_not_eat_food(self):
         """Test if the snake not eats food correctly."""
         self.snake.body = [(5, 5)]
         self.game.food.position = (6, 6)
         initial_length = len(self.snake.body)
         self.assertFalse(self.snake.eat(self.game.food))
         self.assertEqual(len(self.snake.body), initial_length)

class TestFood(unittest.TestCase):

    def setUp(self):
        """Set up for test methods."""
        pygame.init()
        self.game = Game(20, 15, 20)
        self.food = self.game.food
        self.game.screen = MagicMock()  # Mock the screen to avoid actual display
        self.game.running = False #stop game when unit test run

    def tearDown(self):
        pygame.quit()

    def test_food_initialization(self):
        """Test if the food initializes correctly."""
        self.assertIsInstance(self.food.position, tuple)
        self.assertEqual(len(self.food.position), 2)

    def test_generate_food(self):
        """Test if generate food produces valid coordinates."""
        self.game.snake.body = [(5, 5), (5, 4), (5, 3)]
        new_position = self.food.generate_food()
        self.assertIsInstance(new_position, tuple)
        self.assertGreaterEqual(new_position[0], 0)
        self.assertLess(new_position[0], self.game.width)
        self.assertGreaterEqual(new_position[1], 0)
        self.assertLess(new_position[1], self.game.height)
        self.assertNotIn(new_position, self.game.snake.body)

if __name__ == '__main__':
    unittest.main()