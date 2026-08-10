from owul.database.database import database
from owul.mqtt import mqtt_client
from owul.alarm.alarm import DeviceAction, Alarm, current_time

from flask import Flask, abort, request


app = Flask(__name__)


def ensure_device_exists(device):
    existing_devices = mqtt_client.get_devices()
    if device not in existing_devices:
        abort(400, f"Requested device '{device}' does not seem to be paired")


@app.route("/time", methods=["GET"])
def get_time():
    return {"time": str(current_time())}


@app.route("/devices", methods=["GET"])
def get_devices():
    return {"devices": mqtt_client.get_devices()}


@app.route("/devices/<device>", methods=["PUT"])
def device_state(device):
    ensure_device_exists(device)

    data = request.get_json()
    action = data["action"]
    params = data["params"]
    action = DeviceAction(action, params)
    action.perform_on_device(device)
    return {}, 200


@app.get("/alarms")
def get_alarms():
    return database.get("alarms", {})


@app.get("/alarms/<id>")
def get_alarm_data(id):
    alarms = database.get("alarms", {})
    if id not in alarms:
        abort(400, "An alarm with that uuid does not exits")

    return alarms[id]


@app.delete("/alarms/delete/<id>")
def delete_alarm(id):
    alarms = database.get("alarms")
    if id not in alarms:
        abort(400, "An alarm with that uuid does not exits")

    # If an alarm is already active, this will not turn it off
    del alarms[id]
    database.update("alarms", alarms)
    return {}, 200


@app.put("/alarms/update/<id>")
def update_alarm(id):
    # TODO: Perhaps always set it to active when updating it?
    alarms = database.get("alarms")
    if id not in alarms:
        abort(400, "Cannot set the alarm state of a non-existent alarm")

    data = request.get_json()
    existing_alarms = database.get("alarms")
    alarm = Alarm(data)
    alarm_data = alarm.to_dict()
    alarm_data["uuid"] = id
    existing_alarms[id] = alarm_data
    database.update("alarms", existing_alarms)
    return {}, 200


@app.post("/alarms/create")
def create_alarm():
    data = request.get_json()
    if "device" not in data or not isinstance(data["device"], str):
        abort(400, "To create an alarm, a device must be supplied")

    ensure_device_exists(data["device"])

    existing_alarms = database.get("alarms")
    alarm = Alarm(data)
    time_until_alarm = str(alarm.datetime -  current_time())
    alarm_data = alarm.to_dict()
    existing_alarms[alarm_data["uuid"]] = alarm_data
    database.update("alarms", existing_alarms)
    return {"time_left": time_until_alarm}


def index():
    pass