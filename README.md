# Home Assistant Generic Climate Integration
  this is a generic climate integration that supports both heater and cooler in the same component so you don't need to add a separate module for them. On the other hand, you can add a humidity sensor to have your room's humidity in your Google Home application.

![GoogleHomeCooler](https://github.com/imohsenb/homeassistant-generic-climate/raw/images/generic_climate_google_home_cooler.jpeg)
![GoogleHomeHeater](https://github.com/imohsenb/homeassistant-generic-climate/raw/images/generic_climate_google_home_heater.jpeg)
![GoogleHomeMode](https://github.com/imohsenb/homeassistant-generic-climate/raw/images/generic_climate_google_home_mode.jpeg)

### Install through HACS:

Add a custom repository in HACS pointed to https://github.com/imohsenb/homeassistant-generic-climate

The new integration for generic climate should appear under your integrations tab.

Click Install and restart Home Assistant.

### Install manually:

Copy the contents found in https://github.com/imohsenb/homeassistant-generic-climate/tree/master/custom_components/generic_climate/ to your custom_components folder in Home Assistant.

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