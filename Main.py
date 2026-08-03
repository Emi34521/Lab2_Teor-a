## Archivo main
## En este archivo únicamente se ejecutarán las funciones principales del algoritmo
import shunting_yard_aritmetica as shyA
import shunting_yard_regex as shyR


def menu_aritmetica():
    expresion = input("Ingrese la expresión aritmética: ")
    resultado = shyA.evaluar_expresion(expresion)
    print(f"El resultado de la expresión es: {resultado}")


def menu_regex():
    expresion = input("Ingrese la expresión regular: ")
    shyR.procesar_regex(expresion)


if __name__ == "__main__":
    print("1. Expresión aritmética")
    print("2. Expresión regular (Shunting Yard → postfix)")
    opcion = input("Elija una opción (1/2): ").strip()

    if opcion == "1":
        menu_aritmetica()
    elif opcion == "2":
        menu_regex()
    else:
        print("Opción no válida.")
