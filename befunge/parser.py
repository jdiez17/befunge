from befunge.language import Instructions
from befunge.core import Cell

import re

class Parser(object):
    def __init__(self, content):
        self.content = content 

    def lex_char(self, c):
        kind = 'CHAR'

        for i, r in Instructions:
            match = r.search(c)

            if match:
                kind = i

        return {'kind': kind, 'value': c}
    
    def get_program(self):
        rows = []
        column = []
        for line in self.content.splitlines():
            for char in line:
                column.append(self.lex_char(char))

            rows.append(column)
            column = []
       
        return rows
