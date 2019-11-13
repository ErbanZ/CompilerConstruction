# -*- coding: utf-8 -*-

OPERATOR = {'|', '+', '(', ')', '@', '*'}
UNION_OPERATOR = {'|', '+'}
AND_OPERATOR = {'@'}

priority = {
    '|': 3, '+': 3,
    '*': 2,
    '@': 1
}


# 添加连接符
def add_connector(regex):
    """
    :param regex:  a(a|b)*abb
    :return: a@(a|b)*@a@b@b
    """
    result = []
    for i in regex:
        if i not in OPERATOR:
            if len(result) > 0 and (result[-1] not in OPERATOR
                                    or result[-1] == ')'
                                    or result[-1] == '*'):
                result.append('@')
                result.append(i)
            else:
                result.append(i)
        elif i == '(' and len(result) > 0 and result[-1] not in OPERATOR:
            result.append('@')
            result.append(i)
        else:
            result.append(i)
    return ''.join(result) + "$"


# 中缀表达式转前缀表达式
# 如果遇到字母，将其输出。
# 如果遇到左括号，将其入栈。
# 如果遇到右括号，将栈元素弹出并输出直到遇到左括号为止。左括号只弹出不输出。
# 如果遇到限定符，依次弹出栈顶优先级大于或等于该限定符的限定符，然后将其入栈。
# 如果读到了输入的末尾，则将栈中所有元素依次弹出。
def infix_2_postfix(regex):
    """
    :param regex: a(a|b)*abb
    :return: aab|@*abb@@@
    """
    result = []
    stack = []
    for i in regex:
        if i not in OPERATOR and i != '$':
            result.append(i)
        elif i == '(':
            stack.append('(')
        elif i == ')':
            while len(stack) > 0:
                if stack[-1] != '(':
                    result.append(stack.pop(-1))
                else:
                    stack.pop(-1)
                    break
        elif i in OPERATOR:
            while len(stack) > 0 and stack[-1] in {'|', '+', '*', '@'} and priority[i] < priority[stack[-1]]:
                result.append(stack.pop(-1))
            stack.append(i)
        elif i == '$':
            while len(stack) > 0:
                result.append(stack.pop(-1))
    return ''.join(result) + '$'


if __name__ == '__main__':
    Regex = input("Regex :")
    Regex = add_connector(Regex)
    Regex = infix_2_postfix(Regex)
    print(Regex)
