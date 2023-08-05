from typing import Union
from time import sleep
import os


def clear_console() -> None:
    os.system('cls' if os.name == 'nt' else 'clear')


def variable_speed_print(message: str,
                         seconds_per_char: Union[int, float] = 0,
                         space_ratio: Union[int, float] = 0.1,
                         seconds_newline: Union[int, float] = 0) -> None:
    for char in message:
        print(char, end='', flush=True)
        if char == '\n':
            sleep(seconds_newline)
        elif char == ' ':
            sleep(seconds_per_char * space_ratio)
        else:
            sleep(seconds_per_char)
    print()
