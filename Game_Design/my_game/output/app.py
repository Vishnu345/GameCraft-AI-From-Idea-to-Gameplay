import gradio as gr
import pygame
import random
import threading
import importlib.util
import sys

# Dynamically import the Game class from Game.py
spec = importlib.util.spec_from_file_location("Game", "Game.py")
module = importlib.util.module_from_spec(spec)
sys.modules["Game"] = module
spec.loader.exec_module(module)
Game = module.Game

# Game constants
GRID_WIDTH = 80
GRID_HEIGHT = 50
CELL_SIZE = 10
SCREEN_WIDTH = GRID_WIDTH * CELL_SIZE
SCREEN_HEIGHT = GRID_HEIGHT * CELL_SIZE
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
BLACK = (0, 0, 0)


def run_game():
    """
    Runs the Pygame instance of the Snake game in a separate thread.
    """
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("Snake Game")
    clock = pygame.time.Clock()
    font = pygame.font.Font(None, 30)  # Font for displaying score

    game = Game(GRID_WIDTH, GRID_HEIGHT)

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    game.change_direction('up')
                elif event.key == pygame.K_DOWN:
                    game.change_direction('down')
                elif event.key == pygame.K_LEFT:
                    game.change_direction('left')
                elif event.key == pygame.K_RIGHT:
                    game.change_direction('right')

        game.update()

        # Clear screen
        screen.fill(BLACK)

        # Draw snake
        for segment in game.snake:
            pygame.draw.rect(screen, GREEN, (segment[0] * CELL_SIZE, segment[1] * CELL_SIZE, CELL_SIZE, CELL_SIZE))

        # Draw food
        pygame.draw.rect(screen, RED, (game.food[0] * CELL_SIZE, game.food[1] * CELL_SIZE, CELL_SIZE, CELL_SIZE))

        # Display score
        score_text = font.render(f"Score: {game.score}", True, WHITE)  # Render score text
        screen.blit(score_text, (10, 10))  # Position it at the top-left corner

        # Update screen
        pygame.display.flip()
        clock.tick(game.speed)

        if game.game_over:
            running = False
            # Display final score before exiting
            screen.fill(BLACK)
            game_over_text = font.render(f"Game Over! Final Score: {game.score}", True, WHITE)
            screen.blit(game_over_text, (SCREEN_WIDTH // 2 - 120, SCREEN_HEIGHT // 2 - 20))  # Center the text
            pygame.display.flip()
            pygame.time.delay(2000)  # Wait 2 seconds before closing

    pygame.quit()


def start_game_thread():
    """
    Starts the game in a separate thread.
    """
    game_thread = threading.Thread(target=run_game)
    game_thread.daemon = True  # Allows the main program to exit even if the thread is running
    game_thread.start()


def create_ui():
    """
    Creates the Gradio UI for the Snake game.
    """
    with gr.Blocks() as ui:
        gr.Markdown("# Snake Game")
        start_button = gr.Button("Start Game")
        start_button.click(start_game_thread)

        gr.Markdown("## How to Play")
        gr.Markdown("""
            Use the arrow keys to control the snake:
            - Up: Move the snake up
            - Down: Move the snake down
            - Left: Move the snake left
            - Right: Move the snake right

            The goal is to eat the red food and grow longer. Avoid hitting the walls or yourself!
        """)

    return ui


if __name__ == "__main__":
    ui = create_ui()
    ui.launch()