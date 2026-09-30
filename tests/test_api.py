from fastapi.testclient import TestClient

from app.main import app


client = TestClient(app)


def test_root():

    response = client.get("/")

    assert response.status_code == 200

    data = response.json()

    assert data["name"] == (
        "AniVora Cloud Phone"
    )


def test_health():

    response = client.get(
        "/health"
    )

    assert response.status_code == 200

    assert response.json()["status"] == (
        "healthy"
    )


def test_status():

    response = client.get(
        "/v1/status"
    )

    assert response.status_code == 200

    assert response.json()["success"] is True


def test_create_device():

    response = client.post(
        "/v1/devices",
        json={
            "name": "Test Phone",
            "android_version": "Android 14"
        }
    )

    assert response.status_code == 200

    data = response.json()

    assert data["success"] is True

    assert data["device"]["name"] == (
        "Test Phone"
    )


def test_list_devices():

    response = client.get(
        "/v1/devices"
    )

    assert response.status_code == 200

    assert "devices" in response.json()


def test_android_status():

    response = client.get(
        "/v1/android/status"
    )

    assert response.status_code == 200

    assert "android" in response.json()


def test_network_status():

    response = client.get(
        "/v1/network/status"
    )

    assert response.status_code == 200

    assert "network" in response.json()


def test_storage_status():

    response = client.get(
        "/v1/storage/status"
    )

    assert response.status_code == 200

    assert "storage" in response.json()
