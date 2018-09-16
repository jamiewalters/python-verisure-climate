from homeassistant.components.climate import (
    ClimateDevice,
    SUPPORT_TARGET_TEMPERATURE, SUPPORT_FAN_MODE,
    SUPPORT_OPERATION_MODE, SUPPORT_SWING_MODE,
    SUPPORT_ON_OFF)
from homeassistant.const import TEMP_CELSIUS, ATTR_TEMPERATURE
from homeassistant.util import Throttle
from datetime import timedelta
import logging
from .verisure import Session
import jsonpath

jsonpath = jsonpath.jsonpath
session = Session('username', 'password')
_LOGGER = logging.getLogger(__name__)


def setup_platform(hass, config, add_entities, discovery_info=None):
    """Set up the Demo climate devices."""
    session.login()
    heat_pumps = jsonpath(session.get_overview(), '$.heatPumps')
    for heat_pump in heat_pumps:
        device_label = jsonpath(heat_pump[0], '$.deviceLabel')[0]
        _LOGGER.debug(device_label)
        add_entities([
            HeatPump(device_label)
        ])


class HeatPump(ClimateDevice):
    """Representation of a demo climate device."""

    def __init__(self, heatpumpid):
        """Initialize the climate device."""

        self.id = heatpumpid
        self.heatpumpstate = session.get_heat_pump_state(self.id)

        self._name = jsonpath(self.heatpumpstate, '$.area')[0]
        self._support_flags = SUPPORT_TARGET_TEMPERATURE | SUPPORT_FAN_MODE |\
            SUPPORT_OPERATION_MODE | SUPPORT_ON_OFF | SUPPORT_SWING_MODE
        self._target_temperature = jsonpath(self.heatpumpstate, '$.heatPumpConfig.targetTemperature')[0]
        self._unit_of_measurement = TEMP_CELSIUS
        self._current_temperature = jsonpath(self.heatpumpstate, '$.latestClimateSample.temperature')[0]
        self._current_fan_mode = jsonpath(self.heatpumpstate, '$.heatPumpConfig.fanSpeed')[0]
        self._current_operation = jsonpath(self.heatpumpstate, '$.heatPumpConfig.mode')[0]
        self._current_swing_mode = jsonpath(self.heatpumpstate, '$.heatPumpConfig.airSwingDirection.vertical')[0]
        self._fan_list = ['AUTO', 'LOW', 'MEDIUM_LOW', 'MEDIUM', 'MEDIUM_HIGH', 'HIGH']
        self._operation_list = ['HEAT', 'COOL', 'FAN', 'AUTO', 'DRY']
        self._swing_list = ['AUTO', '0_DEGREES', '30_DEGREES', '60_DEGREES', '90_DEGREES']
        self._on = True if jsonpath(self.heatpumpstate, '$.heatPumpConfig.power')[0] == 'ON' else False

    @property
    def supported_features(self):
        """Return the list of supported features."""
        return self._support_flags

    @property
    def should_poll(self):
        """Return the polling state."""
        return False

    @property
    def name(self):
        """Return the name of the climate device."""
        return self._name

    @property
    def temperature_unit(self):
        """Return the unit of measurement."""
        return self._unit_of_measurement

    @property
    def current_temperature(self):
        """Return the current temperature."""
        self._current_temperature = jsonpath(self.heatpumpstate, '$.latestClimateSample.temperature')[0]
        return self._current_temperature

    @property
    def target_temperature(self):
        """Return the temperature we try to reach."""
        self._target_temperature = jsonpath(self.heatpumpstate, '$.heatPumpConfig.targetTemperature')[0]
        return self._target_temperature

    @property
    def current_operation(self):
        """Return current operation ie. heat, cool, idle."""
        self._current_operation = jsonpath(self.heatpumpstate, '$.heatPumpConfig.mode')[0]
        return self._current_operation

    @property
    def operation_list(self):
        """Return the list of available operation modes."""
        return self._operation_list

    @property
    def is_on(self):
        """Return true if the device is on."""
        on_state = jsonpath(self.heatpumpstate, '$.heatPumpConfig.power')[0]
        if on_state == 'ON':
            self._on = True
        else:
            self._on = False

        return self._on

    @property
    def current_fan_mode(self):
        """Return the fan setting."""
        self._current_fan_mode = jsonpath(self.heatpumpstate, '$.heatPumpConfig.fanSpeed')[0]
        return self._current_fan_mode

    @property
    def fan_list(self):
        """Return the list of available fan modes."""
        return self._fan_list

    def set_temperature(self, **kwargs):
        """Set new target temperatures."""
        if kwargs.get(ATTR_TEMPERATURE) is not None:
            self._target_temperature = kwargs.get(ATTR_TEMPERATURE)
            self.session.set_heat_pump_target_temperature(self.id, self._target_temperature)
        self.schedule_update_ha_state()

    def set_swing_mode(self, swing_mode):
        """Set new swing setting."""
        self.session.set_heat_pump_airswingdirection(self.id, swing_mode)
        self._current_swing_mode = swing_mode
        self.schedule_update_ha_state()

    def set_fan_mode(self, fan_mode):
        """Set new target temperature."""
        self.session.set_heat_pump_fan_speed(self.id, fan_mode)
        self._current_fan_mode = fan_mode
        self.schedule_update_ha_state()

    def set_operation_mode(self, operation_mode):
        """Set new target temperature."""
        self.session.set_heat_pump_mode(self.id, operation_mode)
        self._current_operation = operation_mode
        self.schedule_update_ha_state()

    @property
    def current_swing_mode(self):
        """Return the swing setting."""
        self._current_swing_mode = jsonpath(self.heatpumpstate, '$.heatPumpConfig.airSwingDirection.vertical')[0]
        return self._current_swing_mode

    @property
    def swing_list(self):
        """List of available swing modes."""
        return self._swing_list

    def turn_on(self):
        """Turn on."""
        self.session.set_heat_pump_power(self.id, 'ON')
        self._on = True
        self.schedule_update_ha_state()

    def turn_off(self):
        """Turn off."""
        self.session.set_heat_pump_power(self.id, 'OFF')
        self._on = False
        self.schedule_update_ha_state()

    @Throttle(timedelta(seconds=5))
    def update(self):
        self.state = self.session.get_heat_pump_state(self.id)
