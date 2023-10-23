from asts.ast_parser import get_xsbt, parse_ast, extract_method_vars, extract_method_invocation, \
    extract_method_params, get_method_name
from preprocessing.lang_processors.python_processor import PythonProcessor
import string

funs = ['abs', 'all', 'any', 'ascii', 'bin', 'bool', 'breakpoint', 'bytearray', 'bytes',
        'callable', 'chr', 'classmethod', 'compile', 'complex', 'delattr', 'dict', 'dir',
        'divmod', 'enumerate', 'eval', 'exec', 'filter', 'float', 'format', 'frozenset',
        'getattr', 'globals', 'hasattr', 'hash', 'help', 'hex', 'id', 'input', 'int',
        'isinstance', 'issubclass', 'iter', 'len', 'list', 'locals', 'map', 'max',
        'memoryview', 'min', 'next', 'object', 'oct', 'open', 'ord', 'pow', 'print',
        'property', 'range', 'repr', 'reversed', 'round', 'set', 'setattr', 'slice',
        'sorted', 'staticmethod', 'str', 'sum', 'super', 'tuple', 'type', 'vars', 'zip', '__import__']
types = [
    # Super-special typing primitives.
    'Any',
    'Callable',
    'ClassVar',
    'Final',
    'ForwardRef',
    'Generic',
    'Literal',
    'Optional',
    'Protocol',
    'Tuple',
    'Type',
    'TypeVar',
    'Union',

    # ABCs (from collections.abc).
    'AbstractSet',  # collections.abc.Set.
    'ByteString',
    'Container',
    'ContextManager',
    'Hashable',
    'ItemsView',
    'Iterable',
    'Iterator',
    'KeysView',
    'Mapping',
    'MappingView',
    'MutableMapping',
    'MutableSequence',
    'MutableSet',
    'Sequence',
    'Sized',
    'ValuesView',
    'Awaitable',
    'AsyncIterator',
    'AsyncIterable',
    'Coroutine',
    'Collection',
    'AsyncGenerator',
    'AsyncContextManager',

    # Structural checks, a.k.a. protocols.
    'Reversible',
    'SupportsAbs',
    'SupportsBytes',
    'SupportsComplex',
    'SupportsFloat',
    'SupportsIndex',
    'SupportsInt',
    'SupportsRound',

    # Concrete collection types.
    'ChainMap',
    'Counter',
    'Deque',
    'Dict',
    'DefaultDict',
    'List',
    'OrderedDict',
    'Set',
    'FrozenSet',
    'NamedTuple',  # Not really a type.
    'TypedDict',  # Not really a type.
    'Generator',

    # One-off things.
    'AnyStr',
    'cast',
    'final',
    'get_args',
    'get_origin',
    'get_type_hints',
    'NewType',
    'no_type_check',
    'no_type_check_decorator',
    'NoReturn',
    'overload',
    'runtime_checkable',
    'Text',
    'TYPE_CHECKING',
]


pyprocessor = PythonProcessor()

python_code = """
from math import sqrt
import pandas as pd
def allBitsSetInTheGivenRange ( n , l , r ) :
    num = ( ( 1 << r ) - 1 ) ^ ( ( 1 << ( l - 1 ) ) - 1 )
    new_num = n & num
    if ( new_num == 0 ) :
        return "Yes"
    return "No"
"""

def format_code(code):
    return pyprocessor.detokenize_code(code)

def extract_var_name(code):
    code = pyprocessor.detokenize_code(code)
    result = {}
    result['code'] = code

    vars = extract_method_vars(code, parse_ast(code, 'python'), 'python')
    new_vars = list(set(vars))
    new_vars.sort(key=vars.index)

    invocations = extract_method_invocation(code, parse_ast(code, 'python'), 'python')
    new_invocations = list(set(invocations))
    new_invocations.sort(key=invocations.index)

    params = extract_method_params(code, parse_ast(code, 'python'), 'python')
    new_params = list(set(params))
    new_params.sort(key=params.index)

    method_name = get_method_name(code, parse_ast(code, 'python'), 'python')

    if method_name in new_vars:
        new_vars.remove(method_name)

    for p in new_params:
        if p in new_vars:
            new_vars.remove(p)

    for i in new_invocations:
        if i in new_vars:
            new_vars.remove(i)

    result['function_name'] = method_name
    result['formalpara'] = new_params
    result['var'] = new_vars
    return result

if __name__ == '__main__':
    result = extract_var_name(python_code)
    print(result['code'])
    print(result['function_name'])
    print(result['formalpara'])
    print(result['var'])