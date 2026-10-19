# **************************************************************************** #
#                                                                              #
#                                                         :::      ::::::::    #
#    c_master.py                                        :+:      :+:    :+:    #
#                                                     +:+ +:+         +:+      #
#    By: ssaavedr <ssaavedr@student.42urduliz.com>  +#+  +:+       +#+         #
#                                                 +#+#+#+#+#+   +#+            #
#    Created: 2026/10/19 23:33:39 by ssaavedr          #+#    #+#              #
#    Updated: 2026/10/19 23:33:42 by ssaavedr         ###   ########.fr        #
#                                                                              #
# **************************************************************************** #

#!/usr/bin/env python3
"""
C-Master CLI: Entrenador integral de fundamentos, punteros y memoria en C.
Enfocado en programación de sistemas, bajo nivel y desarrollo en Linux.
"""

import os
import random
import sys

CHALLENGES = [
    # ==========================================
    # CATEGORÍA 1: STACK VS HEAP Y SCOPE
    # ==========================================
    {
        "cat": "Memoria: Stack vs Heap",
        "title": "Retorno de variables locales",
        "code": """char *get_name(void)
{
    char name[] = "Urduliz";
    return (name);
}""",
        "q": "¿Qué ocurre cuando otra función llama a get_name() e intenta leer el resultado?",
        "opts": [
            "A) Imprime 'Urduliz' sin ningún problema.",
            "B) Comportamiento indefinido o fallo de segmentación (Dangling pointer / stack use-after-scope).",
            "C) La cadena se almacena automáticamente en el Heap.",
            "D) Provoca una fuga de memoria (leak)."
        ],
        "ans": "B",
        "exp": "El array 'char name[]' se reserva en el Stack (pila local) de get_name(). Al terminar la función, ese marco de pila se destruye. Devolver su dirección deja un puntero colgante (dangling pointer)."
    },
    {
        "cat": "Memoria: Stack vs Heap",
        "title": "Cadenas literales y permisos de solo lectura",
        "code": """char *str = "Hola";
str[0] = 'B';""",
        "q": "¿Qué sucede al intentar ejecutar la segunda línea en un sistema operativo moderno como Linux?",
        "opts": [
            "A) La cadena se convierte en 'Bola'.",
            "B) El compilador lanza un aviso pero cambia el valor en memoria.",
            "C) Segmentation fault (señal SIGSEGV) por intento de escritura en página de solo lectura (.rodata).",
            "D) La variable str se libera automáticamente."
        ],
        "ans": "C",
        "exp": "Los literales de cadena entre comillas dobles se ubican en el segmento de texto/solo lectura (.rodata). Intentar escribir en ellos viola los permisos de memoria y el núcleo (kernel) aborta el proceso con SIGSEGV."
    },

    # ==========================================
    # CATEGORÍA 2: CAZADOR DE BUGS Y LEAKS
    # ==========================================
    {
        "cat": "Cazador de Bugs",
        "title": "Pérdida de referencia en Heap (Memory Leak)",
        "code": """void process(void)
{
    char *ptr = malloc(32);
    ptr = malloc(64);
    free(ptr);
}""",
        "q": "¿Qué fallo técnico tiene esta función?",
        "opts": [
            "A) Ninguno, reasigna el tamaño correctamente a 64 bytes.",
            "B) Provoca una fuga de memoria (leak) de 32 bytes porque se sobreescribe el puntero original sin liberarlo.",
            "C) Provoca un Double Free al terminar.",
            "D) Falla la compilación por doble declaración."
        ],
        "ans": "B",
        "exp": "La dirección del primer bloque de 32 bytes se pierde al asignar el segundo malloc sobre 'ptr'. Ese bloque queda huérfano en el Heap sin posibilidad de ser liberado, provocando un leak permanente."
    },
    {
        "cat": "Cazador de Bugs",
        "title": "Liberación doble (Double Free)",
        "code": """void cleanup(char *s1)
{
    char *s2 = s1;
    free(s1);
    free(s2);
}""",
        "q": "¿Qué error reportará el sistema al ejecutar cleanup()?",
        "opts": [
            "A) Fuga de memoria.",
            "B) Desbordamiento de búfer (Buffer Overflow).",
            "C) Error de ejecución: 'double free or corruption' al intentar liberar dos veces la misma dirección física.",
            "D) La segunda llamada a free() no hace nada y el programa continúa."
        ],
        "ans": "C",
        "exp": "s1 y s2 contienen la misma dirección de memoria. La primera llamada a free() marca el bloque como disponible; la segunda llamada intenta liberar un bloque ya no asignado, corrompiendo la tabla del asignador de memoria."
    },

    # ==========================================
    # CATEGORÍA 3: ARITMÉTICA DE PUNTEROS
    # ==========================================
    {
        "cat": "Aritmética de Punteros",
        "title": "Avance en arrays de enteros",
        "code": """int tab[] = {10, 20, 30, 40, 50};
int *p = tab + 2;
printf("%d", *(p + 1));""",
        "q": "¿Qué número exacto imprime la llamada a printf?",
        "opts": [
            "A) 20",
            "B) 30",
            "C) 40",
            "D) 50"
        ],
        "ans": "C",
        "exp": "'tab' apunta a tab[0] (10). 'tab + 2' apunta a tab[2] (30). 'p + 1' apunta a tab[3] (40). Al desreferenciar con *(p + 1) obtenemos el valor 40."
    },
    {
        "cat": "Aritmética de Punteros",
        "title": "Equivalencia entre corchetes y desreferenciación",
        "code": """char str[] = "42Network";""",
        "q": "¿Cuál de las siguientes expresiones en C es completamente equivalente a 'str[3]'?",
        "opts": [
            "A) *(str + 3)",
            "B) *(3 + str)",
            "C) 3[str]",
            "D) Todas las anteriores son válidas y equivalentes en el estándar de C."
        ],
        "ans": "D",
        "exp": "En C, la notación a[b] se define formalmente como *((a) + (b)). Debido a la propiedad conmutativa de la suma, *(str + 3), *(3 + str) y 3[str] acceden exactamente a la misma posición de memoria."
    },

    # ==========================================
    # CATEGORÍA 4: COMPORTAMIENTO Y SINTAXIS
    # ==========================================
    {
        "cat": "Comportamiento del Compilador",
        "title": "Puntero nulo (NULL Pointer Dereference)",
        "code": """char *ptr = NULL;
*ptr = 'A';""",
        "q": "¿Qué sucede a nivel de sistema operativo al ejecutar la segunda instrucción?",
        "opts": [
            "A) Asigna 'A' a la dirección base 0x0 sin problema.",
            "B) El procesador lanza una interrupción de fallo de página (Page Fault) y el SO envía la señal SIGSEGV al proceso.",
            "C) El compilador optimiza la línea y la borra.",
            "D) Convierte ptr en un puntero válido al Stack."
        ],
        "ans": "B",
        "exp": "NULL equivale a la dirección 0x0. La primera página de la memoria virtual está intencionadamente desasignada y protegida por el SO para atrapar accesos nulos accidentales mediante un segmentation fault."
    },
    {
        "cat": "Punteros a Función",
        "title": "Mapeo y callbacks",
        "code": """int duplicate(int n) { return (n * 2); }
void apply(int *val, int (*f)(int)) { *val = f(*val); }""",
        "q": "¿Cómo se invoca 'apply' sobre una variable 'int x = 5;' para duplicar su valor?",
        "opts": [
            "A) apply(x, duplicate());",
            "B) apply(&x, duplicate);",
            "C) apply(&x, *duplicate);",
            "D) apply(x, &duplicate());"
        ],
        "ans": "B",
        "exp": "Se pasa la dirección de x mediante '&x' para que pueda ser modificada por desreferenciación, y el nombre de la función 'duplicate' sin paréntesis para pasar su dirección de memoria como puntero a función."
    }
]

def clear():
    os.system('clear' if os.name == 'posix' else 'cls')

def run_trainer(pool, title):
    if not pool:
        print("\nNo hay ejercicios en esta categoría.")
        input("\nPulsa [ENTER] para regresar...")
        return

    random.shuffle(pool)
    score = 0
    total = len(pool)

    for i, item in enumerate(pool, start=1):
        clear()
        print("=" * 68)
        print(f" ⚙️  {title.upper()} ({i}/{total}) | {item['cat']}")
        print("=" * 68)
        print(f"\nDesafío: \033[1;36m{item['title']}\033[0m\n")

        if "code" in item and item["code"]:
            print("```c")
            print(item["code"])
            print("```\n")

        print(item["q"] + "\n")
        for opt in item["opts"]:
            print(f"  {opt}")
        print()

        while True:
            ans = input("Tu deducción (A/B/C/D o Q para salir): ").strip().upper()
            if ans in ["A", "B", "C", "D", "Q"]:
                break
            print("Opción inválida. Usa A, B, C o D.")

        if ans == "Q":
            print("\nSesión finalizada.")
            break

        if ans == item["ans"]:
            score += 1
            print("\n✅ ¡EXCELENTE DEDUCCIÓN!")
        else:
            print(f"\n❌ INCORRECTO. La opción correcta era: {item['ans']}")

        print(f"\n💡 ANÁLISIS DE BAJO NIVEL:\n{item['exp']}\n")
        input("Pulsa [ENTER] para continuar...")

    clear()
    print("=" * 68)
    print(f"  ENTRENAMIENTO COMPLETADO: {score}/{total} aciertos ({int((score/total)*100)}%)")
    print("=" * 68)
    if score == total:
        print("🏆 Dominio total de la memoria y punteros en C.")
    elif score >= total * 0.7:
        print("📈 Muy buen razonamiento. Solo falta pulir casos extremos.")
    else:
        print("🛠️ Sigue practicando: la memoria en C se asimila analizando errores reales.")
    input("\nPulsa [ENTER] para volver al menú principal...")

def main():
    while True:
        clear()
        print("=" * 68)
        print("          🛡️  C-MASTER CLI: ENTRENADOR DE BAJO NIVEL")
        print("=" * 68)
        print(" 1. Modo Completo Mixto (Todos los retos mezclados)")
        print(" 2. Stack vs Heap y Ámbito de Memoria (.rodata, data, bss)")
        print(" 3. Cazador de Bugs (Leaks, Double Free, Dangling Pointers)")
        print(" 4. Aritmética de Punteros y Arrays (Offset, Indices, Desref)")
        print(" 5. Comportamiento Indefinido y Punteros a Función")
        print(" 6. Salir")
        print("=" * 68)
        opt = input("Elige una disciplina de estudio (1-6): ").strip()

        if opt == "1":
            run_trainer(list(CHALLENGES), "Modo Completo")
        elif opt == "2":
            subset = [c for c in CHALLENGES if "Stack vs Heap" in c["cat"]]
            run_trainer(subset, "Stack vs Heap")
        elif opt == "3":
            subset = [c for c in CHALLENGES if "Cazador de Bugs" in c["cat"]]
            run_trainer(subset, "Cazador de Bugs")
        elif opt == "4":
            subset = [c for c in CHALLENGES if "Aritmética de Punteros" in c["cat"]]
            run_trainer(subset, "Aritmética de Punteros")
        elif opt == "5":
            subset = [c for c in CHALLENGES if "Comportamiento" in c["cat"] or "Callbacks" in c["cat"]]
            run_trainer(subset, "Comportamiento y Callbacks")
        elif opt == "6":
            clear()
            print("¡Hasta la próxima sesión de código!\n")
            sys.exit(0)

if __name__ == "__main__":
    main()
