import gradio as gr
import threading
import importlib
import sys

# Dynamically import the game module
spec = importlib.util.spec_from_file_location("Game", "Game.py")
GameModule = importlib.util.module_from_spec(spec)
sys.modules["Game"] = GameModule
spec.loader.exec_module(GameModule)

Game = GameModule.Game  # Access the Game class from the imported module


def launch_game():
    """Launches the game in a separate thread."""
    game = Game()
    game.run()


def start_game_button_click():
    """Handles the "Start Game" button click event."""
    threading.Thread(target=launch_game).start()
    return "Game started in a new window!"


def create_ui():
    """Creates the Gradio UI."""
    with gr.Blocks(title="Bouncing Ball Game") as ui:
        gr.Markdown("# Bouncing Ball Game")

        start_button = gr.Button("Start Game")
        game_status = gr.Textbox(label="Game Status")

        gr.Markdown("## Gameplay Instructions:")
        gr.Markdown("""
        - Use the LEFT and RIGHT arrow keys to move the paddle.
        - The objective is to bounce the ball and prevent it from falling off the screen.
        - Hitting obstacles gives you extra points!
        - Press 'P' to pause/unpause the game.
        - Press 'SPACE' on the start screen or game over screen to (re)start the game.
        """)

        start_button.click(start_game_button_click, outputs=game_status)

    return ui


if __name__ == "__main__":
    ui = create_ui()
    ui.launch()