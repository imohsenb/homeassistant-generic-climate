"""Config flow for Generic Climate."""

from __future__ import annotations

import voluptuous as vol

from homeassistant import config_entries
from homeassistant.const import (
    CONF_NAME,
    CONF_UNIQUE_ID,
    PRECISION_HALVES,
    PRECISION_TENTHS,
    PRECISION_WHOLE,
)
import homeassistant.helpers.config_validation as cv
from homeassistant.helpers import selector

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
            if unique_id := user_input.get(CONF_UNIQUE_ID):
                await self.async_set_unique_id(unique_id)
                self._abort_if_unique_id_configured()
            return self.async_create_entry(
                title=user_input.get(CONF_NAME, DEFAULT_NAME),
                data=user_input,
            )

        switch_selector = selector.EntitySelector(
            selector.EntitySelectorConfig(domain="switch")
        )
        sensor_selector = selector.EntitySelector(
            selector.EntitySelectorConfig(domain="sensor")
        )

        schema = vol.Schema(
            {
                vol.Optional(CONF_NAME, default=DEFAULT_NAME): cv.string,
                vol.Optional(CONF_UNIQUE_ID): cv.string,
                vol.Required(CONF_HEATER): switch_selector,
                vol.Required(CONF_SENSOR): sensor_selector,
                vol.Optional(CONF_COOLER): switch_selector,
                vol.Optional(CONF_HUMIDITY_SENSOR): sensor_selector,
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
        self._pending_options: dict | None = None

    async def async_step_init(self, user_input=None):
        """Manage the options."""
        if user_input is not None:
            # Normalize empty strings (if any) to None so async_setup_entry
            # doesn't receive invalid entity IDs.
            normalized = {
                key: (value if value not in ("", []) else None)
                for key, value in user_input.items()
            }

            # If unique_id is changed via options, require explicit confirmation.
            # Note: changing unique_id may create a new entity registry entry.
            new_unique_id = normalized.get(CONF_UNIQUE_ID)
            if new_unique_id and new_unique_id != self._config_entry.unique_id:
                self._pending_options = normalized
                return await self.async_step_confirm_unique_id()

            return self.async_create_entry(title="", data=normalized)

        current = {**self._config_entry.data, **self._config_entry.options}

        switch_selector = selector.EntitySelector(
            selector.EntitySelectorConfig(domain="switch")
        )
        sensor_selector = selector.EntitySelector(
            selector.EntitySelectorConfig(domain="sensor")
        )

        schema = vol.Schema(
            {
                vol.Optional(CONF_NAME, default=current.get(CONF_NAME, DEFAULT_NAME)): cv.string,
                vol.Optional(CONF_UNIQUE_ID, default=current.get(CONF_UNIQUE_ID) or self._config_entry.unique_id): cv.string,
                vol.Optional(CONF_HEATER, default=current.get(CONF_HEATER)): switch_selector,
                vol.Optional(CONF_SENSOR, default=current.get(CONF_SENSOR)): sensor_selector,
                vol.Optional(CONF_COOLER, default=current.get(CONF_COOLER)): switch_selector,
                vol.Optional(
                    CONF_HUMIDITY_SENSOR,
                    default=current.get(CONF_HUMIDITY_SENSOR),
                ): sensor_selector,
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
        )

        return self.async_show_form(step_id="init", data_schema=schema)

    async def async_step_confirm_unique_id(self, user_input=None):
        """Confirm changing unique_id."""
        if self._pending_options is None:
            return await self.async_step_init()

        if user_input is not None:
            if user_input.get("confirm") is True:
                new_unique_id = self._pending_options.get(CONF_UNIQUE_ID)
                if new_unique_id and new_unique_id != self._config_entry.unique_id:
                    self.hass.config_entries.async_update_entry(
                        self._config_entry,
                        unique_id=new_unique_id,
                    )

                options = self._pending_options
                self._pending_options = None
                return self.async_create_entry(title="", data=options)

            # Not confirmed; go back to the options form.
            self._pending_options = None
            return await self.async_step_init()

        current_unique_id = self._config_entry.unique_id
        new_unique_id = self._pending_options.get(CONF_UNIQUE_ID)
        schema = vol.Schema({vol.Required("confirm", default=False): cv.boolean})

        return self.async_show_form(
            step_id="confirm_unique_id",
            data_schema=schema,
            description_placeholders={
                "current_unique_id": str(current_unique_id or ""),
                "new_unique_id": str(new_unique_id or ""),
            },
        )
