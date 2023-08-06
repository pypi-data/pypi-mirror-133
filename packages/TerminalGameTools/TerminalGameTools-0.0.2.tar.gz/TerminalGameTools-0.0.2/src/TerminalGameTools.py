import colorama
from getch import getch

def move_cursor(x: int, y: int):
    '''
    colorama.init must be called for this function to work
    Uses ANSI escape codes to move the cursor to an absolute position.
    :x: the x coordinate to move to. the smallest value that will do anything is 1
    :y: the y coordinate to move to. the smallest value that will do anything is 1
    '''
    print(f'\033[{y};{x}H', end='', flush=True)

def move_cursor_rel(x: int, y: int):
    '''
    colorama.init must be called for this function to work
    Uses ANSI escape codes to move the cursor to a relative position
    :x: the x coordinate to move relatively
    :y: the y coordinate to move relatively
    '''
    if y < 0: # y is less than 0
        print(f'\033[{abs(y)}A', end='', flush=True) # move y down
    elif y > 0: # y is more than 0
        print(f'\033[{y}B', end='', flush=True) # move abs(y) up
    if x > 0: # x is more than 0
        print(f'\033[{x}C', end='', flush=True) # move x right
    elif x < 0: # x is less than 0
        print(f'\033[{abs(x)}D', end='', flush=True) # move abs(x) left

def give_options(options: list[any], cursor: str = '>', prompt: str = None, starting_index: int = 0) -> (int, any):
    '''
    colorama.init must be called for this function to work
    Allows the user to select from a list of options visually using arrow keys/wasd and enter/space
    :options: a list of options that will be displayed
    :cursor: the cursor that will be printed before the current option
    :prompt: the prompt to be printed before the the menu
    :starting_index: the index the cursor will start at
    :returns: a tuple containing the index of the selected item and the value
    '''
    cursor_len = len(cursor)
    options_len = len(options)
    empty_cursor = ' ' * cursor_len
    current_index = starting_index
    def up():
        nonlocal current_index
        current_index -= 1
        if current_index < 0:
            current_index += options_len
    def down():
        nonlocal current_index
        current_index += 1
        if current_index >= options_len:
            current_index %= options_len
    if prompt is not None:
        print(prompt)
    while 1:
        for i, item in enumerate(options):
            print(cursor if current_index == i else empty_cursor, item)
        match getch().lower():
            case 'w':
                up()
            case 's':
                down()
            case ' ' | '\n':
                break
            case '\x1b': # special key
                match getch() + getch():
                    case '[A': # up arrow
                        up()
                    case '[B': # down arrow
                        down()
        move_cursor_rel(0, -options_len)
    return current_index, options[current_index]

def get_yes_no_response(cursor: str = '>', prompt: str = None) -> bool:
    '''
    colorama.init must be called for this function to work
    Allows a user to select yes or no using arrow keys/wasd and enter/space
    :cursor: the cursor that will be printed before the current option
    :prompt: the prompt to be printed before the the menu
    :returns: a boolean; True if yes was selected and False if No was
    '''
    return not give_options(['Yes', 'No'], cursor, prompt)

def get_response(prompt: str = '') -> str:
    '''
    Asks user for input then waits for input
    :prompt: The string to print before
    :returns: the string entered by the user
    '''
    if not prompt:
        prompt = 'Please enter {}: '
    return input(prompt)
