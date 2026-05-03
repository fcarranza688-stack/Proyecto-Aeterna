import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk
import os
import random

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

    def restaurar(self):
        self.hp = self.max_hp

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
        return [Personaje(datos[0].strip(), datos[1], datos[2], datos[3])] + leer_recursivo(i + 1)
    return leer_recursivo(0)

def cargar_sprite(nombre):
    nombre_f = "jcc.png" if "Julio César Chavez" in nombre else nombre.lower().strip() + ".png"
    ruta = buscar_archivo(nombre_f, os.path.expanduser("~"))
    if ruta:
        img = Image.open(ruta).convert("RGBA").resize((180, 180), Image.Resampling.LANCZOS)
        return ImageTk.PhotoImage(img)
    return None

# Variables Globales
todos_los_personajes = cargar_datos()
mi_equipo = []
equipo_enemigo = []
enemigos_en_esta_batalla = []
p_actual_jugador = None
p_actual_enemigo = None
nombre_jugador = "Héroe"
avatar_jugador = None

def limpiar_pantalla():
    canvas.delete("all")
    def destruir_widgets(widgets):
        if not widgets: return
        w = widgets[0]
        if isinstance(w, (tk.Button, tk.Entry, tk.Frame)):
            w.destroy()
        destruir_widgets(widgets[1:])
    destruir_widgets(root.winfo_children())

#==================================================================================================================

def mostrar_about():
    info = (
        "PROYECTO: AETERNA: Pantheon\n"
        "ESTUDIANTE: Felipe Andrés Carranza Masis\n"
        "CARNÉT: 2026110400\n"
        "INSTITUCIÓN: Tecnológico de Costa Rica\n"
        "CURSO: Introducción a la Programación\n"
        "PROFESORES: Santiago Gamboa\n"
        "SEMESTRE: I Semestre 2026\n\n"
        "SINOPSIS: Los multiversos se han mezclado, ahora seres\n"
        "de todos los confines deberán luchar entre sí para\n"
        "determinar quién será el ganador y quién podrá volver a casa."
    )
    messagebox.showinfo("Acerca del Proyecto", info)

def pantalla_inicio():
    limpiar_pantalla()
    ruta = buscar_archivo("pantallainicio.png", os.path.expanduser("~"))
    if ruta:
        img = Image.open(ruta).resize((800, 600), Image.Resampling.LANCZOS)
        global img_tk_inicio
        img_tk_inicio = ImageTk.PhotoImage(img)
        canvas.create_image(0, 0, image=img_tk_inicio, anchor="nw")
    
    tk.Button(root, text="ABOUT", font=("Arial", 10, "bold"), bg="#333333", fg="white",
              command=mostrar_about, width=8).place(x=43, y=37)
    
    canvas.create_text(400, 350, text="Escribe tu nombre:", font=("Arial", 14, "bold"), fill="white")
    entrada_nombre = tk.Entry(root, font=("Arial", 14), justify="center")
    canvas.create_window(400, 390, window=entrada_nombre, width=200)

    def confirmar_inicio():
        global nombre_jugador
        escrito = entrada_nombre.get().strip()
        if escrito: nombre_jugador = escrito
        pantalla_seleccion_avatar()

    tk.Button(root, text="INICIAR AVENTURA", font=("Arial", 12, "bold"), bg="green", fg="white", 
              command=confirmar_inicio).place(x=315, y=440)

def pantalla_seleccion_avatar():
    limpiar_pantalla()
    ruta = buscar_archivo("personajes.jpg", os.path.expanduser("~"))
    if ruta:
        img = Image.open(ruta).resize((800, 600), Image.Resampling.LANCZOS)
        global img_tk_avatar
        img_tk_avatar = ImageTk.PhotoImage(img)
        canvas.create_image(0, 0, image=img_tk_avatar, anchor="nw")
    
    def elegir(tipo):
        global avatar_jugador
        avatar_jugador = tipo
        pantalla_seleccion_recursiva(3)

    # Botones basados en tus coordenadas exactas
    # Guerrero (Hombre)
    tk.Button(root, text="SELECT", font=("Arial", 9, "bold"), bg="#1a3a6c", fg="white",
              command=lambda: elegir("Guerrero")).place(x=171, y=501, width=121, height=49)
    
    # Guerrera (Mujer)
    tk.Button(root, text="SELECT", font=("Arial", 9, "bold"), bg="#1a3a6c", fg="white",
              command=lambda: elegir("Guerrera")).place(x=501, y=500, width=134, height=51)
    
    # Estatua (Centro)
    tk.Button(root, text="INVOCAR", font=("Arial", 8, "bold"), bg="#444444", fg="white",
              command=lambda: elegir("Estatua")).place(x=363, y=358, width=72, height=55)

def pantalla_seleccion_recursiva(cantidad_restante):
    limpiar_pantalla()
    if cantidad_restante == 0:
        global p_actual_jugador
        p_actual_jugador = mi_equipo[0]
        pantalla_mapa()
        return
    
    ruta_sel = buscar_archivo("seleccionpersonajes.png", os.path.expanduser("~"))
    if ruta_sel:
        img_s = Image.open(ruta_sel).resize((800, 600), Image.Resampling.LANCZOS)
        global img_tk_seleccion
        img_tk_seleccion = ImageTk.PhotoImage(img_s)
        canvas.create_image(0, 0, image=img_tk_seleccion, anchor="nw")
    
    canvas.create_text(400, 40, text=f"Recluta tu equipo ({cantidad_restante} restantes)", 
                       font=("Arial", 20, "bold"), fill="white")

    def dibujar_lista_vacia(idx):
        pass 
    dibujar_lista_vacia(0)

    entrada_id = tk.Entry(root, font=("Arial", 18), justify="center")
    canvas.create_window(400, 530, window=entrada_id, width=100)

    def validar_id():
        try:
            sel = int(entrada_id.get())
            if 1 <= sel <= 15:
                p = todos_los_personajes[sel-1]
                if p not in mi_equipo:
                    mi_equipo.append(p)
                    pantalla_seleccion_recursiva(cantidad_restante - 1)
                else: messagebox.showwarning("Aviso", "Ya está en tu equipo.")
            else: messagebox.showerror("Error", "Elige del 1 al 15.")
        except: messagebox.showerror("Error", "Ingresa un número.")

    tk.Button(root, text="SELECCIONAR", command=validar_id).place(x=355, y=560)

def pantalla_mapa():
    limpiar_pantalla()
    canvas.unbind("<Button-1>")
    ruta = buscar_archivo("mapa.png", os.path.expanduser("~"))
    if ruta:
        img = Image.open(ruta).resize((800, 600), Image.Resampling.LANCZOS)
        global img_tk_mapa
        img_tk_mapa = ImageTk.PhotoImage(img)
        canvas.create_image(0, 0, image=img_tk_mapa, anchor="nw")
    canvas.bind("<Button-1>", detectar_zona)

def detectar_zona(event):
    x, y = event.x, event.y
    zonas = [
        (80, 150, 120, 190, 1), (210, 290, 410, 480, 2), (370, 430, 400, 490, 3),
        (499, 563, 137, 219, 4), (616, 766, 142, 249, 5)
    ]
    def checar_zonas(lista):
        if not lista: return
        z = lista[0]
        if z[0] < x < z[1] and z[2] < y < z[3]: iniciar_combate(z[4])
        else: checar_zonas(lista[1:])
    checar_zonas(zonas)

def iniciar_combate(zona):
    global equipo_enemigo, p_actual_enemigo, enemigos_en_esta_batalla
    disponibles = [p for p in todos_los_personajes if p not in mi_equipo]
    if len(disponibles) < 3: disponibles = todos_los_personajes
    equipo_enemigo = [Personaje(p.nombre, p.max_hp, p.atk, p.defensa) for p in random.sample(disponibles, 3)]
    enemigos_en_esta_batalla = list(equipo_enemigo) 
    p_actual_enemigo = equipo_enemigo[0]
    pantalla_combate(zona)

def pantalla_combate(n_zona):
    limpiar_pantalla()
    ruta = buscar_archivo(f"zona{n_zona}.png", os.path.expanduser("~"))
    if ruta:
        img = Image.open(ruta).resize((800, 600), Image.Resampling.LANCZOS)
        global img_tk_zona
        img_tk_zona = ImageTk.PhotoImage(img)
        canvas.create_image(0, 0, image=img_tk_zona, anchor="nw")
    actualizar_interfaz_combate()

def actualizar_interfaz_combate():
    canvas.delete("ui")
    canvas.create_rectangle(0, 480, 800, 600, fill="#1a1a1a", outline="white", tags="ui")
    global spr_j, spr_e
    spr_j = cargar_sprite(p_actual_jugador.nombre)
    spr_e = cargar_sprite(p_actual_enemigo.nombre)
    canvas.create_image(200, 300, image=spr_j, tags="ui")
    canvas.create_image(600, 300, image=spr_e, tags="ui")
    canvas.create_text(200, 450, text=f"{p_actual_jugador.nombre}: {p_actual_jugador.hp} HP", fill="cyan", font=("Arial", 14, "bold"), tags="ui")
    canvas.create_text(600, 450, text=f"{p_actual_enemigo.nombre}: {p_actual_enemigo.hp} HP", fill="orange", font=("Arial", 14, "bold"), tags="ui")
    tk.Button(root, text="ATACAR", bg="#cc0000", fg="white", width=12, command=turno_jugador).place(x=150, y=530)
    tk.Button(root, text="CAMBIAR", bg="#0000cc", fg="white", width=12, command=abrir_menu_cambio).place(x=350, y=530)
    tk.Button(root, text="HUIR", bg="#555555", fg="white", width=12, command=pantalla_mapa).place(x=550, y=530)

def animar_danio(x, y, texto, color):
    t = canvas.create_text(x, y, text=texto, fill=color, font=("Arial", 30, "bold"))
    def anim(pasos):
        if pasos <= 0:
            canvas.delete(t)
            return
        canvas.move(t, 0, -2)
        root.after(30, lambda: anim(pasos - 1))
    anim(15)

def turno_jugador():
    danio, crit = p_actual_jugador.atacar(p_actual_enemigo)
    animar_danio(600, 250, f"-{danio}", "yellow" if crit else "white")
    root.after(600, revisar_estado_combate)

def revisar_estado_combate():
    global p_actual_enemigo
    if p_actual_enemigo.hp <= 0:
        equipo_enemigo.pop(0)
        if not equipo_enemigo:
            def reclutar_recursivo(lista):
                if not lista: return
                enemigo = lista[0]
                if not any(p.nombre == enemigo.nombre for p in mi_equipo):
                    enemigo.restaurar()
                    mi_equipo.append(enemigo)
                reclutar_recursivo(lista[1:])
            reclutar_recursivo(enemigos_en_esta_batalla)
            messagebox.showinfo("Victoria", "¡Enemigos reclutados!")
            pantalla_mapa()
        else:
            p_actual_enemigo = equipo_enemigo[0]
            actualizar_interfaz_combate()
    else: root.after(400, turno_enemigo)

def turno_enemigo():
    danio, crit = p_actual_enemigo.atacar(p_actual_jugador)
    animar_danio(200, 250, f"-{danio}", "red")
    if p_actual_jugador.hp <= 0:
        disponibles = [p for p in mi_equipo if p.hp > 0]
        if not disponibles:
            messagebox.showerror("Fin del Juego", "Tu equipo ha caído.")
            root.destroy()
        else: abrir_menu_cambio()
    actualizar_interfaz_combate()

def abrir_menu_cambio():
    frame = tk.Frame(root, bg="black", bd=2, relief="ridge")
    canvas.create_window(400, 250, window=frame)
    vivos = [p for p in mi_equipo if p.hp > 0 and p != p_actual_jugador]
    def listar_relevos_recursivo(lista):
        if not lista: return
        p = lista[0]
        tk.Button(frame, text=f"Entra {p.nombre}", command=lambda pers=p: [cambiar_p(pers), frame.destroy()]).pack(fill="x")
        listar_relevos_recursivo(lista[1:])
    listar_relevos_recursivo(vivos)
    tk.Button(frame, text="CANCELAR", fg="red", command=frame.destroy).pack()

def cambiar_p(nuevo_p):
    global p_actual_jugador
    p_actual_jugador = nuevo_p
    actualizar_interfaz_combate()

#==================================================================================================================

root = tk.Tk()
root.title("Aeterna RPG")
root.geometry("800x600")
root.resizable(False, False)
canvas = tk.Canvas(root, width=800, height=600, bg="black", highlightthickness=0)
canvas.pack()

pantalla_inicio()
root.mainloop()