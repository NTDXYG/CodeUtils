import ast
import re

import javalang
import pandas as pd
from tqdm import tqdm

from preprocessing.lang_processors.java_processor import JavaProcessor
from program_transformer.language_processors import PythonProcessor
from program_transformer.transformations import BlockSwap, ForWhileTransformer, OperandSwap, ConfusionRemover
root_folder = "D:\\论文代码开源\\code-transformation\\preprocessing\\third_party\\"
jprocessor = JavaProcessor(root_folder=root_folder)

def transform_java_code(java, operand_swap, operand_transform, if_else_transform, for_while_transform):
    decode_code = java
    temp_code_list = []
    operand_swap_code, operand_swap_meta = operand_swap.transform_code(decode_code)
    operand_transform_code, operand_transform_meta = operand_transform.transform_code(decode_code)
    if_else_code, if_else_meta = if_else_transform.transform_code(decode_code)
    for_while_code, for_while_meta = for_while_transform.transform_code(decode_code)
    if operand_swap_meta['success']==True :
        # operand_swap操作成功
        temp_code_list.append(operand_swap_code)
        operand_swap_transform_code, operand_swap_transform_meta = operand_transform.transform_code(operand_swap_code)
        operand_swap_if_else_code, operand_swap_if_else_meta = if_else_transform.transform_code(operand_swap_code)
        operand_swap_for_while_code, operand_swap_for_while_meta = for_while_transform.transform_code(operand_swap_code)
        if operand_swap_transform_meta['success'] == True:
            temp_code_list.append(operand_swap_transform_code)
            operand_swap_transform_if_else_code, operand_swap_transform_if_else_meta = if_else_transform.transform_code(
                operand_swap_transform_code)
            operand_swap_transform_for_while_code, operand_swap_transform_for_while_meta = for_while_transform.transform_code(
                operand_swap_transform_code)
            if operand_swap_transform_if_else_meta['success'] == True:
                temp_code_list.append(operand_swap_transform_if_else_code)
                operand_swap_transform_if_else_for_while_code, operand_swap_transform_if_else_for_while_meta = for_while_transform.transform_code(
                    operand_swap_transform_if_else_code)
                if operand_swap_transform_if_else_for_while_meta['success'] == True:
                    temp_code_list.append(operand_swap_transform_if_else_for_while_code)
            if operand_swap_transform_for_while_meta['success'] == True:
                temp_code_list.append(operand_swap_transform_for_while_code)
        if operand_swap_if_else_meta['success'] == True:
            temp_code_list.append(operand_swap_if_else_code)
            operand_swap_if_else_for_while_code, operand_swap_if_else_for_while_meta = for_while_transform.transform_code(
                operand_swap_if_else_code)
            if operand_swap_if_else_for_while_meta['success'] == True:
                temp_code_list.append(operand_swap_if_else_for_while_code)
        if operand_swap_for_while_meta['success'] == True:
            temp_code_list.append(operand_swap_for_while_code)

    if operand_transform_meta['success']==True:
        temp_code_list.append(operand_transform_code)
        operand_transform_if_else_code, operand_transform_if_else_meta = if_else_transform.transform_code(operand_transform_code)
        operand_transform_for_while_code, operand_transform_for_while_meta = for_while_transform.transform_code(operand_transform_code)
        if operand_transform_if_else_meta['success'] == True:
            temp_code_list.append(operand_transform_if_else_code)
            operand_transform_if_else_for_while_code, operand_transform_if_else_for_while_meta = for_while_transform.transform_code(
                operand_transform_if_else_code)
            if operand_transform_if_else_for_while_meta['success'] == True:
                temp_code_list.append(operand_transform_if_else_for_while_code)
        if operand_transform_for_while_meta['success'] == True:
            temp_code_list.append(operand_transform_for_while_code)

    if if_else_meta['success']==True:
        # if-esle操作成功
        temp_code_list.append(if_else_code)
        if_else_for_while_code, if_else_for_while_meta = for_while_transform.transform_code(if_else_code)
        if if_else_for_while_meta['success'] == True:
            temp_code_list.append(if_else_for_while_code)

    if for_while_meta['success']==True:
        # for-while操作成功
        temp_code_list.append(for_while_code)

    # 如果语法转换成功的个数为0，则直接返回
    if len(temp_code_list) == 0:
        return []

    # 去重
    temp_code_list = list(set(temp_code_list))
    temp_code_list = [jprocessor.detokenize_code(code) for code in temp_code_list]
    return temp_code_list


def transform_python_code(python, operand_swap, operand_transform, if_else_transform, for_while_transform):
    decode_code = python
    temp_code_list = []
    operand_swap_code, operand_swap_meta = operand_swap.transform_code(decode_code)
    operand_transform_code, operand_transform_meta = operand_transform.transform_code(decode_code)
    if_else_code, if_else_meta = if_else_transform.transform_code(decode_code)
    for_while_code, for_while_meta = for_while_transform.transform_code(decode_code)
    if operand_swap_meta['success'] == True:
        # operand_swap操作成功
        temp_code_list.append(operand_swap_code)
        operand_swap_transform_code, operand_swap_transform_meta = operand_transform.transform_code(operand_swap_code)
        operand_swap_if_else_code, operand_swap_if_else_meta = if_else_transform.transform_code(operand_swap_code)
        operand_swap_for_while_code, operand_swap_for_while_meta = for_while_transform.transform_code(operand_swap_code)
        if operand_swap_transform_meta['success'] == True:
            temp_code_list.append(operand_swap_transform_code)
            operand_swap_transform_if_else_code, operand_swap_transform_if_else_meta = if_else_transform.transform_code(
                operand_swap_transform_code)
            operand_swap_transform_for_while_code, operand_swap_transform_for_while_meta = for_while_transform.transform_code(
                operand_swap_transform_code)
            if operand_swap_transform_if_else_meta['success'] == True:
                temp_code_list.append(operand_swap_transform_if_else_code)
                operand_swap_transform_if_else_for_while_code, operand_swap_transform_if_else_for_while_meta = for_while_transform.transform_code(
                    operand_swap_transform_if_else_code)
                if operand_swap_transform_if_else_for_while_meta['success'] == True:
                    temp_code_list.append(operand_swap_transform_if_else_for_while_code)
            if operand_swap_transform_for_while_meta['success'] == True:
                temp_code_list.append(operand_swap_transform_for_while_code)
        if operand_swap_if_else_meta['success'] == True:
            temp_code_list.append(operand_swap_if_else_code)
            operand_swap_if_else_for_while_code, operand_swap_if_else_for_while_meta = for_while_transform.transform_code(
                operand_swap_if_else_code)
            if operand_swap_if_else_for_while_meta['success'] == True:
                temp_code_list.append(operand_swap_if_else_for_while_code)
        if operand_swap_for_while_meta['success'] == True:
            temp_code_list.append(operand_swap_for_while_code)

    if operand_transform_meta['success'] == True:
        temp_code_list.append(operand_transform_code)
        operand_transform_if_else_code, operand_transform_if_else_meta = if_else_transform.transform_code(
            operand_transform_code)
        operand_transform_for_while_code, operand_transform_for_while_meta = for_while_transform.transform_code(
            operand_transform_code)
        if operand_transform_if_else_meta['success'] == True:
            temp_code_list.append(operand_transform_if_else_code)
            operand_transform_if_else_for_while_code, operand_transform_if_else_for_while_meta = for_while_transform.transform_code(
                operand_transform_if_else_code)
            if operand_transform_if_else_for_while_meta['success'] == True:
                temp_code_list.append(operand_transform_if_else_for_while_code)
        if operand_transform_for_while_meta['success'] == True:
            temp_code_list.append(operand_transform_for_while_code)

    if if_else_meta['success'] == True:
        # if-esle操作成功
        temp_code_list.append(if_else_code)
        if_else_for_while_code, if_else_for_while_meta = for_while_transform.transform_code(if_else_code)
        if if_else_for_while_meta['success'] == True:
            temp_code_list.append(if_else_for_while_code)

    if for_while_meta['success'] == True:
        # for-while操作成功
        temp_code_list.append(for_while_code)

    # 如果语法转换成功的个数为0，则直接返回
    if len(temp_code_list) == 0:
        return []
    # 去重
    temp_code_list = list(set(temp_code_list))
    temp_code_list = [PythonProcessor.beautify_python_code(code.split()) for code in temp_code_list if code != '']
    return temp_code_list

def transform_code(code, lang):
    code_list = []
    if lang == 'java':
        # a>b --> b<a
        operand_swap = OperandSwap(
            'D:\论文代码开源\code-transformation\\asts\\build\my-languages.so', 'java'
        )
        # a+=b --> a=a+b
        operand_transform = ConfusionRemover(
            'D:\论文代码开源\code-transformation\\asts\\build\my-languages.so', 'java'
        )
        if_else_transform = BlockSwap(
            'D:\论文代码开源\code-transformation\\asts\\build\my-languages.so', 'java'
        )
        for_while_transform = ForWhileTransformer(
            'D:\论文代码开源\code-transformation\\asts\\build\my-languages.so', 'java'
        )
        code_list = transform_java_code(code, operand_swap, operand_transform, if_else_transform, for_while_transform)
        results = []
        for code in code_list:
            try:
                tokens = javalang.tokenizer.tokenize(code)
                parser = javalang.parser.Parser(tokens)
                tree = parser.parse_member_declaration()
                results.append(code)
            except:
                pass

    if lang == 'python':
        # a>b --> b<a
        operand_swap = OperandSwap(
            'D:\论文代码开源\code-transformation\\asts\\build\my-languages.so', 'python'
        )
        # a+=b --> a=a+b
        operand_transform = ConfusionRemover(
            'D:\论文代码开源\code-transformation\\asts\\build\my-languages.so', 'python'
        )
        if_else_transform = BlockSwap(
            'D:\论文代码开源\code-transformation\\asts\\build\my-languages.so', 'python'
        )
        for_while_transform = ForWhileTransformer(
            'D:\论文代码开源\code-transformation\\asts\\build\my-languages.so', 'python'
        )
        code_list = transform_python_code(code, operand_swap, operand_transform, if_else_transform, for_while_transform)
        results = []
        for code in code_list:
            try:
                tree = ast.parse(code)
                results.append(code)
            except:
                pass
    return results

if __name__ == '__main__':
    py_code = """
    def maxLen(arr, n):
        min_val = min(arr)
        freq = 0
        for i in range(n):
            if arr[i] == min_val:
                freq += 1
            else:
                freq = 0
        return freq
    """
    code_list = transform_code(py_code, 'python')
    print(code_list[0])