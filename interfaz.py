import tkinter as tk
from tkinter import messagebox # ventanas emergentes
from PIL import Image, ImageTk #imagens
import os # interactuar con archivos
import random

class Personaje:
    
    def __init__(self, nombre, hp, atk, defensa):
        self.nombre = nombre #personaje
        self.hp = int(hp) # vida
        self.max_hp = int(hp) # restauración
        self.atk = int(atk) # daño
        self.defensa = int(defensa) #daño total

    def atacar(self, objetivo):
        daño = self.atk - objetivo.defensa
        if daño < 1: daño = 1 
        critico = random.random() < 0.2 #probabilidad del 20% para un crítico
        if critico: daño *= 2 # Duplica el daño
        objetivo.hp -= daño # Aplica reducción de vida
        return daño, critico

    def restaurar(self):
        self.hp = self.max_hp
#=====================================
#IA
#=====================================
def buscar_archivo(nombre_archivo, ruta_busqueda="."):
    #Explora directorios mediante un bucle for para localizar archivos específicos.
    for raiz, _, archivos in os.walk(ruta_busqueda):#os.walk genera tuplas con la ruta actual, subdirectorios y archivos encontrados
        if nombre_archivo in archivos:#Verifica si el archivo deseado está presente en la lista de archivos del directorio actual
            return os.path.join(raiz, nombre_archivo) # Retorna la ruta completa si existe
    return None


def cargar_datos():
    
    ruta_txt = buscar_archivo("personajes.txt", os.path.expanduser("~"))
    if not ruta_txt: return [] # Retorna una lista vacía si el archivo no existe
    with open(ruta_txt, "r", encoding="utf-8") as f:
        lineas = f.readlines() # Lee todo el contenido y lo almacena como una lista de cadenas

#=====================================================
#=====================================================
    def leer_recursivo(i):

        if i >= len(lineas): return [] # detiene la recursión al llegar al final de la lista
        datos = lineas[i].strip().split(",") # Limpia espacios y divide la línea por comas
        if len(datos) < 4: return leer_recursivo(i + 1) # Omite líneas incompletas y pasa a la siguiente

        return [Personaje(datos[0].strip(), datos[1], datos[2], datos[3])] + leer_recursivo(i + 1)
    
    return leer_recursivo(0) # Inicia el ciclo recursivo desde el índice cero

def cargar_sprite(nombre):

    #IA============================
    nombre_f = "jcc.png" if "Julio César Chavez" in nombre else nombre.lower().strip() + ".png"# Aplica una excepción de nombre para un personaje específico o usa el nombre estándar en minúsculas
    #==============================
    ruta = buscar_archivo(nombre_f, os.path.expanduser("~"))
    if ruta:
        # Abre la imagen, asegura el canal alfa (transparencia) y ajusta su tamaño con alta calidad
        img = Image.open(ruta).convert("RGBA").resize((180, 180), Image.Resampling.LANCZOS)
        return ImageTk.PhotoImage(img) # Convierte el objeto de PIL a un formato compatible con la interfaz
    return None # Si no encuentra la imagen, retorna nada para evitar errores de carga

# Variables Globales
todos_los_personajes = cargar_datos() # lista completa de personajes desde el archivo
mi_equipo = [] #  personajes del usuario
equipo_enemigo = [] # personajes enemigo
enemigos_en_esta_batalla = [] # Registro temporal de los enemigos para procesos de reclutamiento post-victoria
p_actual_jugador = None # jugador.   Se inician en None porque al abrir el juego aún no ha empezado ningún combate.  aplica también al enemiggo
p_actual_enemigo = None # IA
nombre_jugador = "Héroe" # Almacena el nombre personalizado que el usuario introduce al inicio



#================================================================00
# voy a usar inteligencia artificial para eliminar algunos canvas, widgets u otros que pueden hacer que el juego fluya incorrectamente, o muy trabado
#IA
#===================================================================
def limpiar_pantalla():
    """Elimina todos los elementos visuales del Canvas y destruye los widgets de Tkinter."""
    canvas.delete("all") # Borra todos los dibujos, textos e imágenes contenidos en el objeto Canvas
    
    def destruir_widgets(widgets):
        """Procesa de forma recursiva la lista de elementos de la interfaz para eliminarlos uno por uno."""
        if not widgets: return # Caso base: finaliza cuando ya no quedan elementos en la lista
        w = widgets[0] # Selecciona el primer elemento de la lista actual
        
        # Verifica si el elemento es un botón, campo de entrada o marco antes de eliminarlo
        if isinstance(w, (tk.Button, tk.Entry, tk.Frame)):
            w.destroy() # Elimina físicamente el widget de la memoria y de la ventana principal
        
        destruir_widgets(widgets[1:]) # Llamada recursiva con el resto de la lista (rebanado)
    
    # Obtiene todos los objetos hijos de la ventana principal y arranca la limpieza recursiva
    destruir_widgets(root.winfo_children())
#==================================================================================================================


#botón de about, con la información del proyecto, estudiante, etc.
def mostrar_about():
    info = (
        "PROYECTO: AETERNA: Pantheon\n"
        "ESTUDIANTE: Felipe Andrés Cararnza Masis (y copilot)\n"
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
    #despliega los elementos visuales de la ventana
    
    limpiar_pantalla() # Llama a la función de limpieza para remover widgets o dibujos de pantallas previas
    
    # Intenta localizar la imagen de fondo en el directorio del usuario para asegurar que el recurso exista
    ruta = buscar_archivo("pantallainicio.png", os.path.expanduser("~"))
    
    if ruta:
        #imagen ajustada a 800x600 y usa un filtro de alta calidad (LANCZOS)
        img = Image.open(ruta).resize((800, 600), Image.Resampling.LANCZOS)
        
        # declarar la variable como global para que python no la borre
        global img_tk_inicio
        img_tk_inicio = ImageTk.PhotoImage(img) # Convierte la imagen procesada a un formato que el Canvas puede leer
        
        # Dibuja la imagen en las coordenadas (0,0) del Canvas, alineada desde la esquina superior izquierda
        canvas.create_image(0, 0, image=img_tk_inicio, anchor="nw")
    

    #hice un archivo aparte en el que subia las imagenes ajustadas a 800x600 y el click me daba coordenadas x,y
    #en base a esas coordenadas coloqué el boton about en la esquina izquierda superior
    
# boton interactivo
    tk.Button(root, text="ABOUT", font=("Arial", 10, "bold"), bg="#333333", fg="white",
              command=mostrar_about, width=8).place(x=43, y=37)
    
    # texto sobre el cuadro de texto para ingresar el nombre
    canvas.create_text(400, 350, text="Escribe tu nombre:", font=("Arial", 14, "bold"), fill="white")
    
    # ingresa el nombre
    entrada_nombre = tk.Entry(root, font=("Arial", 14), justify="center")
    
    # posición
    canvas.create_window(400, 390, window=entrada_nombre, width=200)

    def confirmar_inicio():
        #valida el texto ingresado, pasa a la siguiente pantalla


        global nombre_jugador # Accede a la variable global para actualizar el nombre del usuario
        escrito = entrada_nombre.get().strip() # Obtiene el texto y elimina espacios vacíos innecesarios
        
        # Si el usuario escribió algo, actualiza el nombre global; de lo contrario, mantiene el valor por defecto
        if escrito: nombre_jugador = escrito
        
        # Llama a la función de selección de personajes, indicando que faltan 3 por elegir
        pantalla_seleccion_recursiva(3)

    # Crea el botón principal de inicio que ejecuta la validación y cambia de pantalla al ser presionado
    tk.Button(root, text="INICIAR AVENTURA", font=("Arial", 12, "bold"), bg="green", fg="white", 
              command=confirmar_inicio).place(x=315, y=440)





def pantalla_seleccion_recursiva(cantidad_restante):

    limpiar_pantalla() # Limpia la interfaz para dibujar los elementos de selección
    
    # Si ya no quedan personajes por elegir, se inicializa el combate y se pasa al mapa
    if cantidad_restante == 0:
        global p_actual_jugador
        p_actual_jugador = mi_equipo[0] #el primer elegido es el personaje activo para iniciar
        pantalla_mapa() # Cambia a la pantalla del mapa mundial
        return # Finaliza la recursión
    
    # Carga y muestra la imagen de fondo específica para la fase de selección
    ruta_sel = buscar_archivo("seleccionpersonajes.png", os.path.expanduser("~"))
    if ruta_sel:
        img_s = Image.open(ruta_sel).resize((800, 600), Image.Resampling.LANCZOS)
        global img_tk_seleccion
        img_tk_seleccion = ImageTk.PhotoImage(img_s)
        canvas.create_image(0, 0, image=img_tk_seleccion, anchor="nw")
    
    # Muestra un contador que indica cuántos personajes faltan por reclutar
    canvas.create_text(400, 40, text=f"Recluta tu equipo ({cantidad_restante} restantes)", 
                       font=("Arial", 20, "bold"), fill="white")

    # Crea el campo de entrada donde el usuario digita el  (ID) del personaje 
    entrada_id = tk.Entry(root, font=("Arial", 18), justify="center")
    canvas.create_window(400, 530, window=entrada_id, width=100)

    def validar_id():
       #verificar entrada valida, entre 1 y 15
        try:
            sel = int(entrada_id.get()) # Intenta convertir el texto ingresado a un número entero
           
            if 1 <= sel <= 15: # Comprueba que el ID esté dentro del rango de personajes disponibles 
                p = todos_los_personajes[sel-1] # Obtiene el personaje correspondiente al índice
                if p not in mi_equipo: # Verifica que el personaje no esté ya en la lista del equipo
                    mi_equipo.append(p) # Agrega el personaje al equipo del jugador
                    #  Vuelve a ejecutar la función reduciendo el contador de faltantes                   (recursivo)
                    pantalla_seleccion_recursiva(cantidad_restante - 1)
                else: 
                    messagebox.showwarning("Aviso", "Ya está en tu equipo.")
            else: 
                messagebox.showerror("Error", "Elige del 1 al 15.")
        except: 
            messagebox.showerror("Error", "Ingresa un número válido.")

    # Botón para confirmar la selección del ID ingresado en el campo de texto
    tk.Button(root, text="SELECCIONAR", command=validar_id).place(x=355, y=560)







def pantalla_mapa():
    #===========================
    #IA ayuda
    #===============================
    limpiar_pantalla() # Remueve los elementos de la selección de personajes o de combates previos
    
    # Desvincula cualquier función previa del clic izquierdo para evitar que se ejecuten acciones antiguas
    canvas.unbind("<Button-1>")
    #================================================================================


    # Busca y carga la imagen del mapa desde el directorio del usuario
    ruta = buscar_archivo("mapa.png", os.path.expanduser("~"))
    
    if ruta:
        # Redimensiona a (800x600)
        img = Image.open(ruta).resize((800, 600), Image.Resampling.LANCZOS)
        

        #====================
        #IA
        

        # Uso de variable global para que Python no elimine la imagen de la memoria RAM
        global img_tk_mapa
        img_tk_mapa = ImageTk.PhotoImage(img)
        #=================================
        
        # Dibuja el mapa como fondo en el Canvas
        canvas.create_image(0, 0, image=img_tk_mapa, anchor="nw")
    
    # Vincula el clic izquierdo del mouse (<Button-1>) a la función detectar_zona para iniciar batallas
    canvas.bind("<Button-1>", detectar_zona)

def detectar_zona(event):

    # coordenadas X e Y donde ocurrió el clic del mouse
    x, y = event.x, event.y
    
    # Hitboxes para las zonas
    # Estructura: (x_mínima, x_máxima, y_mínima, y_máxima, número_de_zona)
    zonas = [
        (80, 150, 120, 190, 1),   # Coordenadas Zona 1
        (210, 290, 410, 480, 2),  # Coordenadas Zona 2
        (370, 430, 400, 490, 3),  # Coordenadas Zona 3
        (499, 563, 137, 219, 4),  # Coordenadas Zona 4
        (616, 766, 142, 249, 5)   # Coordenadas Zona 5
    ]
    
    def checar_zonas(lista):
        
        if not lista: return # Caso base: Se recorrieron todas las zonas y ninguna coincidió
        
        z = lista[0] # Toma la primera zona de la lista actual
        
        # Verifica si x y y están dentro de los límites del rectángulo
        if z[0] < x < z[1] and z[2] < y < z[3]: 
            iniciar_combate(z[4]) # Si coincide, inicia el combate pasando el ID de la zona
        else: 
            # Si no coincide, sigue buscando en el resto de la lista (Recursión)
            checar_zonas(lista[1:])
            
    # Llama a la sub-función recursiva para iniciar el chequeo
    checar_zonas(zonas)

def iniciar_combate(zona):

    # Se accede a las variables globales para que los cambios persistan en todo el programa
    global equipo_enemigo, p_actual_enemigo, enemigos_en_esta_batalla
    
    #utilice iteración en vez de reursividad

    # Crea una lista de personajes que NO están en el equipo del jugador (evita pelear contra uno mismo)
    disponibles = [p for p in todos_los_personajes if p not in mi_equipo]
    
    # Si quedan muy pocos personajes fuera del equipo (menos de 3), usa la lista completa para evitar errores
    if len(disponibles) < 3: 
        disponibles = todos_los_personajes
    
    # Selecciona 3 personajes al azar y crea nuevas instancias (objetos) de combate para el equipo enemigo
    equipo_enemigo = [Personaje(p.nombre, p.max_hp, p.atk, p.defensa) for p in random.sample(disponibles, 3)]
    
    # Guarda una copia fija de los enemigos para saber a quiénes reclutar al final de la batalla
    enemigos_en_esta_batalla = list(equipo_enemigo) 
    
    # Define que el primer enemigo de la lista es el que empieza la pelea
    p_actual_enemigo = equipo_enemigo[0]
    
    # Llama a la función visual para cargar el fondo de la zona y mostrar la interfaz
    pantalla_combate(zona)


def pantalla_combate(n_zona):
    
    limpiar_pantalla() # Elimina los elementos del mapa o de combates anteriores
    
    # Busca la imagen de fondo según el número de zona 
    ruta = buscar_archivo(f"zona{n_zona}.png", os.path.expanduser("~"))
    
    if ruta:
        # Carga la imagen y la ajusta al tamaño de la ventana de juego (800x600)
        img = Image.open(ruta).resize((800, 600), Image.Resampling.LANCZOS)
        
        # Se usa una variable global para asegurar que la imagen permanezca en memoria mientras se muestra
        global img_tk_zona
        img_tk_zona = ImageTk.PhotoImage(img)
        
        # Dibuja el fondo de la zona en la capa base del Canvas
        canvas.create_image(0, 0, image=img_tk_zona, anchor="nw")
    
    # Llama a la función que dibuja los personajes, la vida y los botones de acción sobre el fondo
    actualizar_interfaz_combate()


#==================================================================================================================
#no fue echa con ia pero si brindó asistencia para mejorar la experiencia de combate, haciendo que el daño mostrado suba y desaparezca después de un momento, para que el juego no se sienta tan estático
#==================================================================================================================

#Cada vez que  se presiona "Atacar" o ocurre algo en la pelea, esta función se llama para ver reflejado el nuevo estado de la batalla.

def actualizar_interfaz_combate():
    """Refresca todos los elementos visuales de la batalla (imágenes, textos y botones)."""
    # Elimina únicamente los elementos etiquetados como "ui" para no borrar el fondo del combate
    canvas.delete("ui")
    
    # Dibuja un rectángulo oscuro en la parte inferior como panel de control para los botones
    canvas.create_rectangle(0, 480, 800, 600, fill="#1a1a1a", outline="white", tags="ui")
    
    # Declarar como globales las imágenes de los sprites para evitar que Python las limpie de memoria
    global spr_j, spr_e
    spr_j = cargar_sprite(p_actual_jugador.nombre) # Carga la imagen del luchador del jugador
    spr_e = cargar_sprite(p_actual_enemigo.nombre) # Carga la imagen del oponente actual
    
    # Posiciona los sprites en el escenario: Jugador a la izquierda (200) y Enemigo a la derecha (600)
    canvas.create_image(200, 300, image=spr_j, tags="ui")
    canvas.create_image(600, 300, image=spr_e, tags="ui")

    # Muestra los nombres y los puntos de vida (HP) actuales de ambos combatientes
    canvas.create_text(200, 450, text=f"{p_actual_jugador.nombre}: {p_actual_jugador.hp} HP", 
                       fill="cyan", font=("Arial", 14, "bold"), tags="ui")
    canvas.create_text(600, 450, text=f"{p_actual_enemigo.nombre}: {p_actual_enemigo.hp} HP", 
                       fill="orange", font=("Arial", 14, "bold"), tags="ui")

    # Crea y posiciona los botones de acción para el jugador (Atacar, Cambiar de personaje o Huir)
    tk.Button(root, text="ATACAR", bg="#cc0000", fg="white", width=12, command=turno_jugador).place(x=150, y=530)
    tk.Button(root, text="CAMBIAR", bg="#0000cc", fg="white", width=12, command=abrir_menu_cambio).place(x=350, y=530)
    tk.Button(root, text="HUIR", bg="#555555", fg="white", width=12, command=pantalla_mapa).place(x=550, y=530)

#======================================================================================================================


def animar_daño(x, y, texto, color):
    
    # Crea el objeto de texto en el Canvas con el color y tamaño especificado (ej. "-25")
    t = canvas.create_text(x, y, text=texto, fill=color, font=("Arial", 30, "bold"))
    
    def anim(pasos):
        """Función recursiva interna que mueve el texto hacia arriba gradualmente."""
        if pasos <= 0:
            canvas.delete(t) # Elimina el texto del Canvas cuando termina la animación
            return
        
        # Mueve el elemento 0 píxeles en horizontal y -2 píxeles en vertical (hacia arriba)
        canvas.move(t, 0, -2)
        
        # Lógica de temporización: Llama de nuevo a 'anim' tras 30ms reduciendo los pasos restantes
        root.after(30, lambda: anim(pasos - 1))
    
    # Inicia el ciclo de animación con un total de 15 movimientos (pasos)
    anim(15)




def turno_jugador():
    
    # Llama al método atacar del personaje activo y recibe el daño infligido junto a si fue crítico
    daño, crit = p_actual_jugador.atacar(p_actual_enemigo)
    

    #==========================
    #utilicé IA para animar el daño que se muestra en la pantalla de combate, haciendo que el número suba y desaparezca después de un momento. para que el juego no se sienta estático
    #==========================
   
    # Dispara la animación de daño en la posición del enemigo; cambia a amarillo si el golpe fue crítico
    animar_daño(600, 250, f"-{daño}", "yellow" if crit else "white")
    
    # Pausa breve de 600ms para permitir ver la animación antes de verificar si alguien murió
    root.after(600, revisar_estado_combate)
    #===========================================================


def revisar_estado_combate():
    
    global p_actual_enemigo
    
    if p_actual_enemigo.hp <= 0: # Si el enemigo actual se queda sin vida
        equipo_enemigo.pop(0) # Elimina al enemigo derrotado de la lista del equipo rival
        
        if not equipo_enemigo: # Si ya no quedan enemigos en la lista (Victoria total)
            def reclutar_recursivo(lista):
                
                if not lista: return #o hay más enemigos que procesar
                enemigo = lista[0]
                
                #Verifica si el personaje ya existe en el equipo para no duplicarlo
                if not any(p.nombre == enemigo.nombre for p in mi_equipo):
                    enemigo.restaurar() # Cura al nuevo recluta antes de unirlo
                    mi_equipo.append(enemigo) # Lo añade a la colección del jugador
                reclutar_recursivo(lista[1:])
            
            # Inicia el proceso de reclutamiento con los enemigos que participaron en esta batalla
           
           
            reclutar_recursivo(enemigos_en_esta_batalla)
            messagebox.showinfo("Victoria", "¡Enemigos reclutados!")
            pantalla_mapa() # Regresa al mapa mundial tras ganar
        else:
            # Si quedan enemigos, el siguiente en la lista toma el lugar del caído
            p_actual_enemigo = equipo_enemigo[0]
            actualizar_interfaz_combate() # Refresca para mostrar al nuevo oponente
    else:
        # Si el enemigo sobrevivió, espera 400ms y le cede el turno para contraatacar
        root.after(400, turno_enemigo)

def turno_enemigo():
    
    daño, crit = p_actual_enemigo.atacar(p_actual_jugador) # La IA realiza su ataque
    
    
    animar_daño(200, 250, f"-{daño}", "red") # Muestra el daño recibido por el jugador en color rojo
    
    if p_actual_jugador.hp <= 0: # Si el personaje del jugador cae derrotado
        # Busca si quedan otros personajes con vida en el equipo del jugador


        #no supe aplicar recursividad aquí
        disponibles = [p for p in mi_equipo if p.hp > 0]
        
        if not disponibles: # Si no queda nadie vivo en todo el equipo
            messagebox.showerror("Fin del Juego", "Tu equipo ha caído.")
            root.destroy() # Cierra la aplicación (Game Over)
        else:
            # Si hay sobrevivientes, obliga al usuario a elegir un relevo
            abrir_menu_cambio()
            
    actualizar_interfaz_combate() # Actualiza barras de vida y sprites en pantalla



#Función echa con IA para abrir un menú con personajes para cambiar durante la pelea
def abrir_menu_cambio():
   
    # Crea un contenedor (Frame) con fondo negro y borde tipo relieve para que resalte sobre el combate
    frame = tk.Frame(root, bg="black", bd=2, relief="ridge")
    # Coloca el menú justo en el centro del canvas (coordenadas 400, 250)
    canvas.create_window(400, 250, window=frame)
    
    # BLOQUE DE FILTRADO: Crea una lista solo con personajes que tengan vida y que no estén peleando ya
    vivos = [p for p in mi_equipo if p.hp > 0 and p != p_actual_jugador]
    
    def listar_relevos_recursivo(lista):
        """Genera botones de forma recursiva para cada personaje que pueda entrar al combate."""
        if not lista: return # Caso base: no hay más personajes por listar
        p = lista[0] # Toma el primer personaje de la lista filtrada
        
        # Crea un botón que, al presionarse, cambia al personaje y cierra el menú (destruye el frame)
        tk.Button(frame, text=f"Entra {p.nombre}", 
                  command=lambda pers=p: [cambiar_p(pers), frame.destroy()]).pack(fill="x")
        
        # Llamada recursiva con el resto de la lista de compañeros vivos
        listar_relevos_recursivo(lista[1:])
    
    # Inicia la creación de los botones de relevo
    listar_relevos_recursivo(vivos)
    
    # Agrega un botón de cierre al final por si el usuario decide no realizar el cambio
    tk.Button(frame, text="CANCELAR", fg="red", command=frame.destroy).pack()
#================================================================


def cambiar_p(nuevo_p):

    global p_actual_jugador # Accede a la variable global para modificar quién es el luchador activo
    
    # Asigna el nuevo personaje (seleccionado desde el menú de relevos) a la variable de combate
    p_actual_jugador = nuevo_p
    
    # Refresca la pantalla de combate para mostrar el nuevo sprite y los puntos de vida actualizados
    actualizar_interfaz_combate()



root = tk.Tk()
root.title("Aeterna RPG")
root.geometry("800x600")
root.resizable(False, False)
canvas = tk.Canvas(root, width=800, height=600, bg="black", highlightthickness=0)
canvas.pack()

pantalla_inicio()
root.mainloop()