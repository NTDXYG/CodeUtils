import random


class Mutation:
    def __init__(self, code: str):
        self.code = code

class ReplacementMutation(Mutation):
    '''Replacement Mutation'''
    OPERATORS = []
    def __init__(self, code: str, src: str, tgt: str):
        super().__init__(code)
        self.src = src
        self.tgt = tgt
        # self.flag = 0
        # self.number = [str(i) for i in range(10)]

    def mutate(self):
        outputs = []
        for line in self.code.split('\n'):
            # if number is in the line, replace it with a random number
            # if any([x in line for x in self.number]) and self.flag == 0:
            #     for i in range(len(self.number)):
            #         if self.number[i] in line.split() and random.random() < 0.5:
            #             self.flag = 1
            #             line = line.replace(self.number[i], random.choice(self.number))
            #             break
            outputs.append(line.replace(self.src, self.tgt))
        return '\n'.join(outputs)

class AOR(ReplacementMutation):
    '''Arithmetic Operator Replacement'''
    OPERATORS = [' + ', ' - ', ' * ', ' / ', ' ** ', ' % ']

class ROR(ReplacementMutation):
    '''Relational Operator Replacement'''
    OPERATORS = [' > ', ' < ', ' >= ', ' <= ', ' == ', ' != ']

class COR(ReplacementMutation):
    '''Conditional Operator Replacement'''
    OPERATORS = [' && ', ' || ', ' & ', ' | ', ' ^ ']

class SOR(ReplacementMutation):
    '''Shift Operator Replacement'''
    OPERATORS = [' << ', ' >> ', ' >>> ']

class LOR(ReplacementMutation):
    '''Logical Operator Replacement'''
    OPERATORS = [' & ', ' | ', ' ^ ']

class ASR(ReplacementMutation):
    '''Assignment Operator Replacement'''
    OPERATORS = [' = ', ' += ', ' -= ', ' *= ', ' /= ', ' %= ', ' **= ']
