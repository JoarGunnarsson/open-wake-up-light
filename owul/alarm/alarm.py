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


class DeviceAction:
    def __init__(self, action: str, params: dict):
        self.action = action
        self.params = params

    def perform_on_device(self, device: str):
        try:
            if self.action == AlarmActions.STATE:
                self._handle_action_state(device)

            elif self.action == AlarmActions.BRIGHTNESS:
                self._handle_action_brightness(device)

            elif self.action == AlarmActions.GRADUAL_BRIGHTNESS:
                self._handle_action_gradual_brightness(device)

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

        self.data = data
        self.devices = data["devices"]
        self.date = data["date"]
        self.device_action = DeviceAction(data["action"], data["params"])
        self.is_active = data["is_active"]
        self.is_finished = data["is_finished"]
        self.uuid = data.get("uuid", str(uuid.uuid4()))

        alarm_datetime = datetime.datetime.fromisoformat(self.date)
        self.timestamp = (alarm_datetime - datetime.datetime(1970,1,1, tzinfo=datetime.timezone.utc)) / datetime.timedelta(seconds=1)

    def to_dict(self):
        return {
            "devices": self.devices,
            "date": self.date,
            "action": self.device_action.action,
            "params": self.device_action.params,
            "is_active": self.is_active,
            "is_finished": self.is_finished,
            "uuid": self.uuid,
        }
        
    def has_passed(self):
        return self.is_finished or time.time() > self.timestamp + ALARM_GRACE_PERIOD

    def not_yet_active(self):
        return self.timestamp > time.time()

    def start(self):
        self.data["is_active"] = True
        thread = threading.Thread(target=self.run, daemon=True)
        thread.start()
        
    def run(self):
        for device in self.devices:
            self.device_action.perform_on_device(device)
        
        self.shutdown()

    def shutdown(self):
        self.data["is_active"] = False
        self.data["is_finished"] = True
        self.is_finished = True
