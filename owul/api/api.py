from owul.database.database import database
from owul.mqtt import mqtt_client
from owul.alarm import alarm

from flask import Flask, abort, request
from flask_restx import Api, Namespace, Resource, fields

import datetime
import time


app = Flask(__name__)

api = Api(app)
ns = Namespace('')


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


action_params_model = api.model(
    'ActionParams', 
    {
        'state': fields.String(enum=["ON", "OFF", "TOGGLE"]),
        'brightness': fields.Integer(),
        'start_brightness': fields.Integer(),
        'stop_brightness': fields.Integer(),    
    }, strict=True
)

action_field = fields.String(
    enum=[alarm.AlarmActions.STATE, alarm.AlarmActions.BRIGHTNESS, alarm.AlarmActions.GRADUAL_BRIGHTNESS],
    required=True
)

device_control_model = api.model(
    'DeviceControl', 
    {
        'action': action_field,
        'params': fields.Nested(action_params_model, required=True)
    }, strict=True
)

@api.route("/devices/<device>")
class ControlDevice(Resource):
    @api.expect(device_control_model, validate=True)
    def put(self, device):
        ensure_device_exists(device)

        data = request.get_json()
        action = data["action"]
        params = data["params"]
        if action == alarm.AlarmActions.GRADUAL_BRIGHTNESS:
            abort(400, "Device control does not support gradual_brightness")

        while not alarm.do_action_on_device(action, params, device, None):
            time.sleep(alarm.SLEEP_TIME)
    
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


weekday_field_model = api.model(
    'Weekday', 
    {
        'day': fields.String(required=True),
        'value': fields.Boolean(required=True),
    }, strict=True
)

date_data_model = api.model(
    'Date',
    {
        'time': fields.String(required=True),
        'weekdays': fields.List(fields.Nested(weekday_field_model, required=True))
    }, strict=True
)

new_alarm_model = api.model(
    'AlarmCreation', 
    {
        'name': fields.String(required = True),
        'device': fields.String(required = True),
        'action': action_field,
        'params': fields.Nested(action_params_model, required=True),
        'is_active': fields.Boolean(required=True),
        'date': fields.Nested(date_data_model, required=True),
        'minutes_before': fields.Integer(required = True),
    }, strict=True
)

complete_alarm_model = api.model(
    'Alarm', 
    {
        'name': fields.String(required = True),
        'device': fields.String(required = True),
        'action': fields.String(required = True),
        'params': fields.Nested(action_params_model, required=True),
        'is_active': fields.Boolean(required=True),
        'date': fields.Nested(date_data_model, required=True),
        'minutes_before': fields.Integer(required = True),
        'next_activation': fields.String(required=True),
        "id": fields.String(required=True),
    }, strict=True
)

@api.route("/alarms/update/<alarm_id>")
class AlarmEdit(Resource):
    @api.expect(complete_alarm_model, validate=True)
    def put(self, alarm_id):
        # TODO: Perhaps always set it to active when updating it?
        alarms = database.get("alarms")
        if alarm_id not in alarms:
            abort(400, "Cannot set the alarm state of a non-existent alarm")

        alarm_data = request.get_json()
        existing_alarms = database.get("alarms")
        if alarm_data["is_active"]:
            alarm_data["next_activation"] = alarm.next_alarm_datetime(alarm_data)
        else:
            alarm_data["next_activation"] = ""

        existing_alarms[alarm_id] |= alarm_data
        database.update("alarms", existing_alarms)
        return {}, 200


@api.route("/alarms/create")
class AlarmCreation(Resource):
    @api.expect(new_alarm_model, validate=True)
    def post(self):
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
