class AndroidDeviceAdapter:

    def __init__(self):
        self.connected = False

    def connect(self):
        self.connected = True

        return {
            "success": True,
            "connected": True
        }

    def disconnect(self):
        self.connected = False

        return {
            "success": True,
            "connected": False
        }

    def status(self):
        return {
            "connected": self.connected,
            "android_virtualization": False,
            "message": (
                "Android virtualization layer "
                "is not connected yet."
            )
        }


android_adapter = AndroidDeviceAdapter()
