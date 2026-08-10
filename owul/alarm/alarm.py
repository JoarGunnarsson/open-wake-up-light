from owul.mqtt import mqtt_client

import datetime
import threading
import time
import uuid

ALARM_GRACE_PERIOD = 10


class AlarmActions:
    STATE = "state"
    BRIGHTNESS = "brightness"
    GRADUAL_BRIGHTNESS = "gradual_brightness"


def current_time():
    return datetime.datetime.now(tz=datetime.UTC).astimezone()


def next_datetime(current: datetime.datetime, time: str) -> datetime.datetime:
    hour, minute = time.split(":")
    hour = int(hour)
    minute = int(minute)
    new_datetime = current.replace(hour=hour, minute=minute, second=0, microsecond=0, tzinfo=current.tzinfo)
    while new_datetime <= current:
        new_datetime = new_datetime + datetime.timedelta(days=1)
    return new_datetime


class DeviceAction:
    def __init__(self, action: str, params: dict):
        self.action = action
        self.params = params

    def perform_on_device(self, device: str):
        try:
            if self.action == AlarmActions.STATE:
                self._handle_action_state(device)
                return True

            elif self.action == AlarmActions.BRIGHTNESS:
                self._handle_action_brightness(device)
                return True

            elif self.action == AlarmActions.GRADUAL_BRIGHTNESS:
                self._handle_action_gradual_brightness(device)
                # TODO: This should perform a single brightness update, and return 
                # True only if it has been completed.
                return True

            else:
                raise NotImplementedError(f"Action '{self.action}' has not been implemented")
            
        except Exception as e:
            print(f"{e.__class__.__name__}: {e}")
            raise

    def _ensure_params_exist(self, required_params: list[str]):
        for param in required_params:
            if param not in self.params:
                raise ValueError(f"Required parameter '{param} was missing")
            
    def _handle_action_state(self, device: str):
        required_params = ["state"]
        self._ensure_params_exist(required_params)
        
        state = self.params["state"]
        if state == mqtt_client.LightStates.ON:
            mqtt_client.power_on_device(device)

        elif state == mqtt_client.LightStates.OFF:
            mqtt_client.power_off_device(device)

        elif state == mqtt_client.LightStates.TOGGLE:
            mqtt_client.toggle_device(device)

        else:
            raise ValueError(f"Invalid desired state '{state}")

    def _handle_action_brightness(self, device: str):
        required_params = ["brightness"]
        self._ensure_params_exist(required_params)

        brightness = self.params["brightness"]
        mqtt_client.set_device_brightness(device, brightness)

    def _handle_action_gradual_brightness(self, device: str):
        required_params = ["start", "stop", "duration"]
        self._ensure_params_exist(required_params)

        start = float(self.params["start"])
        stop = float(self.params["stop"])
        duration = float(self.params["duration"])
        rate = (stop - start) / duration
        mqtt_client.set_device_brightness(device, start)
        mqtt_client.set_device_gradual_brightness(device, rate)



class Alarm:
    def __init__(self, data: dict):
        self.device = data["device"]
        self.date = data["date"]
        self.device_action = DeviceAction(data["action"], data["params"])
        self.is_active = data.get("is_active", True)
        self.uuid = data.get("uuid", str(uuid.uuid4()))

        self.is_recurring = False
        for value in data["date"]["weekdays"].values():
            if value:
                self.is_recurring = True
                break

        if "next_activation" in data and data["next_activation"] != "":
            self.datetime = datetime.datetime.fromisoformat(data["next_activation"])
        else:
            self.datetime = self.compute_next_datetime()
        self.is_finished = False

    def to_dict(self):
        return {
            "device": self.device,
            "date": self.date,
            "next_activation": str(self.datetime),
            "action": self.device_action.action,
            "params": self.device_action.params,
            "is_active": self.is_active,
            "uuid": self.uuid,
        } 

        
    def has_passed(self):
        return current_time() > self.datetime + datetime.timedelta(seconds=ALARM_GRACE_PERIOD)

    def not_yet_active(self):
        return self.datetime > current_time()
        
    def tick(self):
        print(f"Ticking alarm: {self.to_dict()}", flush=True)
        
        res = self.device_action.perform_on_device(self.device)
        print(f"Res from device: {res}", flush=True)
        self.is_finished |= res

        if self.is_finished:
            print("FINISHED!", flush=True)
            self.finish()

    def finish(self):
        if self.is_recurring:
            self.datetime = self.compute_next_datetime()
        else:
            self.is_active = False
            self.datetime = ""
    
    def compute_next_datetime(self):
        if not self.is_recurring:
            return next_datetime(current_time(), self.date["time"])
        
        pass
