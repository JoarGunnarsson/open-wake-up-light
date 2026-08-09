from owul.database.database import database
from owul.mqtt import mqtt_client
from owul.alarm.alarm import DeviceAction, Alarm

from flask import Flask, abort, request

app = Flask(__name__)
NO_CONTENT = ("", 204)

def ensure_device_exists(device):
    existing_devices = mqtt_client.get_devices()
    if device not in existing_devices:
        abort(400, f"Requested device '{device}' does not seem to be paired")


@app.route("/devices", methods=["GET"])
def get_devices():
    return {"devices": mqtt_client.get_devices()}


@app.route("/devices/<device>/state", methods=["PUT"])
def device_state(device):
    ensure_device_exists(device)

    action = DeviceAction("state", request.get_json())
    action.perform_on_device(device)
    return NO_CONTENT

@app.route("/devices/<device>/brightness", methods=["PUT"])
def device_brightness(device):
    ensure_device_exists(device)

    action = DeviceAction("brightness", request.get_json())
    action.perform_on_device(device)
    return NO_CONTENT


@app.route("/devices/<device>/gradual_brightness", methods=["POST"])
def device_gradual_brightness(device):
    ensure_device_exists(device)
    action = DeviceAction("gradual_brightness", request.get_json())
    action.perform_on_device(device)
    return NO_CONTENT


@app.get("/alarms")
def get_alarms():
    return database.get("alarms", {})


@app.delete("/alarms/<id>")
def delete_alarm(id):
    alarms = database.get("alarms")
    if id not in alarms:
        abort(400, "An alarm with that uuid does not exits")

    # If an alarm is already active, this will not turn it off
    del alarms[id]
    database.update("alarms", alarms)
    return NO_CONTENT


@app.post("/alarms/create")
def create_alarm():
    data = request.get_json()
    if "devices" not in data or not isinstance(data["devices"], list):
        abort(400, "To create an alarm, a list of devices must be supplied")

    for device in data["devices"]:
        ensure_device_exists(device)

    existing_alarms = database.get("alarms")
    alarm = Alarm(data).to_dict()
    existing_alarms[alarm["uuid"]] = alarm
    database.update("alarms", existing_alarms)
    return NO_CONTENT


def index():
    pass