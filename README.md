# Snake
A terminal-based recreation of the classic snake game in Python that runs in the terminal using curses.

## Dependencies
Curses is the only dependency for this project, to install it, do:
```
pip install curses
```

## Configuration
The dimensions of the game are automatically set to the dimensions of the terminal window. Resize the terminal to change those dimensions. The target frame rate cam be changed in:
```
11 target_fps = 20 # target frames per second
```
Make sure that `snakeHigh.txt` is in the same directory as `snake.py`.

## Controls
|Key|Action|
|---|------|
|q|exit|
|space|pause|
|r|restart|
|c|toggle colors|
|left|move left|
|right|move right|
|up|move up|
|down|move down|
