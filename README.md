# open-wake-up-light
An open-source implementation of a wake-up light alarm clock

This project requires an MQTT broker (e.g. Mosquitto), as well as Zigbee2MQTT, in order to communicate with Zigbee devices.

### Zigbee2MQTT configuration
In addition to the files in this repository, some manual configuration of Zigbee2MQTT is needed in `z2m/data/configuration.yaml`. The mqtt server must be set to `mqtt://mosquitto:1883`. Furthermore, if access to the Z2M frontend is desired, the frontend must be enabled, and the base_url set to `/zigbee2mqtt`. An example configuration can be seen below, with certain detail omitted:
```

version: 5
mqtt:
  base_topic: zigbee2mqtt
  server: mqtt://mosquitto:1883
serial:
  ..
advanced:
  log_level: info
  channel: ...
  network_key:
    ...
  pan_id: ...
  ext_pan_id:
    ...
  enable_external_js: false
frontend:
  enabled: true
  port: 8080
  base_url: /zigbee2mqtt
homeassistant:
  enabled: false
devices:
    ...

```


