import re #regex

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
    
# multiplicación implícita 
def insertar_multiplicacion_implicita(tokens):
#básicamente inserta un '*' entre un número y un paréntesis o entre un paréntesis
#de cierre y un número o entre paréntesis de cierre y apertura
    resultado = []
    for token in tokens:
        if resultado:
            anterior = resultado[-1]
            pega_cierre_apertura = anterior == ')' and token == '('
            pega_numero_apertura = es_numero(anterior) and token == '('
            pega_cierre_numero = anterior == ')' and es_numero(token)
            if pega_cierre_apertura or pega_numero_apertura or pega_cierre_numero:
                resultado.append('*')
        resultado.append(token)
    return resultado

#función auxiliar que encuentra el paréntesis de cierre correspondiente al primer paréntesis de apertura
def encontrar_parentesis(tokens):
    inicio = tokens.index('(')
    profundidad = 0
    for i in range(inicio, len(tokens)):
        if tokens[i] == '(':
            profundidad += 1
        elif tokens[i] == ')':
            profundidad -= 1
            if profundidad == 0:
                return inicio, i
    raise ValueError("Paréntesis no balanceados")
 
#función auxiliar que resuelve los paréntesis de manera recursiva
def resolver_parentesis(tokens):
    if '(' not in tokens:
        return tokens
 
    inicio, fin = encontrar_parentesis(tokens)
    sub_tokens = tokens[inicio + 1:fin]           # lo de adentro del paréntesis
    resultado_sub = evaluar_tokens(sub_tokens)     # llamada recursiva
 
    nuevos_tokens = tokens[:inicio] + [str(resultado_sub)] + tokens[fin + 1:]
    return resolver_parentesis(nuevos_tokens)      # por si había más paréntesis

#función principal que implementa el algoritmo de Shunting Yard para expresiones aritméticas
def shunting_yard_aritmetica(tokens):
    salida = []
    operadores = []
    operadores_precedencia = {
        '+': 1,
        '-': 1,
        '*': 2,
        '/': 2,
    }
    for tokenL in tokens:
        if es_numero(tokenL):
            salida.append(tokenL)
        elif tokenL in operadores_precedencia:
            while (operadores and
                   operadores_precedencia[operadores[-1]] >= operadores_precedencia[tokenL]):
                salida.append(operadores.pop())
            operadores.append(tokenL)
    while operadores:
        salida.append(operadores.pop())
    return salida

def evaluar_postfix(postfix):
    stack = []
    for token in postfix:
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
 
#función auxiliar que evalúa los tokens de una expresión aritmética
def evaluar_tokens(tokens):
    tokens = resolver_parentesis(tokens)
    postfix = shunting_yard_aritmetica(tokens)
    return evaluar_postfix(postfix)

# función pública: evalúa una expresión en texto
def evaluar_expresion(expresion):
    tokens = tokenize(expresion)
    tokens = insertar_multiplicacion_implicita(tokens)
    return evaluar_tokens(tokens)
