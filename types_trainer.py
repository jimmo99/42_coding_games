# **************************************************************************** #
#                                                                              #
#                                                         :::      ::::::::    #
#    types_trainer.py                                   :+:      :+:    :+:    #
#                                                     +:+ +:+         +:+      #
#    By: ssaavedr <ssaavedr@student.42urduliz.com>  +#+  +:+       +#+         #
#                                                 +#+#+#+#+#+   +#+            #
#    Created: 2026/10/19 23:34:04 by ssaavedr          #+#    #+#              #
#    Updated: 2026/10/19 23:34:05 by ssaavedr         ###   ########.fr        #
#                                                                              #
# **************************************************************************** #

#!/usr/bin/env python3
"""
Entrenador exhaustivo de Variables, Tipos de Datos y Memoria en C.
Especialmente diseñado para estudiantes de C en 42 (Libft v19.3).
"""

import os
import random
import sys

CATEGORIES = {
    "1": "Enteros, Tamaños y Rangos (int, size_t, char, unsigned)",
    "2": "Punteros y Modificadores (char *, const, static)",
    "3": "Punteros Dobles y Matrices (char **, t_list **)",
    "4": "Punteros Genéricos y Punteros a Función (void *, (*f)())",
    "5": "Estructuras Dinámicas y Listas (t_list)",
}

QUESTIONS = [
    # ========================================================
    # 1. ENTEROS, TAMAÑOS Y RANGOS
    # ========================================================
    {
        "cat": "1",
        "title": "size_t frente a int",
        "q": "¿Por qué las funciones como ft_strlen, ft_memcpy o malloc usan 'size_t' en vez de 'int'?",
        "opts": [
            "A) Porque size_t ocupa menos memoria que un int.",
            "B) Porque size_t es un tipo entero sin signo (unsigned) garantizado para direccionar cualquier tamaño válido en la memoria RAM, sin riesgo de valores negativos.",
            "C) Porque la Norminette prohíbe el uso de int en bucles.",
            "D) Porque size_t solo funciona con cadenas de texto."
        ],
        "ans": "B",
        "exp": "size_t es un entero sin signo (unsigned) definido por la arquitectura del procesador (32 o 64 bits). Un índice o tamaño nunca debe ser negativo; usar int limitaría el tamaño a la mitad y podría causar desbordamientos negativos."
    },
    {
        "cat": "1",
        "title": "Límites de int y ft_itoa",
        "q": "¿Qué ocurre si haces 'int n = -2147483648;' y ejecutas 'n = -n;'?",
        "opts": [
            "A) n pasa a valer 2147483648 de forma normal.",
            "B) Se produce un desbordamiento de entero con signo (Undefined Behavior / Overflow), porque el máximo int positivo es 2147483647.",
            "C) n se convierte en 0.",
            "D) El compilador se niega a compilar el programa."
        ],
        "ans": "B",
        "exp": "En sistemas de 32 bits en complemento a 2, el rango de int es de -2147483648 a 2147483647. El valor positivo de INT_MIN no cabe en un int. Por eso en ft_itoa o ft_putnbr_fd se convierte a long o se trata como caso especial."
    },
    {
        "cat": "1",
        "title": "Casteo en ft_memcmp y ft_strncmp",
        "q": "¿Por qué en ft_memcmp y ft_strncmp se deben restar los caracteres casteándolos a '(unsigned char)'?",
        "opts": [
            "A) Para evitar que caracteres con códigos ASCII mayores a 127 se interpreten como números negativos al restarse.",
            "B) Porque un puntero void * no se puede desreferenciar directamente sin cast.",
            "C) Ambas opciones A y B son correctas.",
            "D) Ninguna, es puramente estético."
        ],
        "ans": "C",
        "exp": "En C el estándar exige que las comparaciones de memoria traten los bytes como valores sin signo (0 a 255). Además, el compilador prohíbe desreferenciar un 'void *' sin castearlo a un tipo con tamaño conocido como 'unsigned char *'."
    },
    {
        "cat": "1",
        "title": "Parámetros int para caracteres en libc",
        "q": "¿Por qué ft_isalpha(int c) o ft_putchar_fd(char c, int fd) reciben el carácter como 'int' en vez de 'char'?",
        "opts": [
            "A) Para permitir que funciones estándar devuelvan o reciban la constante EOF (que vale -1).",
            "B) Porque en C los char ocupan 4 bytes por defecto.",
            "C) Porque no existe el tipo char en la librería estándar.",
            "D) Para ahorrar espacio en la pila."
        ],
        "ans": "A",
        "exp": "En C clásico, las funciones de entrada/salida y clasificación de caracteres reciben int para que puedan representar todos los valores posibles de un unsigned char (0-255) y además el valor EOF (-1)."
    },

    # ========================================================
    # 2. PUNTEROS Y MODIFICADORES
    # ========================================================
    {
        "cat": "2",
        "title": "Uso de 'const char *'",
        "q": "¿Cuál es la diferencia entre 'char *s' y 'const char *s' en los parámetros de una función?",
        "opts": [
            "A) 'char *s' solo lee; 'const char *s' puede escribir.",
            "B) 'const char *s' le indica al compilador y al programador que la memoria apuntada es de solo lectura y no será alterada.",
            "C) 'const' obliga a reservar memoria con malloc.",
            "D) 'const char *' solo acepta cadenas creadas en el Heap."
        ],
        "ans": "B",
        "exp": "El modificador const protege la cadena original. Si intentas hacer s[0] = 'X' con un const char *s, el compilador emitirá un error, evitando escrituras accidentales en cadenas literales."
    },
    {
        "cat": "2",
        "title": "Funciones y variables 'static'",
        "q": "En el proyecto Libft, ¿para qué se utiliza la palabra reservada 'static' antes de una función auxiliar?",
        "opts": [
            "A) Para hacer que la función se ejecute el doble de rápido.",
            "B) Para restringir el alcance (scope) de la función únicamente al archivo .c en el que está declarada, evitando conflictos de nombres globales.",
            "C) Para que la función no use memoria RAM.",
            "D) Es obligatorio para todas las funciones del subject."
        ],
        "ans": "B",
        "exp": "Por la Norminette y buenas prácticas de C, cualquier función auxiliar no incluida en libft.h debe marcarse como static para que sea privada a su propio archivo y no contamine el espacio de nombres de la librería."
    },
    {
        "cat": "2",
        "title": "Aritmética de punteros",
        "q": "Si tienes 'int *tab = malloc(sizeof(int) * 5);', ¿cuántos bytes avanza en la memoria la expresión 'tab + 2'?",
        "opts": [
            "A) Exactamente 2 bytes.",
            "B) 8 bytes (asumiendo que sizeof(int) == 4).",
            "C) 16 bytes.",
            "D) Depende del contenido del array."
        ],
        "ans": "B",
        "exp": "La aritmética de punteros en C siempre avanza en múltiplos del tamaño del tipo al que apunta: 2 * sizeof(int) = 8 bytes. Si fuera char * avanzaría 2 bytes, pero en int * avanza de 4 en 4."
    },

    # ========================================================
    # 3. PUNTEROS DOBLES Y MATRICES
    # ========================================================
    {
        "cat": "3",
        "title": "Estructura de 'char **'",
        "q": "En 'char **tab = ft_split(\"hola mundo\", ' ');', ¿qué tipo exacto es 'tab[0]' y qué tipo exacto es 'tab[0][1]'?",
        "opts": [
            "A) tab[0] es char; tab[0][1] es char *.",
            "B) tab[0] es char * (el string 'hola'); tab[0][1] es char (la letra 'o').",
            "C) Ambos son de tipo char **.",
            "D) tab[0] es void *; tab[0][1] es int."
        ],
        "ans": "B",
        "exp": "tab es char ** (la lista de punteros). Desreferenciar una vez con tab[0] da un char * (la palabra 'hola'). Desreferenciar dos veces con tab[0][1] da el char de esa palabra ('o')."
    },
    {
        "cat": "3",
        "title": "Uso de doble puntero en 't_list **lst'",
        "q": "¿Por qué ft_lstadd_front(t_list **lst, t_list *new) necesita un puntero doble?",
        "opts": [
            "A) Porque maneja dos listas enlazadas independientes.",
            "B) Porque los argumentos en C se pasan por valor (copia); para modificar la dirección del puntero raíz original 'lst' (por ejemplo si la lista estaba vacía), necesitamos pasar su dirección de memoria.",
            "C) Porque cada nodo contiene dos punteros 'next'.",
            "D) Porque la lista está alojada en el stack."
        ],
        "ans": "B",
        "exp": "Si pasaras t_list *lst, la función modificaría una copia local del puntero y el main seguiría teniendo el puntero original apuntando a NULL. Al pasar la dirección (&lst), modificas el puntero original con *lst = new."
    },
    {
        "cat": "3",
        "title": "Terminador de arrays dobles",
        "q": "¿Por qué un 'char **' devuelto por ft_split debe terminar obligatoriamente con NULL?",
        "opts": [
            "A) Porque así lo exige el sistema operativo para hacer free.",
            "B) Porque actúa como centinela (freno): permite recorrer el array con un bucle 'while (tab[i])' sin necesidad de pasar una variable con el total de palabras.",
            "C) Para que printf pueda imprimirlo de una vez.",
            "D) Para evitar que las palabras se mezclen."
        ],
        "ans": "B",
        "exp": "Igual que un string (char *) termina en '\\0' para saber dónde acaba, un array de punteros (char **) termina con un puntero NULL para que cualquier función sepa cuándo parar de leer."
    },

    # ========================================================
    # 4. PUNTEROS GENÉRICOS Y PUNTEROS A FUNCIÓN
    # ========================================================
    {
        "cat": "4",
        "title": "Puntero genérico 'void *'",
        "q": "En C, ¿qué operaciones están PROHIBIDAS directamente sobre un puntero de tipo 'void *'?",
        "opts": [
            "A) Asignarle una dirección de memoria devuelta por malloc.",
            "B) Pasarlo como parámetro a la función free.",
            "C) Desreferenciarlo (*ptr) o sumarle enteros (ptr + 1) directamente sin castearlo antes a otro tipo.",
            "D) Devolverlo en un return."
        ],
        "ans": "C",
        "exp": "Un puntero void * no tiene tipo concreto, por lo que el compilador desconoce cuántos bytes ocupa lo que apunta. No se puede desreferenciar (*ptr) ni aplicar aritmética de punteros sin hacer previamente un cast (por ejemplo a char *)."
    },
    {
        "cat": "4",
        "title": "Sintaxis de puntero a función",
        "q": "En el prototipo 'char *ft_strmapi(char const *s, char (*f)(unsigned int, char));', ¿qué significa 'char (*f)(unsigned int, char)'?",
        "opts": [
            "A) Es una llamada recursiva a la función f.",
            "B) Es un puntero a una función que toma un unsigned int y un char como argumentos y devuelve un char.",
            "C) Es un array de caracteres llamado f.",
            "D) Es un casteo especial de memoria."
        ],
        "ans": "B",
        "exp": "Indica que ft_strmapi no recibe un dato, sino la dirección de memoria de una función que puede invocar en cada iteración ejecutando f(i, s[i])."
    },
    {
        "cat": "4",
        "title": "Diferencia entre strmapi y striteri",
        "q": "¿Por qué ft_striteri pasa 'char *' a la función f en 'void (*f)(unsigned int, char*)' mientras que ft_strmapi pasa 'char'?",
        "opts": [
            "A) Porque ft_striteri modifica el carácter en la cadena original pasando su dirección (&s[i]), mientras que ft_strmapi pasa una copia del carácter para construir un nuevo string.",
            "B) Porque ft_striteri solo sirve para números.",
            "C) Es un error de diseño del subject.",
            "D) Porque ft_strmapi no utiliza memoria dinámica."
        ],
        "ans": "A",
        "exp": "Al pasar la dirección (&s[i]), la función callback 'f' puede alterar directamente los bytes de la cadena original. En strmapi se pasa por valor porque se crea una cadena nueva con malloc."
    },

    # ========================================================
    # 5. ESTRUCTURAS DINÁMICAS Y LISTAS (t_list)
    # ========================================================
    {
        "cat": "5",
        "title": "Estructura t_list",
        "q": "Dada la estructura 'typedef struct s_list { void *content; struct s_list *next; } t_list;', ¿por qué 'next' es de tipo 'struct s_list *' y no simplemente 't_list'?",
        "opts": [
            "A) Porque un struct no puede contener una copia completa de sí mismo (tamaño infinito en memoria); debe contener un puntero a la siguiente caja.",
            "B) Porque los structs no admiten punteros directos.",
            "C) Porque la palabra t_list aún no se ha terminado de definir con el typedef en ese punto.",
            "D) Ambas opciones A y C son correctas."
        ],
        "ans": "D",
        "exp": "Un nodo no puede contener un nodo entero dentro (recursión infinita de tamaño), solo la dirección del siguiente en la RAM. Además, dentro del cuerpo del struct, el alias typedef t_list todavía no está cerrado, por lo que debe usarse struct s_list *."
    },
    {
        "cat": "5",
        "title": "Liberación en ft_lstclear",
        "q": "En 'ft_lstclear(t_list **lst, void (*del)(void *))', ¿cuál es el orden estricto para no provocar fugas ni segfaults?",
        "opts": [
            "A) free(actual); del(actual->content);",
            "B) Guardar temp = actual->next; llamar a del(actual->content); hacer free(actual); avanzar actual = temp.",
            "C) *lst = NULL; y luego llamar a free de todo el bloque.",
            "D) Llamar a free(del) primero."
        ],
        "ans": "B",
        "exp": "Si liberas 'actual' primero, pierdes el puntero 'actual->next' y no puedes avanzar al siguiente nodo. Siempre debes guardar el siguiente, destruir el contenido con del, liberar el nodo con free y avanzar."
    }
]

def clear():
    os.system('clear' if os.name == 'posix' else 'cls')

def run_quiz(pool, title):
    if not pool:
        print("\nNo hay preguntas disponibles.")
        input("\nPulsa [ENTER] para volver...")
        return

    random.shuffle(pool)
    score = 0
    total = len(pool)

    for i, q in enumerate(pool, start=1):
        clear()
        print("=" * 65)
        print(f" 🧪 {title} ({i}/{total})")
        print(f" Tema: {q['title']}")
        print("=" * 65)
        print(f"\n{q['q']}\n")
        for opt in q['opts']:
            print(f"  {opt}")
        print()

        while True:
            ans = input("Tu respuesta (A/B/C/D o Q para salir): ").strip().upper()
            if ans in ["A", "B", "C", "D", "Q"]:
                break

        if ans == "Q":
            break

        if ans == q["ans"]:
            score += 1
            print("\n✅ ¡CORRECTO!")
        else:
            print(f"\n❌ INCORRECTO. La respuesta correcta era: {q['ans']}")

        print(f"\n💡 EXPLICACIÓN TÉCNICA:\n{q['exp']}\n")
        input("Pulsa [ENTER] para continuar...")

    clear()
    print("=" * 65)
    print(f"  Resultado: {score}/{total} aciertos ({int((score/total)*100)}%)")
    print("=" * 65)
    input("\nPulsa [ENTER] para volver al menú...")

def main():
    while True:
        clear()
        print("=" * 65)
        print("   🧠 ENTRENADOR MAESTRO: VARIABLES, TIPOS Y MEMORIA EN C")
        print("=" * 65)
        print(" 1. Modo Examen Total (Todas las preguntas mezcladas)")
        print(" 2. Enteros, Tamaños y Rangos (int, size_t, char, unsigned)")
        print(" 3. Punteros y Modificadores (char *, const, static)")
        print(" 4. Punteros Dobles y Matrices (char **, t_list **)")
        print(" 5. Punteros Genéricos y Callbacks (void *, (*f)())")
        print(" 6. Estructuras Dinámicas y Listas (t_list)")
        print(" 7. Salir")
        print("=" * 65)
        opt = input("Elige una categoría (1-7): ").strip()

        if opt == "1":
            run_quiz(list(QUESTIONS), "TEST COMPLETO DE VARIABLES Y MEMORIA")
        elif opt in CATEGORIES:
            cat_id = str(int(opt) - 1)
            subset = [q for q in QUESTIONS if q["cat"] == cat_id]
            run_quiz(subset, CATEGORIES[cat_id].upper())
        elif opt == "7":
            clear()
            print("¡Ánimo con la Libft y el Cursus! Hasta pronto.\n")
            sys.exit(0)

if __name__ == "__main__":
    main()
