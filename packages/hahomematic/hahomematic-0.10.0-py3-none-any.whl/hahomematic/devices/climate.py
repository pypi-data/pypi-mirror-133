"""Code to create the required entities for thermostat devices."""
from __future__ import annotations

from datetime import datetime, timedelta
import logging
from typing import Any

from hahomematic.const import ATTR_HM_MAX, ATTR_HM_MIN, HmPlatform
import hahomematic.device as hm_device
from hahomematic.devices.entity_definition import (
    FIELD_ACTIVE_PROFILE,
    FIELD_AUTO_MODE,
    FIELD_BOOST_MODE,
    FIELD_COMFORT_MODE,
    FIELD_CONTROL_MODE,
    FIELD_HEATING_COOLING,
    FIELD_HUMIDITY,
    FIELD_LOWERING_MODE,
    FIELD_MANU_MODE,
    FIELD_PARTY_MODE,
    FIELD_SET_POINT_MODE,
    FIELD_SETPOINT,
    FIELD_TEMPERATURE,
    EntityDefinition,
    make_custom_entity,
)
import hahomematic.entity as hm_entity
from hahomematic.entity import CustomEntity

_LOGGER = logging.getLogger(__name__)

HM_MODE_AUTO = 0
HM_MODE_MANU = 1
HM_MODE_AWAY = 2
HM_MODE_BOOST = 3
HMIP_SET_POINT_MODE_AUTO = 0
HMIP_SET_POINT_MODE_MANU = 1
HMIP_SET_POINT_MODE_AWAY = 2

ATTR_TEMPERATURE = "temperature"
HVAC_MODE_OFF = "off"
HVAC_MODE_HEAT = "heat"
HVAC_MODE_AUTO = "auto"
HVAC_MODE_COOL = "cool"
PARTY_INIT_DATE = "2000_01_01 00:00"
PARTY_DATE_FORMAT = "%Y_%m_%d %H:%M"
PRESET_NONE = "none"
PRESET_AWAY = "away"
PRESET_BOOST = "boost"
PRESET_COMFORT = "comfort"
PRESET_ECO = "eco"
TEMP_CELSIUS = "°C"
SUPPORT_TARGET_TEMPERATURE = 1
SUPPORT_PRESET_MODE = 16

HEATING_PROFILES = {"Profile 1": 1, "Profile 2": 2, "Profile 3": 3}
COOLING_PROFILES = {"Profile 4": 4, "Profile 5": 5, "Profile 6": 6}
HM_MIN_VALUE = 4.5
HM_MAX_VALUE = 30.5


class BaseClimateEntity(CustomEntity):
    """Base HomeMatic climate entity."""

    def __init__(
        self,
        device: hm_device.HmDevice,
        device_address: str,
        unique_id: str,
        device_enum: EntityDefinition,
        device_def: dict[str, Any],
        entity_def: dict[str, Any],
        channel_no: int,
    ):
        super().__init__(
            device=device,
            unique_id=unique_id,
            device_address=device_address,
            device_enum=device_enum,
            device_def=device_def,
            entity_def=entity_def,
            platform=HmPlatform.CLIMATE,
            channel_no=channel_no,
        )
        _LOGGER.debug(
            "ClimateEntity.__init__(%s, %s, %s)",
            self._device.interface_id,
            device_address,
            unique_id,
        )

    @property
    def _humidity(self) -> int | None:
        """Return the humidity of the device."""
        return self._get_entity_state(FIELD_HUMIDITY)

    @property
    def _setpoint(self) -> float | None:
        """Return the setpoint of the device."""
        return self._get_entity_state(FIELD_SETPOINT)

    @property
    def _temperature(self) -> float | None:
        """Return the temperature of the device."""
        return self._get_entity_state(FIELD_TEMPERATURE)

    @property
    def temperature_unit(self) -> str:
        """Return temperature unit."""
        return TEMP_CELSIUS

    @property
    def min_temp(self) -> float:
        """Return the minimum temperature."""
        return self._get_entity_attribute(
            FIELD_SETPOINT, ATTR_HM_MIN.lower(), HM_MIN_VALUE
        )

    @property
    def max_temp(self) -> float:
        """Return the maximum temperature."""
        return self._get_entity_attribute(
            FIELD_SETPOINT, ATTR_HM_MAX.lower(), HM_MAX_VALUE
        )

    @property
    def target_temperature_step(self) -> float:
        """Return the supported step of target temperature."""
        return 0.5

    @property
    def current_humidity(self) -> int | None:
        """Return the current humidity."""
        return self._humidity

    @property
    def current_temperature(self) -> float | None:
        """Return current temperature."""
        return self._temperature

    @property
    def target_temperature(self) -> float | None:
        """Return target temperature."""
        return self._setpoint

    @property
    def preset_mode(self) -> str:
        """Return the current preset mode."""
        return PRESET_NONE

    @property
    def preset_modes(self) -> list[str]:
        """Return available preset modes."""
        return [PRESET_NONE]

    @property
    def hvac_mode(self) -> str:
        """Return hvac operation mode."""
        return HVAC_MODE_AUTO

    @property
    def hvac_modes(self) -> list[str]:
        """Return the list of available hvac operation modes."""
        return [HVAC_MODE_AUTO]

    @property
    def supported_features(self) -> int:
        """Return the list of supported features."""
        return SUPPORT_TARGET_TEMPERATURE

    async def set_temperature(self, **kwargs: Any) -> None:
        """Set new target temperature."""
        temperature = kwargs.get(ATTR_TEMPERATURE)
        if temperature is None:
            return None
        await self._send_value(FIELD_SETPOINT, float(temperature))

    # pylint: disable=no-self-use
    async def set_hvac_mode(self, hvac_mode: str) -> None:
        """Set new target hvac mode."""
        return None

    # pylint: disable=no-self-use
    async def set_preset_mode(self, preset_mode: str) -> None:
        """Set new preset mode."""
        return None

    async def enable_away_mode_by_calendar(
        self, start: datetime, end: datetime, away_temperature: float
    ) -> None:
        """Enable the away mode by calendar on thermostat."""
        return None

    async def enable_away_mode_by_duration(
        self, hours: int, away_temperature: float
    ) -> None:
        """Enable the away mode by duration on thermostat."""
        return None

    async def disable_away_mode(self) -> None:
        """Disable the away mode on thermostat."""
        return None

    def _get_entity_attribute(
        self, field_name: str, attr_name: str, default: float
    ) -> float:
        """get entity attribute value"""
        entity = self.data_entities.get(field_name)
        if entity and hasattr(entity, attr_name):
            return float(getattr(entity, attr_name))
        return default


class SimpleRfThermostat(BaseClimateEntity):
    """Simple classic HomeMatic thermostat HM-CC-TC."""


class RfThermostat(BaseClimateEntity):
    """Classic HomeMatic thermostat like HM-CC-RT-DN."""

    @property
    def _boost_mode(self) -> bool | None:
        """Return the boost_mode of the device."""
        return self._get_entity_state(FIELD_BOOST_MODE)

    @property
    def _control_mode(self) -> int | None:
        """Return the control_mode of the device."""
        return self._get_entity_state(FIELD_CONTROL_MODE)

    @property
    def supported_features(self) -> int:
        """Return the list of supported features."""
        return SUPPORT_TARGET_TEMPERATURE | SUPPORT_PRESET_MODE

    @property
    def hvac_mode(self) -> str:
        """Return hvac operation mode."""
        if self.target_temperature and self.target_temperature <= self.min_temp:
            return HVAC_MODE_OFF
        if self._control_mode == HM_MODE_MANU:
            return HVAC_MODE_HEAT
        return HVAC_MODE_AUTO

    @property
    def hvac_modes(self) -> list[str]:
        """Return the list of available hvac operation modes."""
        return [HVAC_MODE_AUTO, HVAC_MODE_HEAT, HVAC_MODE_OFF]

    @property
    def preset_mode(self) -> str:
        """Return the current preset mode."""
        if self._control_mode is None:
            return PRESET_NONE
        if self._control_mode == HM_MODE_BOOST:
            return PRESET_BOOST
        if self._control_mode == HM_MODE_AWAY:
            return PRESET_AWAY
        # This mode (PRESET_AWY) generally is available, but we're hiding it because
        # we can't set it from the Home Assistant UI natively.
        # We could create 2 input_datetime entities and reference them
        # and number.xxx_4_party_temperature when setting the preset.
        # More info on format: https://homematic-forum.de/forum/viewtopic.php?t=34673#p330200
        # Example-payload (21.5° from 2021-03-16T01:00-2021-03-17T23:00):
        # "21.5,60,16,3,21,1380,17,3,21"
        return PRESET_NONE

    @property
    def preset_modes(self) -> list[str]:
        """Return available preset modes."""
        return [PRESET_BOOST, PRESET_COMFORT, PRESET_ECO, PRESET_NONE]

    async def set_hvac_mode(self, hvac_mode: str) -> None:
        """Set new target hvac mode."""
        if hvac_mode == HVAC_MODE_AUTO:
            await self._send_value(FIELD_AUTO_MODE, True)
        elif hvac_mode == HVAC_MODE_HEAT:
            await self._send_value(FIELD_MANU_MODE, self.max_temp)
        elif hvac_mode == HVAC_MODE_OFF:
            await self.set_temperature(temperature=self.min_temp)
        # if switching hvac_mode then disable boost_mode
        if self._boost_mode:
            await self.set_preset_mode(PRESET_NONE)

    async def set_preset_mode(self, preset_mode: str) -> None:
        """Set new preset mode."""
        if preset_mode == PRESET_BOOST:
            await self._send_value(FIELD_BOOST_MODE, True)
        elif preset_mode == PRESET_COMFORT:
            await self._send_value(FIELD_COMFORT_MODE, True)
        elif preset_mode == PRESET_ECO:
            await self._send_value(FIELD_LOWERING_MODE, True)
        elif preset_mode == PRESET_NONE:
            await self._send_value(FIELD_BOOST_MODE, False)


class IPThermostat(BaseClimateEntity):
    """homematic IP thermostat like HmIP-eTRV-B."""

    @property
    def _active_profile(self) -> int | None:
        return self._get_entity_state(FIELD_ACTIVE_PROFILE)

    @property
    def _boost_mode(self) -> bool | None:
        return self._get_entity_state(FIELD_BOOST_MODE)

    @property
    def _control_mode(self) -> int | None:
        return self._get_entity_state(FIELD_CONTROL_MODE)

    @property
    def _is_heating(self) -> bool | None:
        if heating_cooling := self._get_entity_state(FIELD_HEATING_COOLING):
            return str(heating_cooling) == "HEATING"
        return True

    @property
    def _party_mode(self) -> bool | None:
        return self._get_entity_state(FIELD_PARTY_MODE)

    @property
    def _set_point_mode(self) -> int | None:
        return self._get_entity_state(FIELD_SET_POINT_MODE)

    @property
    def supported_features(self) -> int:
        """Return the list of supported features."""
        return SUPPORT_TARGET_TEMPERATURE | SUPPORT_PRESET_MODE

    @property
    def hvac_mode(self) -> str:
        """Return hvac operation mode."""
        if self.target_temperature and self.target_temperature <= self.min_temp:
            return HVAC_MODE_OFF
        if self._set_point_mode == HMIP_SET_POINT_MODE_MANU:
            return HVAC_MODE_HEAT if self._is_heating else HVAC_MODE_COOL
        if self._set_point_mode == HMIP_SET_POINT_MODE_AUTO:
            return HVAC_MODE_AUTO
        return HVAC_MODE_AUTO

    @property
    def hvac_modes(self) -> list[str]:
        """Return the list of available hvac operation modes."""
        return [
            HVAC_MODE_AUTO,
            HVAC_MODE_HEAT if self._is_heating else HVAC_MODE_COOL,
            HVAC_MODE_OFF,
        ]

    @property
    def preset_mode(self) -> str:
        """Return the current preset mode."""
        if self._boost_mode:
            return PRESET_BOOST
        if self._set_point_mode == HMIP_SET_POINT_MODE_AWAY:
            return PRESET_AWAY
        if self.hvac_mode == HVAC_MODE_AUTO:
            return (
                self._current_profile_name
                if self._current_profile_name
                else PRESET_NONE
            )
        return PRESET_NONE

    @property
    def preset_modes(self) -> list[str]:
        """Return available preset modes."""
        presets = [PRESET_BOOST, PRESET_NONE]
        if self.hvac_mode == HVAC_MODE_AUTO:
            presets.extend(self._profile_names)
        return presets

    async def set_hvac_mode(self, hvac_mode: str) -> None:
        """Set new target hvac mode."""
        if hvac_mode == HVAC_MODE_AUTO:
            await self._send_value(FIELD_CONTROL_MODE, HMIP_SET_POINT_MODE_AUTO)
        elif hvac_mode in (HVAC_MODE_HEAT, HVAC_MODE_COOL):
            await self._send_value(FIELD_CONTROL_MODE, HMIP_SET_POINT_MODE_MANU)
        elif hvac_mode == HVAC_MODE_OFF:
            await self._send_value(FIELD_CONTROL_MODE, HMIP_SET_POINT_MODE_MANU)
            await self.set_temperature(temperature=self.min_temp)
        # if switching hvac_mode then disable boost_mode
        if self._boost_mode:
            await self.set_preset_mode(PRESET_NONE)

    async def set_preset_mode(self, preset_mode: str) -> None:
        """Set new preset mode."""
        if preset_mode == PRESET_BOOST:
            await self._send_value(FIELD_BOOST_MODE, True)
        if preset_mode == PRESET_NONE:
            await self._send_value(FIELD_BOOST_MODE, False)

        if preset_mode in self._profile_names:
            if self.hvac_mode != HVAC_MODE_AUTO:
                await self.set_hvac_mode(HVAC_MODE_AUTO)
            profile_idx = self._get_profile_idx_by_name(preset_mode)
            await self._send_value(FIELD_BOOST_MODE, False)
            await self._send_value(FIELD_ACTIVE_PROFILE, profile_idx)

    async def enable_away_mode_by_calendar(
        self, start: datetime, end: datetime, away_temperature: float
    ) -> None:
        """Enable the away mode by calendar on thermostat."""
        await self.put_paramset(
            paramset="VALUES",
            value={
                "CONTROL_MODE": HMIP_SET_POINT_MODE_AWAY,
                "PARTY_TIME_END": end.strftime(PARTY_DATE_FORMAT),
                "PARTY_TIME_START": start.strftime(PARTY_DATE_FORMAT),
            },
        )
        await self.put_paramset(
            paramset="VALUES",
            value={
                "SET_POINT_TEMPERATURE": away_temperature,
            },
        )

    async def enable_away_mode_by_duration(
        self, hours: int, away_temperature: float
    ) -> None:
        """Enable the away mode by duration on thermostat."""
        start = datetime.now() - timedelta(minutes=10)
        end = datetime.now() + timedelta(hours=hours)
        await self.enable_away_mode_by_calendar(
            start=start, end=end, away_temperature=away_temperature
        )

    async def disable_away_mode(self) -> None:
        """Disable the away mode on thermostat."""
        await self.put_paramset(
            paramset="VALUES",
            value={
                "CONTROL_MODE": HMIP_SET_POINT_MODE_AUTO,
                "PARTY_TIME_START": PARTY_INIT_DATE,
                "PARTY_TIME_END": PARTY_INIT_DATE,
            },
        )

    @property
    def _profile_names(self) -> list[str]:
        """Return a collection of profile names."""
        return list(self._relevant_profiles.keys())

    @property
    def _current_profile_name(self) -> str | None:
        """Return a profile index by name."""
        inv_profiles: dict[int, str] = {
            v: k for k, v in self._relevant_profiles.items()
        }
        return (
            inv_profiles[self._active_profile]
            if self._active_profile is not None
            else None
        )

    def _get_profile_idx_by_name(self, profile_name: str) -> int:
        """Return a profile index by name."""
        return self._relevant_profiles[profile_name]

    @property
    def _relevant_profiles(self) -> dict[str, int]:
        """Return the relevant profile groups."""
        return HEATING_PROFILES if self._is_heating else COOLING_PROFILES


def make_simple_thermostat(
    device: hm_device.HmDevice, address: str, group_base_channels: list[int]
) -> list[hm_entity.BaseEntity]:
    """Creates SimpleRfThermostat entities."""
    return make_custom_entity(
        device,
        address,
        SimpleRfThermostat,
        EntityDefinition.SIMPLE_RF_THERMOSTAT,
        group_base_channels,
    )


def make_thermostat(
    device: hm_device.HmDevice, address: str, group_base_channels: list[int]
) -> list[hm_entity.BaseEntity]:
    """Creates RfThermostat entities."""
    return make_custom_entity(
        device,
        address,
        RfThermostat,
        EntityDefinition.RF_THERMOSTAT,
        group_base_channels,
    )


def make_thermostat_group(
    device: hm_device.HmDevice, address: str, group_base_channels: list[int]
) -> list[hm_entity.BaseEntity]:
    """Creates RfThermostat group entities."""
    return make_custom_entity(
        device,
        address,
        RfThermostat,
        EntityDefinition.RF_THERMOSTAT_GROUP,
        group_base_channels,
    )


def make_ip_thermostat(
    device: hm_device.HmDevice, address: str, group_base_channels: list[int]
) -> list[hm_entity.BaseEntity]:
    """Creates IPThermostat entities."""
    return make_custom_entity(
        device,
        address,
        IPThermostat,
        EntityDefinition.IP_THERMOSTAT,
        group_base_channels,
    )


def make_ip_thermostat_group(
    device: hm_device.HmDevice, address: str, group_base_channels: list[int]
) -> list[hm_entity.BaseEntity]:
    """Creates IPThermostat group entities."""
    return make_custom_entity(
        device,
        address,
        IPThermostat,
        EntityDefinition.IP_THERMOSTAT_GROUP,
        group_base_channels,
    )


# Case for device model is not relevant
# device_type and sub_type(IP-only) can be used here
DEVICES: dict[str, tuple[Any, list[int]]] = {
    "BC-RT-TRX-CyG*": (make_thermostat, []),
    "BC-RT-TRX-CyN*": (make_thermostat, []),
    "BC-TC-C-WM*": (make_thermostat, []),
    "HM-CC-RT-DN*": (make_thermostat, []),
    "HM-CC-TC": (make_simple_thermostat, []),
    "HM-CC-VG-1": (make_thermostat_group, []),
    "HM-TC-IT-WM-W-EU": (make_thermostat, []),
    "HmIP-BWTH*": (make_ip_thermostat, []),
    "HmIP-eTRV*": (make_ip_thermostat, []),
    "HmIP-HEATING": (make_ip_thermostat_group, []),
    "HmIP-STHD": (make_ip_thermostat, []),
    "HmIP-WTH*": (make_ip_thermostat, []),
    "HmIPW-STH*": (make_ip_thermostat, []),
    "HmIPW-WTH*": (make_ip_thermostat, []),
    "RfThermostat AA*": (make_ip_thermostat, []),
    "ZEL STG RM FWT": (make_simple_thermostat, []),
}
