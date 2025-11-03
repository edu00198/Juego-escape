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
    'juego.mapa_3_2',
    'juego.mapa_5',
]


def _loader_thread(mods):
    _done_event.clear()
    _progress['total'] = len(mods)
    _progress['loaded'] = 0
    _progress['errors'] = {}

    for name in mods:
        try:
            # Heurística: evitar importar módulos que muy probablemente
            # inicialicen pygame/display o ejecuten bucles en tiempo de import.
            # Para ello, intentamos localizar el archivo fuente y buscar
            # patrones como 'pygame.display' o 'pygame.init' y saltarlos.
            try:
                spec = importlib.util.find_spec(name)
                source_ok = True
                if spec and spec.origin and spec.origin.endswith('.py'):
                    try:
                        with open(spec.origin, 'r', encoding='utf-8', errors='ignore') as f:
                            src = f.read()
                        lowered = src.lower()
                        if 'pygame.display' in lowered or 'pygame.init(' in lowered or 'pygame.display.set_mode' in lowered:
                            # Es muy probable que el módulo abra una ventana al importarlo.
                            print(f"[Loader] Saltando precarga de {name} (contiene inicialización de pygame)")
                            _progress['loaded'] += 0
                            _progress['errors'][name] = 'skipped - gui on import'
                            # Pequeña pausa y continuar
                            time.sleep(0.01)
                            continue
                    except Exception:
                        # Si no podemos leer el fichero, dejamos que el import normal lo intente
                        source_ok = True

            except Exception:
                # Si find_spec falla, continuamos con el import normal
                pass

            # Importar el módulo; si ya existe en sys.modules esto es rápido.
            if name in sys.modules:
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
