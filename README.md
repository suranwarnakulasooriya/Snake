# Snake
A recreation of the classic snake game in Python.

## Dependencies
Pygame is the only dependency for this project, to install it, do:
```
pip install pygame
```

## Usage
Use the arrow keys or WASD to move. Use space to pause and unpause. Use R to restart after a game over. Use escape to close.
The screen is a grid with a certain width, height, and cell size. These values default to 25, 25, and 40, respectively. These values, along with the frame rate and some colors, can be changed in the following lines:
```
16 p = 40 # size of a cell in pixels
17 w = 25 # grid size in cells
18 h = 25 # grid height in cells
19 applecol = red # color of apple
20 snakecol = green # color of snake
21 target_fps = 20
```
Make sure that `snakeHigh.txt` is in the same directory as `snake.py`.

![snake](https://user-images.githubusercontent.com/68828123/184267282-6da72a58-bd68-4cb5-a051-6fd864e3a6f3.gif)

