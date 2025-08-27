#fondo.py solo guarda rutas de fondos.
import os

fondo_prueba = os.path.join(os.path.dirname(os.path.dirname(__file__)), "fondos", "fondo_prueba.png")
fondo_1 = os.path.join(os.path.dirname(os.path.dirname(__file__)), "fondos", "fondo_1.png")
fondo_2 = os.path.join(os.path.dirname(os.path.dirname(__file__)), "fondos", "fondo_2.png")
fondo_prueba = fondo_1  # Puedes cambiar esto a otro fondo si lo deseas