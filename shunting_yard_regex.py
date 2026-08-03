# Tokenización de expresiones regulares para Shunting Yard.
# Operadores / agrupación: |  .  *  (  )
# Operandos: cualquier otro carácter (p. ej. a, b). Se ignoran espacios.

OPERADORES = {'|', '.', '*', '(', ')'}


def tokenize(expresion: str) -> list[str]:
    """Convierte la expresión regex en una lista de tokens de un carácter.

    Ignora espacios en blanco. Cada símbolo de operador/agrupación y cada
    operando se emite como un token independiente.
    """
    tokens = []
    for char in expresion:
        if char.isspace():
            continue
        tokens.append(char)
    return tokens


def es_operando(token: str) -> bool:
    """True si el token es un símbolo del alfabeto (no operador/agrupación)."""
    return token not in OPERADORES


def puede_terminar_operando(token: str) -> bool:
    """True si tras este token puede ir una concatenación implícita."""
    return es_operando(token) or token in (')', '*')


def puede_iniciar_operando(token: str) -> bool:
    """True si este token puede iniciar el segundo factor de una concatenación."""
    return es_operando(token) or token == '('


def insertar_concatenacion_implicita(tokens: list[str]) -> list[str]:
    """Inserta '.' entre tokens cuando la concatenación está implícita.

    Casos: letra+(, )+(letra|()|(), *+(letra|(). No altera '.' ya explícitos.
    Ejemplo: (a|b)*abb → ( a | b ) * . a . b . b
    """
    resultado = []
    for token in tokens:
        if resultado:
            anterior = resultado[-1]
            if puede_terminar_operando(anterior) and puede_iniciar_operando(token):
                resultado.append('.')
        resultado.append(token)
    return resultado


# Precedencia: | (unión) < . (concat) < * (Kleene, unario postfix)
PRECEDENCIA = {
    '|': 1,
    '.': 2,
}


def shunting_yard_regex(tokens: list[str]) -> list[str]:
    """Convierte tokens infix de regex a notación postfix (polaca inversa).

    Ejemplo: ( a | b ) * . a . b . b  →  a b | * a . b . b .
    """
    salida = []
    operadores = []

    for token in tokens:
        if es_operando(token):
            salida.append(token)
        elif token == '*':
            # Unario postfix: se emite de inmediato
            salida.append(token)
        elif token in PRECEDENCIA:
            while (
                operadores
                and operadores[-1] in PRECEDENCIA
                and PRECEDENCIA[operadores[-1]] >= PRECEDENCIA[token]
            ):
                salida.append(operadores.pop())
            operadores.append(token)
        elif token == '(':
            operadores.append(token)
        elif token == ')':
            while operadores and operadores[-1] != '(':
                salida.append(operadores.pop())
            if not operadores or operadores[-1] != '(':
                raise ValueError("Paréntesis no balanceados: falta '('")
            operadores.pop()  # descarta '('
        else:
            raise ValueError(f"Token no reconocido: {token!r}")

    while operadores:
        op = operadores.pop()
        if op == '(':
            raise ValueError("Paréntesis no balanceados: falta ')'")
        salida.append(op)

    return salida


def expresion_a_postfix(expresion: str) -> list[str]:
    """Pipeline: tokenizar → concatenación implícita → Shunting Yard."""
    tokens = tokenize(expresion)
    tokens = insertar_concatenacion_implicita(tokens)
    return shunting_yard_regex(tokens)


MENSAJES_OPERADOR = {
    '.': 'Concatenación con',
    '|': 'Unión con',
    '*': 'Kleene de',
}


def describir_postfix(postfix: list[str]) -> list[str]:
    """Lee el postfix de derecha a izquierda y describe cada símbolo.

    Operadores → frase fija; operandos → '{s} de', salvo el último del
    recorrido (el más a la izquierda del postfix), que es solo '{s}'.
    """
    mensajes = []
    for i, token in enumerate(reversed(postfix)):
        es_ultimo = i == len(postfix) - 1
        if token in MENSAJES_OPERADOR:
            mensajes.append(MENSAJES_OPERADOR[token])
        elif es_ultimo:
            mensajes.append(token)
        else:
            mensajes.append(f'{token} de')
    return mensajes
