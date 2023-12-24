# DEPENDENCIES ====================================================================================

import curses # for i/o
from random import randint # to generate random apple position
from os import path # to read and write high score
from time import sleep # to manage frame rate
from datetime import datetime # ^

# CONFIGURATION ===================================================================================

w,h = 20,20 # grid width and height
target_fps = 10 # target frames per second

# FUNCTIONS =======================================================================================

def generate_apple(s:list,a:int,b:int) -> (int,int): 
    x,y = randint(0,a-1),randint(0,b-1) # random apple position
    while (y,x) in s: x,y = randint(0,a-1),randint(0,b-1) # regenerate apple if it intersects snake
    return (y,x)

def blit(scr,cell,r,c) -> None:
    if cell: # draw an apple or a snake block if the cell is filled
        if (r,c) == apple: scr.addstr('',curses.color_pair(2))
        else: scr.addstr('█',curses.color_pair(3))
    else: scr.addstr(' ') # otherwise: space

def close(score:int,highscore:int,stdscr:curses.window) -> None:
    with open(f'{dir}/snakeHigh.txt','w') as f: f.write(str(highscore)); f.close() # save highscore
    stdscr.keypad(0); curses.nocbreak(); curses.endwin() # end curses
    exit(f'GAME ENDED | SCORE: {score}') # end python with message

# SETUP  ==========================================================================================

if __name__ == '__main__': # grid setup
    w = max(10,min(100,w)); h = max(10,min(100,h)) # clamp grid dimensions
    grid = [[0]*w for _ in range(h)] # empty grid

    # game setup
    snake = [(0,0),(0,1),(0,2),(0,3)] # snake is a list of coords, starts 4 cells long
    d = 'r' # direction of snake
    score = 0; gameover = False; paused = False
    apple = generate_apple(snake,w,h)

    # read high score
    dir = path.dirname(path.realpath(__file__))
    with open(f'{dir}/snakeHigh.txt','r') as f: highscore = f.read(); f.close()
    highscore.strip()
    highscore = int(highscore)

    # i/o setup
    stdscr = curses.initscr()
    curses.start_color(); curses.use_default_colors()
    curses.cbreak(); curses.noecho()
    stdscr.nodelay(True) # make curses.getch() nonblocking
    stdscr.keypad(True) # accept keypad escape sequences
    target_frametime = 1/target_fps # target time per frame in seconds
   
    for i in range(0,8): # generate ansi colors, i values are used to draw red/green
        try: curses.init_pair(i+1,i,-1)
        except curses.ERR: pass

# EVENT LOOP  =====================================================================================

while __name__ == '__main__':
    try:
        
        # INPUT  ==================================================================================

        dt1 = datetime.now() # get current time
        input_char = stdscr.getch(); stdscr.erase() # get input and clear screen

        if input_char == ord('q'): close(score,highscore,stdscr) # quit on q
        elif input_char == ord(' '): paused ^= 1 # toggle pause on space

        if not gameover and not paused: # change direction on arrows if game is active
            # snake will not immediately go the opposite direction since it would immediately die
            if (input_char == curses.KEY_RIGHT) and d != 'l': d = 'r'
            elif (input_char == curses.KEY_LEFT) and d != 'r': d = 'l'
            elif (input_char == curses.KEY_UP) and d != 'd': d = 'u'
            elif (input_char == curses.KEY_DOWN) and d != 'u': d = 'd'
            head = snake[-1] # the snake's head is the last index

        # GAME LOGIC  =============================================================================

            # increase length of snake in current direction
            if d == 'r':
                if head[1] == w-1: snake.append((head[0],0))
                else: snake.append((head[0],head[1]+1))
            elif d == 'l':
                if head[1] == 0: snake.append((head[0],w-1))
                else: snake.append((head[0],head[1]-1))
            elif d == 'u':
                if head[0] == 0: snake.append((h-1,head[1]))
                else: snake.append((head[0]-1,head[1]))
            else:
                if head[0] == h-1: snake.append((0,head[1]))
                else: snake.append((head[0]+1,head[1]))
            
            # if the snake has reached the apple, generate a new apple and let the snake grow
            if snake[-1] == apple:
                apple = generate_apple(snake, w, h); score += 1
                highscore = max(highscore,score) # adjust high score
            else: snake.pop(0) # otherwise, cut the snake's tail so it stays the same size

            if len(snake) != len(list(set(snake))): gameover = True # kill if snake intersects self

        elif gameover: # restart on r
            if input_char == ord('r'):
                snake = [(0,0),(0,1),(0,2),(0,3)]
                apple = generate_apple(snake, w, h)
                d = 'r'; paused = False; gameover = False; score = 0

        nxt = [[0]*w for _ in range(h)] # next grid starts empty
        for block in snake: nxt[block[0]][block[1]] = 2 # add snake to next grid
        nxt[apple[0]][apple[1]] = 1 # add apple to next grid
        grid = nxt # update grid
        
        # OUTPUT  =================================================================================

        # header shoes restart prompt, "paused", or nothing depending on game state
        if gameover:
            stdscr.addstr('╭'+ '─'*((w+8-12)//2))
            stdscr.addstr('R TO RESTART',curses.color_pair(3))
            stdscr.addstr('─'*((w+8-12)//2+w%2) + '╮\n')
        elif paused:
            stdscr.addstr('╭'+ '─'*((w+8-6)//2))
            stdscr.addstr('PAUSED',curses.color_pair(3))
            stdscr.addstr('─'*((w+8-6)//2+w%2) + '╮\n')
        else: stdscr.addstr('╭'+ '─'*(w+8) + '╮\n')

        # subheader
        stdscr.addstr('│╭' + '─'*((w-5)//2))
        stdscr.addstr('SNAKE',curses.color_pair(3))
        stdscr.addstr('─'*(((w-5)//2)+((w%2)==0)) + '╮╭')
        stdscr.addstr('SCOR',curses.color_pair(3))
        stdscr.addstr('╮│\n')

        # main body
        for r in range(h):
            stdscr.addstr('││') 
            for c in range(w): blit(stdscr,grid[r][c],r,c) # snake and apple

            # score and highscore
            stdscr.addstr('│')
            if r == 0:
                stdscr.addstr('│')
                stdscr.addstr(f'{score:04}',curses.color_pair(2))
                stdscr.addstr('│')
            elif r == 2:
                stdscr.addstr('╭')
                stdscr.addstr('HIGH',curses.color_pair(3))
                stdscr.addstr('╮')
            elif r == 3:
                stdscr.addstr('│')
                stdscr.addstr(f'{highscore:04}',curses.color_pair(2))
                stdscr.addstr('│')

            # empty box to fill up height
            elif r == 5: stdscr.addstr('╭────╮')
            elif r > 5 and r != h: stdscr.addstr('│    │')

            # sides and bottoms of sidebar panels
            elif r in [8,11]: stdscr.addstr('│    │')
            elif r in [1,4]: stdscr.addstr('╰────╯')

            stdscr.addstr('│\n') # next line

        # bottom of panels
        stdscr.addstr('│╰'+'─'*w+'╯╰────╯│\n'); stdscr.addstr('╰'+ '─'*(w+8) + '╯\n')

        sleep(max(0,target_frametime-(datetime.now()-dt1).microseconds/1e6)) # maintain frame rate
        stdscr.refresh()

    except KeyboardInterrupt: close(score,highscore,stdscr) # quit on ^C