from typing import Dict, List, Union, cast

from .utils.string_utils import simplify_expression
from .parse_tree import ParseTree
from .utils.mode import Mode
from .utils.io_utils import clear_console, variable_speed_print
from sys import argv


class InteractivePlayground:
    def __init__(self, run_on_init: bool = False, *args, **kwargs) -> None:
        self.__options = args
        self.__current_mode: Union[Mode, List[Mode]] = [
            Mode.DISPLAY, Mode.EVAL]
        self.__mode_dict: Dict[str, Mode] = {
            'a': Mode.ANIMATE,
            'd': Mode.DISPLAY,
            'e': Mode.EVAL
        }
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
        variable_speed_print(message=greeting, seconds_per_char=0.05)

    # Help Menu
    def help(self) -> None:
        help_menu = 'HELP MENU\n'\
                    '=========\n'\
                    'Enter:\n'\
                    '?> help\n'\
                    '         to display this help menu\n'\
                    '?> mode\n'\
                    '         to select your mode'
        print(help_menu)

    def mode(self, ) -> None:
        mode_list = 'CURRENTLY SUPPORTED MODES\n'\
                    '-------------------------\n'\
                    'a. ANIMATE\n'\
                    'd. DISPLAY\n'\
                    'e. EVAL\n\n'\
                    f'current mode: {self.__current_mode}'
        print(mode_list)
        new_mode = simplify_expression(
            input('Enter your desired mode (or permutation thereof): '))
        if new_mode != '':
            if ',' in new_mode:
                self.__current_mode = [self.__mode_dict[m]
                                       for m in new_mode.split(sep=',')]
            else:
                self.__current_mode = self.__mode_dict[new_mode]

    def perform_action(self, parse_tree: ParseTree, action: Mode):
        if action == Mode.ANIMATE:
            parse_tree.animate(1)
        elif action == Mode.DISPLAY:
            print(str(parse_tree))
        elif action == Mode.EVAL:
            print(parse_tree.expression, '=', round(
                cast(Union[int, float], parse_tree.evaluate()), 5))
        print()

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
        if '-q' not in self.__options:
            self.introduction()
        expression = input('?> ')
        while expression not in {'', 'exit', 'quit'}:
            try:
                if expression == 'mode':
                    self.mode()
                elif expression == 'help':
                    self.help()
                else:
                    t = ParseTree()
                    t.read(expression)
                    if type(self.__current_mode) is list:
                        for action in self.__current_mode:
                            self.perform_action(parse_tree=t, action=action)
                    else:
                        self.perform_action(
                            parse_tree=t, action=cast(Mode, self.__current_mode))
            except KeyError as e:
                print(f'Invalid mode {e}')
            except Exception as e:
                print(e)
            finally:
                expression = input('?> ')
        print('Bye :)')


if __name__ == '__main__':
    MAIN = InteractivePlayground(False, *argv)
    MAIN.run()
