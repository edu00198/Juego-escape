import pickle
import os
import sys

# Ajustes de paths
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

def get_save_file(slot=1):
    return f"savegame_{slot}.pkl"

def save_game(state, slot=1):
    """Guarda el estado del juego en un archivo pickle."""
    save_file = get_save_file(slot)
    try:
        with open(save_file, 'wb') as f:
            pickle.dump(state, f)
        print(f"Juego guardado exitosamente en slot {slot}.")
    except Exception as e:
        print(f"Error al guardar: {e}")

def load_game(slot=1):
    """Carga el estado del juego desde el archivo pickle."""
    save_file = get_save_file(slot)
    if os.path.exists(save_file):
        try:
            with open(save_file, 'rb') as f:
                state = pickle.load(f)
            print(f"Juego cargado exitosamente desde slot {slot}.")
            return state
        except Exception as e:
            print(f"Error al cargar: {e}")
            return None
    else:
        print(f"No hay partida guardada en slot {slot}.")
        return None

def delete_save(slot=1):
    """Elimina el archivo de guardado."""
    save_file = get_save_file(slot)
    if os.path.exists(save_file):
        os.remove(save_file)
        print(f"Partida guardada eliminada del slot {slot}.")
    else:
        print(f"No hay partida guardada en slot {slot} para eliminar.")

def list_saves():
    """Lista los slots con partidas guardadas."""
    saves = []
    for slot in range(1, 6):  # Asumimos 5 slots
        if os.path.exists(get_save_file(slot)):
            saves.append(slot)
    return saves
