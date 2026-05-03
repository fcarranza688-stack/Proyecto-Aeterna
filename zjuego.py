import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk
import os
import random

# --- CLASE PERSONAJE ---
class Personaje:
    def __init__(self, nombre, hp, atk, defensa):
        self.nombre = nombre
        self.hp = int(hp)
        self.max_hp = int(hp)
        self.atk = int(atk)
        self.defensa = int(defensa)

    def atacar(self, objetivo):
        danio = self.atk - objetivo.defensa
        if danio < 1: danio = 1
        critico = random.random() < 0.2
        if critico: danio *= 2
        objetivo.hp -= danio
        return danio, critico

# --- UTILIDADES ---
def buscar_archivo(nombre_archivo, ruta_busqueda="."):
    for raiz, _, archivos in os.walk(ruta_busqueda):
        if nombre_archivo in archivos:
            return os.path.join(raiz, nombre_archivo)
    return None

def cargar_datos():
    ruta_txt = buscar_archivo("personajes.txt", os.path.expanduser("~"))
    if not ruta_txt: return []
    with open(ruta_txt, "r", encoding="utf-8") as f:
        lineas = f.readlines()
    def leer_recursivo(i):
        if i >= len(lineas): return []
        datos = lineas[i].strip().split(",")
        if len(datos) < 4: return leer_recursivo(i + 1)
        p = Personaje(datos[0].strip(), datos[1], datos[2], datos[3])
        return [p] + leer_recursivo(i + 1)
    return leer_recursivo(0)

def cargar_sprite(nombre, size=(180, 180)):
    nombre_f = "jcc.png" if "Julio César Chavez" in nombre else nombre.lower().strip() + ".png"
    ruta = buscar_archivo(nombre_f, os.path.expanduser("~"))
    if ruta:
        img = Image.open(ruta).convert("RGBA").resize(size, Image.Resampling.LANCZOS)
        img_tk = ImageTk.PhotoImage(img)
        return img_tk
    return None

# --- PANTALLAS ---
def pantalla_inicio():
    canvas.delete("all")
    ruta = buscar_archivo("pantallainicio.png", os.path.expanduser("~"))
    if ruta:
        img = Image.open(ruta).resize((800, 600), Image.Resampling.LANCZOS)
        global img_tk_inicio
        img_tk_inicio = ImageTk.PhotoImage(img)
        canvas.create_image(0, 0, image=img_tk_inicio, anchor="nw")
    btn = tk.Button(root, text="INICIAR JUEGO", font=("Arial", 14, "bold"), bg="green", fg="white", 
                    command=lambda: pantalla_seleccion_recursiva(3))
    canvas.create_window(400, 450, window=btn)

def pantalla_seleccion_recursiva(cantidad_restante):
    canvas.delete("all")
    canvas.referencias = [] # Limpiar imágenes previas
    
    # Cargar fondo de selección
    ruta = buscar_archivo("seleccionpersonajes.png", os.path.expanduser("~"))
    if ruta:
        img = Image.open(ruta).resize((800, 600), Image.Resampling.LANCZOS)
        global img_tk_sel
        img_tk_sel = ImageTk.PhotoImage(img)
        canvas.create_image(0, 0, image=img_tk_sel, anchor="nw")

    if cantidad_restante == 0:
        pantalla_mapa()
        return

    canvas.create_text(400, 40, text=f"Selecciona tu equipo ({cantidad_restante} restantes)", 
                       font=("Arial", 20, "bold"), fill="white", outline="black")

    def dibujar_opciones(lista, idx=0, x=150, y=140):
        if idx >= len(lista) or idx >= 9: return
        p = lista[idx]
        
        # Cargar mini-sprite para la selección
        s_mini = cargar_sprite(p.nombre, size=(120, 120))
        if s_mini:
            canvas.referencias.append(s_mini)
            canvas.create_image(x, y, image=s_mini)

        btn = tk.Button(root, text=f"{p.nombre}\nHP:{p.hp}", width=12, bg="#1a1a1a", fg="cyan",
                        command=lambda p=p: agregar_y_continuar(p))
        canvas.create_window(x, y + 80, window=btn)
        
        nuevo_x = x + 250 if (idx + 1) % 3 != 0 else 150
        nuevo_y = y if (idx + 1) % 3 != 0 else y + 180
        dibujar_opciones(lista, idx + 1, nuevo_x, nuevo_y)

    def agregar_y_continuar(personaje):
        mi_equipo.append(personaje)
        pantalla_seleccion_recursiva(cantidad_restante - 1)

    dibujar_opciones([p for p in todos_los_personajes if p not in mi_equipo])

def pantalla_mapa():
    canvas.delete("all")
    ruta = buscar_archivo("mapa.png", os.path.expanduser("~"))
    if ruta:
        img = Image.open(ruta).resize((800, 600), Image.Resampling.LANCZOS)
        global img_tk_mapa
        img_tk_mapa = ImageTk.PhotoImage(img)
        canvas.create_image(0, 0, image=img_tk_mapa, anchor="nw")
    canvas.bind("<Button-1>", detectar_zona)

def detectar_zona(event):
    x, y = event.x, event.y
    # Coordenadas de las zonas según tu lógica
    if 84 <= x <= 148 and 127 <= y <= 186: pantalla_combate(1)
    elif 218 <= x <= 284 and 412 <= y <= 476: pantalla_combate(2)
    elif 370 <= x <= 428 and 409 <= y <= 486: pantalla_combate(3)
    elif 506 <= x <= 563 and 141 <= y <= 210: pantalla_combate(4)
    elif 616 <= x <= 767 and 142 <= y <= 251: pantalla_combate(5)

def pantalla_combate(n_zona):
    canvas.delete("all")
    canvas.unbind("<Button-1>")
    ruta = buscar_archivo(f"zona{n_zona}.png", os.path.expanduser("~"))
    if ruta:
        img = Image.open(ruta).resize((800, 600), Image.Resampling.LANCZOS)
        global img_tk_zona
        img_tk_zona = ImageTk.PhotoImage(img)
        canvas.create_image(0, 0, image=img_tk_zona, anchor="nw")
    ejecutar_fase_combate()

def ejecutar_fase_combate():
    canvas.delete("ui")
    canvas.referencias_batalla = []
    
    if not [p for p in mi_equipo if p.hp > 0]:
        messagebox.showinfo("Fin", "Tu equipo ha sido derrotado...")
        pantalla_inicio()
        return
    if not equipo_enemigo:
        messagebox.showinfo("Fin", "¡Has conquistado todas las zonas!")
        pantalla_inicio()
        return

    p_jugador = random.choice([p for p in mi_equipo if p.hp > 0])
    p_enemigo = random.choice(equipo_enemigo)

    s_j = cargar_sprite(p_jugador.nombre)
    s_e = cargar_sprite(p_enemigo.nombre)
    canvas.referencias_batalla = [s_j, s_e]

    canvas.create_image(200, 350, image=s_j, tags="ui")
    canvas.create_image(600, 350, image=s_e, tags="ui")
    
    canvas.create_text(200, 480, text=f"{p_jugador.nombre}\nHP: {p_jugador.hp}", fill="white", font=("Arial", 12, "bold"), tags="ui")
    canvas.create_text(600, 480, text=f"{p_enemigo.nombre}\nHP: {p_enemigo.hp}", fill="white", font=("Arial", 12, "bold"), tags="ui")

    def animar_danio(x, y, texto, color):
        t = canvas.create_text(x, y, text=texto, fill=color, font=("Arial", 24, "bold"), tags="anim")
        def subir(p=10):
            if p > 0:
                canvas.move(t, 0, -3)
                root.after(50, lambda: subir(p-1))
            else: canvas.delete(t)
        subir()

    def realizar_ataque():
        d_j, c_j = p_jugador.atacar(p_enemigo)
        animar_danio(600, 300, f"-{d_j}", "yellow" if c_j else "white")

        if p_enemigo.hp <= 0:
            equipo_enemigo.remove(p_enemigo)
            messagebox.showinfo("Victoria", f"{p_enemigo.nombre} ha sido derrotado")
            pantalla_mapa()
        else:
            root.after(600, contraataque)

    def contraataque():
        d_e, c_e = p_enemigo.atacar(p_jugador)
        animar_danio(200, 300, f"-{d_e}", "red")
        if p_jugador.hp <= 0:
            messagebox.showwarning("Caído", f"{p_jugador.nombre} no puede seguir luchando")
            pantalla_mapa()
        else:
            root.after(600, ejecutar_fase_combate)

    btn = tk.Button(root, text="ATACAR", bg="red", fg="white", font=("Arial", 12, "bold"), command=realizar_ataque)
    canvas.create_window(400, 540, window=btn, tags="ui")

# --- INICIO DE LA APP ---
root = tk.Tk()
root.title("Aeterna - RPG")
root.geometry("800x600")
canvas = tk.Canvas(root, width=800, height=600, bg="black")
canvas.pack()

todos_los_personajes = cargar_datos()
mi_equipo = []
equipo_enemigo = random.sample(todos_los_personajes, 5) if len(todos_los_personajes) >= 5 else todos_los_personajes

pantalla_inicio()
root.mainloop()