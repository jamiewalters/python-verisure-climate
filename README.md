# Access Verisure HeatPumps in HomeAssistant

NB! This component does not work as it should and is work under progress. Feel free to test it and if you are capable to sort out the problems you are more than welcome to help out.

After HA Climate 1.0-change refactoring work needs to be done.
This is a custom component made by https://github.com/jamiewalters/ for exposing heatpumps through Verisure as climate components in homeassistant.
This is based on the vsure python lib developed at: https://github.com/persandstrom/python-verisure

## Installation 

To install this component:

- Copy the files in this repository to your /config/custom_components/verisureclimate
- Add verisureclimate to HASS configuration as shown:
    <pre>climate:
      - platform: verisureclimate
        username: *username*
        password: *password*
    </pre>
- Restart homeassistant


### Legal Disclaimer
This software is not affiliated with Verisure Holding AB and the developers take no legal responsibility for the functionality or security of your Verisure Alarms and devices.
