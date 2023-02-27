def getPostfix(regex):
    # Check if the parentheses are balanced
    open_parentheses = 0
    for char in regex:
        if char == '(':
            open_parentheses += 1
        elif char == ')':
            open_parentheses -= 1
            if open_parentheses < 0:
                raise Exception('Regex not balanced')
    if open_parentheses > 0:
        raise Exception('Regex not balanced')

    # Check for invalid characters at the start and end of the regex
    if regex[0] in ('*', '+', '|') or regex[-1] == '|':
        raise Exception('Invalid start or end of regex')

    # Check for invalid combinations of symbols
    for i in range(len(regex) - 1):
        if regex[i] in '+*' and regex[i+1] in '+|' and not (regex[i] == '*' and regex[i+1] == '|'):
            raise Exception('Invalid combination of symbols')

    # Check for invalid alternations
    for i in range(len(regex) - 1):
        if regex[i:i+2] == '||':
            raise Exception('Invalid alternations')

    # Check for invalid repetitions
    for i in range(len(regex) - 1):
        if regex[i:i+2] == '**':
            raise Exception('Invalid repetitions')

    # Add explicit concatenation between characters where necessary
    formatted_regex = format_regex(regex)

    # Convert infix expression to postfix notation
    op_precedence = {"|": 1, ".": 2, "*": 3}
    stack = []
    postfix = []
    regex_len = len(formatted_regex)
    i = 0

    while i < regex_len:
        char = formatted_regex[i]
        i += 1
        
        if char == "(":
            stack.append(char)
        elif char == ")":
            while stack and stack[-1] != "(":
                postfix.append(stack.pop())
            if stack and stack[-1] == "(":
                stack.pop()
        elif char in op_precedence:
            while stack and stack[-1] != "(" and op_precedence[char] <= op_precedence[stack[-1]]:
                postfix.append(stack.pop())
            stack.append(char)
        else:
            postfix.append(char)

    while stack:
        postfix.append(stack.pop())

    temp_reg = "".join(postfix)
    post = remove_dot_before_pipe(temp_reg)

    return post


def format_regex(regex):
    formatted_regex = ''
    operators = set(["|", "*", "+", "?"])
    operator_db = set(["|"])
    for i in range(len(regex)):
        char = regex[i]
        if i + 1 < len(regex):
            next_char = regex[i + 1]
            formatted_regex += char
            if char != '(' and next_char != ')' and (next_char not in operators or char in operator_db) and next_char != '?':
                if next_char != '|':
                    formatted_regex += '.'
        elif char == '?' and regex[i-1] == ')':
            formatted_regex = formatted_regex[:-1] + char + '.' if formatted_regex[-1] != ')' else formatted_regex + char + '.'
        else:
            formatted_regex += char
    return formatted_regex


def remove_dot_before_pipe(s):
    s = list(s)
    i = 0
    while i < len(s) - 1:
        if s[i] == '.' and s[i+1] == '|':
            s[i] = ''
            i += 1
        i += 1
    return ''.join(s)