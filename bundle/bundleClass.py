import time

class Bundle:
    def __init__(self, name: str):
        self.name = name
        self.active_requests = []  # aquí se guardan las peticiones activas

    def add_request(self, request: dict):
        """
        Guarda una nueva petición con timestamp.
        :param request: dict con los datos de la petición
        """
        req_info = {
            "timestamp": time.time(),
            "request": request
        }
        self.active_requests.append(req_info)

    def remove_request(self, request: dict):
        """
        Elimina una petición si ya terminó.
        :param request: dict que se quiere eliminar
        """
        self.active_requests = [
            r for r in self.active_requests if r["request"] != request
        ]

    def list_requests(self):
        """Devuelve todas las peticiones en curso."""
        return self.active_requests

    def clear_requests(self):
        """Vacía todas las peticiones activas (por ejemplo al reiniciar el bundle)."""
        self.active_requests.clear()
