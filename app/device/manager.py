import secrets
from datetime import datetime, timezone


class DeviceManager:

    def __init__(self):
        self.devices = {}

    def create_device(
        self,
        name: str,
        android_version: str = "Android 14"
    ):
        device_id = (
            "device_"
            + secrets.token_hex(8)
        )

        device = {
            "id": device_id,
            "name": name,
            "android_version": android_version,
            "status": "stopped",
            "created_at": datetime.now(
                timezone.utc
            ).isoformat()
        }

        self.devices[device_id] = device

        return device

    def list_devices(self):
        return list(
            self.devices.values()
        )

    def get_device(self, device_id: str):
        return self.devices.get(device_id)

    def start_device(self, device_id: str):
        device = self.get_device(
            device_id
        )

        if not device:
            return None

        device["status"] = "running"

        return device

    def stop_device(self, device_id: str):
        device = self.get_device(
            device_id
        )

        if not device:
            return None

        device["status"] = "stopped"

        return device

    def delete_device(self, device_id: str):
        if device_id not in self.devices:
            return False

        del self.devices[device_id]

        return True


device_manager = DeviceManager()
