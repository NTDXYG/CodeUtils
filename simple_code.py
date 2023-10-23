import ast

import javalang

from program_transformer.attack import transform_code

py_code = """
def maxLen(arr, n):
    min_val = min(arr)
    freq = 0
    for i in range(n):
        if arr[i] == min_val:
            freq += 1
    return freq
"""

java_code = '''
public static int validPosition(int[] arr, int N, int K) {
    int count = 0;
    int sum = 0;
    for(int i = 0; i < N; i++) {
        sum += arr[i];
    }
    for(int i = 0; i < N; i++) {
        if((arr[i] + K) > (sum - arr[i])) {
            count++;
        }
    }
    return count;
}
'''

from func_timeout import func_set_timeout


@func_set_timeout(1)
def simple(code, lang):
    if lang == 'python':
        from python_extra import extract_var_name
    else:
        from java_extra import extract_var_name
    try:
        result = extract_var_name(code)
        # raw_code = result['code']
        code = result['code']
        func_name = result['function_name']
        params = result['formalpara']
        vars = list(result['var'])
        code = code.replace(' ' + func_name + ' ', ' f ')
        code = code + " "
        new_code = []
        for line in code.split('\n'):
            line = line.replace('    ', '|TAB| ')
            for p in range(len(params)):
                line = ' '.join(['arg_' + str(p) if x == params[p] else x for x in line.split()])
            line = line.replace('|TAB| ', '    ')
            new_code.append(line)

        code = '\n'.join(new_code)
        new_code = []
        for line in code.split('\n'):
            line = line.replace('    ', '|TAB| ')
            for v in range(len(vars)):
                line = ' '.join(['var_' + str(v) if x == vars[v] else x for x in line.split()])
            line = line.replace('|TAB| ', '    ')
            new_code.append(line)

        code = '\n'.join(new_code)

        if lang == 'java':
            try:
                tokens = javalang.tokenizer.tokenize(code)
                parser = javalang.parser.Parser(tokens)
                tree = parser.parse_member_declaration()
            except:
                print('syntax error')
                return False

        if lang == 'python':
            code = code.replace(' ;\n', '\n')
            try:
                tree = ast.parse(code)
            except:
                print('syntax error')
                return False
        code_list = transform_code(code, lang)
        if len(code_list) == 0:
            return False
        else:
            return code
    except:
        print('parse error')
        return False

code = simple(java_code, 'java')
print(code)