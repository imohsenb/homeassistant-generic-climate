# Home Assistant Generic Climate Integration
  this is a generic climate integration that supports both heater and cooler in the same component so you don't need to add a separate module for them. Besides that, you can add a humidity sensor to have your room's humidity in your Google Home application.
<p align="center">
<img src="https://github.com/imohsenb/homeassistant-generic-climate/raw/images/generic_climate_google_home_cooler.jpeg" alt="Google Home Cooler mode" width="200"/>
<img src="https://github.com/imohsenb/homeassistant-generic-climate/raw/images/generic_climate_google_home_heater.jpeg" alt="Google Home Heater Mode" width="200"/>
<img src="https://github.com/imohsenb/homeassistant-generic-climate/raw/images/generic_climate_google_home_mode.jpeg" alt="Google Home Select Mode" width="200"/>
</p>

### Install through HACS:

Add a custom repository in HACS pointed to https://github.com/imohsenb/homeassistant-generic-climate

The new integration for generic climate should appear under your integrations tab.

Click Install and restart Home Assistant.

### Install manually:

Copy the contents found in https://github.com/imohsenb/homeassistant-generic-climate/tree/master/custom_components/generic_climate/ to your custom_components folder in Home Assistant.

Restart Home Assistant.

### Configuration.yaml

This integration now supports UI configuration (Settings → Devices & services → Add integration → "Generic Climate").

Legacy YAML configuration is still supported:

````
climate:
  - platform: generic_climate
    name: Living Room Climate
    unique_id: living_room_generic_climate
    heater: switch.livingroom_heater
    cooler: switch.livingroom_cooler
    target_sensor: sensor.livingroom_temperature
    humidity_sensor: sensor.livingroom_humidity
    hot_tolerance: 0

````

### Gift
If you would like to have a charming [Climate thermostat card](https://github.com/imohsenb/homeassistant-climate-card), please take a look at my custom card:
<p align="center">
<img src="https://github.com/imohsenb/homeassistant-climate-card/raw/images/cooling.gif" alt="Google Home Cooler mode" width="400"/>
<img src="https://github.com/imohsenb/homeassistant-climate-card/raw/images/heating.gif" alt="Google Home Heater Mode" width="400"/>
</p>


### Notes
- This component is a fork of the mainline `generic_thermostat`.