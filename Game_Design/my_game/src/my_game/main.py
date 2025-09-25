#!/usr/bin/env python
import sys
import warnings
from datetime import datetime
import os
from my_game.crew import MyGame

warnings.filterwarnings("ignore", category=SyntaxWarning, module="pysbd")

os.makedirs('output', exist_ok=True)

topic= "simple snake game"
module_name = "Game"
class_name = "Game"

def run():
    """
    Run the crew.
    """
    inputs = {
        'topic': topic,
        'module_name': module_name,
        'class_name': class_name
    }
    
    try:
        MyGame().crew().kickoff(inputs=inputs)
    except Exception as e:
        raise Exception(f"An error occurred while running the crew: {e}")
    
if __name__ == "__main__":
    run()


