import string
from collections import deque

var_values = dict()
type_of_ops = ['-', '+', '*', '/']


class VariableUnknown(Exception):
    pass


class WrongExpression(Exception):
    pass


def check_variable_name(name):
    ok = True
    for c in name:
        if c not in string.ascii_letters:
            ok = False
    return ok


def is_variable(word):
    ok = False
    for c in word:
        if c in string.ascii_letters:
            ok = True
            break
    return ok


def is_operation(word):
    ok = True
    for c in word:
        if c not in type_of_ops:
            ok = False
    if len(word) > 1 and word[0] in ('*', '/'):
        ok = False
    return ok

def is_number_or_variable(word):
    ok = True
    for c in word:
        if c not in string.ascii_letters and c not in string.digits:
            ok = False
    return ok


def get_precedence(op):
    if op[0] in ('+', '-'):
        return 1
    elif op in ('/', '*'):
        return 2
    else:
        return 0

def convert_to_postfix_notation(expression):
    stack = deque()
    result = ''
    words_prev = expression.split()
    words = []
    for word in words_prev:
        if word[0] == '(':
            words.append('(')
            words.append(word[1:])
        elif word[-1] == ')':
            words.append(word[:-1])
            words.append(')')
        else:
            words.append(word)

    check_braces = deque()
    for word in words:
        if word == '(':
            check_braces.append('(')
        elif word == ')':
            if not check_braces:
                raise WrongExpression()
            else:
                top = check_braces.pop()
                if top != '(':
                    raise WrongExpression()

    for word in words:
        if is_number_or_variable(word):
            result += word + ' '
        elif word == '(':
            stack.append(word)
        elif word == ')':
            while len(stack) > 0:
                top_elem = stack.pop()
                if top_elem == '(':
                    # stack.append(top_elem)
                    break
                result += str(top_elem) + ' '
        elif is_operation(word):
            if len(stack) == 0:
                stack.append(word)
            else:
                top_elem = stack.pop()
                if top_elem == '(':
                    stack.append(top_elem)
                    stack.append(word)
                elif get_precedence(word) > get_precedence(top_elem):
                    stack.append(top_elem)
                    stack.append(word)
                elif get_precedence(word) <= get_precedence(top_elem):
                    result += str(top_elem) + ' '
                    while len(stack) > 0:
                        top_elem = stack.pop()
                        if top_elem == '(' or get_precedence(top_elem) < get_precedence(word):
                            stack.append(top_elem)
                            break
                        else:
                            result += str(top_elem) + ' '
                    stack.append(word)
        else:
            # the word we don't expect
            raise WrongExpression()
    while stack:
        top_elem = stack.pop()
        if top_elem in ('(', ')'):
            raise WrongExpression()
        result += top_elem + ' '
    return result


def perform_the_operation(num1, num2, op):
    if op[0] == '+':
        return num1 + num2
    elif op[0] == '-':
        koef = 1
        for c in op:
            koef *= -1
        return num1 + num2 * koef
    elif op == '/':
        return num1 / num2
    elif op == '*':
        return num1 * num2
    else:
        return 0


def get_value(word):
    if is_variable(word):
        if word in var_values:
            val = var_values[word]
        else:
            raise VariableUnknown()
    else:
        val = float(word)
    return val


def evaluate_postfix_notation(expression):
    stack = deque()
    words = expression.split()
    for word in words:
        if is_number_or_variable(word):
            stack.append(word)
        elif is_operation(word):
            num2 = stack.pop()
            num1 = stack.pop()
            val1 = get_value(num1)
            val2 = get_value(num2)

            res = perform_the_operation(val1, val2, word)
            stack.append(str(res))

    top_elem = stack.pop()
    value = get_value(top_elem)
    return int(value)


def evaluate_expression(expression):
    return 0


while True:
    input_string = input()
    if input_string == '/exit':
        print('Bye!')
        break
    elif input_string == '/help':
        print('The program calculates the sum of numbers')
        continue
    elif len(input_string) > 0 and input_string[0] == '/':
        print('Unknown command')
        continue
    elif input_string == '':
        continue

    if input_string.count('=') == 1:
        words = input_string.split('=')
        var_name = words[0].strip()
        if check_variable_name(var_name):
            value_expression = words[1].strip()
            try:
                postfix_notation = convert_to_postfix_notation(value_expression)
                value = evaluate_postfix_notation(postfix_notation)
                if value is not None:
                    var_values[var_name] = float(value)
            except:
                print('Invalid expression')
        else:
            print('Invalid identifier')
    elif input_string.count('=') > 1:
        print('Invalid expression')
    else:
        try:
            postfix_notation = convert_to_postfix_notation(input_string)
            value = evaluate_postfix_notation(postfix_notation)
            if value is not None:
                print(value)
        except VariableUnknown:
            print('Variable unknown')
        except WrongExpression:
            print('Invalid expression')





