import gradio as gr
import pygame
import threading
import time
from Game import Game


def draw_game(screen, game, cell_size, font):
    """Draws the game elements on the screen."""
    screen.fill((0, 0, 0))  # Black background

    # Draw snake
    for x, y in game.snake:
        pygame.draw.rect(screen, (0, 255, 0), (x * cell_size, y * cell_size, cell_size, cell_size))

    # Draw food
    pygame.draw.rect(screen, (255, 0, 0), (game.food[0] * cell_size, game.food[1] * cell_size, cell_size, cell_size))

    # Display score
    score_text = font.render(f"Score: {game.score}", True, (255, 255, 255))
    screen.blit(score_text, (5, 5))

    if game.game_over:
        game_over_text = font.render("Game Over!!", True, (255, 255, 255))
        text_rect = game_over_text.get_rect(center=(screen.get_width() // 2, screen.get_height() // 2))
        screen.blit(game_over_text, text_rect)


def game_loop(game, screen, cell_size, font, clock):
    """Main game loop handling events, updates, and rendering."""
    while not game.game_over:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return
            if event.type == pygame.KEYDOWN:
                direction_map = {
                    pygame.K_UP: 'up',
                    pygame.K_DOWN: 'down',
                    pygame.K_LEFT: 'left',
                    pygame.K_RIGHT: 'right'
                }
                if event.key in direction_map:
                    game.change_direction(direction_map[event.key])

        game.update()
        draw_game(screen, game, cell_size, font)
        pygame.display.flip()
        time.sleep(max(0.05, 0.5 / game.speed))
        clock.tick(60)


def start_game(grid_width, grid_height, initial_speed):
    """Initializes and runs the game."""
    pygame.init()
    cell_size = 20
    width, height = grid_width * cell_size, grid_height * cell_size
    screen = pygame.display.set_mode((width, height))
    pygame.display.set_caption("Snake Game")
    font = pygame.font.Font(None, 25)
    clock = pygame.time.Clock()

    game = Game(grid_width, grid_height, initial_speed)
    game_loop(game, screen, cell_size, font, clock)
    pygame.quit()


def launch_game(grid_width, grid_height, initial_speed):
    """Launches the game in a separate thread."""
    thread = threading.Thread(target=start_game, args=(grid_width, grid_height, initial_speed))
    thread.daemon = True
    thread.start()
    return f"Game started with {grid_width}x{grid_height} grid."


def get_instructions():
    """Returns game instructions."""
    return """
    ## How to Play:
    - Use the arrow keys to move the snake.
    - Eat the red squares to grow.
    - Avoid hitting the walls or yourself.
    """


if __name__ == "__main__":
    with gr.Blocks() as demo:
        gr.Markdown("# Snake Game 🎮")
        grid_width_slider = gr.Slider(10, 100, value=20, step=1, label="Grid Width")
        grid_height_slider = gr.Slider(10, 100, value=20, step=1, label="Grid Height")
        initial_speed_slider = gr.Slider(1, 10, value=5, step=1, label="Initial Speed")
        start_button = gr.Button("Start Game")
        instructions = gr.Markdown(get_instructions())
        game_status = gr.Textbox(label="Status")

        start_button.click(
            fn=launch_game,
            inputs=[grid_width_slider, grid_height_slider, initial_speed_slider],
            outputs=game_status
        )

    demo.launch()