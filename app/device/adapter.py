import os
import subprocess
import time


class AndroidDeviceAdapter:

    def __init__(self):
        self.emulator_command = os.getenv(
            "ANDROID_EMULATOR",
            "emulator"
        )

        self.adb_command = os.getenv(
            "ANDROID_ADB",
            "adb"
        )

        self.running_devices = {}

    def _run(
        self,
        command,
        timeout=30
    ):

        try:

            result = subprocess.run(
                command,
                capture_output=True,
                text=True,
                timeout=timeout
            )

            return {
                "success": result.returncode == 0,
                "returncode": result.returncode,
                "stdout": result.stdout.strip(),
                "stderr": result.stderr.strip()
            }

        except FileNotFoundError:

            return {
                "success": False,
                "returncode": -1,
                "stdout": "",
                "stderr": (
                    f"Command not found: "
                    f"{command[0]}"
                )
            }

        except subprocess.TimeoutExpired:

            return {
                "success": False,
                "returncode": -1,
                "stdout": "",
                "stderr": "Command timed out"
            }

        except Exception as error:

            return {
                "success": False,
                "returncode": -1,
                "stdout": "",
                "stderr": str(error)
            }

    def check_tools(self):

        emulator = self._run(
            [
                self.emulator_command,
                "-version"
            ]
        )

        adb = self._run(
            [
                self.adb_command,
                "version"
            ]
        )

        return {
            "emulator_available": emulator["success"],
            "adb_available": adb["success"],
            "emulator_output": (
                emulator["stdout"]
                or emulator["stderr"]
            ),
            "adb_output": (
                adb["stdout"]
                or adb["stderr"]
            )
        }

    def list_avds(self):

        result = self._run(
            [
                self.emulator_command,
                "-list-avds"
            ]
        )

        if not result["success"]:

            return {
                "success": False,
                "devices": [],
                "error": result["stderr"]
            }

        devices = [
            line.strip()
            for line in result["stdout"].splitlines()
            if line.strip()
        ]

        return {
            "success": True,
            "devices": devices
        }

    def list_connected_devices(self):

        result = self._run(
            [
                self.adb_command,
                "devices"
            ]
        )

        if not result["success"]:

            return {
                "success": False,
                "devices": [],
                "error": result["stderr"]
            }

        devices = []

        for line in result["stdout"].splitlines():

            line = line.strip()

            if not line:
                continue

            if line.startswith("List of devices"):
                continue

            parts = line.split()

            if len(parts) >= 2:

                devices.append(
                    {
                        "serial": parts[0],
                        "status": parts[1]
                    }
                )

        return {
            "success": True,
            "devices": devices
        }

    def start_avd(
        self,
        avd_name: str,
        headless: bool = True
    ):

        if not avd_name.strip():

            return {
                "success": False,
                "error": "AVD name cannot be empty"
            }

        command = [
            self.emulator_command,
            "-avd",
            avd_name,
            "-accel",
            "auto",
            "-no-boot-anim"
        ]

        if headless:

            command.extend(
                [
                    "-no-window"
                ]
            )

        try:

            process = subprocess.Popen(
                command,
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL
            )

            self.running_devices[avd_name] = {
                "avd": avd_name,
                "pid": process.pid,
                "process": process,
                "status": "starting"
            }

            return {
                "success": True,
                "avd": avd_name,
                "pid": process.pid,
                "status": "starting"
            }

        except FileNotFoundError:

            return {
                "success": False,
                "error": (
                    "Android Emulator was not found."
                )
            }

        except Exception as error:

            return {
                "success": False,
                "error": str(error)
            }

    def wait_for_device(
        self,
        serial=None,
        timeout=120
    ):

        start_time = time.time()

        while (
            time.time() - start_time
            < timeout
        ):

            devices = (
                self.list_connected_devices()
            )

            if devices["success"]:

                for device in devices["devices"]:

                    if (
                        serial is None
                        or device["serial"] == serial
                    ):

                        if device["status"] == "device":

                            return {
                                "success": True,
                                "device": device
                            }

            time.sleep(2)

        return {
            "success": False,
            "error": (
                "Android device did not become "
                "ready before timeout."
            )
        }

    def stop_device(
        self,
        serial
    ):

        if not serial:

            return {
                "success": False,
                "error": "Device serial is required"
            }

        result = self._run(
            [
                self.adb_command,
                "-s",
                serial,
                "emu",
                "kill"
            ]
        )

        return {
            "success": result["success"],
            "serial": serial,
            "message": (
                "Device stopped."
                if result["success"]
                else result["stderr"]
            )
        }

    def device_info(
        self,
        serial
    ):

        if not serial:

            return {
                "success": False,
                "error": "Device serial is required"
            }

        properties = [
            "ro.product.model",
            "ro.product.manufacturer",
            "ro.build.version.release",
            "ro.build.version.sdk",
            "ro.product.cpu.abi"
        ]

        info = {
            "serial": serial
        }

        for property_name in properties:

            result = self._run(
                [
                    self.adb_command,
                    "-s",
                    serial,
                    "shell",
                    "getprop",
                    property_name
                ]
            )

            if result["success"]:

                info[property_name] = (
                    result["stdout"]
                )

        return {
            "success": True,
            "device": info
        }

    def screenshot(
        self,
        serial,
        output_path
    ):

        if not serial:

            return {
                "success": False,
                "error": "Device serial is required"
            }

        try:

            with open(
                output_path,
                "wb"
            ) as output:

                result = subprocess.run(
                    [
                        self.adb_command,
                        "-s",
                        serial,
                        "exec-out",
                        "screencap",
                        "-p"
                    ],
                    stdout=output,
                    stderr=subprocess.PIPE,
                    timeout=30
                )

            if result.returncode != 0:

                return {
                    "success": False,
                    "error": (
                        result.stderr.decode(
                            errors="replace"
                        )
                    )
                }

            return {
                "success": True,
                "serial": serial,
                "file": output_path
            }

        except Exception as error:

            return {
                "success": False,
                "error": str(error)
            }

    def status(self):

        tools = self.check_tools()

        avds = self.list_avds()

        connected = (
            self.list_connected_devices()
        )

        return {
            "connected": (
                connected["success"]
                and len(
                    connected["devices"]
                ) > 0
            ),
            "android_virtualization": (
                tools["emulator_available"]
            ),
            "adb_available": (
                tools["adb_available"]
            ),
            "available_avds": avds.get(
                "devices",
                []
            ),
            "connected_devices": connected.get(
                "devices",
                []
            )
        }


android_adapter = AndroidDeviceAdapter()
