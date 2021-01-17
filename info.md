# Home Assistant Generic Climate Integration
  this is a generic climate integration that supports both heater and cooler in the same component so you don't need to add a separate module for them. On the other hand, you can add a humidity sensor to have your room's humidity in your Google Home application.



### Install through HACS:

Add a custom repository in HACS pointed to https://github.com/ee02217/homeassistant-generic-climate

The new integration for generic climate should appear under your integrations tab.

Click Install and restart Home Assistant.

### Install manually:

Copy the contents found in https://github.com/ee02217/homeassistant-generic-climate/tree/master/custom_components/generic_climate/ to your custom_components folder in Home Assistant.

Restart Home Assistant.

### Configuration.yaml

````
climate:
  - platform: generic_climate
    name: Living Room Climate
    heater: switch.livingroom_heater
    cooler: switch.livingroom_cooler
    target_sensor: sensor.livingroom_temperature
    humidity_sensor: sensor.livingroom_humidity
    hot_tolerance: 0

````
