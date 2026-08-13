from owul.database.database import database
from owul.mqtt import mqtt_client
from owul.alarm import alarm

from flask import Flask, abort, request
import datetime

app = Flask(__name__)


def ensure_device_exists(device):
    existing_devices = mqtt_client.get_devices()
    if device not in existing_devices:
        abort(400, f"Requested device '{device}' does not seem to be paired")


@app.route("/time", methods=["GET"])
def get_time():
    return {"time": str(alarm.current_time())}


@app.route("/devices", methods=["GET"])
def get_devices():
    return {"devices": mqtt_client.get_devices()}


@app.route("/devices/<device>", methods=["PUT"])
def device_state(device):
    ensure_device_exists(device)

    data = request.get_json()
    action = data["action"]
    params = data["params"]
    alarm.do_action_on_device(action, params, device)
    return {}, 200


@app.get("/alarms")
def get_alarms():
    return database.get("alarms", {})


@app.get("/alarms/next_alarm")
def get_next_alarm():
    min_time_left = None
    closest_datetime = None

    current_time = alarm.current_time()
    for alarm_data in database.get("alarms").values():
        if not alarm_data["is_active"]:
            continue

        time_left = alarm.parse_datetime_string(alarm_data["next_activation"]) - current_time
        if time_left < datetime.timedelta(seconds=0):
            print("Something has gone wrong, alarm with next activation in the past is still active", flush=True)
            continue

        if min_time_left is None or time_left < min_time_left:
            min_time_left = time_left
            closest_datetime = alarm_data["next_activation"]

    if min_time_left is not None:
        min_time_left = min_time_left.total_seconds()

    return  {"datetime": closest_datetime, "time_left": min_time_left}


@app.get("/alarms/<id>")
def get_alarm_data(id):
    alarms = database.get("alarms", {})
    if id not in alarms:
        abort(400, "An alarm with that id does not exist")

    return alarms[id]


@app.delete("/alarms/delete/<id>")
def delete_alarm(id):
    alarms = database.get("alarms")
    if id not in alarms:
        abort(400, "An alarm with that id does not exist")

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

    alarm_data = request.get_json()
    existing_alarms = database.get("alarms")
    if alarm_data["is_active"]:
        alarm_data["next_activation"] = alarm.next_alarm_datetime(alarm_data)
    else:
        alarm_data["next_activation"] = ""

    existing_alarms[id] |= alarm_data
    database.update("alarms", existing_alarms)
    return {}, 200


@app.post("/alarms/create")
def create_alarm():
    data = request.get_json()
    if "device" not in data or not isinstance(data["device"], str):
        abort(400, "To create an alarm, a device must be supplied")

    ensure_device_exists(data["device"])

    existing_alarms = database.get("alarms")
    new_alarm = alarm.create_alarm(data)

    time_until_alarm = alarm.time_until_alarm(new_alarm)

    existing_alarms[new_alarm["id"]] = new_alarm
    database.update("alarms", existing_alarms)

    return {"time_left": time_until_alarm}


def index():
    pass