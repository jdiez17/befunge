from befunge.parser import Parser
from befunge.datasource import Terminal

import sys
import random

class Interpreter(object):
    pc = [0, 0]
    stack = []
    direction = '>'
    string_mode = False
    running = False

    height = 25
    width = 80
    
    debug = False

    def __init__(self, content):
        parser = Parser(content)

        self.__datasource = Terminal() 
        self.__parser = parser
        self.__program = parser.get_program()
  
    def execute(self, debug=True):
        self.debug = debug
        self.running = True
        
        if self.debug:
            print self.__program

        while self.running:
            self.step()
            self.__increment_pc()
 
        print 

    def __pop_two(self):
        return (self.__pop(), self.__pop())

    def __push(self, i):
        return self.stack.append(i)

    def __pop(self):
        return self.stack.pop()
         
    def __increment_pc(self):
        delta = {
            '>': [0, 1],
            '<': [0, -1],
            '^': [-1, 0],
            'v': [1, 0],
        }.get(self.direction, [0, 0])
 
        self.pc = [self.pc[0] + delta[0], self.pc[1] + delta[1]]
 
        # Wrap around the y axis.         
        if self.pc[0] < 0 and self.direction == '^': 
            self.pc[0] = self.height
        if self.pc[0] > self.height and self.direction == 'v':
            self.pc[0] = 0

        # Wrap around the x axis.
        if self.pc[1] < 0 and self.direction == '<':
            self.pc[1] = self.width
        if self.pc[1] > self.width and self.direction == '>':
            self.pc[1] = 0

       
   
    def step(self):
        x, y = self.pc[0], self.pc[1] 
        try:
            instruction = self.__program[x][y]
        except IndexError:
            instruction = {'kind': 'NOP', 'value': ' '}

        self.op(instruction['kind'], instruction['value'])
   
    def op(self, kind, value):
        if self.string_mode and kind != 'STRING_MODE':
            self.__push(ord(value))
        else:
            # State changers.
            if kind == 'STRING_MODE':
                self.string_mode = not self.string_mode
            if kind in ['MOVE_RIGHT', 'MOVE_LEFT', 'MOVE_UP', 'MOVE_DOWN']:
                self.direction = value
            if kind == 'MOVE_RANDOM':
                self.direction = random.choice(['v', '^', '<', '>'])
            if kind == 'NUMBER':
                self.__push(int(value))
            if kind == 'SKIP':
                self.__increment_pc()
            
            ## Conditionals.
            if kind == 'COND_X':
                self.direction = '>' if self.__pop() == 0 else '<'
            if kind == 'COND_Y':
                self.direction = 'v' if self.__pop() == 0 else '^'
            
            # Operations.
            if kind == 'ADDITION':
                (a, b) = self.__pop_two()
                self.__push(a + b)
            if kind == 'MULTIPLICATION':
                (a, b) = self.__pop_two()
                self.__push(a * b)
            if kind == 'DUP':
                try:
                    val = self.stack[-1]
                except IndexError:
                    val = 0

                self.__push(val)
            if kind == 'SUBTRACTION':
                (a, b) = self.__pop_two()

                self.__push(b - a)
            if kind == 'SWAP':
                (a, b) = self.__pop_two()

                self.__push(a)
                self.__push(b)
            if kind == 'GREATER_THAN':
                a, b = self.__pop_two()

                self.__push(1 if b > a else 0)
            if kind == 'LOGICAL_NOT':
                a = self.__pop()

                self.__push(1 if a == 0 else 0)
            if kind == 'MODULO':
                (a, b) = self.__pop_two()
                
                self.__push(a % b)
            if kind == 'INT_DIVISION':
                (a, b) = self.__pop_two()
                
                self.__push(b / a) 


            # IO.
            if kind == 'OUTPUT_INT':
                self.__datasource.write(str(self.__pop()))
            if kind == 'OUTPUT_CHAR':
                self.__datasource.write(chr(self.__pop()))

            if kind == 'INPUT_CHAR':
                self.__push(ord(self.__datasource.next()))
            if kind == 'INPUT_INT':
                self.__push(int(self.__datasource.next()))

            # Reflection.
            if kind == 'GET':
                instruction = self.__program[self.__pop()][self.__pop()]
                self.__push(ord(instruction['value']))

            if kind == 'PUT':
                y, x = self.__pop_two()
                v = self.__pop()

                self.__program[y][x] = self.__parser.lex_char(chr(v))
    
            if kind == 'END':
                self.running = False

        if self.debug:
            print x, y, instruction, self.stack
