import curses 
from random import randint
import signal
import sys

#constants

WIDE_MODE = True

WINDOW_WIDTH = 60  # number of columns of window box 
WINDOW_HEIGHT = 20 # number of rows of window box 
'''
Number of blocks in window per line = WINDOW_WIDTH -2. 
Block x index ranges from 1 to WINDOW_WIDTH -2.
Number of blocks in window per column = WINDOW_HEIGHT -2. 
Block y index ranges from 1 to WINDOW_HEIGHT -2.
'''



# setup window
curses.initscr()
if WIDE_MODE:
    win = curses.newwin(WINDOW_HEIGHT, WINDOW_WIDTH*2-3, 0, 0) # rows, columns
else:
    win = curses.newwin(WINDOW_HEIGHT, WINDOW_WIDTH, 0, 0) # rows, columns
    
# allow window to be properly cleared when program is exited with ctrl+c   
def signal_handler(sig, frame):
    curses.endwin()
    sys.exit(0)
signal.signal(signal.SIGINT, signal_handler)
    
def write_block(y,x,c):    
    if WIDE_MODE:            
        win.addch(y, x*2-1,c)
    else:
        win.addch(y, x,c)

win.keypad(1)
curses.noecho()
curses.curs_set(0)
win.border(0)
win.nodelay(1) # -1

# overwrite top and bottom borders so their margins are similar to sides
if WIDE_MODE:
    win.addstr(0, 0, ' '+'_'*(WINDOW_WIDTH*2-5)+' ')
    # write overline character
    win.insstr(WINDOW_HEIGHT-1, 0, ' ' +chr(175)*(WINDOW_WIDTH*2-5)+' ')
else:
    win.addstr(0, 0, ' '+'_'*(WINDOW_WIDTH-2)+' ')
    # write overline charater, use insstr to prevent scroll error
    win.insstr(WINDOW_HEIGHT-1, 0, ' '+chr(175)*(WINDOW_WIDTH-2)+' ') 
 
# snake and food
snake = [(4, 4), (4, 3), (4, 2)]
food = (6, 6)

write_block(food[0], food[1], '#')
# game logic
score = 0

ESC = 27
key = curses.KEY_RIGHT

while key != ESC:
    win.addstr(0, 2, 'Score ' + str(score) + ' ')
    win.timeout(150 - (len(snake)) // 5 + len(snake)//10 % 120) # increase speed

    prev_key = key
    event = win.getch()
    key = event if event != -1 else prev_key

    if key not in [curses.KEY_LEFT, curses.KEY_RIGHT, curses.KEY_UP, curses.KEY_DOWN, ESC]:
        key = prev_key

    # calculate the next coordinates
    y = snake[0][0]
    x = snake[0][1]
    if key == curses.KEY_DOWN:
        y += 1
    if key == curses.KEY_UP:
        y -= 1
    if key == curses.KEY_LEFT:
        x -= 1
    if key == curses.KEY_RIGHT:
        x += 1

    snake.insert(0, (y, x)) # append O(n)

    # check if we hit the border
    if y == 0: break
    if y == WINDOW_HEIGHT-1: break
    if x == 0: break
    if x == WINDOW_WIDTH -1: break

    # if snake runs over itself
    if snake[0] in snake[1:]: break

    if snake[0] == food:
        # eat the food
        score += 1
        food = ()
        while food == ():
            food = (randint(1,WINDOW_HEIGHT-2), randint(1,WINDOW_WIDTH -2))
            if food in snake:
                food = ()
        write_block(food[0], food[1], '#')
    else:
        # move snake
        last = snake.pop()
        write_block(last[0], last[1], ' ')            
    write_block(snake[0][0], snake[0][1], '*')


curses.endwin()
print(f"Final score = {score}")
