from typing import Union, cast
from .parse_tree import ParseTree
from .utils.modes import Mode
from .utils.io_utils import clear_console, variable_speed_print


class InteractivePlayground:
    def __init__(self, run_on_init: bool = False) -> None:
        self.__current_mode = Mode.DISPLAY, Mode.EVAL
        if run_on_init:
            self.run()

    # Introductory Menu
    def introduction(self) -> None:
        greeting = 'Greetings...\n'\
                   '\n'\
                   '                \"This is a utility program which aims\n'\
                   '                    to show the beauty of parse trees\n'\
                   '                           in a fun and engaging way\"\n'\
                   '\n'\
                   'Don\'t be intimidated :)\n'\
                   'It was designed to be easy to use, yet extensible.\n'\
                   '\n'\
                   '                                               Enjoy!'
        variable_speed_print(message=greeting, seconds_per_char=0.1)

    # Help Menu
    def help(self) -> str:
        return 'HELP MENU'

    def mode(self, ) -> None:
        mode_list = 'CURRENTLY SUPPORTED MODES'\
                    '-------------------------'\
                    '1. '

    # REPL Simulation

    def run(self):
        '''
        Runs the animated_parse_tree program interactively

        Parameters
        ----------
        **kwargs
            Keyword arguments to be passed to ParseTree().animate.

        Returns
        -------
        None
            This program does not return anything.

        Examples
        --------
        ```bash
        ?> 1 + 2
        1 + 2 = 3

        +
        / \\
        1 2
        ```
        '''
        clear_console()
        self.introduction()
        expression = input('?> ')
        while expression not in {'', 'exit', 'quit'}:
            try:
                t = ParseTree()
                t.read(expression)
                print(str(t))
                print()
                print(expression, '=', round(
                    cast(Union[int, float], t.evaluate()), 5))
            except Exception as e:
                print(e)
            finally:
                expression = input('?> ')
        print('Bye :)')


if __name__ == '__main__':
    MAIN = InteractivePlayground()
    MAIN.run()
