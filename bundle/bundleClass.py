import time

class bundleClass:
    def __init__(self, name: str):
        self.name = name
        self.active_requests = []  # list to store active requests

    def add_request(self, request: dict):
        """
        Save a new request with timestamp.
        :param request: dict with the request data
        """
        req_info = {
            "timestamp": time.time(),
            "request": request
        }
        self.active_requests.append(req_info)

    def remove_request(self, request: dict):
        """
        Remove a request when it has finished.
        :param request: dict that should be removed
        """
        self.active_requests = [
            r for r in self.active_requests if r["request"] != request
        ]

    def list_requests(self):
        """Return all current active requests."""
        return self.active_requests

    def clear_requests(self):
        """Clear all active requests (for example when restarting the bundle)."""
        self.active_requests.clear()
