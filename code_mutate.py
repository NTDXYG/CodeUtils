import random
from itertools import combinations
from program_mutation import mutation

code = """
from math import sqrt
import pandas as pd

def allBitsSetInTheGivenRange ( n , l , r ) :
    num = ( ( 1 << r ) - 1 ) ^ ( ( 1 << ( l - 1 ) ) - 1 )
    new_num = n & num
    if ( new_num == 0 ) :
        return "Yes"
    return "No"
"""

MUTATORS = [mutation.AOR, mutation.ROR, mutation.COR, mutation.SOR, mutation.LOR, mutation.ASR]

def apply(code, return_num=1):
    datas = []
    for mutator_class in MUTATORS:
        for o1, o2 in combinations(mutator_class.OPERATORS, 2):
            mutator = mutator_class(code, o1, o2)
            m = mutator.mutate()
            if m != code:
                datas.append(m)
    return random.sample(datas, return_num)

if __name__ == '__main__':
    print(apply(code, return_num=1)[0])