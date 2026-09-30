from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

from app.device.manager import device_manager
from app.device.adapter import android_adapter
from app.network.manager import network_manager
from app.storage.manager import storage_manager


router = APIRouter(
    prefix="/v1"
)


class CreateDeviceRequest(BaseModel):

    name: str

    android_version: str = "Android 14"


class NetworkConfigRequest(BaseModel):

    mode: str


@router.get("/status")
def status():

    return {
        "success": True,
        "service": "AniVora Cloud Phone",
        "status": "online"
    }


@router.post("/devices")
def create_device(
    request: CreateDeviceRequest
):

    if not request.name.strip():

        raise HTTPException(
            status_code=400,
            detail="Device name cannot be empty"
        )

    device = device_manager.create_device(
        request.name,
        request.android_version
    )

    return {
        "success": True,
        "device": device
    }


@router.get("/devices")
def list_devices():

    return {
        "success": True,
        "devices": device_manager.list_devices()
    }


@router.get("/devices/{device_id}")
def get_device(device_id: str):

    device = device_manager.get_device(
        device_id
    )

    if not device:

        raise HTTPException(
            status_code=404,
            detail="Device not found"
        )

    return {
        "success": True,
        "device": device
    }


@router.post("/devices/{device_id}/start")
def start_device(device_id: str):

    device = device_manager.start_device(
        device_id
    )

    if not device:

        raise HTTPException(
            status_code=404,
            detail="Device not found"
        )

    return {
        "success": True,
        "device": device
    }


@router.post("/devices/{device_id}/stop")
def stop_device(device_id: str):

    device = device_manager.stop_device(
        device_id
    )

    if not device:

        raise HTTPException(
            status_code=404,
            detail="Device not found"
        )

    return {
        "success": True,
        "device": device
    }


@router.delete("/devices/{device_id}")
def delete_device(device_id: str):

    deleted = device_manager.delete_device(
        device_id
    )

    if not deleted:

        raise HTTPException(
            status_code=404,
            detail="Device not found"
        )

    return {
        "success": True,
        "deleted": True
    }


@router.get("/android/status")
def android_status():

    return {
        "success": True,
        "android": android_adapter.status()
    }


@router.post("/android/connect")
def android_connect():

    return android_adapter.connect()


@router.post("/android/disconnect")
def android_disconnect():

    return android_adapter.disconnect()


@router.get("/network/status")
def network_status():

    return {
        "success": True,
        "network": network_manager.status()
    }


@router.post("/network/configure")
def configure_network(
    request: NetworkConfigRequest
):

    try:

        result = network_manager.configure(
            request.mode
        )

        return {
            "success": True,
            "network": result
        }

    except ValueError as error:

        raise HTTPException(
            status_code=400,
            detail=str(error)
        )


@router.get("/storage/status")
def storage_status():

    return {
        "success": True,
        "storage": storage_manager.status()
    }


@router.post("/storage/reset")
def reset_storage():

    return {
        "success": True,
        "storage": storage_manager.reset()
  }
