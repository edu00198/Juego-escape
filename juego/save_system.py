import os
import pickle

# Carpeta de guardados dentro del módulo juego
SAVE_DIR = os.path.join(os.path.dirname(__file__), 'saves')
os.makedirs(SAVE_DIR, exist_ok=True)

def _slot_path(slot: int) -> str:
    return os.path.join(SAVE_DIR, f"slot_{int(slot)}.sav")

def save_game(state, slot: int = 1) -> bool:
    """
    Guarda 'state' en el slot indicado. Devuelve True si tuvo éxito.
    """
    try:
        path = _slot_path(slot)
        with open(path, 'wb') as f:
            pickle.dump(state, f)
        print(f"[save_system] Guardado en {path}")
        return True
    except Exception as e:
        print(f"[save_system] Error guardando slot {slot}: {e}")
        return False

def load_game(slot: int):
    """
    Carga y devuelve el estado guardado en el slot, o None si no existe / falla.
    """
    try:
        path = _slot_path(slot)
        if not os.path.exists(path):
            print(f"[save_system] No existe archivo para slot {slot}")
            return None
        with open(path, 'rb') as f:
            state = pickle.load(f)
        print(f"[save_system] Cargado slot {slot} desde {path}")
        return state
    except Exception as e:
        print(f"[save_system] Error cargando slot {slot}: {e}")
        return None

def list_saves():
    """
    Devuelve una lista de números de slot (ints) que actualmente contienen guardados.
    """
    slots = []
    try:
        for name in os.listdir(SAVE_DIR):
            if name.startswith("slot_") and name.endswith(".sav"):
                try:
                    num = int(name[len("slot_"):-len(".sav")])
                    slots.append(num)
                except Exception:
                    pass
    except Exception as e:
        print(f"[save_system] Error listando saves: {e}")
    return sorted(slots)

def delete_save(slot: int) -> bool:
    """
    Elimina el archivo de guardado para el slot indicado. Devuelve True si se eliminó.
    """
    try:
        path = _slot_path(slot)
        if os.path.exists(path):
            os.remove(path)
            print(f"[save_system] Eliminado save: {path}")
            return True
        else:
            print(f"[save_system] No se encontró save para slot {slot} ({path})")
            return False
    except Exception as e:
        print(f"[save_system] Error eliminando slot {slot}: {e}")
        return False
