import re 
#función auxiliar que ayuda a "tokenizar" la expresión ingresada 
def tokenize(expresion):
    return re.findall(r'\d+\.?\d*|[+\-*/()]', expresion)
#función auxiliar que ayuda a determinar si un token es un número
def es_numero(token):
    try:
        float(token)
        return True
    except ValueError:
        return False

#función principal que implementa el algoritmo de Shunting Yard para expresiones aritméticas
def shunting_yard_aritmetica(expresion):
    ## creación de la pila de entrada y salida 
    entrada = []
    salida = []
    ## creación de la pila de operadores 
    operadores = []
    ## creación de la lista de operadores y su precedencia
    operadores_precedencia = {
        '+': 1,
        '-': 1,
        '*': 2,
        '/': 2,
        '(': 0,
        ')': 0
    }
    tokens = tokenize(expresion)
    #leemos cada token de la expresión
    for tokenL in tokens:
        if es_numero(tokenL):
            salida.append(tokenL)
        elif tokenL in operadores_precedencia:
            while (operadores and operadores[-1] != '(' and
                   operadores_precedencia[operadores[-1]] >= operadores_precedencia[tokenL]):
                salida.append(operadores.pop())
            operadores.append(tokenL)
        elif tokenL == '(':
            operadores.append(tokenL)
        elif tokenL == ')':
            while operadores and operadores[-1] != '(':
                salida.append(operadores.pop())
            operadores.pop()  # Eliminar el paréntesis izquierdo
    while operadores:
        salida.append(operadores.pop())
    return salida

#función que evalúa la expresión en notación "infix" y devuelve un resultado numérico 
def evaluar_expresion(expresion):
    infix = shunting_yard_aritmetica(expresion)
    stack = []
    for token in infix:
        if es_numero(token):
            stack.append(float(token))
        else:
            b = stack.pop()
            a = stack.pop()
            if token == '+':
                stack.append(a + b)
            elif token == '-':
                stack.append(a - b)
            elif token == '*':
                stack.append(a * b)
            elif token == '/':
                stack.append(a / b)
    return stack[0]

    
    
    