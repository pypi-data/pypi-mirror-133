# from typing import Dict, List, cast

# from .utils.io_utils import clear_console

# from .node import Node
# from .operand_ import Operand
# from .operator_ import Operator

# from .utils.string_utils import concatenate_horizontally, simplify_expression
# from .parser import Parser
# from .lexer import Lexer
# from .tokenizer import Tokenizer
# import os
# from copy import deepcopy
# from time import sleep


# class Scene:
#     def __init__(self,
#     parse_tree_class,
#                  token_lookup: Dict,
#                  implicit_operator: Operator,
#                  seconds_per_frame: int = 1) -> None:
#         self.parse_tree_class = parse_tree_class
#         self.token_lookup = token_lookup
#         self.implicit_operator = implicit_operator
#         self.seconds_per_frame = seconds_per_frame

#     def stencil(self, expression, tokens=None, lexed=None, parsed=None, tree=None) -> None:
#         clear_console()
#         if tokens is None:
#             process = 'TOKENIZATION'
#         elif lexed is None:
#             process = 'LEXING'
#         elif parsed is None:
#             process = 'PARSING'
#         elif tree is None:
#             process = 'BUILDING PARSE TREE'
#         else:
#             process = 'REDUCING PARSE TREE'
#         print(f'CURRENT PROCESS: {process}')
#         print()
#         print(f'Expression: {expression}')
#         if tokens is not None:
#             print()
#             print('TOKENS >>>')
#             print(tokens)
#         if lexed is not None:
#             print()
#             print('LEXED TOKENS >>>')
#             print(lexed)
#             print()
#         if parsed is not None:
#             print('PARSED TOKENS >>>')
#             print(parsed)
#             print()
#         if tree is not None:
#             print('COMPLETE PARSE TREE >>>')
#             print(tree)
#             print()

#     def animate_tokenization(self, expression):
#         tokens: List[str] = []
#         for i, j, t in Tokenizer(token_lookup=self.token_lookup).tokenize(expression=expression, kind='lazy'):
#             self.stencil(expression)
#             print(' ' * (i + 12) + '\u2191' + ' ' * (j - i - 1) + '\u2191')
#             print(' ' * (i + 12) + 'i' + ' ' * (j - i - 1) + 'j')
#             print(t)
#             tokens = t
#             sleep(self.seconds_per_frame)
#         return tokens

#     def animate_lexing(self, expression, tokens):
#         lexed = []
#         prefix = 1
#         for o, c, l, t in Lexer(token_lookup=self.token_lookup, implicit_operator=self.implicit_operator).lex(tokens=tokens, kind='lazy'):
#             self.stencil(expression, tokens)
#             arrow = '\u2191'
#             print(' ' * prefix + f'{arrow:^{len(t) + 2}}')
#             print(f'(: {o}; ): {c}')
#             print(l)
#             lexed = l
#             sleep(self.seconds_per_frame)
#             prefix += len(t) + 4
#         return lexed

#     def animate_parsing(self, lexed):
#         return Parser(token_lookup=self.token_lookup, implicit_operator=self.implicit_operator).parse(lexed)

#     def animate_building(self, expression, tokens, lexed, parsed):
#         tree = None
#         for i in range(1, len(parsed) + 1):
#             self.stencil(expression, tokens, lexed, parsed)
#             tmp_parsed = deepcopy(parsed[:i])
#             t = self.parse_tree_class()
#             t.build_sub_tree(tmp_parsed)
#             print(t)
#             tree = t
#             sleep(self.seconds_per_frame)
#         return tree

#     def animate_reduction(self, expression, tokens, lexed, parsed, tree, tree_repr):
#         reduced_tree = tree
#         prev_display = ''
#         for t in self.dfs_reduce(node=tree.root, tree=tree):
#             if str(t) == prev_display:
#                 continue
#             self.stencil(expression, tokens, lexed, parsed, tree_repr)
#             prev_display = str(t)
#             print(prev_display)
#             sleep(self.seconds_per_frame)
#         self.stencil(expression, tokens, lexed, parsed, tree_repr)
#         reduced_tree.root = Operand(value=reduced_tree.root())
#         print(str(reduced_tree))
#         return reduced_tree.root

#     def dfs_reduce(self, node: Node, tree):
#         for c in node.children:
#             yield from self.dfs_reduce(c, tree)
#         for i, c in enumerate(node.children):
#             node.children[i] = Operand(value=c())
#             yield tree

#     def animate(self, expression):
#         expression_stripped = simplify_expression(expression)
#         tokens = self.animate_tokenization(expression_stripped)
#         lexed = self.animate_lexing(expression_stripped, tokens)
#         parsed = self.animate_parsing(lexed)
#         t = self.animate_building(expression_stripped, tokens, lexed, parsed)
#         complete_tree = str(t)
#         result = self.animate_reduction(
#             expression, tokens, lexed, parsed, t, complete_tree)
#         self.stencil(expression_stripped, tokens, lexed, parsed, complete_tree)
#         print('REDUCED PARSE TREE >>>')
#         print(result)
#         print()
#         print('EVALUATION >>>')
#         result = t.evaluate()
#         print(expression, '=', round(result, 5))
#         return result
