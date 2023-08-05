from typing import Union
from time import sleep
import os


def clear_console():
    os.system('cls' if os.name == 'nt' else 'clear')


def variable_speed_print(message: str, seconds_per_char: Union[int, float] = 0):
    for char in message:
        print(char, end='')
        if char == ' ':
            sleep(seconds_per_char / 10)
        else:
            sleep(seconds_per_char)
    print()
