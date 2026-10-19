# **************************************************************************** #
#                                                                              #
#                                                         :::      ::::::::    #
#    libft_cards.py                                     :+:      :+:    :+:    #
#                                                     +:+ +:+         +:+      #
#    By: ssaavedr <ssaavedr@student.42urduliz.com>  +#+  +:+       +#+         #
#                                                 +#+#+#+#+#+   +#+            #
#    Created: 2026/10/19 23:34:35 by ssaavedr          #+#    #+#              #
#    Updated: 2026/10/19 23:34:36 by ssaavedr         ###   ########.fr        #
#                                                                              #
# **************************************************************************** #

#!/usr/bin/env python3
"""
Entrenador de Memoria y Funciones para Libft 42 (Subject v19.3).
Incluye las 43 funciones:
 - Parte 1: Libc (23 funciones)
 - Parte 2: Adicionales (11 funciones)
 - Parte 3: Listas enlazadas (9 funciones)
"""

import os
import random
import sys

FUNCTIONS_DB = [
    # ==========================================
    # PARTE 1: FUNCIONES DE LIBC (23)
    # ==========================================
    {
        "name": "ft_isalpha",
        "part": "Parte 1: Libc",
        "proto": "int ft_isalpha(int c);",
        "desc": "Comprueba si el carácter recibido es alfabético (a-z o A-Z).",
        "ret": "Devuelve 1 si es alfabético, 0 si no lo es.",
        "trap": "Recibe un int (no un char) para compatibilidad con EOF (-1)."
    },
    {
        "name": "ft_isdigit",
        "part": "Parte 1: Libc",
        "proto": "int ft_isdigit(int c);",
        "desc": "Comprueba si el carácter recibido es un dígito decimal ('0' a '9').",
        "ret": "Devuelve 1 si cumple la condición, 0 si no.",
        "trap": "Comprueba el código ASCII del carácter entre '0' (48) y '9' (57)."
    },
    {
        "name": "ft_isalnum",
        "part": "Parte 1: Libc",
        "proto": "int ft_isalnum(int c);",
        "desc": "Comprueba si el carácter es alfanumérico (es letra o dígito).",
        "ret": "Devuelve 1 si es letra o número, 0 en caso contrario.",
        "trap": "Equivale a comprobar ft_isalpha(c) || ft_isdigit(c)."
    },
    {
        "name": "ft_isascii",
        "part": "Parte 1: Libc",
        "proto": "int ft_isascii(int c);",
        "desc": "Comprueba si el entero cabe en la tabla ASCII de 7 bits (0 a 127).",
        "ret": "Devuelve 1 si está entre 0 y 127, 0 si está fuera.",
        "trap": "Acepta cualquier int sin desbordar; solo mira si 0 <= c <= 127."
    },
    {
        "name": "ft_isprint",
        "part": "Parte 1: Libc",
        "proto": "int ft_isprint(int c);",
        "desc": "Comprueba si el carácter es imprimible, incluyendo el espacio.",
        "ret": "Devuelve 1 si está entre 32 y 126 (ambos incluidos), 0 si no.",
        "trap": "El espacio (32) cuenta como imprimible. Los saltos de línea (\\n, \\t) NO."
    },
    {
        "name": "ft_strlen",
        "part": "Parte 1: Libc",
        "proto": "size_t ft_strlen(const char *s);",
        "desc": "Calcula la longitud de la cadena de texto hasta el carácter '\\0'.",
        "ret": "Devuelve el número de caracteres como size_t (sin contar el '\\0').",
        "trap": "No cuenta el byte nulo final. Si recibe NULL sin proteger, produce segfault."
    },
    {
        "name": "ft_memset",
        "part": "Parte 1: Libc",
        "proto": "void *ft_memset(void *s, int c, size_t n);",
        "desc": "Rellena los primeros 'n' bytes del bloque de memoria 's' con el byte 'c'.",
        "ret": "Devuelve el puntero original 's'.",
        "trap": "El parámetro 'c' se convierte internamente a unsigned char antes de escribir."
    },
    {
        "name": "ft_bzero",
        "part": "Parte 1: Libc",
        "proto": "void ft_bzero(void *s, size_t n);",
        "desc": "Escribe ceros ('\\0') en los primeros 'n' bytes del bloque de memoria.",
        "ret": "No devuelve nada (void).",
        "trap": "Es equivalente a ft_memset(s, 0, n), pero no devuelve ningún puntero."
    },
    {
        "name": "ft_memcpy",
        "part": "Parte 1: Libc",
        "proto": "void *ft_memcpy(void *dest, const void *src, size_t n);",
        "desc": "Copia 'n' bytes desde la memoria 'src' hacia la memoria 'dest'.",
        "ret": "Devuelve el puntero destino 'dest'.",
        "trap": "NO maneja solapamiento (overlap). Si dest y src se pisan, usa ft_memmove."
    },
    {
        "name": "ft_memmove",
        "part": "Parte 1: Libc",
        "proto": "void *ft_memmove(void *dest, const void *src, size_t n);",
        "desc": "Copia 'n' bytes de 'src' a 'dest' de forma segura aunque se solapen.",
        "ret": "Devuelve el puntero 'dest'.",
        "trap": "Si dest > src, debe copiar de atrás hacia adelante para no sobreescribir datos."
    },
    {
        "name": "ft_strlcpy",
        "part": "Parte 1: Libc",
        "proto": "size_t ft_strlcpy(char *dst, const char *src, size_t size);",
        "desc": "Copia hasta size - 1 caracteres de src a dst, terminando siempre en '\\0'.",
        "ret": "Devuelve la longitud total de 'src' (lo que intentó copiar).",
        "trap": "Si size es 0, no escribe nada ni pone '\\0', pero sigue devolviendo strlen(src)."
    },
    {
        "name": "ft_strlcat",
        "part": "Parte 1: Libc",
        "proto": "size_t ft_strlcat(char *dst, const char *src, size_t size);",
        "desc": "Concatena 'src' al final de 'dst', garantizando que el total no supere 'size'.",
        "ret": "Devuelve strlen(dst inicial) + strlen(src). Si size <= dst_len, devuelve size + strlen(src).",
        "trap": "Calcula el tamaño que intentó crear para detectar truncamientos."
    },
    {
        "name": "ft_toupper",
        "part": "Parte 1: Libc",
        "proto": "int ft_toupper(int c);",
        "desc": "Convierte una letra minúscula a mayúscula si es posible.",
        "ret": "Devuelve la letra en mayúscula o el valor original de 'c' si no era minúscula.",
        "trap": "Resta 32 solo si 'c' está estrictamente entre 'a' y 'z'."
    },
    {
        "name": "ft_tolower",
        "part": "Parte 1: Libc",
        "proto": "int ft_tolower(int c);",
        "desc": "Convierte una letra mayúscula a minúscula si es posible.",
        "ret": "Devuelve la letra en minúscula o el valor original si no era mayúscula.",
        "trap": "Suma 32 solo si 'c' está estrictamente entre 'A' y 'Z'."
    },
    {
        "name": "ft_strchr",
        "part": "Parte 1: Libc",
        "proto": "char *ft_strchr(const char *s, int c);",
        "desc": "Busca la primera aparición del carácter 'c' en la cadena 's'.",
        "ret": "Puntero a la primera coincidencia, o NULL si no se encuentra.",
        "trap": "Si buscas '\\0', debe devolver el puntero al carácter nulo final, NO NULL."
    },
    {
        "name": "ft_strrchr",
        "part": "Parte 1: Libc",
        "proto": "char *ft_strrchr(const char *s, int c);",
        "desc": "Busca la última aparición del carácter 'c' en la cadena 's'.",
        "ret": "Puntero a la última coincidencia, o NULL si no existe.",
        "trap": "Recorre desde el final hacia el principio o guarda la última posición vista."
    },
    {
        "name": "ft_strncmp",
        "part": "Parte 1: Libc",
        "proto": "int ft_strncmp(const char *s1, const char *s2, size_t n);",
        "desc": "Compara hasta 'n' caracteres entre dos cadenas de texto.",
        "ret": "0 si son iguales en esos 'n' bytes, o la resta (s1[i] - s2[i]) como unsigned char.",
        "trap": "Los caracteres deben castearse a (unsigned char) antes de restar para evitar signos erróneos."
    },
    {
        "name": "ft_memchr",
        "part": "Parte 1: Libc",
        "proto": "void *ft_memchr(const void *s, int c, size_t n);",
        "desc": "Busca el primer byte 'c' dentro de los primeros 'n' bytes de un bloque de memoria.",
        "ret": "Puntero al byte coincidente, o NULL si no aparece en los 'n' bytes.",
        "trap": "No se detiene al encontrar '\\0', examina estrictamente los 'n' bytes completos."
    },
    {
        "name": "ft_memcmp",
        "part": "Parte 1: Libc",
        "proto": "int ft_memcmp(const void *s1, const void *s2, size_t n);",
        "desc": "Compara los primeros 'n' bytes de dos bloques de memoria.",
        "ret": "0 si son idénticos, o la diferencia (s1[i] - s2[i]) como unsigned char.",
        "trap": "Al igual que ft_memchr, no frena con '\\0', compara exactamente 'n' bytes."
    },
    {
        "name": "ft_strnstr",
        "part": "Parte 1: Libc",
        "proto": "char *ft_strnstr(const char *big, const char *little, size_t len);",
        "desc": "Busca la subcadena 'little' dentro de 'big' sin examinar más allá de 'len' caracteres.",
        "ret": "Puntero al inicio de la coincidencia, 'big' si little está vacía, o NULL si no se encuentra.",
        "trap": "Si la longitud de 'little' supera a 'len', debe devolver NULL de inmediato."
    },
    {
        "name": "ft_atoi",
        "part": "Parte 1: Libc",
        "proto": "int ft_atoi(const char *nptr);",
        "desc": "Convierte una cadena con números en su valor entero equivalente (int).",
        "ret": "El número entero resultante.",
        "trap": "Salta espacios iniciales (isspace) y solo acepta UN único signo (+ o -)."
    },
    {
        "name": "ft_calloc",
        "part": "Parte 1: Libc",
        "proto": "void *ft_calloc(size_t nmemb, size_t size);",
        "desc": "Reserva memoria para un array de elementos y limpia todos los bytes a 0.",
        "ret": "Puntero a la memoria reservada limpia, o NULL si falla el malloc.",
        "trap": "Si nmemb o size es 0, debe devolver un puntero único válido para pasar a free()."
    },
    {
        "name": "ft_strdup",
        "part": "Parte 1: Libc",
        "proto": "char *ft_strdup(const char *s);",
        "desc": "Duplica la cadena 's' reservando memoria dinámica nueva con malloc.",
        "ret": "Puntero a la nueva cadena clonada, o NULL si malloc falla.",
        "trap": "Requiere reservar strlen(s) + 1 para copiar también el terminador nulo '\\0'."
    },

    # ==========================================
    # PARTE 2: FUNCIONES ADICIONALES (11)
    # ==========================================
    {
        "name": "ft_substr",
        "part": "Parte 2: Adicionales",
        "proto": "char *ft_substr(char const *s, unsigned int start, size_t len);",
        "desc": "Extrae una subcadena de 's' que empieza en el índice 'start' y mide máximo 'len'.",
        "ret": "La nueva cadena reservada con malloc, o NULL si falla la asignación.",
        "trap": "Si start >= strlen(s), debe devolver ft_strdup(\"\") (un puntero liberable), no NULL."
    },
    {
        "name": "ft_strjoin",
        "part": "Parte 2: Adicionales",
        "proto": "char *ft_strjoin(char const *s1, char const *s2);",
        "desc": "Une las cadenas 's1' y 's2' en una nueva cadena creada dinámicamente.",
        "ret": "La cadena concatenada en el heap, o NULL si falla la reserva.",
        "trap": "Reserva strlen(s1) + strlen(s2) + 1 bytes. No modifica las originales."
    },
    {
        "name": "ft_strtrim",
        "part": "Parte 2: Adicionales",
        "proto": "char *ft_strtrim(char const *s1, char const *set);",
        "desc": "Crea una copia de 's1' eliminando del inicio y del final los caracteres presentes en 'set'.",
        "ret": "La cadena recortada con malloc, o NULL si falla la asignación.",
        "trap": "Solo recorta de los extremos; no elimina caracteres de 'set' que estén en el medio."
    },
    {
        "name": "ft_split",
        "part": "Parte 2: Adicionales",
        "proto": "char **ft_split(char const *s, char c);",
        "desc": "Divide 's' en un array de palabras (char **) separadas por el carácter 'c'.",
        "ret": "El array de cadenas terminado en NULL, o NULL si falla cualquier malloc.",
        "trap": "Si falla un malloc a mitad de camino, debe liberar todas las cadenas previas y el array padre."
    },
    {
        "name": "ft_itoa",
        "part": "Parte 2: Adicionales",
        "proto": "char *ft_itoa(int n);",
        "desc": "Convierte un entero (int) en una cadena de caracteres creada con malloc.",
        "ret": "El string que representa al número, o NULL si falla la memoria.",
        "trap": "Cuidado con INT_MIN (-2147483648): cambiarle el signo a secas desborda un int con signo."
    },
    {
        "name": "ft_strmapi",
        "part": "Parte 2: Adicionales",
        "proto": "char *ft_strmapi(char const *s, char (*f)(unsigned int, char));",
        "desc": "Aplica la función 'f' a cada carácter de 's' para generar una nueva cadena con malloc.",
        "ret": "La nueva cadena resultante, o NULL si la asignación falla.",
        "trap": "Pasa como argumentos a 'f' el índice del carácter (unsigned int) y el carácter en sí."
    },
    {
        "name": "ft_striteri",
        "part": "Parte 2: Adicionales",
        "proto": "void ft_striteri(char *s, void (*f)(unsigned int, char*));",
        "desc": "Aplica la función 'f' a cada carácter de la cadena 's' modificándola directamente (in-place).",
        "ret": "No devuelve nada (void).",
        "trap": "Pasa la dirección (&s[i]) a la función para que esta pueda alterar la letra original."
    },
    {
        "name": "ft_putchar_fd",
        "part": "Parte 2: Adicionales",
        "proto": "void ft_putchar_fd(char c, int fd);",
        "desc": "Escribe el carácter 'c' en el descriptor de archivo (fd) especificado usando write.",
        "ret": "No devuelve nada (void).",
        "trap": "Llama directamente a write(fd, &c, 1)."
    },
    {
        "name": "ft_putstr_fd",
        "part": "Parte 2: Adicionales",
        "proto": "void ft_putstr_fd(char *s, int fd);",
        "desc": "Escribe la cadena de texto 's' completa en el descriptor de archivo 'fd'.",
        "ret": "No devuelve nada (void).",
        "trap": "Usa ft_strlen o recorre con write mientras s no sea nulo."
    },
    {
        "name": "ft_putendl_fd",
        "part": "Parte 2: Adicionales",
        "proto": "void ft_putendl_fd(char *s, int fd);",
        "desc": "Escribe la cadena 's' en el descriptor 'fd' seguida de un salto de línea ('\\n').",
        "ret": "No devuelve nada (void).",
        "trap": "Equivale a llamar a ft_putstr_fd(s, fd) y luego ft_putchar_fd('\\n', fd)."
    },
    {
        "name": "ft_putnbr_fd",
        "part": "Parte 2: Adicionales",
        "proto": "void ft_putnbr_fd(int n, int fd);",
        "desc": "Escribe el número entero 'n' en el descriptor de archivo 'fd'.",
        "ret": "No devuelve nada (void).",
        "trap": "Gestionar números negativos y el caso límite de INT_MIN sin desbordar."
    },

    # ==========================================
    # PARTE 3: LISTAS ENLAZADAS (9)
    # ==========================================
    {
        "name": "ft_lstnew",
        "part": "Parte 3: Listas Enlazadas",
        "proto": "t_list *ft_lstnew(void *content);",
        "desc": "Crea y reserva un nuevo nodo de lista con 'content' y inicializa 'next' a NULL.",
        "ret": "Puntero al nuevo nodo creado (t_list *), o NULL si falla el malloc.",
        "trap": "El contenido se asigna por puntero directo: node->content = content."
    },
    {
        "name": "ft_lstadd_front",
        "part": "Parte 3: Listas Enlazadas",
        "proto": "void ft_lstadd_front(t_list **lst, t_list *new);",
        "desc": "Añade el nodo 'new' al principio de la lista enlazada.",
        "ret": "No devuelve nada (void).",
        "trap": "Recibe t_list ** para poder actualizar la cabeza de la lista si estaba vacía (*lst == NULL)."
    },
    {
        "name": "ft_lstsize",
        "part": "Parte 3: Listas Enlazadas",
        "proto": "unsigned int ft_lstsize(t_list *lst);",
        "desc": "Cuenta y devuelve el número total de nodos que componen la lista.",
        "ret": "La cantidad de elementos de la lista como entero sin signo.",
        "trap": "Recorre con un puntero temporal hasta encontrar lst == NULL."
    },
    {
        "name": "ft_lstlast",
        "part": "Parte 3: Listas Enlazadas",
        "proto": "t_list *ft_lstlast(t_list *lst);",
        "desc": "Devuelve el puntero al último nodo de la lista enlazada.",
        "ret": "El último nodo, o NULL si la lista de entrada está completamente vacía.",
        "trap": "La condición del bucle debe ser while (lst && lst->next) para frenar en el último nodo."
    },
    {
        "name": "ft_lstadd_back",
        "part": "Parte 3: Listas Enlazadas",
        "proto": "void ft_lstadd_back(t_list **lst, t_list *new);",
        "desc": "Añade el nodo 'new' al final de la lista.",
        "ret": "No devuelve nada (void).",
        "trap": "Si la lista está vacía (*lst == NULL), el nuevo nodo se convierte en el primero (*lst = new)."
    },
    {
        "name": "ft_lstdelone",
        "part": "Parte 3: Listas Enlazadas",
        "proto": "void ft_lstdelone(t_list *lst, void (*del)(void *));",
        "desc": "Libera la memoria del contenido con la función 'del' y luego libera el nodo con free.",
        "ret": "No devuelve nada (void).",
        "trap": "NO libera ni modifica el nodo siguiente (lst->next); solo destruye ese nodo individual."
    },
    {
        "name": "ft_lstclear",
        "part": "Parte 3: Listas Enlazadas",
        "proto": "void ft_lstclear(t_list **lst, void (*del)(void *));",
        "desc": "Libera y borra el nodo dado y TODOS sus sucesores en cadena, dejando *lst en NULL.",
        "ret": "No devuelve nada (void).",
        "trap": "Debes guardar el puntero al siguiente (next = actual->next) antes de hacer free del actual."
    },
    {
        "name": "ft_lstiter",
        "part": "Parte 3: Listas Enlazadas",
        "proto": "void ft_lstiter(t_list *lst, void (*f)(void *));",
        "desc": "Itera por todos los nodos de la lista y aplica la función 'f' al contenido de cada uno.",
        "ret": "No devuelve nada (void).",
        "trap": "Solo recorre y ejecuta f(lst->content); no altera la estructura de enlaces de la lista."
    },
    {
        "name": "ft_lstmap",
        "part": "Parte 3: Listas Enlazadas",
        "proto": "t_list *ft_lstmap(t_list *lst, void *(*f)(void *), void (*del)(void *));",
        "desc": "Crea una lista NUEVA aplicando la función 'f' al contenido de cada nodo de la lista original.",
        "ret": "Puntero a la nueva lista creada, o NULL si falla cualquier malloc.",
        "trap": "Si falla una reserva en mitad del proceso, debe usar 'del' y 'ft_lstclear' en la lista parcial."
    }
]

def clear():
    os.system('clear' if os.name == 'posix' else 'cls')

def run_flashcards(pool):
    random.shuffle(pool)
    known = 0
    total = len(pool)

    for i, f in enumerate(pool, start=1):
        clear()
        print("=" * 65)
        print(f" 📇 MODO FLASHCARD ({i}/{total}) | {f['part']}")
        print("=" * 65)
        print(f"\nFunción:   \033[1;36m{f['name']}\033[0m")
        print(f"Prototipo: \033[1;33m{f['proto']}\033[0m\n")
        print("Piensa: ¿Qué hace? ¿Qué memoria usa? ¿Cuál es su comportamiento clave?")
        input("\n[PULSA ENTER PARA REVELAR LA RESPUESTA]")

        print("\n" + "-" * 65)
        print(f"🎯 PROPÓSITO: {f['desc']}")
        print(f"↩️ RETORNO:   {f['ret']}")
        print(f"⚠️ CLAVE/TRAMPA: {f['trap']}")
        print("-" * 65)

        while True:
            resp = input("\n¿Te la sabías bien? (s/n/q para salir): ").strip().lower()
            if resp in ['s', 'n', 'q']:
                break
        if resp == 'q':
            break
        if resp == 's':
            known += 1

    clear()
    print("=" * 65)
    print(f"  Tarjetas repasadas. Dominadas: {known} de {total}")
    print("=" * 65)
    input("\nPulsa [ENTER] para regresar...")

def run_quiz_mode(pool):
    random.shuffle(pool)
    score = 0
    total = min(15, len(pool))

    for i in range(total):
        target = pool[i]
        # Seleccionar 3 distractores
        distractors = [f for f in FUNCTIONS_DB if f["name"] != target["name"]]
        options = random.sample(distractors, 3) + [target]
        random.shuffle(options)

        clear()
        print("=" * 65)
        print(f" 🧩 QUIZ IDENTIFICADOR ({i+1}/{total}) | {target['part']}")
        print("=" * 65)
        print(f"\n¿A qué función corresponde esta descripción?\n")
        print(f"\"{target['desc']}\"\n")
        print(f"Retorno: {target['ret']}\n")

        letters = ["A", "B", "C", "D"]
        correct_letter = ""
        for idx, opt in enumerate(options):
            print(f"  {letters[idx]}) {opt['name']}  -->  {opt['proto']}")
            if opt["name"] == target["name"]:
                correct_letter = letters[idx]
        print()

        while True:
            ans = input("Tu respuesta (A/B/C/D o Q para salir): ").strip().upper()
            if ans in ["A", "B", "C", "D", "Q"]:
                break

        if ans == "Q":
            break

        if ans == correct_letter:
            score += 1
            print(f"\n✅ ¡Correcto! Era {target['name']}.")
        else:
            print(f"\n❌ Incorrecto. La opción correcta era {correct_letter}) {target['name']}.")
        print(f"💡 Nota clave: {target['trap']}")
        input("\nPulsa [ENTER] para continuar...")

    clear()
    print(f"Quiz terminado: {score} aciertos de {total}.")
    input("\nPulsa [ENTER] para regresar...")

def filter_menu():
    while True:
        clear()
        print("=" * 65)
        print("      📚 MEMORIZADOR OFICIAL LIBFT (43 FUNCIONES)")
        print("=" * 65)
        print(" 1. Todas las funciones (43 funciones)")
        print(" 2. Solo Parte 1: Libc (23 funciones)")
        print(" 3. Solo Parte 2: Adicionales (11 funciones)")
        print(" 4. Solo Parte 3: Listas Enlazadas (9 funciones)")
        print(" 5. Salir")
        print("=" * 65)
        c = input("Selecciona el bloque a repasar (1-5): ").strip()

        if c == "1":
            return list(FUNCTIONS_DB)
        elif c == "2":
            return [f for f in FUNCTIONS_DB if "Parte 1" in f["part"]]
        elif c == "3":
            return [f for f in FUNCTIONS_DB if "Parte 2" in f["part"]]
        elif c == "4":
            return [f for f in FUNCTIONS_DB if "Parte 3" in f["part"]]
        elif c == "5":
            return None

def main():
    while True:
        clear()
        print("=" * 65)
        print("        🎯 ENTRENADOR DE MEMORIA DE FUNCIONES - 42")
        print("=" * 65)
        print(" 1. Modo Tarjetas Flash (Estudiar y memorizar a tu ritmo)")
        print(" 2. Modo Quiz Examen (Preguntas de opción múltiple)")
        print(" 3. Salir")
        print("=" * 65)
        opt = input("Elige una modalidad (1-3): ").strip()

        if opt == "1":
            subset = filter_menu()
            if subset:
                run_flashcards(subset)
        elif opt == "2":
            subset = filter_menu()
            if subset:
                run_quiz_mode(subset)
        elif opt == "3":
            clear()
            print("¡A por todas en la evaluación!\n")
            sys.exit(0)

if __name__ == "__main__":
    main()
