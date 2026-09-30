class NetworkManager:

    def __init__(self):
        self.mode = "private"
        self.connected = False

    def status(self):
        return {
            "mode": self.mode,
            "connected": self.connected
        }

    def configure(self, mode: str):

        allowed_modes = [
            "private",
            "direct"
        ]

        if mode not in allowed_modes:
            raise ValueError(
                "Unsupported network mode"
            )

        self.mode = mode

        return self.status()


network_manager = NetworkManager()
