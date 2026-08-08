from paho.mqtt import publish, subscribe
import json
import os


hostname = "mosquitto"
port = 1883


class LightStates:
    ON = "ON"
    OFF = "OFF"
    TOGGLE = "TOGGLE"


MOCK_ZIGBEE = os.getenv("MOCK_ZIGBEE")


def data_to_json(msg: bytes):
    return json.loads(msg.payload.decode("utf-8"))

def get_health() -> dict:
    if MOCK_ZIGBEE:
        return {}
    
    msg = subscribe.simple("zigbee2mqtt/bridge/health", hostname=hostname, port=port)
    health = data_to_json(msg)
    return health


def get_devices() -> list[str]:
    if MOCK_ZIGBEE:
        return []
    msg = subscribe.simple("zigbee2mqtt/bridge/devices", hostname=hostname, port=port)
    devices = data_to_json(msg)
    device_list = [dev["friendly_name"] for dev in devices if dev["type"] != "Coordinator"]
    return device_list


def set_device_state(friendly_name: str, payload: str):
    if MOCK_ZIGBEE:
        return None
    topic = f"zigbee2mqtt/{friendly_name}/set"
    return publish.single(topic, payload, hostname=hostname, port=port)


def get_device_state(friendly_name: str):
    if MOCK_ZIGBEE:
        return None
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



