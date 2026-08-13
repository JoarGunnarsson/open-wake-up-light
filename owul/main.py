from owul.mqtt import mqtt_client
from owul.database.database import database
from owul.alarm import alarm
from owul.api.api import app

import threading
import time

SLEEP_TIME = 1


def update_alarms(alarms: dict):
    for id, alarm_json in alarms.items():
        if not alarm.is_active(alarm_json):
            continue
        
        if alarm.triggers_in_the_future(alarm_json):
            continue

        alarm.tick(alarm_json)
        alarms[id] = alarm_json


def run_alarms():
    alarms = database.get("alarms")
    if alarms is None:
        database.update("alarms", {})
        alarms = {}

    while True:
        alarms = database.get("alarms")
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