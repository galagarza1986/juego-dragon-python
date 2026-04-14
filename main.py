import tkinter as tk

from model.juego import Juego
from view.juego_view import JuegoView
from controller.juego_controller import JuegoController


def main():
    """
    Punto de entrada del programa.

    Aquí se crean las tres partes principales del patrón MVC:
    - Modelo: Juego
    - Vista: JuegoView
    - Controlador: JuegoController
    """
    # Ventana principal de Tkinter.
    root = tk.Tk()

    # Modelo: guarda el estado lógico de la partida.
    juego = Juego()

    # Vista: construye y muestra la interfaz gráfica.
    vista = JuegoView(root)

    # Controlador: conecta modelo y vista, maneja hilos y eventos.
    JuegoController(juego, vista)

    # Inicia el ciclo principal de la ventana.
    root.mainloop()


if __name__ == "__main__":
    main()
