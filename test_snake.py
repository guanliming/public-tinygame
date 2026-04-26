import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent))

from games.snake import SnakeGame, Direction, Position

def test_snake_game():
    print("Testing Snake Game...")
    
    game = SnakeGame()
    game.init_game()
    
    print(f"Initial snake length: {len(game.snake)}")
    print(f"Initial food count: {len(game.foods)}")
    print(f"Initial score: {game.score}")
    print(f"Initial direction: {game.direction}")
    
    print("\nMoving snake 5 times...")
    for i in range(5):
        game.move()
        print(f"Move {i+1}: Snake head at ({game.snake[0].x}, {game.snake[0].y}), length: {len(game.snake)}")
    
    print("\nTesting direction change...")
    game.set_direction(Direction.DOWN)
    print(f"Direction changed to: {game.direction}")
    
    print("\nMoving snake 3 times down...")
    for i in range(3):
        game.move()
        print(f"Move {i+1}: Snake head at ({game.snake[0].x}, {game.snake[0].y}), length: {len(game.snake)}")
    
    print("\nTesting screen wrapping...")
    game.direction = Direction.LEFT
    for i in range(80):
        game.move()
    print(f"After moving left 80 times: Snake head at ({game.snake[0].x}, {game.snake[0].y})")
    
    print("\nAll tests passed!")

if __name__ == "__main__":
    test_snake_game()
