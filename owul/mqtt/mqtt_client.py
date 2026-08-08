from paho.mqtt import publish, subscribe
import json


hostname = "localhost"
port = 1883


class LightStates:
    ON = "ON"
    OFF = "OFF"
    TOGGLE = "TOGGLE"


def get_health() -> dict:
    msg = subscribe.simple("zigbee2mqtt/bridge/health", hostname=hostname, port=port)
    health = json.loads(msg.payload.decode("utf-8"))
    return health


def get_devices() -> list[str]:
    # The device must check in to Z2M after a restart before it will be marked as available
    health = get_health()
    devices: dict = health.get("devices", {})
    return list(devices.keys())


def set_device_state(friendly_name: str, payload: str):
    topic = f"zigbee2mqtt/{friendly_name}/set"
    return publish.single(topic, payload, hostname=hostname, port=port)


def get_device_state(friendly_name: str):
    topic = f"zigbee2mqtt/{friendly_name}/get"
    payload = json.dumps({"state": ""})
    return publish.single(topic, payload, hostname=hostname, port=port)


def power_on_device(friendly_name: str):
    payload = {"state":LightStates.ON}
    return set_device_state(friendly_name, json.dumps(payload))


def power_off_device(friendly_name: str):
    payload = {"state":LightStates.OFF}
    return set_device_state(friendly_name, json.dumps(payload))


def toggle_device(friendly_name: str):
    payload = {"state":LightStates.TOGGLE}
    return set_device_state(friendly_name, json.dumps(payload))


def set_device_brightness(friendly_name: str, brightness: float):
    payload = {"brightness": brightness}
    return set_device_state(friendly_name, json.dumps(payload))


def set_device_gradual_brightness(friendly_name: str, rate: float):
    payload = {
        "brightness_move": rate
    }
    return set_device_state(friendly_name, json.dumps(payload))



