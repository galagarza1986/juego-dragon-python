import random
import threading
import time
from queue import Queue, Empty

from model.obstaculo import Obstaculo


class JuegoController:
    """
    Controlador del juego.

    En MVC, el controlador actúa como intermediario entre:
    - el modelo (datos y estado lógico)
    - la vista (interfaz gráfica)

    Aquí se coordina:
    - el inicio y reinicio del juego
    - la entrada del usuario (salto)
    - los hilos del juego
    - la sincronización con Lock
    - el envío de eventos a la interfaz por medio de una Queue
    """

    def __init__(self, juego, vista):
        # Referencias al modelo y a la vista.
        self.juego = juego
        self.vista = vista

        # Lock:
        # sirve para que varios hilos no modifiquen al mismo tiempo
        # los mismos datos compartidos.
        self.lock = threading.Lock()

        # Queue:
        # cola de eventos usada para comunicar hilos secundarios
        # con la interfaz gráfica de Tkinter.
        self.eventos = Queue()

        # Referencias a los hilos del juego.
        self.hilo_fisica = None
        self.hilo_obstaculos = None
        self.hilo_puntaje = None

        # Bandera general para detener los bucles de los hilos.
        self.detener = False

        self._configurar()

    def _configurar(self):
        """
        Conecta botones, teclado y deja la escena inicial lista.
        """
        self.vista.btn_iniciar.config(command=self.iniciar_juego)
        self.vista.btn_reiniciar.config(command=self.reiniciar_juego)

        # Evento del teclado: barra espaciadora.
        self.vista.root.bind("<space>", self.evento_saltar)

        # Dibujo inicial.
        self.vista.dibujar_escena_inicial(self.juego)

        # after() hace que Tkinter llame periódicamente a una función.
        # Aquí sirve para revisar la cola de eventos sin bloquear la interfaz.
        self.vista.root.after(20, self.procesar_eventos)

    def evento_saltar(self, event=None):
        """
        Se ejecuta cuando el usuario presiona la barra espaciadora.
        """
        with self.lock:
            if self.juego.en_curso and not self.juego.game_over:
                self.juego.personaje.saltar()

    def iniciar_juego(self):
        """
        Inicia una nueva partida y crea los hilos principales.
        """
        if self.juego.en_curso:
            return

        with self.lock:
            self.juego.reiniciar()
            self.juego.en_curso = True
            self.detener = False

        self.vista.dibujar_escena_inicial(self.juego)
        self.vista.mostrar_puntaje(0)
        self.vista.mostrar_estado("Juego en curso. Presione espacio para saltar.")
        self.vista.desactivar_inicio()

        # Hilo 1: física, movimiento y colisiones.
        self.hilo_fisica = threading.Thread(target=self.loop_fisica, daemon=True)

        # Hilo 2: generación de nuevos obstáculos.
        self.hilo_obstaculos = threading.Thread(target=self.loop_obstaculos, daemon=True)

        # Hilo 3: incremento del puntaje.
        self.hilo_puntaje = threading.Thread(target=self.loop_puntaje, daemon=True)

        self.hilo_fisica.start()
        self.hilo_obstaculos.start()
        self.hilo_puntaje.start()

    def reiniciar_juego(self):
        """
        Detiene la partida actual y deja el juego listo nuevamente.
        """
        self.detener = True

        with self.lock:
            self.juego.reiniciar()

        self.vista.dibujar_escena_inicial(self.juego)
        self.vista.mostrar_puntaje(0)
        self.vista.mostrar_estado("Juego reiniciado. Presione Iniciar.")
        self.vista.activar_inicio()

    def loop_fisica(self):
        """
        Hilo encargado de:
        - aplicar gravedad al personaje
        - mover el personaje verticalmente
        - mover obstáculos
        - detectar colisiones
        """
        while not self.detener:
            time.sleep(0.03)

            with self.lock:
                if not self.juego.en_curso or self.juego.game_over:
                    continue

                personaje = self.juego.personaje

                # Aplicamos gravedad y actualizamos la posición vertical.
                personaje.velocidad_y += self.juego.gravedad
                personaje.y += personaje.velocidad_y

                # Si el personaje toca el suelo, se corrige su posición.
                suelo_y_personaje = 390 - personaje.alto
                if personaje.y >= suelo_y_personaje:
                    personaje.y = suelo_y_personaje
                    personaje.velocidad_y = 0
                    personaje.en_suelo = True

                # Enviamos evento para actualizar la posición visual del personaje.
                self.eventos.put({
                    "tipo": "personaje",
                    "personaje": personaje
                })

                obstaculos_a_eliminar = []

                for obstaculo in self.juego.obstaculos:
                    # El obstáculo avanza hacia la izquierda.
                    obstaculo.x -= obstaculo.velocidad

                    # Si salió completamente de pantalla, se marca para eliminar.
                    if obstaculo.x + obstaculo.ancho < 0:
                        obstaculos_a_eliminar.append(obstaculo)
                    else:
                        # Si sigue activo, se actualiza su posición visual.
                        self.eventos.put({
                            "tipo": "actualizar_obstaculo",
                            "obstaculo": obstaculo
                        })

                        # Verificamos colisión.
                        if self.hay_colision(personaje, obstaculo):
                            self.juego.game_over = True
                            self.juego.en_curso = False
                            self.eventos.put({
                                "tipo": "game_over",
                                "puntaje": self.juego.puntaje
                            })

                # Eliminamos los obstáculos que ya salieron del escenario.
                for obstaculo in obstaculos_a_eliminar:
                    if obstaculo in self.juego.obstaculos:
                        self.juego.obstaculos.remove(obstaculo)
                        self.eventos.put({
                            "tipo": "eliminar_obstaculo",
                            "obstaculo": obstaculo
                        })

    def loop_obstaculos(self):
        """
        Hilo encargado de generar nuevos obstáculos cada cierto tiempo.
        """
        while not self.detener:
            time.sleep(random.uniform(1.3, 2.2))

            with self.lock:
                if not self.juego.en_curso or self.juego.game_over:
                    continue

                tipo = random.choice(["fuego", "dragon"])

                if tipo == "fuego":
                    obstaculo = Obstaculo(
                        x=960,
                        y=340,
                        ancho=50,
                        alto=50,
                        velocidad=random.randint(9, 13),
                        tipo="fuego"
                    )
                else:
                    obstaculo = Obstaculo(
                        x=960,
                        y=305,
                        ancho=85,
                        alto=85,
                        velocidad=random.randint(11, 15),
                        tipo="dragon"
                    )

                self.juego.obstaculos.append(obstaculo)

                # La vista lo dibujará cuando procese este evento.
                self.eventos.put({
                    "tipo": "crear_obstaculo",
                    "obstaculo": obstaculo
                })

    def loop_puntaje(self):
        """
        Hilo encargado de incrementar el puntaje mientras el jugador siga vivo.
        """
        while not self.detener:
            time.sleep(0.2)

            with self.lock:
                if not self.juego.en_curso or self.juego.game_over:
                    continue

                self.juego.puntaje += 1

                self.eventos.put({
                    "tipo": "puntaje",
                    "puntaje": self.juego.puntaje
                })

    def hay_colision(self, personaje, obstaculo):
        """
        Revisa si las cajas de colisión del personaje y del obstáculo
        se superponen.

        Esta función usa una detección de colisión por rectángulos.
        """
        px1 = personaje.x
        py1 = personaje.y
        px2 = personaje.x + personaje.ancho
        py2 = personaje.y + personaje.alto

        ox1 = obstaculo.x
        oy1 = obstaculo.y
        ox2 = obstaculo.x + obstaculo.ancho
        oy2 = obstaculo.y + obstaculo.alto

        return (px1 < ox2 and px2 > ox1 and py1 < oy2 and py2 > oy1)

    def procesar_eventos(self):
        """
        Procesa la cola de eventos desde el hilo principal de Tkinter.

        Esto es importante porque Tkinter no debe actualizar sus widgets
        directamente desde hilos secundarios.
        """
        try:
            while True:
                evento = self.eventos.get_nowait()
                tipo = evento["tipo"]

                if tipo == "personaje":
                    self.vista.actualizar_personaje(evento["personaje"])

                elif tipo == "crear_obstaculo":
                    self.vista.crear_obstaculo(evento["obstaculo"])

                elif tipo == "actualizar_obstaculo":
                    self.vista.actualizar_obstaculo(evento["obstaculo"])

                elif tipo == "eliminar_obstaculo":
                    self.vista.eliminar_obstaculo(evento["obstaculo"])

                elif tipo == "puntaje":
                    self.vista.mostrar_puntaje(evento["puntaje"])

                elif tipo == "game_over":
                    self.vista.mostrar_estado("El personaje chocó con un obstáculo.")
                    self.vista.mostrar_game_over(evento["puntaje"])
                    self.vista.activar_inicio()

        except Empty:
            pass

        # Se vuelve a programar esta función para revisar eventos otra vez.
        self.vista.root.after(20, self.procesar_eventos)
