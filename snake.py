import pygame
from random import randint
from PIL import ImageColor # to convert hex to rgb

# colors
red = '#e06c75'
green = '#98c379'
yellow = '#e5c07b'
blue = '#61afef'
purple = '#c678dd'
teal = '#58b6c2'
orange = '#d19a66'

# =====================================================

w = 50
h = 26
p = 40
delay = 30
applecol = red
snakecol = green

# =====================================================

def generate_apple(s,a,b):
    x,y = randint(0,a-1),randint(0,b-1)
    while (y,x) in s:
        x,y = randint(0,a-1),randint(0,b-1)
    return (y,x)

w = max(30,min(100,w))
h = max(25,min(100,h))
sw = w*p
sh = h*p+4*p

grid = [[0]*w for _ in range(h)]
rgb = {0:'#282c34',1:applecol,2:ImageColor.getcolor(snakecol,'RGB')} # 0 = bg, 1 = apple, 2 = snake
snake = [(0,0),(0,1),(0,2),(0,3)] # the snake is a list of coordinates
d = 'r' # direction of the snake
score = 0
apple = generate_apple(snake,w,h)
dead = False
paused = False

with open('./snakeHigh.txt','r') as f:
    highscore = f.read()
    f.close()
highscore.strip()
highscore = int(highscore)

pygame.init()
pygame.font.init()
screen = pygame.display.set_mode((sw,sh))
font = pygame.font.Font('./font.ttf',p)

# restart
rs = font.render('press R to restart',True,(rgb[1]))
rrs = rs.get_rect()
rrs.topleft = (sw//2-9*p,sh-p-p//2)

while True:
    pygame.time.delay(delay)
    screen.fill(0x20242d)

    for event in pygame.event.get(): # close window on quit
        if event.type == pygame.QUIT:
            with open('./snakeHigh.txt','w') as f:
                f.write(str(highscore))
                f.close(); exit()

    keys = pygame.key.get_pressed() # quit on esc and pause on space
    if keys[pygame.K_ESCAPE]:
        with open('./snakeHigh.txt','w') as f:
                f.write(str(highscore))
                f.close(); exit()
    if keys[pygame.K_SPACE]: paused = not paused

    if not dead and not paused:
        # change direction on input
        if keys[pygame.K_RIGHT] and d != 'l': d = 'r'
        elif keys[pygame.K_LEFT] and d != 'r': d = 'l'
        elif keys[pygame.K_UP] and d != 'd': d = 'u'
        elif keys[pygame.K_DOWN] and d != 'u': d = 'd'

        # the snake's head is the last index
        head = snake[-1]

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
        elif d == 'd':
            if head[0] == h-1: snake.append((0,head[1]))
            else: snake.append((head[0]+1,head[1]))
        
        # if the snake has reached the apple, generate a new apple and let the snake grow
        if snake[-1] == apple: apple = generate_apple(snake, w, h); score += 1
        else: snake.pop(0) # otherwise, cut the snake's tail so it stays the same size

        # kill if snake's head intersects itself
        if snake.index(snake[-1]) != len(snake)-1: dead = True

        highscore = max(highscore,score) # adjust high score
    
    elif dead: # restard on R key
        screen.blit(rs,rrs)
        if keys[pygame.K_r]:
            snake = [(0,0),(0,1),(0,2),(0,3)]
            apple = generate_apple(snake, w, h)
            d = 'r'
            paused = False
            dead = False
            score = 0

    # score
    sc = font.render(f'score:{score:04}',True,rgb[1])
    rsc = sc.get_rect()
    rsc.topleft = (p,p//2)
    # high score
    hs = font.render(f'high score:{highscore:04}',True,rgb[1])
    rhs = hs.get_rect()
    rhs.topleft = (sw-16*p,p//2)

    # display score and high score
    screen.blit(sc,rsc)
    screen.blit(hs,rhs)

    # snake 
    nxt = [[0]*w for _ in range(h)]
    for block in snake:
        nxt[block[0]][block[1]] = 2
    
    # apple
    nxt[apple[0]][apple[1]] = 1
    
    # draw grid
    grid = nxt
    for r in range(h):
        for c in range(w):
            pygame.draw.rect(screen,rgb[grid[r][c]],(c*p,r*p+2*p,p,p))

    pygame.display.update()