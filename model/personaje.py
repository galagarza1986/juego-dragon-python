class Personaje:
    """
    Modelo del personaje principal.

    En MVC, el modelo representa los datos del programa.
    Esta clase NO dibuja nada en pantalla; solo guarda el estado lógico
    del personaje para que luego la vista lo muestre.

    Atributos principales:
    - x, y: posición del personaje en el escenario
    - ancho, alto: tamaño aproximado para las colisiones
    - velocidad_y: velocidad vertical del salto
    - en_suelo: indica si el personaje está apoyado en el piso
    """

    def __init__(self):
        # Posición horizontal fija del personaje.
        self.x = 110

        # Tamaño aproximado del GIF mostrado en pantalla.
        # Se mantiene como referencia para calcular colisiones,
        # aunque el personaje visualmente se dibuja con una imagen.
        self.ancho = 92
        self.alto = 67

        # El suelo visual del juego está alrededor de y = 390.
        # Para que el personaje quede "parado" sobre el suelo,
        # colocamos su coordenada Y inicial en:
        # suelo - alto del personaje
        self.y = 390 - self.alto

        # Velocidad vertical actual.
        # Cuando el personaje salta, este valor se vuelve negativo
        # para que suba en pantalla.
        self.velocidad_y = 0

        # True si el personaje está tocando el suelo.
        self.en_suelo = True

    def saltar(self):
        """
        Inicia el salto del personaje.

        Solo se permite saltar si el personaje está en el suelo.
        Al saltar:
        - la velocidad vertical se vuelve negativa
        - en_suelo pasa a False
        """
        if self.en_suelo:
            self.velocidad_y = -18
            self.en_suelo = False
