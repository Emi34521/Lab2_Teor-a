##Archivo main 
##En este archivo únicamente se ejecutarán las funciones principales del algoritmo 
import shunting_yard_aritmetica as shyA 

if __name__ == "__main__":
    expresion = input("Ingrese la expresión aritmética: ")
    resultado = shyA.evaluar_expresion(expresion)
    print(f"El resultado de la expresión es: {resultado}")
    