# Snake
A terminal-based recreation of the classic snake game in Python.

## Dependencies
Curses is the only dependency for this project, to install it, do:
```
pip install curses
```

## Configuration
The dimensions of the game grid and target FPS can be changes in the following lines:
```
11 w,h = 20,20 # grid width and height
12 target_fps = 10 # target frames per second
```
Make sure that `snakeHigh.txt` is in the same directory as `snake.py`.

## Controls
|Key|Action|
|---|------|
|q|exit|
|space|pause|
|r|restart|
|left|move left|
|right|move right|
|up|move up|
|down|move down|

![snake](https://user-images.githubusercontent.com/68828123/184267282-6da72a58-bd68-4cb5-a051-6fd864e3a6f3.gif)

