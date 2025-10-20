import threading
import importlib
import sys
import time

_lock = threading.Lock()
_thread = None
_done_event = threading.Event()
_progress = {
    'total': 0,
    'loaded': 0,
    'errors': {}
}

# Lista de módulos que se consideran "pesados" y conviene precargar.
_MODULES_TO_LOAD = [
    'juego.mapa_1',
    'juego.mapa_2',
    'juego.jugador',
    'juego.mapa_3',
    'juego.mapa_4',
    'juego.mapa_5',
]


def _loader_thread(mods):
    _done_event.clear()
    _progress['total'] = len(mods)
    _progress['loaded'] = 0
    _progress['errors'] = {}

    for name in mods:
        try:
            # Importar el módulo; si ya existe en sys.modules esto es rápido.
            if name in sys.modules:
                # rebinding local variable for easier access later
                importlib.reload(sys.modules[name])
            else:
                importlib.import_module(name)
            _progress['loaded'] += 1
            print(f"[Loader] Módulo precargado: {name} ({_progress['loaded']}/{_progress['total']})")
        except Exception as e:
            _progress['errors'][name] = str(e)
            print(f"[Loader] Error cargando {name}: {e}")
        # Pequeña pausa para evitar bloquear demasiado la CPU y dar tiempo al hilo principal
        time.sleep(0.05)

    _done_event.set()
    print("[Loader] Precarga finalizada")


def start_background_load(modules=None):
    """Inicia la precarga de módulos en un hilo en background.

    Si ya se está ejecutando, no hace nada.
    """
    global _thread
    with _lock:
        if _thread and _thread.is_alive():
            print("[Loader] Ya se está ejecutando la precarga")
            return

        mods = modules if modules is not None else list(_MODULES_TO_LOAD)
        _thread = threading.Thread(target=_loader_thread, args=(mods,), daemon=True)
        _thread.start()
        print("[Loader] Hilo de precarga iniciado")


def is_done():
    return _done_event.is_set()


def get_progress():
    return dict(_progress)


def wait_until_done(timeout=None):
    """Bloquea hasta que la precarga termine o se alcance el timeout (segundos)."""
    _done_event.wait(timeout)
