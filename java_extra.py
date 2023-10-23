# encoding: utf-8
from asts.ast_parser import extract_method_vars, parse_ast, extract_method_invocation, \
    extract_method_params, get_method_name
from preprocessing.lang_processors.java_processor import JavaProcessor
from preprocessing.util import get_sequence as func

import javalang as javalang

root_folder = "D:\\论文代码开源\\code-transformation\\preprocessing\\third_party\\"
jprocessor = JavaProcessor(root_folder=root_folder)

java_code = """
public String readFile (String filename) {
String content = null;
int var = 0;
File file = new File(filename);
FileReader reader = null;
try {
reader = new FileReader(file);
char[] chars = new char[(int)file.length()];
reader.read(chars);
content = new String(chars);
reader.close();
} catch (IOException e) {
e.printStackTrace();
} finally {
if(reader != null){
reader.close();
}
}
return content;
}
"""

def format_code(code):
    return jprocessor.detokenize_code(code)

def trans_to_sequences(ast):
    sequence = []
    func(ast, sequence)
    return sequence

def extract_var_name(code):
    code = jprocessor.detokenize_code(code)
    print(code)
    result = {}
    result['code'] = code

    vars = extract_method_vars(code, parse_ast(code, 'java'), 'java')
    new_vars = list(set(vars))
    new_vars.sort(key=vars.index)

    invocations = extract_method_invocation(code, parse_ast(code, 'java'), 'java')
    new_invocations = list(set(invocations))
    new_invocations.sort(key=invocations.index)

    params = extract_method_params(code, parse_ast(code, 'java'), 'java')
    new_params = list(set(params))
    new_params.sort(key=params.index)

    method_name = get_method_name(code, parse_ast(code, 'java'), 'java')

    if method_name in new_vars:
        new_vars.remove(method_name)

    for p in new_params:
        if p in new_vars:
            new_vars.remove(p)

    for i in new_invocations:
        if i in new_vars:
            new_vars.remove(i)

    if 'else' in new_vars:
        new_vars.remove('else')

    result['function_name'] = method_name
    result['formalpara'] = new_params
    result['var'] = new_vars
    return result

if __name__ == '__main__':
    result = extract_var_name(java_code)
    print(result['code'])
    print(result['function_name'])
    print(result['formalpara'])
    print(result['var'])