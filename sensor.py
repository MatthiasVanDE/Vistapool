import logging
from homeassistant.components.sensor import SensorEntity
from homeassistant.helpers.update_coordinator import CoordinatorEntity
from homeassistant.const import UnitOfTemperature
from .const import DOMAIN

_LOGGER = logging.getLogger(__name__)

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

    async_add_entities(sensors)


#
# ==================== HELPER FOR RELAY INFO ====================
#

def make_s_relay_info_sensors(coordinator, relay_number: int):
    """
    Hulpfunctie die de SensorEntity's voor relays.relay{N}.info.* teruggeeft,
    met s_ prefix in de Unique ID.
    """
    base = f"relay{relay_number}"
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
        # extra 's_' prefix in unique_id
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
        info = (data.get("relays", {})
                    .get(f"relay{self._relay_number}", {})
                    .get("info", {}))
        return info.get(self._field, None)


#
# ==================== EXAMPLE SENSOR CLASSES ====================
# Alles eronder is gewoon net als voorheen, maar met "s_" prefix
#

#
# --------------- GLOBAL / TOP-LEVEL ---------------
#

class S_GlobalSensorBase(CoordinatorEntity, SensorEntity):
    """Top-level info (isAWS, wifi, id, ...)."""
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
        return self.coordinator.data.get("updatedAt", None)


class S_GlobalCreatedAtSensor(S_GlobalSensorBase):
    def __init__(self, coordinator):
        super().__init__(coordinator)
        self._attr_name = "Created At"
        self._attr_unique_id = f"s_{coordinator.api._pool_id}_created_at"

    @property
    def native_value(self):
        return self.coordinator.data.get("createdAt", None)


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
    """backwash.* => Filtratie/Backwash device."""
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
        return self.coordinator.data.get("backwash", {}).get("mode", None)

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
        return self.coordinator.data.get("backwash", {}).get("status", None)

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
        return self.coordinator.data.get("backwash", {}).get("startAt", None)


#
# --------------- LIGHT ---------------
#

class S_LightSensorBase(CoordinatorEntity, SensorEntity):
    """light.* => Filtratie/Light device? Of separate 'Lighting' device."""
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
        return self.coordinator.data.get("light", {}).get("from", None)

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
        return self.coordinator.data.get("hidro", {}).get("hasHidroControl", None)

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
        return self.coordinator.data.get("filtration", {}) \
                   .get("interval1", {}) \
                   .get("from", None)

# ... enzovoort, exact zelfde code maar "s_" prefix in unique_id

class S_FiltrationInterval1ToSensor(S_FiltrationSensorBase):
    def __init__(self, coordinator):
        super().__init__(coordinator)
        self._attr_name = "Filtration Interval1 To"
        self._attr_unique_id = f"s_{coordinator.api._pool_id}_filtration_interval1_to"

    @property
    def native_value(self):
        return self.coordinator.data.get("filtration", {}) \
                   .get("interval1", {}) \
                   .get("to", None)

# Enzovoort voor interval2, interval3, etc.

class S_FiltrationIntelTimeSensor(S_FiltrationSensorBase):
    def __init__(self, coordinator):
        super().__init__(coordinator)
        self._attr_name = "Filtration Intel Time"
        self._attr_unique_id = f"s_{coordinator.api._pool_id}_filtration_intel_time"

    @property
    def native_value(self):
        return self.coordinator.data.get("filtration", {}) \
                   .get("intel", {}) \
                   .get("time", None)

# etc..


#
# --------------- MAIN ---------------
#
class S_MainSensorBase(CoordinatorEntity, SensorEntity):
    @property
    def device_info(self):
        return {
            "identifiers": {(DOMAIN, f"{self.coordinator.api._pool_id}_main")},
            "name": "Algemeen (Main)",
            "manufacturer": "Vistapool",
            "model": "Vistapool Controller"
        }

class S_MainHideRelaysSensor(S_MainSensorBase):
    def __init__(self, coordinator):
        super().__init__(coordinator)
        self._attr_name = "Hide Relays"
        self._attr_unique_id = f"s_{coordinator.api._pool_id}_main_hideRelays"

    @property
    def native_value(self):
        return self.coordinator.data.get("main", {}).get("hideRelays", None)


# ... etc. herhaal voor elk veld met "s_" prefix in unique_id


#
# --------------- MODULES ---------------
#
class S_ModulesSensorBase(CoordinatorEntity, SensorEntity):
    @property
    def device_info(self):
        return {
            "identifiers": {(DOMAIN, f"{self.coordinator.api._pool_id}_modules")},
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

# etc. Voor elk veld => s_ prefix

#
# --------------- RELAYS ---------------
#
class S_RelaysSensorBase(CoordinatorEntity, SensorEntity):
    @property
    def device_info(self):
        return {
            "identifiers": {(DOMAIN, f"{self.coordinator.api._pool_id}_relays")},
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

# ... etc for backwash, i.e. S_RelaysBackwashGpioSensor, etc.


#
# =============== RELAYS RELAY4 EXAMPLE ================
#
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

# etc. voor de rest van relay4.info.* velden

#
# =============== FORM KEYS ================
#
class S_FormSensorBase(CoordinatorEntity, SensorEntity):
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

# etc. herhaal voor city, name, zipcode, lat, street

