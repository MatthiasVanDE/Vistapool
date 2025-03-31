import logging
from homeassistant.components.sensor import SensorEntity
from homeassistant.helpers.update_coordinator import CoordinatorEntity
from homeassistant.const import UnitOfTemperature
from .const import DOMAIN
from datetime import datetime, timezone

_LOGGER = logging.getLogger(__name__)

#
# =================== Mapping Tables ===================
#
FILTRATION_MODE_MAP = {
    "Manual": 0,
    "Auto": 1,
    "Smart": 3
}
FILTRATION_MODE_NAMES = {v: k for k, v in FILTRATION_MODE_MAP.items()}

BACKWASH_MODE_MAP = {
    "Manual": 0,
    "Automatic": 1
}
BACKWASH_MODE_NAMES = {v: k for k, v in BACKWASH_MODE_MAP.items()}

FILTRATION_STATUS_MAP = {
    "Off": 0,
    "On": 1
}
FILTRATION_STATUS_NAMES = {v: k for k, v in FILTRATION_STATUS_MAP.items()}

BACKWASH_STATUS_MAP = {
    "Off": 0,
    "On": 1
}
BACKWASH_STATUS_NAMES = {v: k for k, v in BACKWASH_STATUS_MAP.items()}

TRUE_FALSE_MAP = {
    "False": 0,
    "True": 1
}
TRUE_FALSE_NAMES = {v: k for k, v in TRUE_FALSE_MAP.items()}


def intervalTime(value):
    return datetime.fromtimestamp(value, tz=timezone.utc).strftime("%H:%M:%S")


async def async_setup_entry(hass, entry, async_add_entities):
    """Set up a sensor for every single JSON field, grouped by category."""
    coordinator = hass.data[DOMAIN][entry.entry_id]
    sensors = []

    #
    # ============ GLOBAL / TOP-LEVEL KEYS ============
    #
    sensors.append(S_GlobalIsAWSSensor(coordinator))
    sensors.append(S_GlobalWifiSensor(coordinator))
    sensors.append(S_GlobalIdSensor(coordinator))
    sensors.append(S_GlobalCompanySensor(coordinator))
    sensors.append(S_GlobalUpdatedAtSensor(coordinator))
    sensors.append(S_GlobalCreatedAtSensor(coordinator))
    sensors.append(S_GlobalPresentSensor(coordinator))

    #
    # ============ BACKWASH KEYS ============
    #
    sensors.append(S_BackwashIntervalSensor(coordinator))
    sensors.append(S_BackwashModeSensor(coordinator))
    sensors.append(S_BackwashRemainingTimeSensor(coordinator))
    sensors.append(S_BackwashStatusSensor(coordinator))
    sensors.append(S_BackwashFrequencySensor(coordinator))
    sensors.append(S_BackwashStartAtSensor(coordinator))

    #
    # ============ LIGHT KEYS ============
    #
    sensors.append(S_LightModeSensor(coordinator))
    sensors.append(S_LightFreqSensor(coordinator))
    sensors.append(S_LightToSensor(coordinator))
    sensors.append(S_LightFromSensor(coordinator))
    sensors.append(S_LightStatusSensor(coordinator))

    #
    # ============ HIDRO KEYS ============
    #
    sensors.append(S_HidroClorationEnabledSensor(coordinator))
    sensors.append(S_HidroTemperatureEnabledSensor(coordinator))
    sensors.append(S_HidroControlSensor(coordinator))
    sensors.append(S_HidroFl1Sensor(coordinator))
    sensors.append(S_HidroTemperatureValueSensor(coordinator))
    sensors.append(S_HidroAl4Sensor(coordinator))
    sensors.append(S_HidroHasHidroControlSensor(coordinator))
    sensors.append(S_HidroCoverSensor(coordinator))
    sensors.append(S_HidroCurrentSensor(coordinator))
    sensors.append(S_HidroCellPartialTimeSensor(coordinator))
    sensors.append(S_HidroIsElectrolysisSensor(coordinator))
    sensors.append(S_HidroFl2Sensor(coordinator))
    sensors.append(S_HidroCellTotalTimeSensor(coordinator))
    sensors.append(S_HidroReductionSensor(coordinator))
    sensors.append(S_HidroLevelSensor(coordinator))
    sensors.append(S_HidroMaxAllowedValueSensor(coordinator))
    sensors.append(S_HidroLowSensor(coordinator))
    sensors.append(S_HidroCoverEnabledSensor(coordinator))
    sensors.append(S_HidroMeasureSensor(coordinator))

    #
    # ============ FILTRATION KEYS ============
    #
    sensors.append(S_FiltrationInterval1FromSensor(coordinator))
    sensors.append(S_FiltrationInterval1ToSensor(coordinator))
    sensors.append(S_FiltrationInterval2FromSensor(coordinator))
    sensors.append(S_FiltrationInterval2ToSensor(coordinator))
    sensors.append(S_FiltrationInterval3FromSensor(coordinator))
    sensors.append(S_FiltrationInterval3ToSensor(coordinator))

    sensors.append(S_FiltrationIntelTimeSensor(coordinator))
    sensors.append(S_FiltrationIntelTempSensor(coordinator))

    sensors.append(S_FiltrationTimerVel2Sensor(coordinator))
    sensors.append(S_FiltrationHasSmartSensor(coordinator))

    sensors.append(S_FiltrationHeatingTempSensor(coordinator))
    sensors.append(S_FiltrationHeatingClimaSensor(coordinator))
    sensors.append(S_FiltrationHeatingTempHiSensor(coordinator))

    sensors.append(S_FiltrationManVelSensor(coordinator))
    sensors.append(S_FiltrationHasHeatSensor(coordinator))
    sensors.append(S_FiltrationPumpTypeSensor(coordinator))
    sensors.append(S_FiltrationTimerVel3Sensor(coordinator))
    sensors.append(S_FiltrationStatusSensor(coordinator))
    sensors.append(S_FiltrationTimerVel1Sensor(coordinator))

    sensors.append(S_FiltrationModeSensor(coordinator))

    # Filtration.smart
    sensors.append(S_FiltrationSmartTempMinSensor(coordinator))
    sensors.append(S_FiltrationSmartTempHighSensor(coordinator))
    sensors.append(S_FiltrationSmartFreezeSensor(coordinator))

    #
    # ============ MAIN KEYS ============
    #
    sensors.append(S_MainHideRelaysSensor(coordinator))
    sensors.append(S_MainHasUVSensor(coordinator))
    sensors.append(S_MainRSSISensor(coordinator))
    sensors.append(S_MainHasLEDSensor(coordinator))
    sensors.append(S_MainLEDPulseSensor(coordinator))
    sensors.append(S_MainHasIOSensor(coordinator))
    sensors.append(S_MainHasLinkedAutoSensor(coordinator))
    sensors.append(S_MainHideTemperatureSensor(coordinator))
    sensors.append(S_MainHideLightingSensor(coordinator))
    sensors.append(S_MainFWUEnabledSensor(coordinator))
    sensors.append(S_MainNetworkPresentSensor(coordinator))
    sensors.append(S_MainVersionSensor(coordinator))
    sensors.append(S_MainHasPHSensor(coordinator))
    sensors.append(S_MainHasBackwashSensor(coordinator))
    sensors.append(S_MainHasWifiSensor(coordinator))
    sensors.append(S_MainHasCDSensor(coordinator))
    sensors.append(S_MainHideFiltrationSensor(coordinator))
    sensors.append(S_MainHasCLSensor(coordinator))
    sensors.append(S_MainHasRXSensor(coordinator))
    sensors.append(S_MainTemperatureSensor(coordinator))
    sensors.append(S_MainWifiVersionSensor(coordinator))
    sensors.append(S_MainLocalTimeSensor(coordinator))
    sensors.append(S_MainHasLinkedSensor(coordinator))
    sensors.append(S_MainHasHidroSensor(coordinator))

    #
    # ============ MODULES KEYS ============
    #
    # modules.rx
    sensors.append(S_ModulesRxPumpStatusSensor(coordinator))
    sensors.append(S_ModulesRxCurrentSensor(coordinator))
    sensors.append(S_ModulesRxTankSensor(coordinator))
    sensors.append(S_ModulesRxStatusValueSensor(coordinator))

    # modules.ph
    sensors.append(S_ModulesPhTypeSensor(coordinator))
    sensors.append(S_ModulesPhTankSensor(coordinator))
    sensors.append(S_ModulesPhCurrentSensor(coordinator))
    sensors.append(S_ModulesPhPumpHighOnSensor(coordinator))
    sensors.append(S_ModulesPhStatusHighValueSensor(coordinator))
    sensors.append(S_ModulesPhStatusLowValueSensor(coordinator))
    sensors.append(S_ModulesPhAl3Sensor(coordinator))
    sensors.append(S_ModulesPhPumpLowOnSensor(coordinator))

    # modules.cl
    sensors.append(S_ModulesClPumpStatusSensor(coordinator))
    sensors.append(S_ModulesClCurrentSensor(coordinator))
    sensors.append(S_ModulesClStatusValueSensor(coordinator))
    sensors.append(S_ModulesClTankSensor(coordinator))

    # modules.cd
    sensors.append(S_ModulesCdCurrentSensor(coordinator))
    sensors.append(S_ModulesCdStatusValueSensor(coordinator))
    sensors.append(S_ModulesCdTankSensor(coordinator))

    # modules.uv
    sensors.append(S_ModulesUvTotalSensor(coordinator))
    sensors.append(S_ModulesUvPartialSensor(coordinator))
    sensors.append(S_ModulesUvStatusSensor(coordinator))

    # modules.io
    sensors.append(S_ModulesIoActivationSensor(coordinator))
    sensors.append(S_ModulesIoStatusSensor(coordinator))
    sensors.append(S_ModulesIoLevelSensor(coordinator))

    #
    # ============ RELAYS KEYS ============
    #
    # relays.filtration
    sensors.append(S_RelaysFiltrationHeatingStatusSensor(coordinator))
    sensors.append(S_RelaysFiltrationHeatingGpioSensor(coordinator))
    sensors.append(S_RelaysFiltrationGpioSensor(coordinator))

    # relays.backwash
    sensors.append(S_RelaysBackwashGpioSensor(coordinator))

    # relays.io
    sensors.append(S_RelaysIoGpioSensor(coordinator))

    # relays.rx
    sensors.append(S_RelaysRxGpioSensor(coordinator))

    # relays.light
    sensors.append(S_RelaysLightGpioSensor(coordinator))

    # relays.cl
    sensors.append(S_RelaysClGpioSensor(coordinator))

    # relays.cd
    sensors.append(S_RelaysCdGpioSensor(coordinator))

    # relays.ph (acid/base)
    sensors.append(S_RelaysPhAcidGpioSensor(coordinator))
    sensors.append(S_RelaysPhBaseGpioSensor(coordinator))

    # relayX (1..4) + uv
    sensors.append(S_RelaysUvGpioSensor(coordinator))

    sensors.append(S_RelaysRelay4NameSensor(coordinator))
    sensors.append(S_RelaysRelay4InfoFromSensor(coordinator))
    sensors.append(S_RelaysRelay4InfoDelaySensor(coordinator))
    sensors.append(S_RelaysRelay4InfoOnOffSensor(coordinator))
    sensors.append(S_RelaysRelay4InfoFreq2Sensor(coordinator))
    sensors.append(S_RelaysRelay4InfoManAutoTempSensor(coordinator))
    sensors.append(S_RelaysRelay4InfoSignalSensor(coordinator))
    sensors.append(S_RelaysRelay4InfoFrom2Sensor(coordinator))
    sensors.append(S_RelaysRelay4InfoPolaritySensor(coordinator))
    sensors.append(S_RelaysRelay4InfoStatusSensor(coordinator))
    sensors.append(S_RelaysRelay4InfoFreqSensor(coordinator))
    sensors.append(S_RelaysRelay4InfoToSensor(coordinator))
    sensors.append(S_RelaysRelay4InfoTo2Sensor(coordinator))
    sensors.append(S_RelaysRelay4InfoTiempoOnSensor(coordinator))
    sensors.append(S_RelaysRelay4InfoKeySensor(coordinator))

    # relay1, relay2, relay3 -> name + info
    sensors.append(S_RelaysRelay1NameSensor(coordinator))
    sensors.extend(make_s_relay_info_sensors(coordinator, relay_number=1))
    sensors.append(S_RelaysRelay2NameSensor(coordinator))
    sensors.extend(make_s_relay_info_sensors(coordinator, relay_number=2))
    sensors.append(S_RelaysRelay3NameSensor(coordinator))
    sensors.extend(make_s_relay_info_sensors(coordinator, relay_number=3))

    #
    # ============ FORM KEYS ============
    #
    sensors.append(S_FormLngSensor(coordinator))
    sensors.append(S_FormCountrySensor(coordinator))
    sensors.append(S_FormCitySensor(coordinator))
    sensors.append(S_FormNameSensor(coordinator))
    sensors.append(S_FormZipcodeSensor(coordinator))
    sensors.append(S_FormLatSensor(coordinator))
    sensors.append(S_FormStreetSensor(coordinator))

    async_add_entities(sensors, update_before_add=True)


#
# ==================== HELPER FOR RELAY INFO ====================
#

def make_s_relay_info_sensors(coordinator, relay_number: int):
    """
    Hulpfunctie die de SensorEntity's voor relays.relay{N}.info.* teruggeeft,
    met s_ prefix in de Unique ID.
    """
    return [
        S_RelayInfoGenericSensor(coordinator, relay_number, "from"),
        S_RelayInfoGenericSensor(coordinator, relay_number, "delay"),
        S_RelayInfoGenericSensor(coordinator, relay_number, "onoff"),
        S_RelayInfoGenericSensor(coordinator, relay_number, "freq2"),
        S_RelayInfoGenericSensor(coordinator, relay_number, "manAutoTemp"),
        S_RelayInfoGenericSensor(coordinator, relay_number, "signal"),
        S_RelayInfoGenericSensor(coordinator, relay_number, "from2"),
        S_RelayInfoGenericSensor(coordinator, relay_number, "polarity"),
        S_RelayInfoGenericSensor(coordinator, relay_number, "status"),
        S_RelayInfoGenericSensor(coordinator, relay_number, "freq"),
        S_RelayInfoGenericSensor(coordinator, relay_number, "to"),
        S_RelayInfoGenericSensor(coordinator, relay_number, "to2"),
        S_RelayInfoGenericSensor(coordinator, relay_number, "tiempoOn"),
        S_RelayInfoGenericSensor(coordinator, relay_number, "key"),
    ]


class S_RelayInfoGenericSensor(CoordinatorEntity, SensorEntity):
    """
    Reads relays.relay{N}.info.<field>.
    e.g. relays.relay1.info.freq
    """

    def __init__(self, coordinator, relay_number, field):
        super().__init__(coordinator)
        self._relay_number = relay_number
        self._field = field
        self._attr_name = f"Relay{relay_number} Info {field}"
        self._attr_unique_id = f"s_{coordinator.api._pool_id}_relay{relay_number}_info_{field}"

    @property
    def device_info(self):
        return {
            "identifiers": {(DOMAIN, f"{self.coordinator.api._pool_id}_relays")},
            "name": "Relays",
            "manufacturer": "Vistapool",
            "model": "Vistapool Controller"
        }

    @property
    def native_value(self):
        data = self.coordinator.data
        info = (
            data.get("relays", {})
                .get(f"relay{self._relay_number}", {})
                .get("info", {})
        )
        return info.get(self._field, None)


#
# ==================== EXAMPLE SENSOR CLASSES ====================
# Vanaf hier staan alle klassen die exact de JSON-structuur weerspiegelen
# (zoals we in de conversation hebben doorgenomen).
#

#
# --------------- GLOBAL / TOP-LEVEL ---------------
#

class S_GlobalSensorBase(CoordinatorEntity, SensorEntity):
    """Top-level info (isAWS, wifi, id, company, updatedAt, createdAt, present)."""
    async def async_added_to_hass(self):
        await super().async_added_to_hass()
        self.async_on_remove(
            self.coordinator.async_add_listener(self.async_write_ha_state)
        )

    @property
    def device_info(self):
        return {
            "identifiers": {(DOMAIN, f"{self.coordinator.api._pool_id}_global")},
            "name": "Algemeen (Global)",
            "manufacturer": "Vistapool",
            "model": "Vistapool Controller"
        }


class S_GlobalIsAWSSensor(S_GlobalSensorBase):
    def __init__(self, coordinator):
        super().__init__(coordinator)
        self._attr_name = "isAWS"
        self._attr_unique_id = f"s_{coordinator.api._pool_id}_isaws"

    @property
    def native_value(self):
        return self.coordinator.data.get("isAWS", None)


class S_GlobalWifiSensor(S_GlobalSensorBase):
    def __init__(self, coordinator):
        super().__init__(coordinator)
        self._attr_name = "Wifi"
        self._attr_unique_id = f"s_{coordinator.api._pool_id}_wifi"

    @property
    def native_value(self):
        return self.coordinator.data.get("wifi", None)


class S_GlobalIdSensor(S_GlobalSensorBase):
    def __init__(self, coordinator):
        super().__init__(coordinator)
        self._attr_name = "Pool ID"
        self._attr_unique_id = f"s_{coordinator.api._pool_id}_id"

    @property
    def native_value(self):
        return self.coordinator.data.get("id", None)


class S_GlobalCompanySensor(S_GlobalSensorBase):
    def __init__(self, coordinator):
        super().__init__(coordinator)
        self._attr_name = "Company"
        self._attr_unique_id = f"s_{coordinator.api._pool_id}_company"

    @property
    def native_value(self):
        return self.coordinator.data.get("company", None)


class S_GlobalUpdatedAtSensor(S_GlobalSensorBase):
    def __init__(self, coordinator):
        super().__init__(coordinator)
        self._attr_name = "Updated At"
        self._attr_unique_id = f"s_{coordinator.api._pool_id}_updated_at"

    @property
    def native_value(self):
        value = self.coordinator.data.get("updatedAt", None)
        return datetime.fromtimestamp(value)

class S_GlobalCreatedAtSensor(S_GlobalSensorBase):
    def __init__(self, coordinator):
        super().__init__(coordinator)
        self._attr_name = "Created At"
        self._attr_unique_id = f"s_{coordinator.api._pool_id}_created_at"

    @property
    def native_value(self):
        value = self.coordinator.data.get("createdAt", None)
        return datetime.fromtimestamp(value)

class S_GlobalPresentSensor(S_GlobalSensorBase):
    def __init__(self, coordinator):
        super().__init__(coordinator)
        self._attr_name = "Present"
        self._attr_unique_id = f"s_{coordinator.api._pool_id}_present"

    @property
    def native_value(self):
        return self.coordinator.data.get("present", None)

#
# --------------- BACKWASH ---------------
#

class S_BackwashSensorBase(CoordinatorEntity, SensorEntity):
    """Keys: interval, mode, remainingTime, status, frequency, startAt."""
    async def async_added_to_hass(self):
        await super().async_added_to_hass()
        self.async_on_remove(
            self.coordinator.async_add_listener(self.async_write_ha_state)
        )

    @property
    def device_info(self):
        return {
            "identifiers": {(DOMAIN, f"{self.coordinator.api._pool_id}_filtratie")},
            "name": "Filtratie",
            "manufacturer": "Vistapool",
            "model": "Vistapool Controller"
        }

class S_BackwashIntervalSensor(S_BackwashSensorBase):
    def __init__(self, coordinator):
        super().__init__(coordinator)
        self._attr_name = "Backwash Interval"
        self._attr_unique_id = f"s_{coordinator.api._pool_id}_backwash_interval"

    @property
    def native_value(self):
        return self.coordinator.data.get("backwash", {}).get("interval", None)

class S_BackwashModeSensor(S_BackwashSensorBase):
    def __init__(self, coordinator):
        super().__init__(coordinator)
        self._attr_name = "Backwash Mode"
        self._attr_unique_id = f"s_{coordinator.api._pool_id}_backwash_mode"

    @property
    def native_value(self):
        value = self.coordinator.data.get("backwash", {}).get("mode", None)
        return BACKWASH_MODE_NAMES.get(value, "unknown")

class S_BackwashRemainingTimeSensor(S_BackwashSensorBase):
    def __init__(self, coordinator):
        super().__init__(coordinator)
        self._attr_name = "Backwash Remaining Time"
        self._attr_unique_id = f"s_{coordinator.api._pool_id}_backwash_remainingTime"

    @property
    def native_value(self):
        return self.coordinator.data.get("backwash", {}).get("remainingTime", None)

class S_BackwashStatusSensor(S_BackwashSensorBase):
    def __init__(self, coordinator):
        super().__init__(coordinator)
        self._attr_name = "Backwash Status"
        self._attr_unique_id = f"s_{coordinator.api._pool_id}_backwash_status"

    @property
    def native_value(self):
        value = self.coordinator.data.get("backwash", {}).get("status", None)
        return BACKWASH_STATUS_NAMES.get(value, "unknown")

class S_BackwashFrequencySensor(S_BackwashSensorBase):
    def __init__(self, coordinator):
        super().__init__(coordinator)
        self._attr_name = "Backwash Frequency"
        self._attr_unique_id = f"s_{coordinator.api._pool_id}_backwash_frequency"

    @property
    def native_value(self):
        return self.coordinator.data.get("backwash", {}).get("frequency", None)

class S_BackwashStartAtSensor(S_BackwashSensorBase):
    def __init__(self, coordinator):
        super().__init__(coordinator)
        self._attr_name = "Backwash StartAt"
        self._attr_unique_id = f"s_{coordinator.api._pool_id}_backwash_startAt"

    @property
    def native_value(self):
        value = self.coordinator.data.get("backwash", {}).get("startAt", None)
        return datetime.fromtimestamp(value)

#
# --------------- LIGHT ---------------
#

class S_LightSensorBase(CoordinatorEntity, SensorEntity):
    """Keys: mode, freq, to, from, status."""
    async def async_added_to_hass(self):
        await super().async_added_to_hass()
        self.async_on_remove(
            self.coordinator.async_add_listener(self.async_write_ha_state)
        )

    @property
    def device_info(self):
        return {
            "identifiers": {(DOMAIN, f"{self.coordinator.api._pool_id}_filtratie")},
            "name": "Filtratie",
            "manufacturer": "Vistapool",
            "model": "Vistapool Controller"
        }

class S_LightModeSensor(S_LightSensorBase):
    def __init__(self, coordinator):
        super().__init__(coordinator)
        self._attr_name = "Light Mode"
        self._attr_unique_id = f"s_{coordinator.api._pool_id}_light_mode"

    @property
    def native_value(self):
        return self.coordinator.data.get("light", {}).get("mode", None)

class S_LightFreqSensor(S_LightSensorBase):
    def __init__(self, coordinator):
        super().__init__(coordinator)
        self._attr_name = "Light Frequency"
        self._attr_unique_id = f"s_{coordinator.api._pool_id}_light_freq"

    @property
    def native_value(self):
        return self.coordinator.data.get("light", {}).get("freq", None)

class S_LightToSensor(S_LightSensorBase):
    def __init__(self, coordinator):
        super().__init__(coordinator)
        self._attr_name = "Light To"
        self._attr_unique_id = f"s_{coordinator.api._pool_id}_light_to"

    @property
    def native_value(self):
        return self.coordinator.data.get("light", {}).get("to", None)

class S_LightFromSensor(S_LightSensorBase):
    def __init__(self, coordinator):
        super().__init__(coordinator)
        self._attr_name = "Light From"
        self._attr_unique_id = f"s_{coordinator.api._pool_id}_light_from"

    @property
    def native_value(self):
        value = self.coordinator.data.get("light", {}).get("from", None)
        return intervalTime(value)

class S_LightStatusSensor(S_LightSensorBase):
    def __init__(self, coordinator):
        super().__init__(coordinator)
        self._attr_name = "Light Status"
        self._attr_unique_id = f"s_{coordinator.api._pool_id}_light_status"

    @property
    def native_value(self):
        return self.coordinator.data.get("light", {}).get("status", None)

#
# --------------- HIDRO ---------------
#

class S_HydrolyseSensorBase(CoordinatorEntity, SensorEntity):
    """Keys: cloration_enabled, temperature_enabled, control, fl1, fl2, etc."""
    async def async_added_to_hass(self):
        await super().async_added_to_hass()
        self.async_on_remove(
            self.coordinator.async_add_listener(self.async_write_ha_state)
        )

    @property
    def device_info(self):
        return {
            "identifiers": {(DOMAIN, f"{self.coordinator.api._pool_id}_hydrolyse")},
            "name": "Hydrolyse",
            "manufacturer": "Vistapool",
            "model": "Vistapool Controller"
        }

class S_HidroClorationEnabledSensor(S_HydrolyseSensorBase):
    def __init__(self, coordinator):
        super().__init__(coordinator)
        self._attr_name = "Cloration Enabled"
        self._attr_unique_id = f"s_{coordinator.api._pool_id}_hidro_cloration_enabled"

    @property
    def native_value(self):
        return self.coordinator.data.get("hidro", {}).get("cloration_enabled", None)

class S_HidroTemperatureEnabledSensor(S_HydrolyseSensorBase):
    def __init__(self, coordinator):
        super().__init__(coordinator)
        self._attr_name = "Hidro Temperature Enabled"
        self._attr_unique_id = f"s_{coordinator.api._pool_id}_hidro_temperature_enabled"

    @property
    def native_value(self):
        return self.coordinator.data.get("hidro", {}).get("temperature_enabled", None)

class S_HidroControlSensor(S_HydrolyseSensorBase):
    def __init__(self, coordinator):
        super().__init__(coordinator)
        self._attr_name = "Hidro Control"
        self._attr_unique_id = f"s_{coordinator.api._pool_id}_hidro_control"

    @property
    def native_value(self):
        return self.coordinator.data.get("hidro", {}).get("control", None)

class S_HidroFl1Sensor(S_HydrolyseSensorBase):
    def __init__(self, coordinator):
        super().__init__(coordinator)
        self._attr_name = "Hidro fl1"
        self._attr_unique_id = f"s_{coordinator.api._pool_id}_hidro_fl1"

    @property
    def native_value(self):
        return self.coordinator.data.get("hidro", {}).get("fl1", None)

class S_HidroTemperatureValueSensor(S_HydrolyseSensorBase):
    def __init__(self, coordinator):
        super().__init__(coordinator)
        self._attr_name = "Hidro Temperature Value"
        self._attr_unique_id = f"s_{coordinator.api._pool_id}_hidro_temperature_value"

    @property
    def native_value(self):
        return self.coordinator.data.get("hidro", {}).get("temperature_value", None)

class S_HidroAl4Sensor(S_HydrolyseSensorBase):
    def __init__(self, coordinator):
        super().__init__(coordinator)
        self._attr_name = "Hidro al4"
        self._attr_unique_id = f"s_{coordinator.api._pool_id}_hidro_al4"

    @property
    def native_value(self):
        return self.coordinator.data.get("hidro", {}).get("al4", None)

class S_HidroHasHidroControlSensor(S_HydrolyseSensorBase):
    def __init__(self, coordinator):
        super().__init__(coordinator)
        self._attr_name = "Hidro HasHidroControl"
        self._attr_unique_id = f"s_{coordinator.api._pool_id}_hidro_hasHidroControl"

    @property
    def native_value(self):
        value = self.coordinator.data.get("hidro", {}).get("hasHidroControl", None)
        return TRUE_FALSE_NAMES.get(value, "unknown")

class S_HidroCoverSensor(S_HydrolyseSensorBase):
    def __init__(self, coordinator):
        super().__init__(coordinator)
        self._attr_name = "Hidro Cover"
        self._attr_unique_id = f"s_{coordinator.api._pool_id}_hidro_cover"

    @property
    def native_value(self):
        return self.coordinator.data.get("hidro", {}).get("cover", None)

class S_HidroCurrentSensor(S_HydrolyseSensorBase):
    def __init__(self, coordinator):
        super().__init__(coordinator)
        self._attr_name = "Hidro Current"
        self._attr_unique_id = f"s_{coordinator.api._pool_id}_hidro_current"

    @property
    def native_value(self):
        return self.coordinator.data.get("hidro", {}).get("current", None)

class S_HidroCellPartialTimeSensor(S_HydrolyseSensorBase):
    def __init__(self, coordinator):
        super().__init__(coordinator)
        self._attr_name = "Hidro CellPartialTime"
        self._attr_unique_id = f"s_{coordinator.api._pool_id}_hidro_cellPartialTime"

    @property
    def native_value(self):
        return self.coordinator.data.get("hidro", {}).get("cellPartialTime", None)

class S_HidroIsElectrolysisSensor(S_HydrolyseSensorBase):
    def __init__(self, coordinator):
        super().__init__(coordinator)
        self._attr_name = "Hidro is_electrolysis"
        self._attr_unique_id = f"s_{coordinator.api._pool_id}_hidro_is_electrolysis"

    @property
    def native_value(self):
        return self.coordinator.data.get("hidro", {}).get("is_electrolysis", None)

class S_HidroFl2Sensor(S_HydrolyseSensorBase):
    def __init__(self, coordinator):
        super().__init__(coordinator)
        self._attr_name = "Hidro fl2"
        self._attr_unique_id = f"s_{coordinator.api._pool_id}_hidro_fl2"

    @property
    def native_value(self):
        return self.coordinator.data.get("hidro", {}).get("fl2", None)

class S_HidroCellTotalTimeSensor(S_HydrolyseSensorBase):
    def __init__(self, coordinator):
        super().__init__(coordinator)
        self._attr_name = "Hidro CellTotalTime"
        self._attr_unique_id = f"s_{coordinator.api._pool_id}_hidro_cellTotalTime"

    @property
    def native_value(self):
        return self.coordinator.data.get("hidro", {}).get("cellTotalTime", None)

class S_HidroReductionSensor(S_HydrolyseSensorBase):
    def __init__(self, coordinator):
        super().__init__(coordinator)
        self._attr_name = "Hidro Reduction"
        self._attr_unique_id = f"s_{coordinator.api._pool_id}_hidro_reduction"

    @property
    def native_value(self):
        return self.coordinator.data.get("hidro", {}).get("reduction", None)

class S_HidroLevelSensor(S_HydrolyseSensorBase):
    def __init__(self, coordinator):
        super().__init__(coordinator)
        self._attr_name = "Hidro Level"
        self._attr_unique_id = f"s_{coordinator.api._pool_id}_hidro_level"

    @property
    def native_value(self):
        return self.coordinator.data.get("hidro", {}).get("level", None)

class S_HidroMaxAllowedValueSensor(S_HydrolyseSensorBase):
    def __init__(self, coordinator):
        super().__init__(coordinator)
        self._attr_name = "Hidro MaxAllowedValue"
        self._attr_unique_id = f"s_{coordinator.api._pool_id}_hidro_maxAllowedValue"

    @property
    def native_value(self):
        return self.coordinator.data.get("hidro", {}).get("maxAllowedValue", None)

class S_HidroLowSensor(S_HydrolyseSensorBase):
    def __init__(self, coordinator):
        super().__init__(coordinator)
        self._attr_name = "Hidro Low"
        self._attr_unique_id = f"s_{coordinator.api._pool_id}_hidro_low"

    @property
    def native_value(self):
        return self.coordinator.data.get("hidro", {}).get("low", None)

class S_HidroCoverEnabledSensor(S_HydrolyseSensorBase):
    def __init__(self, coordinator):
        super().__init__(coordinator)
        self._attr_name = "Hidro cover_enabled"
        self._attr_unique_id = f"s_{coordinator.api._pool_id}_hidro_cover_enabled"

    @property
    def native_value(self):
        return self.coordinator.data.get("hidro", {}).get("cover_enabled", None)

class S_HidroMeasureSensor(S_HydrolyseSensorBase):
    def __init__(self, coordinator):
        super().__init__(coordinator)
        self._attr_name = "Hidro measure"
        self._attr_unique_id = f"s_{coordinator.api._pool_id}_hidro_measure"

    @property
    def native_value(self):
        return self.coordinator.data.get("hidro", {}).get("measure", None)

#
# --------------- FILTRATION ---------------
#

class S_FiltrationSensorBase(CoordinatorEntity, SensorEntity):
    async def async_added_to_hass(self):
        await super().async_added_to_hass()
        self.async_on_remove(
            self.coordinator.async_add_listener(self.async_write_ha_state)
        )

    @property
    def device_info(self):
        return {
            "identifiers": {(DOMAIN, f"{self.coordinator.api._pool_id}_filtratie")},
            "name": "Filtratie",
            "manufacturer": "Vistapool",
            "model": "Vistapool Controller"
        }

class S_FiltrationInterval1FromSensor(S_FiltrationSensorBase):
    def __init__(self, coordinator):
        super().__init__(coordinator)
        self._attr_name = "Filtration Interval1 From"
        self._attr_unique_id = f"s_{coordinator.api._pool_id}_filtration_interval1_from"

    @property
    def native_value(self):
        value = (
            self.coordinator.data.get("filtration", {})
                .get("interval1", {})
                .get("from", None)
        )
        return intervalTime(value)


class S_FiltrationInterval1ToSensor(S_FiltrationSensorBase):
    def __init__(self, coordinator):
        super().__init__(coordinator)
        self._attr_name = "Filtration Interval1 To"
        self._attr_unique_id = f"s_{coordinator.api._pool_id}_filtration_interval1_to"

    @property
    def native_value(self):
        value = (
            self.coordinator.data.get("filtration", {})
                .get("interval1", {})
                .get("to", None)
        )
        return intervalTime(value)

class S_FiltrationInterval2FromSensor(S_FiltrationSensorBase):
    def __init__(self, coordinator):
        super().__init__(coordinator)
        self._attr_name = "Filtration Interval2 From"
        self._attr_unique_id = f"s_{coordinator.api._pool_id}_filtration_interval2_from"

    @property
    def native_value(self):
        value = (
            self.coordinator.data.get("filtration", {})
                .get("interval2", {})
                .get("from", None)
        )
        return intervalTime(value)

class S_FiltrationInterval2ToSensor(S_FiltrationSensorBase):
    def __init__(self, coordinator):
        super().__init__(coordinator)
        self._attr_name = "Filtration Interval2 To"
        self._attr_unique_id = f"s_{coordinator.api._pool_id}_filtration_interval2_to"

    @property
    def native_value(self):
        value = (
            self.coordinator.data.get("filtration", {})
                .get("interval2", {})
                .get("to", None)
        )
        return intervalTime(value)

class S_FiltrationInterval3FromSensor(S_FiltrationSensorBase):
    def __init__(self, coordinator):
        super().__init__(coordinator)
        self._attr_name = "Filtration Interval3 From"
        self._attr_unique_id = f"s_{coordinator.api._pool_id}_filtration_interval3_from"

    @property
    def native_value(self):
        value = (
            self.coordinator.data.get("filtration", {})
                .get("interval3", {})
                .get("from", None)
        )
        return intervalTime(value)

class S_FiltrationInterval3ToSensor(S_FiltrationSensorBase):
    def __init__(self, coordinator):
        super().__init__(coordinator)
        self._attr_name = "Filtration Interval3 To"
        self._attr_unique_id = f"s_{coordinator.api._pool_id}_filtration_interval3_to"

    @property
    def native_value(self):
        value = (
            self.coordinator.data.get("filtration", {})
                .get("interval3", {})
                .get("to", None)
        )
        return intervalTime(value)

class S_FiltrationIntelTimeSensor(S_FiltrationSensorBase):
    def __init__(self, coordinator):
        super().__init__(coordinator)
        self._attr_name = "Filtration Intel Time"
        self._attr_unique_id = f"s_{coordinator.api._pool_id}_filtration_intel_time"

    @property
    def native_value(self):
        return (
            self.coordinator.data.get("filtration", {})
                .get("intel", {})
                .get("time", None)
        )


class S_FiltrationIntelTempSensor(S_FiltrationSensorBase):
    def __init__(self, coordinator):
        super().__init__(coordinator)
        self._attr_name = "Filtration Intel Temp"
        self._attr_unique_id = f"s_{coordinator.api._pool_id}_filtration_intel_temp"

    @property
    def native_value(self):
        return (
            self.coordinator.data.get("filtration", {})
                .get("intel", {})
                .get("temp", None)
        )

class S_FiltrationTimerVel2Sensor(S_FiltrationSensorBase):
    def __init__(self, coordinator):
        super().__init__(coordinator)
        self._attr_name = "Filtration TimerVel2"
        self._attr_unique_id = f"s_{coordinator.api._pool_id}_filtration_timerVel2"

    @property
    def native_value(self):
        return self.coordinator.data.get("filtration", {}).get("timerVel2", None)

class S_FiltrationHasSmartSensor(S_FiltrationSensorBase):
    def __init__(self, coordinator):
        super().__init__(coordinator)
        self._attr_name = "Filtration hasSmart"
        self._attr_unique_id = f"s_{coordinator.api._pool_id}_filtration_hasSmart"

    @property
    def native_value(self):
        value = self.coordinator.data.get("filtration", {}).get("hasSmart", None)
        return TRUE_FALSE_NAMES.get(value, "unknown")

class S_FiltrationHeatingTempSensor(S_FiltrationSensorBase):
    def __init__(self, coordinator):
        super().__init__(coordinator)
        self._attr_name = "Filtration Heating Temp"
        self._attr_unique_id = f"s_{coordinator.api._pool_id}_filtration_heating_temp"

    @property
    def native_value(self):
        return (
            self.coordinator.data.get("filtration", {})
                .get("heating", {})
                .get("temp", None)
        )

class S_FiltrationHeatingClimaSensor(S_FiltrationSensorBase):
    def __init__(self, coordinator):
        super().__init__(coordinator)
        self._attr_name = "Filtration Heating Clima"
        self._attr_unique_id = f"s_{coordinator.api._pool_id}_filtration_heating_clima"

    @property
    def native_value(self):
        return (
            self.coordinator.data.get("filtration", {})
                .get("heating", {})
                .get("clima", None)
        )

class S_FiltrationHeatingTempHiSensor(S_FiltrationSensorBase):
    def __init__(self, coordinator):
        super().__init__(coordinator)
        self._attr_name = "Filtration Heating TempHi"
        self._attr_unique_id = f"s_{coordinator.api._pool_id}_filtration_heating_tempHi"

    @property
    def native_value(self):
        return (
            self.coordinator.data.get("filtration", {})
                .get("heating", {})
                .get("tempHi", None)
        )

class S_FiltrationManVelSensor(S_FiltrationSensorBase):
    def __init__(self, coordinator):
        super().__init__(coordinator)
        self._attr_name = "Filtration manVel"
        self._attr_unique_id = f"s_{coordinator.api._pool_id}_filtration_manVel"

    @property
    def native_value(self):
        return self.coordinator.data.get("filtration", {}).get("manVel", None)

class S_FiltrationHasHeatSensor(S_FiltrationSensorBase):
    def __init__(self, coordinator):
        super().__init__(coordinator)
        self._attr_name = "Filtration hasHeat"
        self._attr_unique_id = f"s_{coordinator.api._pool_id}_filtration_hasHeat"

    @property
    def native_value(self):
        value = self.coordinator.data.get("filtration", {}).get("hasHeat", None)
        return TRUE_FALSE_NAMES.get(value, "unknown")

class S_FiltrationPumpTypeSensor(S_FiltrationSensorBase):
    def __init__(self, coordinator):
        super().__init__(coordinator)
        self._attr_name = "Filtration pumpType"
        self._attr_unique_id = f"s_{coordinator.api._pool_id}_filtration_pumpType"

    @property
    def native_value(self):
        return self.coordinator.data.get("filtration", {}).get("pumpType", None)

class S_FiltrationTimerVel3Sensor(S_FiltrationSensorBase):
    def __init__(self, coordinator):
        super().__init__(coordinator)
        self._attr_name = "Filtration timerVel3"
        self._attr_unique_id = f"s_{coordinator.api._pool_id}_filtration_timerVel3"

    @property
    def native_value(self):
        return self.coordinator.data.get("filtration", {}).get("timerVel3", None)

class S_FiltrationStatusSensor(S_FiltrationSensorBase):
    def __init__(self, coordinator):
        super().__init__(coordinator)
        self._attr_name = "Filtration Status"
        self._attr_unique_id = f"s_{coordinator.api._pool_id}_filtration_status"

    @property
    def native_value(self):
        value = self.coordinator.data.get("filtration", {}).get("status", None)
        return FILTRATION_STATUS_NAMES.get(value, "unknown")

class S_FiltrationTimerVel1Sensor(S_FiltrationSensorBase):
    def __init__(self, coordinator):
        super().__init__(coordinator)
        self._attr_name = "Filtration timerVel1"
        self._attr_unique_id = f"s_{coordinator.api._pool_id}_filtration_timerVel1"

    @property
    def native_value(self):
        return self.coordinator.data.get("filtration", {}).get("timerVel1", None)

class S_FiltrationModeSensor(S_FiltrationSensorBase):
    def __init__(self, coordinator):
        super().__init__(coordinator)
        self._attr_name = "Filtration Mode"
        self._attr_unique_id = f"s_{coordinator.api._pool_id}_filtration_mode"

    @property
    def native_value(self):
        value = self.coordinator.data.get("filtration", {}).get("mode", None)
        return FILTRATION_MODE_NAMES.get(value, "unknown")

class S_FiltrationSmartTempMinSensor(S_FiltrationSensorBase):
    def __init__(self, coordinator):
        super().__init__(coordinator)
        self._attr_name = "Filtration Smart tempMin"
        self._attr_unique_id = f"s_{coordinator.api._pool_id}_filtration_smart_tempMin"

    @property
    def native_value(self):
        return (
            self.coordinator.data.get("filtration", {})
                .get("smart", {})
                .get("tempMin", None)
        )

class S_FiltrationSmartTempHighSensor(S_FiltrationSensorBase):
    def __init__(self, coordinator):
        super().__init__(coordinator)
        self._attr_name = "Filtration Smart tempHigh"
        self._attr_unique_id = f"s_{coordinator.api._pool_id}_filtration_smart_tempHigh"

    @property
    def native_value(self):
        return (
            self.coordinator.data.get("filtration", {})
                .get("smart", {})
                .get("tempHigh", None)
        )

class S_FiltrationSmartFreezeSensor(S_FiltrationSensorBase):
    def __init__(self, coordinator):
        super().__init__(coordinator)
        self._attr_name = "Filtration Smart freeze"
        self._attr_unique_id = f"s_{coordinator.api._pool_id}_filtration_smart_freeze"

    @property
    def native_value(self):
        return (
            self.coordinator.data.get("filtration", {})
                .get("smart", {})
                .get("freeze", None)
        )

#
# --------------- MAIN KEYS ---------------
#

class S_MainSensorBase(CoordinatorEntity, SensorEntity):
    """Keys in data['main']"""
    async def async_added_to_hass(self):
        await super().async_added_to_hass()
        self.async_on_remove(
            self.coordinator.async_add_listener(self.async_write_ha_state)
        )

    @property
    def device_info(self):
        return {
            "identifiers": {(DOMAIN, f'{self.coordinator.api._pool_id}_main')},
            "name": "Algemeen (Main)",
            "manufacturer": "Vistapool",
            "model": "Vistapool Controller"
        }

class S_MainHasIOSensor(S_MainSensorBase):
    """Reads main.hasIO."""
    def __init__(self, coordinator):
        super().__init__(coordinator)
        self._attr_name = "Has IO (Main)"
        self._attr_unique_id = f"s_{coordinator.api._pool_id}_main_hasIO"

    @property
    def native_value(self):
        value = self.coordinator.data.get("main", {}).get("hasIO", None)
        return TRUE_FALSE_NAMES.get(value, "unknown")

# De rest van alle main.* keys (hasUV, RSSI, hasLED, LEDPulse, etc.):

class S_MainHideRelaysSensor(S_MainSensorBase):
    def __init__(self, coordinator):
        super().__init__(coordinator)
        self._attr_name = "Hide Relays"
        self._attr_unique_id = f"s_{coordinator.api._pool_id}_main_hideRelays"

    @property
    def native_value(self):
        return self.coordinator.data.get("main", {}).get("hideRelays", None)

class S_MainHasUVSensor(S_MainSensorBase):
    def __init__(self, coordinator):
        super().__init__(coordinator)
        self._attr_name = "Has UV"
        self._attr_unique_id = f"s_{coordinator.api._pool_id}_main_hasUV"

    @property
    def native_value(self):
        value = self.coordinator.data.get("main", {}).get("hasUV", None)
        return TRUE_FALSE_NAMES.get(value, "unknown")

class S_MainRSSISensor(S_MainSensorBase):
    def __init__(self, coordinator):
        super().__init__(coordinator)
        self._attr_name = "Main RSSI"
        self._attr_unique_id = f"s_{coordinator.api._pool_id}_main_rssi"

    @property
    def native_value(self):
        return self.coordinator.data.get("main", {}).get("RSSI", None)

class S_MainHasLEDSensor(S_MainSensorBase):
    def __init__(self, coordinator):
        super().__init__(coordinator)
        self._attr_name = "Has LED"
        self._attr_unique_id = f"s_{coordinator.api._pool_id}_main_hasLED"

    @property
    def native_value(self):
        value = self.coordinator.data.get("main", {}).get("hasLED", None)
        return TRUE_FALSE_NAMES.get(value, "unknown")

class S_MainLEDPulseSensor(S_MainSensorBase):
    def __init__(self, coordinator):
        super().__init__(coordinator)
        self._attr_name = "LED Pulse"
        self._attr_unique_id = f"s_{coordinator.api._pool_id}_main_ledpulse"

    @property
    def native_value(self):
        return self.coordinator.data.get("main", {}).get("LEDPulse", None)

class S_MainHasLinkedAutoSensor(S_MainSensorBase):
    def __init__(self, coordinator):
        super().__init__(coordinator)
        self._attr_name = "Has LinkedAuto"
        self._attr_unique_id = f"s_{coordinator.api._pool_id}_main_hasLinkedAuto"

    @property
    def native_value(self):
        value = self.coordinator.data.get("main", {}).get("hasLinkedAuto", None)
        return TRUE_FALSE_NAMES.get(value, "unknown")

class S_MainHideTemperatureSensor(S_MainSensorBase):
    def __init__(self, coordinator):
        super().__init__(coordinator)
        self._attr_name = "Hide Temperature"
        self._attr_unique_id = f"s_{coordinator.api._pool_id}_main_hideTemperature"

    @property
    def native_value(self):
        return self.coordinator.data.get("main", {}).get("hideTemperature", None)

class S_MainHideLightingSensor(S_MainSensorBase):
    def __init__(self, coordinator):
        super().__init__(coordinator)
        self._attr_name = "Hide Lighting"
        self._attr_unique_id = f"s_{coordinator.api._pool_id}_main_hideLighting"

    @property
    def native_value(self):
        return self.coordinator.data.get("main", {}).get("hideLighting", None)

class S_MainFWUEnabledSensor(S_MainSensorBase):
    def __init__(self, coordinator):
        super().__init__(coordinator)
        self._attr_name = "FWU Enabled"
        self._attr_unique_id = f"s_{coordinator.api._pool_id}_main_FWU_enabled"

    @property
    def native_value(self):
        return self.coordinator.data.get("main", {}).get("FWU_enabled", None)

class S_MainNetworkPresentSensor(S_MainSensorBase):
    def __init__(self, coordinator):
        super().__init__(coordinator)
        self._attr_name = "Network Present"
        self._attr_unique_id = f"s_{coordinator.api._pool_id}_main_networkPresent"

    @property
    def native_value(self):
        return self.coordinator.data.get("main", {}).get("networkPresent", None)

class S_MainVersionSensor(S_MainSensorBase):
    def __init__(self, coordinator):
        super().__init__(coordinator)
        self._attr_name = "Main Version"
        self._attr_unique_id = f"s_{coordinator.api._pool_id}_main_version"

    @property
    def native_value(self):
        return self.coordinator.data.get("main", {}).get("version", None)

class S_MainHasPHSensor(S_MainSensorBase):
    def __init__(self, coordinator):
        super().__init__(coordinator)
        self._attr_name = "Has pH"
        self._attr_unique_id = f"s_{coordinator.api._pool_id}_main_hasPH"

    @property
    def native_value(self):
        value = self.coordinator.data.get("main", {}).get("hasPH", None)
        return TRUE_FALSE_NAMES.get(value, "unknown")

class S_MainHasBackwashSensor(S_MainSensorBase):
    def __init__(self, coordinator):
        super().__init__(coordinator)
        self._attr_name = "Has Backwash"
        self._attr_unique_id = f"s_{coordinator.api._pool_id}_main_hasBackwash"

    @property
    def native_value(self):
        value = self.coordinator.data.get("main", {}).get("hasBackwash", None)
        return TRUE_FALSE_NAMES.get(value, "unknown")

class S_MainHasWifiSensor(S_MainSensorBase):
    def __init__(self, coordinator):
        super().__init__(coordinator)
        self._attr_name = "Has Wifi"
        self._attr_unique_id = f"s_{coordinator.api._pool_id}_main_hasWifi"

    @property
    def native_value(self):
        value = self.coordinator.data.get("main", {}).get("hasWifi", None)
        return TRUE_FALSE_NAMES.get(value, "unknown")

class S_MainHasCDSensor(S_MainSensorBase):
    def __init__(self, coordinator):
        super().__init__(coordinator)
        self._attr_name = "Has CD"
        self._attr_unique_id = f"s_{coordinator.api._pool_id}_main_hasCD"

    @property
    def native_value(self):
        value = self.coordinator.data.get("main", {}).get("hasCD", None)
        return TRUE_FALSE_NAMES.get(value, "unknown")

class S_MainHideFiltrationSensor(S_MainSensorBase):
    def __init__(self, coordinator):
        super().__init__(coordinator)
        self._attr_name = "Hide Filtration"
        self._attr_unique_id = f"s_{coordinator.api._pool_id}_main_hideFiltration"

    @property
    def native_value(self):
        return self.coordinator.data.get("main", {}).get("hideFiltration", None)

class S_MainHasCLSensor(S_MainSensorBase):
    def __init__(self, coordinator):
        super().__init__(coordinator)
        self._attr_name = "Has CL"
        self._attr_unique_id = f"s_{coordinator.api._pool_id}_main_hasCL"

    @property
    def native_value(self):
        value = self.coordinator.data.get("main", {}).get("hasCL", None)
        return TRUE_FALSE_NAMES.get(value, "unknown")

class S_MainHasRXSensor(S_MainSensorBase):
    def __init__(self, coordinator):
        super().__init__(coordinator)
        self._attr_name = "Has RX"
        self._attr_unique_id = f"s_{coordinator.api._pool_id}_main_hasRX"

    @property
    def native_value(self):
        value = self.coordinator.data.get("main", {}).get("hasRX", None)
        return TRUE_FALSE_NAMES.get(value, "unknown")

class S_MainTemperatureSensor(S_MainSensorBase):
    def __init__(self, coordinator):
        super().__init__(coordinator)
        self._attr_name = "Main Temperature"
        self._attr_unique_id = f"s_{coordinator.api._pool_id}_main_temperature"
        self._attr_native_unit_of_measurement = UnitOfTemperature.CELSIUS

    @property
    def native_value(self):
        return self.coordinator.data.get("main", {}).get("temperature", None)

class S_MainWifiVersionSensor(S_MainSensorBase):
    def __init__(self, coordinator):
        super().__init__(coordinator)
        self._attr_name = "Wifi Version"
        self._attr_unique_id = f"s_{coordinator.api._pool_id}_main_wifiVersion"

    @property
    def native_value(self):
        return self.coordinator.data.get("main", {}).get("wifiVersion", None)

class S_MainLocalTimeSensor(S_MainSensorBase):
    def __init__(self, coordinator):
        super().__init__(coordinator)
        self._attr_name = "Local Time"
        self._attr_unique_id = f"s_{coordinator.api._pool_id}_main_localTime"

    @property
    def native_value(self):
        value =  self.coordinator.data.get("main", {}).get("localTime", None)
        return datetime.fromtimestamp(value)

class S_MainHasLinkedSensor(S_MainSensorBase):
    def __init__(self, coordinator):
        super().__init__(coordinator)
        self._attr_name = "Has Linked"
        self._attr_unique_id = f"s_{coordinator.api._pool_id}_main_hasLinked"

    @property
    def native_value(self):
        value = self.coordinator.data.get("main", {}).get("hasLinked", None)
        return TRUE_FALSE_NAMES.get(value, "unknown")

class S_MainHasHidroSensor(S_MainSensorBase):
    def __init__(self, coordinator):
        super().__init__(coordinator)
        self._attr_name = "Has Hidro"
        self._attr_unique_id = f"s_{coordinator.api._pool_id}_main_hasHidro"

    @property
    def native_value(self):
        value = self.coordinator.data.get("main", {}).get("hasHidro", None)
        return TRUE_FALSE_NAMES.get(value, "unknown")

#
# --------------- MODULES ---------------
#

class S_ModulesSensorBase(CoordinatorEntity, SensorEntity):
    async def async_added_to_hass(self):
        await super().async_added_to_hass()
        self.async_on_remove(
            self.coordinator.async_add_listener(self.async_write_ha_state)
        )

    @property
    def device_info(self):
        return {
            "identifiers": {(DOMAIN, f'{self.coordinator.api._pool_id}_modules')},
            "name": "Modules",
            "manufacturer": "Vistapool",
            "model": "Vistapool Controller"
        }


class S_ModulesRxPumpStatusSensor(S_ModulesSensorBase):
    def __init__(self, coordinator):
        super().__init__(coordinator)
        self._attr_name = "Modules rx pump_status"
        self._attr_unique_id = f"s_{coordinator.api._pool_id}_modules_rx_pump_status"

    @property
    def native_value(self):
        return (
            self.coordinator.data.get("modules", {})
                .get("rx", {})
                .get("pump_status", None)
        )

class S_ModulesRxCurrentSensor(S_ModulesSensorBase):
    def __init__(self, coordinator):
        super().__init__(coordinator)
        self._attr_name = "Modules rx current"
        self._attr_unique_id = f"s_{coordinator.api._pool_id}_modules_rx_current"

    @property
    def native_value(self):
        return (
            self.coordinator.data.get("modules", {})
                .get("rx", {})
                .get("current", None)
        )

class S_ModulesRxTankSensor(S_ModulesSensorBase):
    def __init__(self, coordinator):
        super().__init__(coordinator)
        self._attr_name = "Modules rx tank"
        self._attr_unique_id = f"s_{coordinator.api._pool_id}_modules_rx_tank"

    @property
    def native_value(self):
        return (
            self.coordinator.data.get("modules", {})
                .get("rx", {})
                .get("tank", None)
        )

class S_ModulesRxStatusValueSensor(S_ModulesSensorBase):
    def __init__(self, coordinator):
        super().__init__(coordinator)
        self._attr_name = "Modules rx status.value"
        self._attr_unique_id = f"s_{coordinator.api._pool_id}_modules_rx_status_value"

    @property
    def native_value(self):
        status = (
            self.coordinator.data.get("modules", {})
                .get("rx", {})
                .get("status", {})
        )
        return status.get("value", None)


#
# modules.ph
#
class S_ModulesPhTypeSensor(S_ModulesSensorBase):
    def __init__(self, coordinator):
        super().__init__(coordinator)
        self._attr_name = "Modules ph type"
        self._attr_unique_id = f"s_{coordinator.api._pool_id}_modules_ph_type"

    @property
    def native_value(self):
        return (
            self.coordinator.data.get("modules", {})
                .get("ph", {})
                .get("type", None)
        )

class S_ModulesPhTankSensor(S_ModulesSensorBase):
    def __init__(self, coordinator):
        super().__init__(coordinator)
        self._attr_name = "Modules ph tank"
        self._attr_unique_id = f"s_{coordinator.api._pool_id}_modules_ph_tank"

    @property
    def native_value(self):
        return (
            self.coordinator.data.get("modules", {})
                .get("ph", {})
                .get("tank", None)
        )

class S_ModulesPhCurrentSensor(S_ModulesSensorBase):
    def __init__(self, coordinator):
        super().__init__(coordinator)
        self._attr_name = "Modules ph current"
        self._attr_unique_id = f"s_{coordinator.api._pool_id}_modules_ph_current"

    @property
    def native_value(self):
        return (
            self.coordinator.data.get("modules", {})
                .get("ph", {})
                .get("current", None)
        )

class S_ModulesPhPumpHighOnSensor(S_ModulesSensorBase):
    def __init__(self, coordinator):
        super().__init__(coordinator)
        self._attr_name = "Modules ph pump_high_on"
        self._attr_unique_id = f"s_{coordinator.api._pool_id}_modules_ph_pump_high_on"

    @property
    def native_value(self):
        return (
            self.coordinator.data.get("modules", {})
                .get("ph", {})
                .get("pump_high_on", None)
        )

class S_ModulesPhStatusHighValueSensor(S_ModulesSensorBase):
    def __init__(self, coordinator):
        super().__init__(coordinator)
        self._attr_name = "Modules ph status.high_value"
        self._attr_unique_id = f"s_{coordinator.api._pool_id}_modules_ph_status_high_value"

    @property
    def native_value(self):
        stat = (
            self.coordinator.data.get("modules", {})
                .get("ph", {})
                .get("status", {})
        )
        return stat.get("high_value", None)

class S_ModulesPhStatusLowValueSensor(S_ModulesSensorBase):
    def __init__(self, coordinator):
        super().__init__(coordinator)
        self._attr_name = "Modules ph status.low_value"
        self._attr_unique_id = f"s_{coordinator.api._pool_id}_modules_ph_status_low_value"

    @property
    def native_value(self):
        stat = (
            self.coordinator.data.get("modules", {})
                .get("ph", {})
                .get("status", {})
        )
        return stat.get("low_value", None)

class S_ModulesPhAl3Sensor(S_ModulesSensorBase):
    def __init__(self, coordinator):
        super().__init__(coordinator)
        self._attr_name = "Modules ph al3"
        self._attr_unique_id = f"s_{coordinator.api._pool_id}_modules_ph_al3"

    @property
    def native_value(self):
        return (
            self.coordinator.data.get("modules", {})
                .get("ph", {})
                .get("al3", None)
        )

class S_ModulesPhPumpLowOnSensor(S_ModulesSensorBase):
    def __init__(self, coordinator):
        super().__init__(coordinator)
        self._attr_name = "Modules ph pump_low_on"
        self._attr_unique_id = f"s_{coordinator.api._pool_id}_modules_ph_pump_low_on"

    @property
    def native_value(self):
        return (
            self.coordinator.data.get("modules", {})
                .get("ph", {})
                .get("pump_low_on", None)
        )

#
# modules.cl
#
class S_ModulesClPumpStatusSensor(S_ModulesSensorBase):
    def __init__(self, coordinator):
        super().__init__(coordinator)
        self._attr_name = "Modules cl pump_status"
        self._attr_unique_id = f"s_{coordinator.api._pool_id}_modules_cl_pump_status"

    @property
    def native_value(self):
        return (
            self.coordinator.data.get("modules", {})
                .get("cl", {})
                .get("pump_status", None)
        )

class S_ModulesClCurrentSensor(S_ModulesSensorBase):
    def __init__(self, coordinator):
        super().__init__(coordinator)
        self._attr_name = "Modules cl current"
        self._attr_unique_id = f"s_{coordinator.api._pool_id}_modules_cl_current"

    @property
    def native_value(self):
        return (
            self.coordinator.data.get("modules", {})
                .get("cl", {})
                .get("current", None)
        )

class S_ModulesClStatusValueSensor(S_ModulesSensorBase):
    def __init__(self, coordinator):
        super().__init__(coordinator)
        self._attr_name = "Modules cl status.value"
        self._attr_unique_id = f"s_{coordinator.api._pool_id}_modules_cl_status_value"

    @property
    def native_value(self):
        stat = (
            self.coordinator.data.get("modules", {})
                .get("cl", {})
                .get("status", {})
        )
        return stat.get("value", None)

class S_ModulesClTankSensor(S_ModulesSensorBase):
    def __init__(self, coordinator):
        super().__init__(coordinator)
        self._attr_name = "Modules cl tank"
        self._attr_unique_id = f"s_{coordinator.api._pool_id}_modules_cl_tank"

    @property
    def native_value(self):
        return (
            self.coordinator.data.get("modules", {})
                .get("cl", {})
                .get("tank", None)
        )

#
# modules.cd
#
class S_ModulesCdCurrentSensor(S_ModulesSensorBase):
    def __init__(self, coordinator):
        super().__init__(coordinator)
        self._attr_name = "Modules cd current"
        self._attr_unique_id = f"s_{coordinator.api._pool_id}_modules_cd_current"

    @property
    def native_value(self):
        return (
            self.coordinator.data.get("modules", {})
                .get("cd", {})
                .get("current", None)
        )

class S_ModulesCdStatusValueSensor(S_ModulesSensorBase):
    def __init__(self, coordinator):
        super().__init__(coordinator)
        self._attr_name = "Modules cd status.value"
        self._attr_unique_id = f"s_{coordinator.api._pool_id}_modules_cd_status_value"

    @property
    def native_value(self):
        stat = (
            self.coordinator.data.get("modules", {})
                .get("cd", {})
                .get("status", {})
        )
        return stat.get("value", None)

class S_ModulesCdTankSensor(S_ModulesSensorBase):
    def __init__(self, coordinator):
        super().__init__(coordinator)
        self._attr_name = "Modules cd tank"
        self._attr_unique_id = f"s_{coordinator.api._pool_id}_modules_cd_tank"

    @property
    def native_value(self):
        return (
            self.coordinator.data.get("modules", {})
                .get("cd", {})
                .get("tank", None)
        )

#
# modules.uv
#
class S_ModulesUvTotalSensor(S_ModulesSensorBase):
    def __init__(self, coordinator):
        super().__init__(coordinator)
        self._attr_name = "Modules uv total"
        self._attr_unique_id = f"s_{coordinator.api._pool_id}_modules_uv_total"

    @property
    def native_value(self):
        return (
            self.coordinator.data.get("modules", {})
                .get("uv", {})
                .get("total", None)
        )

class S_ModulesUvPartialSensor(S_ModulesSensorBase):
    def __init__(self, coordinator):
        super().__init__(coordinator)
        self._attr_name = "Modules uv partial"
        self._attr_unique_id = f"s_{coordinator.api._pool_id}_modules_uv_partial"

    @property
    def native_value(self):
        return (
            self.coordinator.data.get("modules", {})
                .get("uv", {})
                .get("partial", None)
        )

class S_ModulesUvStatusSensor(S_ModulesSensorBase):
    def __init__(self, coordinator):
        super().__init__(coordinator)
        self._attr_name = "Modules uv status"
        self._attr_unique_id = f"s_{coordinator.api._pool_id}_modules_uv_status"

    @property
    def native_value(self):
        return (
            self.coordinator.data.get("modules", {})
                .get("uv", {})
                .get("status", None)
        )

#
# modules.io
#
class S_ModulesIoActivationSensor(S_ModulesSensorBase):
    def __init__(self, coordinator):
        super().__init__(coordinator)
        self._attr_name = "Modules io activation"
        self._attr_unique_id = f"s_{coordinator.api._pool_id}_modules_io_activation"

    @property
    def native_value(self):
        return (
            self.coordinator.data.get("modules", {})
                .get("io", {})
                .get("activation", None)
        )

class S_ModulesIoStatusSensor(S_ModulesSensorBase):
    def __init__(self, coordinator):
        super().__init__(coordinator)
        self._attr_name = "Modules io status"
        self._attr_unique_id = f"s_{coordinator.api._pool_id}_modules_io_status"

    @property
    def native_value(self):
        return (
            self.coordinator.data.get("modules", {})
                .get("io", {})
                .get("status", None)
        )

class S_ModulesIoLevelSensor(S_ModulesSensorBase):
    def __init__(self, coordinator):
        super().__init__(coordinator)
        self._attr_name = "Modules io level"
        self._attr_unique_id = f"s_{coordinator.api._pool_id}_modules_io_level"

    @property
    def native_value(self):
        return (
            self.coordinator.data.get("modules", {})
                .get("io", {})
                .get("level", None)
        )

#
# --------------- RELAYS ---------------
#

class S_RelaysSensorBase(CoordinatorEntity, SensorEntity):
    async def async_added_to_hass(self):
        await super().async_added_to_hass()
        self.async_on_remove(
            self.coordinator.async_add_listener(self.async_write_ha_state)
        )

    @property
    def device_info(self):
        return {
            "identifiers": {(DOMAIN, f'{self.coordinator.api._pool_id}_relays')},
            "name": "Relays",
            "manufacturer": "Vistapool",
            "model": "Vistapool Controller"
        }

class S_RelaysFiltrationHeatingStatusSensor(S_RelaysSensorBase):
    def __init__(self, coordinator):
        super().__init__(coordinator)
        self._attr_name = "Relays Filtration Heating Status"
        self._attr_unique_id = f"s_{coordinator.api._pool_id}_relays_filtration_heating_status"

    @property
    def native_value(self):
        return (
            self.coordinator.data.get("relays", {})
                .get("filtration", {})
                .get("heating", {})
                .get("status", None)
        )

class S_RelaysFiltrationHeatingGpioSensor(S_RelaysSensorBase):
    def __init__(self, coordinator):
        super().__init__(coordinator)
        self._attr_name = "Relays Filtration Heating GPIO"
        self._attr_unique_id = f"s_{coordinator.api._pool_id}_relays_filtration_heating_gpio"

    @property
    def native_value(self):
        return (
            self.coordinator.data.get("relays", {})
                .get("filtration", {})
                .get("heating", {})
                .get("gpio", None)
        )

class S_RelaysFiltrationGpioSensor(S_RelaysSensorBase):
    def __init__(self, coordinator):
        super().__init__(coordinator)
        self._attr_name = "Relays Filtration GPIO"
        self._attr_unique_id = f"s_{coordinator.api._pool_id}_relays_filtration_gpio"

    @property
    def native_value(self):
        return (
            self.coordinator.data.get("relays", {})
                .get("filtration", {})
                .get("gpio", None)
        )

class S_RelaysBackwashGpioSensor(S_RelaysSensorBase):
    def __init__(self, coordinator):
        super().__init__(coordinator)
        self._attr_name = "Relays Backwash GPIO"
        self._attr_unique_id = f"s_{coordinator.api._pool_id}_relays_backwash_gpio"

    @property
    def native_value(self):
        return (
            self.coordinator.data.get("relays", {})
                .get("backwash", {})
                .get("gpio", None)
        )

class S_RelaysIoGpioSensor(S_RelaysSensorBase):
    def __init__(self, coordinator):
        super().__init__(coordinator)
        self._attr_name = "Relays IO GPIO"
        self._attr_unique_id = f"s_{coordinator.api._pool_id}_relays_io_gpio"

    @property
    def native_value(self):
        return (
            self.coordinator.data.get("relays", {})
                .get("io", {})
                .get("gpio", None)
        )

class S_RelaysRxGpioSensor(S_RelaysSensorBase):
    def __init__(self, coordinator):
        super().__init__(coordinator)
        self._attr_name = "Relays RX GPIO"
        self._attr_unique_id = f"s_{coordinator.api._pool_id}_relays_rx_gpio"

    @property
    def native_value(self):
        return (
            self.coordinator.data.get("relays", {})
                .get("rx", {})
                .get("gpio", None)
        )

class S_RelaysLightGpioSensor(S_RelaysSensorBase):
    def __init__(self, coordinator):
        super().__init__(coordinator)
        self._attr_name = "Relays Light GPIO"
        self._attr_unique_id = f"s_{coordinator.api._pool_id}_relays_light_gpio"

    @property
    def native_value(self):
        return (
            self.coordinator.data.get("relays", {})
                .get("light", {})
                .get("gpio", None)
        )

class S_RelaysClGpioSensor(S_RelaysSensorBase):
    def __init__(self, coordinator):
        super().__init__(coordinator)
        self._attr_name = "Relays Cl GPIO"
        self._attr_unique_id = f"s_{coordinator.api._pool_id}_relays_cl_gpio"

    @property
    def native_value(self):
        return (
            self.coordinator.data.get("relays", {})
                .get("cl", {})
                .get("gpio", None)
        )

class S_RelaysCdGpioSensor(S_RelaysSensorBase):
    def __init__(self, coordinator):
        super().__init__(coordinator)
        self._attr_name = "Relays Cd GPIO"
        self._attr_unique_id = f"s_{coordinator.api._pool_id}_relays_cd_gpio"

    @property
    def native_value(self):
        return (
            self.coordinator.data.get("relays", {})
                .get("cd", {})
                .get("gpio", None)
        )

class S_RelaysPhAcidGpioSensor(S_RelaysSensorBase):
    def __init__(self, coordinator):
        super().__init__(coordinator)
        self._attr_name = "Relays pH acid GPIO"
        self._attr_unique_id = f"s_{coordinator.api._pool_id}_relays_ph_acid_gpio"

    @property
    def native_value(self):
        return (
            self.coordinator.data.get("relays", {})
                .get("ph", {})
                .get("acid", {})
                .get("gpio", None)
        )

class S_RelaysPhBaseGpioSensor(S_RelaysSensorBase):
    def __init__(self, coordinator):
        super().__init__(coordinator)
        self._attr_name = "Relays pH base GPIO"
        self._attr_unique_id = f"s_{coordinator.api._pool_id}_relays_ph_base_gpio"

    @property
    def native_value(self):
        return (
            self.coordinator.data.get("relays", {})
                .get("ph", {})
                .get("base", {})
                .get("gpio", None)
        )

class S_RelaysUvGpioSensor(S_RelaysSensorBase):
    def __init__(self, coordinator):
        super().__init__(coordinator)
        self._attr_name = "Relays UV GPIO"
        self._attr_unique_id = f"s_{coordinator.api._pool_id}_relays_uv_gpio"

    @property
    def native_value(self):
        return (
            self.coordinator.data.get("relays", {})
                .get("uv", {})
                .get("gpio", None)
        )

class S_RelaysRelay4NameSensor(S_RelaysSensorBase):
    def __init__(self, coordinator):
        super().__init__(coordinator)
        self._attr_name = "Relay4 Name"
        self._attr_unique_id = f"s_{coordinator.api._pool_id}_relays_relay4_name"

    @property
    def native_value(self):
        return (
            self.coordinator.data.get("relays", {})
                .get("relay4", {})
                .get("name", None)
        )

class S_RelaysRelay4InfoFromSensor(S_RelaysSensorBase):
    def __init__(self, coordinator):
        super().__init__(coordinator)
        self._attr_name = "Relay4 Info From"
        self._attr_unique_id = f"s_{coordinator.api._pool_id}_relays_relay4_info_from"

    @property
    def native_value(self):
        info = (
            self.coordinator.data.get("relays", {})
                .get("relay4", {})
                .get("info", {})
        )
        return info.get("from", None)

class S_RelaysRelay4InfoDelaySensor(S_RelaysSensorBase):
    def __init__(self, coordinator):
        super().__init__(coordinator)
        self._attr_name = "Relay4 Info Delay"
        self._attr_unique_id = f"s_{coordinator.api._pool_id}_relays_relay4_info_delay"

    @property
    def native_value(self):
        info = (
            self.coordinator.data.get("relays", {})
                .get("relay4", {})
                .get("info", {})
        )
        return info.get("delay", None)

class S_RelaysRelay4InfoOnOffSensor(S_RelaysSensorBase):
    def __init__(self, coordinator):
        super().__init__(coordinator)
        self._attr_name = "Relay4 Info onoff"
        self._attr_unique_id = f"s_{coordinator.api._pool_id}_relays_relay4_info_onoff"

    @property
    def native_value(self):
        info = (
            self.coordinator.data.get("relays", {})
                .get("relay4", {})
                .get("info", {})
        )
        return info.get("onoff", None)

class S_RelaysRelay4InfoFreq2Sensor(S_RelaysSensorBase):
    def __init__(self, coordinator):
        super().__init__(coordinator)
        self._attr_name = "Relay4 Info freq2"
        self._attr_unique_id = f"s_{coordinator.api._pool_id}_relays_relay4_info_freq2"

    @property
    def native_value(self):
        info = (
            self.coordinator.data.get("relays", {})
                .get("relay4", {})
                .get("info", {})
        )
        return info.get("freq2", None)

class S_RelaysRelay4InfoManAutoTempSensor(S_RelaysSensorBase):
    def __init__(self, coordinator):
        super().__init__(coordinator)
        self._attr_name = "Relay4 Info manAutoTemp"
        self._attr_unique_id = f"s_{coordinator.api._pool_id}_relays_relay4_info_manAutoTemp"

    @property
    def native_value(self):
        info = (
            self.coordinator.data.get("relays", {})
                .get("relay4", {})
                .get("info", {})
        )
        return info.get("manAutoTemp", None)

class S_RelaysRelay4InfoSignalSensor(S_RelaysSensorBase):
    def __init__(self, coordinator):
        super().__init__(coordinator)
        self._attr_name = "Relay4 Info signal"
        self._attr_unique_id = f"s_{coordinator.api._pool_id}_relays_relay4_info_signal"

    @property
    def native_value(self):
        info = (
            self.coordinator.data.get("relays", {})
                .get("relay4", {})
                .get("info", {})
        )
        return info.get("signal", None)

class S_RelaysRelay4InfoFrom2Sensor(S_RelaysSensorBase):
    def __init__(self, coordinator):
        super().__init__(coordinator)
        self._attr_name = "Relay4 Info from2"
        self._attr_unique_id = f"s_{coordinator.api._pool_id}_relays_relay4_info_from2"

    @property
    def native_value(self):
        info = (
            self.coordinator.data.get("relays", {})
                .get("relay4", {})
                .get("info", {})
        )
        return info.get("from2", None)

class S_RelaysRelay4InfoPolaritySensor(S_RelaysSensorBase):
    def __init__(self, coordinator):
        super().__init__(coordinator)
        self._attr_name = "Relay4 Info polarity"
        self._attr_unique_id = f"s_{coordinator.api._pool_id}_relays_relay4_info_polarity"

    @property
    def native_value(self):
        info = (
            self.coordinator.data.get("relays", {})
                .get("relay4", {})
                .get("info", {})
        )
        return info.get("polarity", None)

class S_RelaysRelay4InfoStatusSensor(S_RelaysSensorBase):
    def __init__(self, coordinator):
        super().__init__(coordinator)
        self._attr_name = "Relay4 Info status"
        self._attr_unique_id = f"s_{coordinator.api._pool_id}_relays_relay4_info_status"

    @property
    def native_value(self):
        info = (
            self.coordinator.data.get("relays", {})
                .get("relay4", {})
                .get("info", {})
        )
        return info.get("status", None)

class S_RelaysRelay4InfoFreqSensor(S_RelaysSensorBase):
    def __init__(self, coordinator):
        super().__init__(coordinator)
        self._attr_name = "Relay4 Info freq"
        self._attr_unique_id = f"s_{coordinator.api._pool_id}_relays_relay4_info_freq"

    @property
    def native_value(self):
        info = (
            self.coordinator.data.get("relays", {})
                .get("relay4", {})
                .get("info", {})
        )
        return info.get("freq", None)

class S_RelaysRelay4InfoToSensor(S_RelaysSensorBase):
    def __init__(self, coordinator):
        super().__init__(coordinator)
        self._attr_name = "Relay4 Info to"
        self._attr_unique_id = f"s_{coordinator.api._pool_id}_relays_relay4_info_to"

    @property
    def native_value(self):
        info = (
            self.coordinator.data.get("relays", {})
                .get("relay4", {})
                .get("info", {})
        )
        return info.get("to", None)

class S_RelaysRelay4InfoTo2Sensor(S_RelaysSensorBase):
    def __init__(self, coordinator):
        super().__init__(coordinator)
        self._attr_name = "Relay4 Info to2"
        self._attr_unique_id = f"s_{coordinator.api._pool_id}_relays_relay4_info_to2"

    @property
    def native_value(self):
        info = (
            self.coordinator.data.get("relays", {})
                .get("relay4", {})
                .get("info", {})
        )
        return info.get("to2", None)

class S_RelaysRelay4InfoTiempoOnSensor(S_RelaysSensorBase):
    def __init__(self, coordinator):
        super().__init__(coordinator)
        self._attr_name = "Relay4 Info tiempoOn"
        self._attr_unique_id = f"s_{coordinator.api._pool_id}_relays_relay4_info_tiempoOn"

    @property
    def native_value(self):
        info = (
            self.coordinator.data.get("relays", {})
                .get("relay4", {})
                .get("info", {})
        )
        return info.get("tiempoOn", None)

class S_RelaysRelay4InfoKeySensor(S_RelaysSensorBase):
    def __init__(self, coordinator):
        super().__init__(coordinator)
        self._attr_name = "Relay4 Info key"
        self._attr_unique_id = f"s_{coordinator.api._pool_id}_relays_relay4_info_key"

    @property
    def native_value(self):
        info = (
            self.coordinator.data.get("relays", {})
                .get("relay4", {})
                .get("info", {})
        )
        return info.get("key", None)

class S_RelaysRelay1NameSensor(S_RelaysSensorBase):
    def __init__(self, coordinator):
        super().__init__(coordinator)
        self._attr_name = "Relay1 Name"
        self._attr_unique_id = f"s_{coordinator.api._pool_id}_relays_relay1_name"

    @property
    def native_value(self):
        return (
            self.coordinator.data.get("relays", {})
                .get("relay1", {})
                .get("name", None)
        )

class S_RelaysRelay2NameSensor(S_RelaysSensorBase):
    def __init__(self, coordinator):
        super().__init__(coordinator)
        self._attr_name = "Relay2 Name"
        self._attr_unique_id = f"s_{coordinator.api._pool_id}_relays_relay2_name"

    @property
    def native_value(self):
        return (
            self.coordinator.data.get("relays", {})
                .get("relay2", {})
                .get("name", None)
        )

class S_RelaysRelay3NameSensor(S_RelaysSensorBase):
    def __init__(self, coordinator):
        super().__init__(coordinator)
        self._attr_name = "Relay3 Name"
        self._attr_unique_id = f"s_{coordinator.api._pool_id}_relays_relay3_name"

    @property
    def native_value(self):
        return (
            self.coordinator.data.get("relays", {})
                .get("relay3", {})
                .get("name", None)
        )

#
# ============ FORM KEYS ============
#

class S_FormSensorBase(CoordinatorEntity, SensorEntity):
    async def async_added_to_hass(self):
        await super().async_added_to_hass()
        self.async_on_remove(
            self.coordinator.async_add_listener(self.async_write_ha_state)
        )

    @property
    def device_info(self):
        return {
            "identifiers": {(DOMAIN, f"{self.coordinator.api._pool_id}_form")},
            "name": "Form",
            "manufacturer": "Vistapool",
            "model": "Vistapool Controller"
        }

class S_FormLngSensor(S_FormSensorBase):
    def __init__(self, coordinator):
        super().__init__(coordinator)
        self._attr_name = "Form lng"
        self._attr_unique_id = f"s_{coordinator.api._pool_id}_form_lng"

    @property
    def native_value(self):
        return self.coordinator.data.get("form", {}).get("lng", None)

class S_FormCountrySensor(S_FormSensorBase):
    def __init__(self, coordinator):
        super().__init__(coordinator)
        self._attr_name = "Form country"
        self._attr_unique_id = f"s_{coordinator.api._pool_id}_form_country"

    @property
    def native_value(self):
        return self.coordinator.data.get("form", {}).get("country", None)

class S_FormCitySensor(S_FormSensorBase):
    def __init__(self, coordinator):
        super().__init__(coordinator)
        self._attr_name = "Form city"
        self._attr_unique_id = f"s_{coordinator.api._pool_id}_form_city"

    @property
    def native_value(self):
        return self.coordinator.data.get("form", {}).get("city", None)

class S_FormNameSensor(S_FormSensorBase):
    def __init__(self, coordinator):
        super().__init__(coordinator)
        self._attr_name = "Form name"
        self._attr_unique_id = f"s_{coordinator.api._pool_id}_form_name"

    @property
    def native_value(self):
        return self.coordinator.data.get("form", {}).get("name", None)

class S_FormZipcodeSensor(S_FormSensorBase):
    def __init__(self, coordinator):
        super().__init__(coordinator)
        self._attr_name = "Form zipcode"
        self._attr_unique_id = f"s_{coordinator.api._pool_id}_form_zipcode"

    @property
    def native_value(self):
        return self.coordinator.data.get("form", {}).get("zipcode", None)

class S_FormLatSensor(S_FormSensorBase):
    def __init__(self, coordinator):
        super().__init__(coordinator)
        self._attr_name = "Form lat"
        self._attr_unique_id = f"s_{coordinator.api._pool_id}_form_lat"

    @property
    def native_value(self):
        return self.coordinator.data.get("form", {}).get("lat", None)

class S_FormStreetSensor(S_FormSensorBase):
    def __init__(self, coordinator):
        super().__init__(coordinator)
        self._attr_name = "Form street"
        self._attr_unique_id = f"s_{coordinator.api._pool_id}_form_street"

    @property
    def native_value(self):
        return self.coordinator.data.get("form", {}).get("street", None)
