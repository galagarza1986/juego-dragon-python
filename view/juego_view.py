import tkinter as tk
from tkinter import ttk
from pathlib import Path
from PIL import Image, ImageTk


class JuegoView:
    """
    Vista del juego.

    En MVC, la vista se encarga de mostrar información al usuario.
    Aquí se construye la ventana, se cargan imágenes y se dibujan
    los elementos visuales sobre un Canvas.

    ¿Qué es Canvas en Tkinter?
    Canvas es un componente gráfico de Tkinter que sirve como
    "superficie de dibujo". En él se pueden colocar:
    - imágenes
    - texto
    - líneas
    - rectángulos
    - óvalos
    - polígonos

    En este proyecto, el Canvas funciona como el escenario del juego:
    ahí se dibuja el fondo, el personaje, los obstáculos y los mensajes.
    """

    def __init__(self, root):
        # root es la ventana principal creada con tk.Tk()
        self.root = root
        self.root.title("Salto del Dragón - Hilos + Tkinter + MVC")
        self.root.geometry("980x580")
        self.root.resizable(False, False)

        # Referencias a widgets y elementos visuales.
        self.canvas = None
        self.btn_iniciar = None
        self.btn_reiniciar = None
        self.lbl_estado = None
        self.lbl_puntaje = None

        # Referencias a elementos que se dibujan dentro del Canvas.
        self.item_personaje = None
        self.item_texto = None
        self.items_obstaculos = {}

        # Carpeta donde están los recursos gráficos del juego.
        self.assets_dir = Path(__file__).resolve().parent.parent / "assets"

        # Referencias a imágenes para evitar que tkinter las elimine de memoria.
        # Si no guardamos estas referencias, las imágenes podrían no mostrarse.
        self.img_fondo = None
        self.img_personaje = None
        self.img_fuego = None
        self.img_dragon = None

        self._cargar_imagenes()
        self._crear_interfaz()

    def _cargar_imagenes(self):
        """Carga y prepara las imágenes que usará el juego."""
        # Cargamos el fondo JPG y lo redimensionamos para que encaje
        # exactamente en el tamaño del Canvas.
        fondo = Image.open(self.assets_dir / "pantano.jpg")
        fondo = fondo.resize((940, 470))
        self.img_fondo = ImageTk.PhotoImage(fondo)

        # Cargamos el personaje y lo reducimos para que quede proporcionado.
        self.img_personaje = tk.PhotoImage(file=str(self.assets_dir / "h2.gif")).subsample(3, 3)

        # Cargamos el fuego.
        self.img_fuego = tk.PhotoImage(file=str(self.assets_dir / "f.gif"))

        # Cargamos el dragón y lo reducimos para que no quede demasiado grande.
        self.img_dragon = tk.PhotoImage(file=str(self.assets_dir / "maloani.gif")).subsample(3, 3)

    def _crear_interfaz(self):
        """
        Construye la interfaz principal.

        Aquí se crean:
        - etiquetas
        - botones
        - el Canvas donde se dibuja el juego
        """
        frame = ttk.Frame(self.root, padding=10)
        frame.pack(fill="both", expand=True)

        titulo = ttk.Label(frame, text="SALTO DEL DRAGÓN", font=("Arial", 22, "bold"))
        titulo.pack(anchor="w")

        barra = ttk.Frame(frame)
        barra.pack(fill="x", pady=(8, 8))

        self.btn_iniciar = ttk.Button(barra, text="Iniciar juego")
        self.btn_iniciar.pack(side="left", padx=(0, 8))

        self.btn_reiniciar = ttk.Button(barra, text="Reiniciar")
        self.btn_reiniciar.pack(side="left")

        self.lbl_puntaje = ttk.Label(barra, text="Puntaje: 0", font=("Arial", 11, "bold"))
        self.lbl_puntaje.pack(side="right")

        self.lbl_estado = ttk.Label(
            frame,
            text="Presione Iniciar. Luego use la barra espaciadora para saltar.",
            font=("Arial", 11)
        )
        self.lbl_estado.pack(anchor="w", pady=(0, 8))

        # Canvas:
        # Es el escenario del juego. Mide 940x470 píxeles y sobre él
        # dibujamos fondo, personaje, obstáculos y mensajes.
        self.canvas = tk.Canvas(
            frame,
            width=940,
            height=470,
            bg="#d9efff",
            highlightthickness=1,
            highlightbackground="#7f9db3"
        )
        self.canvas.pack()

    def dibujar_escena_inicial(self, juego):
        """
        Dibuja la escena principal:
        - limpia el Canvas
        - coloca el fondo
        - muestra un texto superior
        - dibuja al personaje
        """
        self.canvas.delete("all")
        self.items_obstaculos.clear()

        # Fondo principal con imagen.
        self.canvas.create_image(0, 0, image=self.img_fondo, anchor="nw")

        # Texto decorativo superior.
        self.canvas.create_text(
            760, 35,
            text="Evita el fuego y al dragón",
            font=("Arial", 16, "bold"),
            fill="white"
        )

        # Ya no se dibuja la línea gris horizontal para que el escenario
        # se vea más limpio visualmente.
        self._dibujar_personaje(juego.personaje)

    def _dibujar_personaje(self, personaje):
        """Dibuja el personaje usando su imagen GIF."""
        self.item_personaje = self.canvas.create_image(
            personaje.x,
            personaje.y,
            image=self.img_personaje,
            anchor="nw"
        )

        self.item_texto = self.canvas.create_text(
            personaje.x + 45,
            personaje.y - 10,
            text="Héroe",
            font=("Arial", 9, "bold"),
            fill="white"
        )

    def actualizar_personaje(self, personaje):
        """
        Mueve el personaje a su nueva posición dentro del Canvas.
        coords() cambia la posición de un elemento ya dibujado.
        """
        self.canvas.coords(self.item_personaje, personaje.x, personaje.y)
        self.canvas.coords(self.item_texto, personaje.x + 45, personaje.y - 10)

    def crear_obstaculo(self, obstaculo):
        """
        Dibuja un nuevo obstáculo con imagen según su tipo.
        Además guarda la referencia en un diccionario para poder moverlo
        o eliminarlo después.
        """
        if obstaculo.tipo == "fuego":
            item = self.canvas.create_image(
                obstaculo.x,
                obstaculo.y,
                image=self.img_fuego,
                anchor="nw"
            )
        else:
            item = self.canvas.create_image(
                obstaculo.x,
                obstaculo.y,
                image=self.img_dragon,
                anchor="nw"
            )

        self.items_obstaculos[id(obstaculo)] = item

    def actualizar_obstaculo(self, obstaculo):
        """Mueve visualmente un obstáculo existente."""
        item = self.items_obstaculos.get(id(obstaculo))
        if item:
            self.canvas.coords(item, obstaculo.x, obstaculo.y)

    def eliminar_obstaculo(self, obstaculo):
        """
        Elimina un obstáculo del Canvas y del diccionario visual.
        """
        item = self.items_obstaculos.pop(id(obstaculo), None)
        if item:
            self.canvas.delete(item)

    def mostrar_puntaje(self, puntaje):
        """Actualiza el texto del puntaje."""
        self.lbl_puntaje.config(text=f"Puntaje: {puntaje}")

    def mostrar_estado(self, mensaje):
        """Actualiza el mensaje informativo del usuario."""
        self.lbl_estado.config(text=mensaje)

    def mostrar_game_over(self, puntaje):
        """Muestra un panel de fin de juego encima del escenario."""
        self.canvas.create_rectangle(280, 150, 660, 280, fill="#111111", outline="white", width=2)
        self.canvas.create_text(
            470, 190,
            text="GAME OVER",
            font=("Arial", 28, "bold"),
            fill="#ff4d4d"
        )
        self.canvas.create_text(
            470, 225,
            text=f"Puntaje final: {puntaje}",
            font=("Arial", 16, "bold"),
            fill="white"
        )
        self.canvas.create_text(
            470, 255,
            text="Presione Reiniciar para jugar otra vez",
            font=("Arial", 13),
            fill="white"
        )

    def activar_inicio(self):
        """Activa el botón de iniciar."""
        self.btn_iniciar.config(state="normal")

    def desactivar_inicio(self):
        """Desactiva el botón de iniciar mientras la partida corre."""
        self.btn_iniciar.config(state="disabled")
