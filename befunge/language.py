import inspect
import re

class BaseInstructions(object):
    def __init__(self):
        # Ideally this would be a dict comprehension.
        instr = [n for n, obj in inspect.getmembers(self) 
            if not n.startswith("__") and not inspect.isroutine(obj)]

        self.instructions = dict() 
        for i in instr:
           self.instructions[i] = re.compile(getattr(self, i))

    def __iter__(self):
        return iter(self.instructions.items())

class Befunge93Instructions(BaseInstructions):
    NUMBER = r"([0-9])"
    ADDITION = r"\+"
    SUBTRACTION = r"\-"
    MULTIPLICATION = r"\*"
    INT_DIVISION = r"\\"
    MODULO = r"%"
    NOT = r"\!"
    GREATER_THAN = r"`"
    MOVE_RIGHT = r"\>"
    MOVE_LEFT = r"\<"
    MOVE_UP = r"\^"
    MOVE_DOWN = r"v"
    MOVE_RANDOM = r"\?"
    COND_X = r"\_"
    COND_Y = r"\|"
    STRING_MODE = r"\""
    DUP = r"\:"
    SWAP = r"\\"
    POP = r"\$"
    OUTPUT_INT = r"\."
    OUTPUT_CHAR = r","
    SKIP = r"#"
    PUT = r"p"
    GET = r"g"
    INPUT_INT = r"\&"
    INPUT_CHAR = r"~"
    END = r"@"
    NOP = r"\ "

    def __init__(self):
        BaseInstructions.__init__(self)

Instructions = Befunge93Instructions() # We always want to have this instantiated.
