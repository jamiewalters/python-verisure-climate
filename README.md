# Access Verisure HeatPumps in HomeAssistant

This is a custom component for exposing heatpumps through Verisure as climate components in homeassistant.
This is based on the vsure python lib developed at: https://github.com/persandstrom/python-verisure

## Installation 

To install this component:

- Copy the files in this repository to your /config/custom_components/climate
- Add verisureclimate to HASS configuration as shown:
    <pre>climate:
      - platform: verisureclimate
        username: *username*
        password: *password*
    </pre>
- Restart homeassistant


### Legal Disclaimer
This software is not affiliated with Verisure Holding AB and the developers take no legal responsibility for the functionality or security of your Verisure Alarms and devices.
