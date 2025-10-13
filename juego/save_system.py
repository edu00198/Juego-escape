import pickle
import os
import sys

# Ajustes de paths
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

SAVE_FILE = "savegame.pkl"

def save_game(state):
    """Guarda el estado del juego en un archivo pickle."""
    try:
        with open(SAVE_FILE, 'wb') as f:
            pickle.dump(state, f)
        print("Juego guardado exitosamente.")
    except Exception as e:
        print(f"Error al guardar: {e}")

def load_game():
    """Carga el estado del juego desde el archivo pickle."""
    if os.path.exists(SAVE_FILE):
        try:
            with open(SAVE_FILE, 'rb') as f:
                state = pickle.load(f)
            print("Juego cargado exitosamente.")
            return state
        except Exception as e:
            print(f"Error al cargar: {e}")
            return None
    else:
        print("No hay partida guardada.")
        return None

def delete_save():
    """Elimina el archivo de guardado."""
    if os.path.exists(SAVE_FILE):
        os.remove(SAVE_FILE)
        print("Partida guardada eliminada.")
    else:
        print("No hay partida guardada para eliminar.")
