import random

class Personaje: #clase personaje, con nombre, hp, atk y defensa
    def __init__(self, nombre, hp, atk, defensa): 
        self.nombre = nombre
        self.hp = hp
        self.max_hp = hp
        self.atk = atk
        self.defensa = defensa

    def atacar(self, objetivo):#función para atacar a otro personaje
        danio = self.atk - objetivo.defensa#el daño se calcula con el ataque del atacante menos la defensa del objetivo
        if danio < 1:
            danio = 1

        if random.random() < 0.2:#20% de probabilidad de crítico, el daño se duplica
            danio *= 2
            print(f"CRÍTICO: {self.nombre} hizo {danio} a {objetivo.nombre}")
        else:
            print(f"{self.nombre} hizo {danio} a {objetivo.nombre}")

        objetivo.hp -= danio


# ---------------- COMBATE ----------------

def pelea_recursiva(ataca, defiende):#función recursiva para manejar el combate entre dos personajes
    if ataca.hp <= 0:
        return defiende, ataca 
    if defiende.hp <= 0:
        return ataca, defiende

    ataca.atacar(defiende)

    return pelea_recursiva(defiende, ataca)


# ---------------- UTILIDADES RECURSIVAS ----------------

def mostrar_equipo(equipo, i=0):#función recursiva para mostrar el equipo de personajes, indicando si están en KO o su HP actual
    if i < len(equipo): #
        p = equipo[i]
        estado = "KO" if p.hp <= 0 else f"HP:{p.hp}"
        print(f"{i}. {p.nombre} ({estado})")#imprime el índice, nombre y estado del personaje
        mostrar_equipo(equipo, i + 1)


def elegir_personaje(equipo): #función para elegir un personaje del equipo, verificando que la entrada sea válida y que el personaje no esté en KO
    print("\nElige personaje:")
    mostrar_equipo(equipo)

    try:
        idx = int(input("> "))
        if 0 <= idx < len(equipo) and equipo[idx].hp > 0:
            return equipo[idx]
        else:
            print("Inválido o en KO")
            return elegir_personaje(equipo)
    except:
        print("Entrada inválida")
        return elegir_personaje(equipo)


def eliminar_personaje(lista, objetivo, i=0):
    if i >= len(lista):
        return lista

    if lista[i] == objetivo:
        return lista[:i] + lista[i+1:]

    return eliminar_personaje(lista, objetivo, i + 1)


# ---------------- TRANSFERENCIA ----------------

def procesar_resultado(ganador, perdedor, equipo_ganador, equipo_perdedor, es_jugador_ganador):
    if es_jugador_ganador:
        print(f"\n¡BIEN HECHO! {ganador.nombre} derrotó a {perdedor.nombre}. Se une a tu equipo.")
    else:
        print(f"\n¡MALA SUERTE! {ganador.nombre} derrotó a {perdedor.nombre}. El enemigo te lo ha robado.")

    # Restaurar vida al máximo para el nuevo bando
    perdedor.hp = perdedor.max_hp

    # Transferir personaje
    equipo_ganador.append(perdedor)
    nuevo_equipo_perdedor = eliminar_personaje(equipo_perdedor, perdedor)

    return equipo_ganador, nuevo_equipo_perdedor


# ---------------- BATALLA TOTAL ----------------

def batalla_total(mi_equipo, enemigo_equipo, puntos=0):
    if not mi_equipo:
        print(f"\n--- GAME OVER ---")
        print(f"Perdiste todo tu equipo. Puntaje final: {puntos}")
        return
    if not enemigo_equipo:
        print(f"\n--- ¡VICTORIA TOTAL! ---")
        print(f"Has reclutado a todos. Puntaje final: {puntos}")
        return

    print("\n--- TU TURNO DE ATACAR ---")
    mi_p = elegir_personaje(mi_equipo)

    # El enemigo elige a alguien al azar de su equipo actual
    enemigo_p = enemigo_equipo[random.randint(0, len(enemigo_equipo)-1)]
    print(f"El enemigo envía a {enemigo_p.nombre} a la batalla.")

    ganador, perdedor = pelea_recursiva(mi_p, enemigo_p)

    # Verificamos quién ganó comparando los objetos
    if ganador == mi_p:
        # Ganó el jugador: robas al enemigo
        mi_equipo, enemigo_equipo = procesar_resultado(
            ganador, perdedor, mi_equipo, enemigo_equipo, True
        )
        return batalla_total(mi_equipo, enemigo_equipo, puntos + 1)
    else:
        # Ganó el enemigo: te roban a tu personaje
        enemigo_equipo, mi_equipo = procesar_resultado(
            ganador, perdedor, enemigo_equipo, mi_equipo, False
        )
        # Se sigue la batalla con lo que te queda
        return batalla_total(mi_equipo, enemigo_equipo, puntos)


# ---------------- CARGA DE DATOS ----------------

def cargar_datos():#función para cargar los datos de los personajes desde un archivo de texto, utilizando recursión
    with open("Zproyecto_imaginary_battle/personajes.txt", "r", encoding="utf-8") as f:
        lineas = f.readlines()

    def leer(i):
        if i >= len(lineas):
            return []

        datos = lineas[i].strip().split(",")

        if len(datos) < 4:
            return leer(i + 1)

        p = Personaje(datos[0], int(datos[1]), int(datos[2]), int(datos[3]))
        return [p] + leer(i + 1)

    return leer(0)


# ---------------- SELECCIÓN ----------------

def seleccionar(lista, cantidad):
    if cantidad == 0:
        return []

    mostrar_equipo(lista)

    try:
        idx = int(input(f"\nElige ({cantidad} restantes): "))
        if 0 <= idx < len(lista):
            elegido = lista[idx]
            nueva_lista = lista[:idx] + lista[idx+1:]
            return [elegido] + seleccionar(nueva_lista, cantidad - 1)
        else:
            return seleccionar(lista, cantidad)
    except:
        return seleccionar(lista, cantidad)


# ---------------- MAIN ----------------

todos = cargar_datos() #
copia = todos[:] #hacemos una copia de la lista de personajes para evitar modificar la original

print("\n--- SELECCIÓN ---")
mis_personajes = seleccionar(copia, 3)

# enemigo usa lista restante (evita duplicados)
enemigos = random.sample(copia, 3)

print("\nTu equipo:")
mostrar_equipo(mis_personajes)

print("\nEquipo enemigo:")
mostrar_equipo(enemigos)

batalla_total(mis_personajes, enemigos)