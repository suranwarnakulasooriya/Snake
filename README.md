# Snake
A recreation of the classic snake game in Python.

## Dependencies
Pygame is the only dependency for this project, to install it, do:
```
pip install pygame
```

## Usage
Use the arrow keys or WASD to move. Use space to pause and unpause. Use R to restart after a game over. Use escape to close.
The screen is a grid with a certain width, height, and cell size. These values default to 50, 25, and 40, respectively. These values, along with the artificial delay and some colors, can be changed in the following lines:
```
15 p = 40 # size of a cell in pixels
16 w = 50 # grid size in cells
17 h = 26 # grid height in cells
18 delay = 30 # artificial delay in milliseconds
19 applecol = red # color of apple
20 snakecol = green # color of snake
```
Make sure that `snakeHigh.txt` and `font.ttf` are in the same directory as `snake.py`.
