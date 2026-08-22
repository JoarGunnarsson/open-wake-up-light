from owul.mqtt import mqtt_client

import datetime
import uuid

ALARM_GRACE_PERIOD = 10
SLEEP_TIME = 1

class AlarmActions:
    STATE = "state"
    BRIGHTNESS = "brightness"
    GRADUAL_BRIGHTNESS = "gradual_brightness"


def current_time():
    return datetime.datetime.now(tz=datetime.UTC).astimezone()


def next_datetime(current: datetime.datetime, time: str, weekdays: list[int] | None) -> datetime.datetime:
    hour, minute = time.split(":")
    hour = int(hour)
    minute = int(minute)
    new_datetime = current.replace(hour=hour, minute=minute, second=0, microsecond=0, tzinfo=current.tzinfo)
    while True:
        if new_datetime > current:
            if not weekdays:
                break

            if new_datetime.weekday() in weekdays:
                break

        new_datetime = new_datetime + datetime.timedelta(days=1)
    return new_datetime


def do_action_on_device(action: str, params: dict, device: str, percent: float | None = None) -> bool:
    try:
        if action == AlarmActions.STATE:
            _handle_action_state(params, device)
            return True

        elif action == AlarmActions.BRIGHTNESS:
            _handle_action_brightness(params, device)
            return True

        elif action == AlarmActions.GRADUAL_BRIGHTNESS:
            return _handle_action_gradual_brightness(params, device, percent)
            # TODO: This should perform a single brightness update, and return 
            # True only if it has been completed.

        else:
            raise NotImplementedError(f"Action '{action}' has not been implemented")
        
    except Exception as e:
        print(f"{e.__class__.__name__}: {e}")
        raise


def _ensure_params_exist(params: dict, required_params: list[str]):
    for param in required_params:
        if param not in params:
            raise ValueError(f"Required parameter '{param} was missing")

        
def _handle_action_state(params: dict, device: str):
    required_params = ["state"]
    _ensure_params_exist(params, required_params)
    
    state = params["state"]
    if state == mqtt_client.LightStates.ON:
        mqtt_client.power_on_device(device)

    elif state == mqtt_client.LightStates.OFF:
        mqtt_client.power_off_device(device)

    elif state == mqtt_client.LightStates.TOGGLE:
        mqtt_client.toggle_device(device)

    else:
        raise ValueError(f"Invalid desired state '{state}")


def _handle_action_brightness(params: dict, device: str):
    required_params = ["brightness"]
    _ensure_params_exist(params, required_params)

    brightness = params["brightness"]
    mqtt_client.set_device_brightness(device, brightness)


def _handle_action_gradual_brightness(params, device: str, percent: float | None):
    required_params = ["start_brightness", "stop_brightness"]
    _ensure_params_exist(params, required_params)

    # TODO: start == 0 will turns off the light and does not set the gradual brightness.
    # Perhaps sleep here, or wait until the bulb has updated its status
    if percent is None:
        percent = 0

    start_brightness = params["start_brightness"]
    stop_brightness = params["stop_brightness"]

    current_brightness = (stop_brightness - start_brightness) * percent + start_brightness
    current_brightness = min(stop_brightness, current_brightness)

    mqtt_client.set_device_brightness(device, current_brightness)
    return current_brightness >= stop_brightness


def parse_datetime_string(time_str: str) -> datetime.datetime:
    return datetime.datetime.fromisoformat(time_str)


def is_active(alarm: dict) -> bool:
    return alarm["is_active"]


def tick(alarm: dict):
    next_activaton = alarm["next_activation"]
    if not next_activaton:
        return alarm

    minutes_before = alarm.get("minutes_before", None) 
    minutes_before = int(minutes_before) if minutes_before is not None else 0
    time_for_first_action = parse_datetime_string(next_activaton) - datetime.timedelta(minutes=minutes_before) 

    if time_for_first_action > current_time():
        return alarm

    if current_time() > parse_datetime_string(next_activaton) + datetime.timedelta(seconds=ALARM_GRACE_PERIOD):
        print(f"Alarm has passed, and is more than {ALARM_GRACE_PERIOD} seconds old")
        return finish_alarm(alarm)

    if minutes_before == 0:
        percent = 1 if current_time() > time_for_first_action else 0
    else:
        percent = (current_time() - time_for_first_action).total_seconds() / (60 * minutes_before)
        
    print(f"percent: {percent}", flush=True)
    if percent > 1:
        print("Larger than 100 percent!... Current time is probably after next_activation...")
        
    is_finished = do_action_on_device(alarm["action"], alarm["params"], alarm["device"], percent)
    print(f"Result from device: {is_finished}", flush=True)

    if is_finished:
        print("Alarm was finished!", flush=True)
        alarm = finish_alarm(alarm)

    return alarm


def check_recurring(alarm: dict) -> bool:
    for weekday in alarm["date"]["weekdays"]:
        if weekday["value"]:
            return True

    return False


def finish_alarm(alarm: dict) -> dict:
    is_recurring = check_recurring(alarm)
    if is_recurring:
        alarm["next_activation"] = next_alarm_datetime(alarm)
    else:
        alarm["is_active"] = False
        alarm["next_activation"] = ""

    return alarm


def next_alarm_datetime(alarm: dict) -> str:
    if not check_recurring(alarm):
        return str(next_datetime(current_time(), alarm["date"]["time"], None))

    # TODO: Compute it by checking weekdays
    weekdays = []
    for weekday, day in enumerate(alarm["date"]["weekdays"]):
        if day["value"]:
            weekdays.append(weekday)

    return str(next_datetime(current_time(), alarm["date"]["time"], weekdays))


def time_until_alarm(alarm: dict) -> str:
    next_activation = parse_datetime_string(alarm["next_activation"])
    return str(next_activation -  current_time())


def create_alarm(data: dict) -> dict:
    data["id"] = str(uuid.uuid4())
    data["next_activation"] = next_alarm_datetime(data)
    return data
