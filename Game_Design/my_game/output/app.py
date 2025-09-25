import gradio as gr
import threading
import importlib
import pygame
import sys

# Constants for the game
GAME_WIDTH = 20
GAME_HEIGHT = 15
CELL_SIZE = 20


def launch_game():
    """
    Launches the Snake game in a separate thread.
    """
    try:
        # Dynamically import the game module
        spec = importlib.util.spec_from_file_location("Game", "Game.py")
        game_module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(game_module)

        # Instantiate and run the game
        game = game_module.Game(GAME_WIDTH, GAME_HEIGHT, CELL_SIZE)
        game.run()
    except Exception as e:
        print(f"Error launching game: {e}")


def start_game_button_click():
    """
    Handles the 'Start Game' button click event.
    Launches the game in a separate thread to avoid blocking the Gradio UI.
    """
    game_thread = threading.Thread(target=launch_game)
    game_thread.daemon = True  # Allow the main program to exit even if the thread is running
    game_thread.start()
    return "Game started in a new window!"


def close():
    pygame.quit()
    sys.exit()


# Gradio UI definition
with gr.Blocks(title="Snake Game Launcher") as iface:
    gr.Markdown("# Welcome to Snake Game!")
    gr.Markdown("Click the button below to start the game.")

    start_button = gr.Button("Start Game")
    output_text = gr.Textbox(label="Status")

    gr.Markdown("## How to Play:")
    gr.Markdown("""
    - Use the arrow keys (Up, Down, Left, Right) to control the snake's direction.
    - The goal is to eat the red food to grow longer.
    - Avoid colliding with the walls or the snake's own body.
    - If you collide, the game is over. Press 'R' to restart the game.
    """)

    start_button.click(start_game_button_click, outputs=output_text)

if __name__ == "__main__":
    iface.launch()