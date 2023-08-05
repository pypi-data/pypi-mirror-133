from typing import List


def strip_whitespace(string: str) -> str:
    return string.replace(' ', '')


def simplify_expression(expr: str) -> str:
    return strip_whitespace(expr).lower()


def concatenate_horizontally(*args: str) -> str:
    string_list: List[List[str]] = []
    for string in args:
        string_list.append(string.splitlines())
    result = ''
    total_height = max(map(lambda ls: len(ls), string_list))
    for i in range(total_height):
        for ls in string_list:
            try:
                result += ls[i]
            except IndexError:
                pass
        result += '\n'
    return result


def pad(left_pad: int, body: str, right_pad: int, pad_char: str = ' '):
    return pad_char * left_pad + body + pad_char * right_pad
