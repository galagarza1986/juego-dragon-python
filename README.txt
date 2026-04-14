Juego de salto estilo arcade con hilos en Python usando tkinter y MVC.

Esta versión usa imágenes reales:
- Fondo: assets/pantano.jpg
- Personaje: assets/h2.gif
- Fuego: assets/f.gif
- Dragón: assets/maloani.gif

Controles:
- Botón "Iniciar juego"
- Barra espaciadora para saltar
- Botón "Reiniciar"

Conceptos didácticos aplicados:
- threading
- múltiples hilos
- sincronización con Lock
- actualización segura de la interfaz con Queue + after()
- organización con MVC
- eventos de teclado con tkinter

Importante:
Tkinter no debe actualizarse directamente desde hilos secundarios.
Por eso los hilos del juego envían eventos a una cola, y la interfaz
los procesa desde el hilo principal con after().

Nota:
Para cargar el fondo JPG se usa Pillow (PIL).
Si hiciera falta instalarlo:
py -3.11 -m pip install pillow
