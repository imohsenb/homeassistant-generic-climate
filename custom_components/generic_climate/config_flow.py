"""Config flow for Generic Climate."""

from __future__ import annotations

import voluptuous as vol

from homeassistant import config_entries
from homeassistant.const import (
    CONF_NAME,
    PRECISION_HALVES,
    PRECISION_TENTHS,
    PRECISION_WHOLE,
)
import homeassistant.helpers.config_validation as cv

from .climate import (
    CONF_AWAY_TEMP,
    CONF_COLD_TOLERANCE,
    CONF_COOLER,
    CONF_HEATER,
    CONF_HOT_TOLERANCE,
    CONF_HUMIDITY_SENSOR,
    CONF_INITIAL_HVAC_MODE,
    CONF_KEEP_ALIVE,
    CONF_MAX_TEMP,
    CONF_MIN_DUR,
    CONF_MIN_TEMP,
    CONF_PRECISION,
    CONF_SENSOR,
    CONF_TARGET_TEMP,
    DEFAULT_NAME,
    DEFAULT_TOLERANCE,
)
from . import DOMAIN


class GenericClimateConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    """Handle a config flow for Generic Climate."""

    VERSION = 1

    async def async_step_user(self, user_input=None):
        """Handle the initial step."""
        errors: dict[str, str] = {}

        if user_input is not None:
            return self.async_create_entry(
                title=user_input.get(CONF_NAME, DEFAULT_NAME),
                data=user_input,
            )

        schema = vol.Schema(
            {
                vol.Optional(CONF_NAME, default=DEFAULT_NAME): cv.string,
                vol.Required(CONF_HEATER): cv.entity_id,
                vol.Required(CONF_SENSOR): cv.entity_id,
                vol.Optional(CONF_COOLER): cv.entity_id,
                vol.Optional(CONF_HUMIDITY_SENSOR): cv.entity_id,
                vol.Optional(CONF_MIN_TEMP): vol.Coerce(float),
                vol.Optional(CONF_MAX_TEMP): vol.Coerce(float),
                vol.Optional(CONF_TARGET_TEMP): vol.Coerce(float),
                vol.Optional(CONF_AWAY_TEMP): vol.Coerce(float),
                vol.Optional(CONF_COLD_TOLERANCE, default=DEFAULT_TOLERANCE): vol.Coerce(
                    float
                ),
                vol.Optional(CONF_HOT_TOLERANCE, default=DEFAULT_TOLERANCE): vol.Coerce(
                    float
                ),
                vol.Optional(CONF_MIN_DUR): cv.positive_time_period,
                vol.Optional(CONF_KEEP_ALIVE): cv.positive_time_period,
                vol.Optional(CONF_INITIAL_HVAC_MODE): vol.In(
                    ["off", "heat", "cool"]
                ),
                vol.Optional(CONF_PRECISION): vol.In(
                    [PRECISION_TENTHS, PRECISION_HALVES, PRECISION_WHOLE]
                ),
            }
        )

        return self.async_show_form(step_id="user", data_schema=schema, errors=errors)

    @staticmethod
    def async_get_options_flow(config_entry):
        """Get the options flow for this handler."""
        return GenericClimateOptionsFlow(config_entry)


class GenericClimateOptionsFlow(config_entries.OptionsFlow):
    """Handle an options flow for Generic Climate."""

    def __init__(self, config_entry: config_entries.ConfigEntry) -> None:
        self._config_entry = config_entry

    async def async_step_init(self, user_input=None):
        """Manage the options."""
        if user_input is not None:
            # Normalize empty strings (if any) to None so async_setup_entry
            # doesn't receive invalid entity IDs.
            normalized = {
                key: (value if value not in ("", []) else None)
                for key, value in user_input.items()
            }
            return self.async_create_entry(title="", data=normalized)

        current = {**self._config_entry.data, **self._config_entry.options}

        schema_dict: dict[vol.Marker, object] = {
            vol.Optional(CONF_NAME, default=current.get(CONF_NAME, DEFAULT_NAME)): cv.string,
            # Required in the base entry; keeping editable.
            vol.Optional(CONF_HEATER, default=current.get(CONF_HEATER)): cv.entity_id,
            vol.Optional(CONF_SENSOR, default=current.get(CONF_SENSOR)): cv.entity_id,
            vol.Optional(CONF_MIN_TEMP, default=current.get(CONF_MIN_TEMP)): vol.Coerce(float),
            vol.Optional(CONF_MAX_TEMP, default=current.get(CONF_MAX_TEMP)): vol.Coerce(float),
            vol.Optional(CONF_TARGET_TEMP, default=current.get(CONF_TARGET_TEMP)): vol.Coerce(float),
            vol.Optional(CONF_AWAY_TEMP, default=current.get(CONF_AWAY_TEMP)): vol.Coerce(float),
            vol.Optional(
                CONF_COLD_TOLERANCE,
                default=current.get(CONF_COLD_TOLERANCE, DEFAULT_TOLERANCE),
            ): vol.Coerce(float),
            vol.Optional(
                CONF_HOT_TOLERANCE,
                default=current.get(CONF_HOT_TOLERANCE, DEFAULT_TOLERANCE),
            ): vol.Coerce(float),
            vol.Optional(CONF_MIN_DUR, default=current.get(CONF_MIN_DUR)): cv.positive_time_period,
            vol.Optional(CONF_KEEP_ALIVE, default=current.get(CONF_KEEP_ALIVE)): cv.positive_time_period,
            vol.Optional(
                CONF_INITIAL_HVAC_MODE,
                default=current.get(CONF_INITIAL_HVAC_MODE),
            ): vol.In(["off", "heat", "cool"]),
            vol.Optional(CONF_PRECISION, default=current.get(CONF_PRECISION)): vol.In(
                [PRECISION_TENTHS, PRECISION_HALVES, PRECISION_WHOLE]
            ),
        }

        if current.get(CONF_COOLER):
            schema_dict[vol.Optional(CONF_COOLER, default=current.get(CONF_COOLER))] = cv.entity_id
        else:
            schema_dict[vol.Optional(CONF_COOLER)] = cv.entity_id

        if current.get(CONF_HUMIDITY_SENSOR):
            schema_dict[
                vol.Optional(
                    CONF_HUMIDITY_SENSOR,
                    default=current.get(CONF_HUMIDITY_SENSOR),
                )
            ] = cv.entity_id
        else:
            schema_dict[vol.Optional(CONF_HUMIDITY_SENSOR)] = cv.entity_id

        schema = vol.Schema(schema_dict)

        return self.async_show_form(step_id="init", data_schema=schema)
