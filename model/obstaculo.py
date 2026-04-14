class Obstaculo:
    """
    Modelo de un obstáculo del juego.

    Un obstáculo puede ser de dos tipos:
    - fuego
    - dragón

    El controlador crea estos objetos y la vista los dibuja con imágenes.
    """

    def __init__(self, x, y, ancho, alto, velocidad, tipo):
        # Posición del obstáculo en el escenario.
        self.x = x
        self.y = y

        # Tamaño lógico para colisiones.
        self.ancho = ancho
        self.alto = alto

        # Velocidad con la que el obstáculo se mueve hacia la izquierda.
        self.velocidad = velocidad

        # Tipo del obstáculo: "fuego" o "dragon".
        self.tipo = tipo
