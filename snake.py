# DEPENDENCIES ====================================================================================

import curses # for i/o
from random import randint # to generate random apple position
from os import path # to read and write high score
from datetime import datetime # to manage frame rate
from time import sleep #      ^

# CONFIGURATION ===================================================================================

target_fps = 20 # target frames per second

# FUNCTIONS =======================================================================================

def init_dimens(screen:curses.window) -> (bool,int,int): # get dimensions of game from terminal
    h,w = screen.getmaxyx()[0]-2,screen.getmaxyx()[1]-2; f = True
    if w < 25 or h < 25: f = False # the screen is not functional if the dimensions are too small
    #w = h
    return f,w,h # return whether the screen is big enough and dimens

def generate_apple(s:list[(int,int)],a:int,b:int) -> (int,int): 
    x,y = randint(0,a-1),randint(0,b-1) # random apple position
    while (y,x) in s: x,y = randint(0,a-1),randint(0,b-1) # regenerate apple if it intersects snake
    return (y,x)

def close(score:int,highscore:int,stdscr:curses.window) -> None:
    with open(f'{dir}/snakeHigh.txt','w') as f: f.write(str(highscore)); f.close() # save highscore
    stdscr.keypad(0); curses.nocbreak(); curses.endwin() # end curses
    exit(f'GAME ENDED | SCORE: {score}') # end python with message

# SETUP ===========================================================================================

if __name__ == '__main__':

    # i/o setup
    fullscr = curses.initscr()
    curses.start_color(); curses.use_default_colors() # use ansi colors
    #curses.cbreak(); curses.noecho(); fullscr.nodelay(True) # make getch() nonblocking
    #curses.curs_set(0); fullscr.keypad(True) # hide mouse and allow keyboard input
    target_frametime = 1/target_fps # target time per frame in seconds

    f,w,h = init_dimens(fullscr) # get dimens
    stdscr = fullscr.subwin(h+2,w+2,0,0)
    curses.cbreak(); curses.noecho(); stdscr.nodelay(True)
    curses.curs_set(0); stdscr.keypad(True)

    grid = [[0]*w for _ in range(h)] # empty grid
    tui_color = True # game starts with colors

    # game setup
    snake = [(0,0),(0,1),(0,2),(0,3)] # snake is a list of coords, starts 4 cells long
    d = 'r'; score = 0; gameover = False; paused = False # snake direction, score, and game state
    apple = generate_apple(snake,w,h) # apple is at a random position

    # read high score
    dir = path.dirname(path.realpath(__file__))
    with open(f'{dir}/snakeHigh.txt','r') as f: highscore = int(f.read().strip()); f.close()
   
    for i in range(0,3): # generate ansi colors, i values are used to draw red/green
        try: curses.init_pair(i+1,i,-1)
        except curses.ERR: pass

    color_map = {True:[2,3],False:[0,0]}

# EVENT LOOP ======================================================================================

while __name__ == '__main__':
    try:
        # INPUT ===================================================================================

        
        dt1 = datetime.now() # get current time
        input_char = stdscr.getch(); stdscr.erase() # get input and clear screen

        if input_char == curses.KEY_RESIZE: # reset game if window is resized
            curses.resize_term(30,30)
            f,w,h = init_dimens(stdscr); # get new dimens
            snake = [(0,0),(0,1),(0,2),(0,3)]; apple = generate_apple(snake, w, h)
            d = 'r'; arrow = '→'; paused = True; gameover = False; score = 0

        elif input_char == ord('q'): close(score,highscore,stdscr) # quit on q
        elif input_char == ord(' '): paused ^= 1 # toggle pause on space
        elif input_char == ord('c'): tui_color ^= 1

        if gameover: # restart on r
            if input_char == ord('r'):
                snake = [(0,0),(0,1),(0,2),(0,3)]; apple = generate_apple(snake, w, h)
                d = 'r'; arrow = '→'; paused = False; gameover = False; score = 0

        elif not gameover and not paused and f: # change direction on arrows if game is active
            # snake will not immediately go the opposite direction since it would immediately die
            if (input_char == curses.KEY_RIGHT) and d != 'l': d = 'r'
            elif (input_char == curses.KEY_LEFT) and d != 'r': d = 'l'
            elif (input_char == curses.KEY_UP) and d != 'd': d = 'u'
            elif (input_char == curses.KEY_DOWN) and d != 'u': d = 'd'
            head = [snake[-1][0],snake[-1][1]] # the snake's head is the last index

        # GAME LOGIC ==============================================================================

            # increase length of snake in current direction
            if d == 'r':   arrow = '→'; head[1] += 1
            elif d == 'l': arrow = '←'; head[1] -= 1
            elif d == 'u': arrow = '↑'; head[0] -= 1
            else:          arrow = '↓'; head[0] += 1
            
            snake.append((head[0]%h,head[1]%w))
            # if the snake has reached the apple, generate a new apple and let the snake grow
            if snake[-1] == apple:
                apple = generate_apple(snake, w, h); score += 1
                highscore = max(highscore,score) # adjust high score
            else: snake.pop(0) # otherwise, cut the snake's tail so it stays the same size

            if len(snake) != len(list(set(snake))): gameover = True # kill if snake intersects self

        nxt = [[0]*w for _ in range(h)] # next grid starts empty
        for block in snake: nxt[block[0]][block[1]] = 2 # add snake to next grid
        nxt[apple[0]][apple[1]] = 1 # add apple to next grid
        grid = nxt # update grid
        
        # OUTPUT ==================================================================================

        if f: # if the screen is big enough to draw on
            stdscr.border() # border
            # draw apple
            stdscr.addstr(apple[0]+1,apple[1]+1,'',curses.color_pair(color_map[tui_color][0]))
            for block in snake: # draw snake
                stdscr.addstr(block[0]+1,block[1]+1,'█',curses.color_pair(color_map[tui_color][not gameover]))
            stdscr.addstr(0,1,f' {score} ') # score text
            stdscr.addstr(h+1,1,f' {highscore} ') # high score text
            dims = f' {w}x{h} '; stdscr.addstr(h+1,w+1-len(dims),dims) # show dimens
            if gameover: stdscr.addstr(0,w-12,'R TO RESTART') # restart text
            elif paused:
                stdscr.addstr(snake[-1][0]+1,snake[-1][1]+1,arrow, # draw arrow to show snake...
                curses.color_pair(color_map[tui_color][1])) # ...direction when paused
                stdscr.addstr(0,w-6,'PAUSED') # paused text
        else: stdscr.addstr('Window is not big enough (need at least 25x25).') # error text

        sleep(max(0,target_frametime-(datetime.now()-dt1).microseconds/1e6)) # maintain frame rate
        stdscr.refresh()

except KeyboardInterrupt: close(score,highscore,stdscr) # quit on ^C
