import curses
import random
import time

def main(stdscr):
    # Setup initial game state
    curses.curs_set(0)  # Hide cursor
    curses.init_pair(1, curses.COLOR_GREEN, curses.COLOR_BLACK)  # Snake color
    curses.init_pair(2, curses.COLOR_RED, curses.COLOR_BLACK)    # Food color
    curses.init_pair(3, curses.COLOR_CYAN, curses.COLOR_BLACK)   # Border color
    curses.init_pair(4, curses.COLOR_YELLOW, curses.COLOR_BLACK) # Score color
    
    # Set up the screen
    sh, sw = stdscr.getmaxyx()
    w = curses.newwin(sh, sw, 0, 0)
    w.keypad(1)
    w.timeout(100)  # Refresh rate in ms
    
    # Initial snake position (middle of the screen)
    snake_x = sw // 4
    snake_y = sh // 2
    
    # Initial snake body
    snake = [
        [snake_y, snake_x],
        [snake_y, snake_x - 1],
        [snake_y, snake_x - 2]
    ]
    
    # Initial food position
    food = [sh // 2, sw // 2]
    w.addch(food[0], food[1], curses.ACS_DIAMOND, curses.color_pair(2))
    
    # Initial movement direction (right)
    key = curses.KEY_RIGHT
    
    # Score
    score = 0
    
    # Game boundaries
    min_y, max_y = 1, sh - 2
    min_x, max_x = 1, sw - 2
    
    # Draw border
    draw_border(w, min_y, min_x, max_y, max_x)
    
    # Game loop
    while True:
        # Display score
        w.addstr(0, 2, f" SCORE: {score} ", curses.color_pair(4))
        
        # Get next key
        next_key = w.getch()
        key = key if next_key == -1 else next_key
        
        # Check if game is over (hitting the border)
        if (snake[0][0] <= min_y or snake[0][0] >= max_y or 
            snake[0][1] <= min_x or snake[0][1] >= max_x):
            game_over(w, score)
            break
        
        # Check if snake hits itself
        if snake[0] in snake[1:]:
            game_over(w, score)
            break
        
        # Determine new head based on key press
        new_head = [snake[0][0], snake[0][1]]
        
        if key == curses.KEY_DOWN:
            new_head[0] += 1
        elif key == curses.KEY_UP:
            new_head[0] -= 1
        elif key == curses.KEY_LEFT:
            new_head[1] -= 1
        elif key == curses.KEY_RIGHT:
            new_head[1] += 1
        
        # Insert new head
        snake.insert(0, new_head)
        
        # Check if snake ate the food
        if snake[0] == food:
            # Increase score
            score += 10
            
            # Create new food
            while True:
                food = [random.randint(min_y + 1, max_y - 1), 
                        random.randint(min_x + 1, max_x - 1)]
                if food not in snake:
                    break
            w.addch(food[0], food[1], curses.ACS_DIAMOND, curses.color_pair(2))
        else:
            # Remove tail
            tail = snake.pop()
            w.addch(tail[0], tail[1], ' ')
        
        # Draw snake
        for i, segment in enumerate(snake):
            character = curses.ACS_BLOCK if i == 0 else curses.ACS_CKBOARD
            try:
                w.addch(segment[0], segment[1], character, curses.color_pair(1))
            except curses.error:
                pass  # Ignore errors when drawing at the edge

def draw_border(win, min_y, min_x, max_y, max_x):
    """Draw a border around the game area"""
    # Draw corners
    win.addch(min_y, min_x, curses.ACS_ULCORNER, curses.color_pair(3))
    win.addch(min_y, max_x, curses.ACS_URCORNER, curses.color_pair(3))
    win.addch(max_y, min_x, curses.ACS_LLCORNER, curses.color_pair(3))
    win.addch(max_y, max_x, curses.ACS_LRCORNER, curses.color_pair(3))
    
    # Draw horizontal lines
    for x in range(min_x + 1, max_x):
        win.addch(min_y, x, curses.ACS_HLINE, curses.color_pair(3))
        win.addch(max_y, x, curses.ACS_HLINE, curses.color_pair(3))
    
    # Draw vertical lines
    for y in range(min_y + 1, max_y):
        win.addch(y, min_x, curses.ACS_VLINE, curses.color_pair(3))
        win.addch(y, max_x, curses.ACS_VLINE, curses.color_pair(3))

def game_over(win, score):
    """Display game over screen with final score"""
    h, w = win.getmaxyx()
    text = f" GAME OVER! Final Score: {score} "
    x = w // 2 - len(text) // 2
    y = h // 2
    
    win.clear()
    win.addstr(y, x, text, curses.color_pair(2) | curses.A_BOLD)
    win.addstr(y + 2, x, " Press any key to exit... ", curses.color_pair(4))
    win.refresh()
    win.getch()

if __name__ == "__main__":
    try:
        # Initialize curses
        curses.initscr()
        curses.start_color()
        curses.wrapper(main)
    finally:
        # Clean up terminal
        curses.endwin()
        print("Snake Game ended. Thanks for playing!")

