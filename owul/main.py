from owul.mqtt import mqtt_client
from owul.database.database import database
from owul.alarm.alarm import Alarm
from owul.api.api import app

import threading
import time

SLEEP_TIME = 1


def update_alarms(alarms: dict):
    for id, alarm_json in alarms.copy().items():
        alarm = Alarm(alarm_json)
        if alarm.is_active:
            continue

        if alarm.has_passed():
            print("Alarm has passed, removing it")
            del alarms[id]
            continue

        if alarm.not_yet_active():
            continue

        print("Starting the alarm!")
        alarm.start()


def run_alarms():
    alarms = database.get("alarms")
    if alarms is None:
        database.update("alarms", {})
        alarms = {}

    while True:
        current_time = time.monotonic()
        desired_wake_time = current_time + SLEEP_TIME

        update_alarms(alarms)
        database.update("alarms", alarms)

        time.sleep(max(0, desired_wake_time - time.monotonic()))


def main():
    devices = mqtt_client.get_devices()
    print(f"Found the following paired devices: {devices}")

    alarm_thread = threading.Thread(target=run_alarms, daemon=True)
    alarm_thread.start()

    app.run(host="0.0.0.0", port=9000)