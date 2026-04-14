from model.personaje import Personaje


class Juego:
    """
    Modelo principal del juego.

    Esta clase centraliza el estado lógico de la partida:
    - personaje
    - lista de obstáculos
    - puntaje
    - si el juego está corriendo
    - si ocurrió game over
    """

    def __init__(self):
        # Personaje principal del juego.
        self.personaje = Personaje()

        # Lista donde se guardan los obstáculos activos.
        self.obstaculos = []

        # Puntaje actual del jugador.
        self.puntaje = 0

        # True mientras la partida está activa.
        self.en_curso = False

        # True cuando el personaje choca y termina la partida.
        self.game_over = False

        # Altura aproximada del suelo dentro del escenario.
        self.suelo_y = 390

        # Valor de gravedad aplicado al salto.
        self.gravedad = 1.1

    def reiniciar(self):
        """
        Restaura el juego a su estado inicial.
        Se usa al iniciar una nueva partida o al reiniciar.
        """
        self.personaje = Personaje()
        self.obstaculos = []
        self.puntaje = 0
        self.en_curso = False
        self.game_over = False
