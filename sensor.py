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
    sensors.append(GlobalIsAWSSensor(coordinator))
    sensors.append(GlobalWifiSensor(coordinator))
    sensors.append(GlobalIdSensor(coordinator))
    sensors.append(GlobalCompanySensor(coordinator))
    sensors.append(GlobalUpdatedAtSensor(coordinator))
    sensors.append(GlobalCreatedAtSensor(coordinator))
    sensors.append(GlobalPresentSensor(coordinator))

    #
    # ============ BACKWASH KEYS ============
    #
    sensors.append(BackwashIntervalSensor(coordinator))
    sensors.append(BackwashModeSensor(coordinator))
    sensors.append(BackwashRemainingTimeSensor(coordinator))
    sensors.append(BackwashStatusSensor(coordinator))
    sensors.append(BackwashFrequencySensor(coordinator))
    sensors.append(BackwashStartAtSensor(coordinator))

    #
    # ============ LIGHT KEYS ============
    #
    sensors.append(LightModeSensor(coordinator))
    sensors.append(LightFreqSensor(coordinator))
    sensors.append(LightToSensor(coordinator))
    sensors.append(LightFromSensor(coordinator))
    sensors.append(LightStatusSensor(coordinator))

    #
    # ============ HIDRO KEYS ============
    #
    sensors.append(HidroClorationEnabledSensor(coordinator))
    sensors.append(HidroTemperatureEnabledSensor(coordinator))
    sensors.append(HidroControlSensor(coordinator))
    sensors.append(HidroFl1Sensor(coordinator))
    sensors.append(HidroTemperatureValueSensor(coordinator))
    sensors.append(HidroAl4Sensor(coordinator))
    sensors.append(HidroHasHidroControlSensor(coordinator))
    sensors.append(HidroCoverSensor(coordinator))
    sensors.append(HidroCurrentSensor(coordinator))
    sensors.append(HidroCellPartialTimeSensor(coordinator))
    sensors.append(HidroIsElectrolysisSensor(coordinator))
    sensors.append(HidroFl2Sensor(coordinator))
    sensors.append(HidroCellTotalTimeSensor(coordinator))
    sensors.append(HidroReductionSensor(coordinator))
    sensors.append(HidroLevelSensor(coordinator))
    sensors.append(HidroMaxAllowedValueSensor(coordinator))
    sensors.append(HidroLowSensor(coordinator))
    sensors.append(HidroCoverEnabledSensor(coordinator))
    sensors.append(HidroMeasureSensor(coordinator))

    #
    # ============ FILTRATION KEYS ============
    #
    sensors.append(FiltrationInterval1FromSensor(coordinator))
    sensors.append(FiltrationInterval1ToSensor(coordinator))
    sensors.append(FiltrationInterval2FromSensor(coordinator))
    sensors.append(FiltrationInterval2ToSensor(coordinator))
    sensors.append(FiltrationInterval3FromSensor(coordinator))
    sensors.append(FiltrationInterval3ToSensor(coordinator))

    sensors.append(FiltrationIntelTimeSensor(coordinator))
    sensors.append(FiltrationIntelTempSensor(coordinator))

    sensors.append(FiltrationTimerVel2Sensor(coordinator))
    sensors.append(FiltrationHasSmartSensor(coordinator))

    sensors.append(FiltrationHeatingTempSensor(coordinator))
    sensors.append(FiltrationHeatingClimaSensor(coordinator))
    sensors.append(FiltrationHeatingTempHiSensor(coordinator))

    sensors.append(FiltrationManVelSensor(coordinator))
    sensors.append(FiltrationHasHeatSensor(coordinator))
    sensors.append(FiltrationPumpTypeSensor(coordinator))
    sensors.append(FiltrationTimerVel3Sensor(coordinator))
    sensors.append(FiltrationStatusSensor(coordinator))
    sensors.append(FiltrationTimerVel1Sensor(coordinator))

    sensors.append(FiltrationModeSensor(coordinator))

    # Filtration.smart
    sensors.append(FiltrationSmartTempMinSensor(coordinator))
    sensors.append(FiltrationSmartTempHighSensor(coordinator))
    sensors.append(FiltrationSmartFreezeSensor(coordinator))

    #
    # ============ MAIN KEYS ============
    #
    sensors.append(MainHideRelaysSensor(coordinator))
    sensors.append(MainHasUVSensor(coordinator))
    sensors.append(MainRSSISensor(coordinator))
    sensors.append(MainHasLEDSensor(coordinator))
    sensors.append(MainLEDPulseSensor(coordinator))
    sensors.append(MainHasIOSensor(coordinator))
    sensors.append(MainHasLinkedAutoSensor(coordinator))
    sensors.append(MainHideTemperatureSensor(coordinator))
    sensors.append(MainHideLightingSensor(coordinator))
    sensors.append(MainFWUEnabledSensor(coordinator))
    sensors.append(MainNetworkPresentSensor(coordinator))
    sensors.append(MainVersionSensor(coordinator))
    sensors.append(MainHasPHSensor(coordinator))
    sensors.append(MainHasBackwashSensor(coordinator))
    sensors.append(MainHasWifiSensor(coordinator))
    sensors.append(MainHasCDSensor(coordinator))
    sensors.append(MainHideFiltrationSensor(coordinator))
    sensors.append(MainHasCLSensor(coordinator))
    sensors.append(MainHasRXSensor(coordinator))
    sensors.append(MainTemperatureSensor(coordinator))  # watertemp
    sensors.append(MainWifiVersionSensor(coordinator))
    sensors.append(MainLocalTimeSensor(coordinator))
    sensors.append(MainHasLinkedSensor(coordinator))
    sensors.append(MainHasHidroSensor(coordinator))

    #
    # ============ MODULES KEYS ============
    #
    # modules.rx
    sensors.append(ModulesRxPumpStatusSensor(coordinator))
    sensors.append(ModulesRxCurrentSensor(coordinator))
    sensors.append(ModulesRxTankSensor(coordinator))
    sensors.append(ModulesRxStatusValueSensor(coordinator))

    # modules.ph
    sensors.append(ModulesPhTypeSensor(coordinator))
    sensors.append(ModulesPhTankSensor(coordinator))
    sensors.append(ModulesPhCurrentSensor(coordinator))
    sensors.append(ModulesPhPumpHighOnSensor(coordinator))
    sensors.append(ModulesPhStatusHighValueSensor(coordinator))
    sensors.append(ModulesPhStatusLowValueSensor(coordinator))
    sensors.append(ModulesPhAl3Sensor(coordinator))
    sensors.append(ModulesPhPumpLowOnSensor(coordinator))

    # modules.cl
    sensors.append(ModulesClPumpStatusSensor(coordinator))
    sensors.append(ModulesClCurrentSensor(coordinator))
    sensors.append(ModulesClStatusValueSensor(coordinator))
    sensors.append(ModulesClTankSensor(coordinator))

    # modules.cd
    sensors.append(ModulesCdCurrentSensor(coordinator))
    sensors.append(ModulesCdStatusValueSensor(coordinator))
    sensors.append(ModulesCdTankSensor(coordinator))

    # modules.uv
    sensors.append(ModulesUvTotalSensor(coordinator))
    sensors.append(ModulesUvPartialSensor(coordinator))
    sensors.append(ModulesUvStatusSensor(coordinator))

    # modules.io
    sensors.append(ModulesIoActivationSensor(coordinator))
    sensors.append(ModulesIoStatusSensor(coordinator))
    sensors.append(ModulesIoLevelSensor(coordinator))

    #
    # ============ RELAYS KEYS ============
    #
    # relays.filtration
    sensors.append(RelaysFiltrationHeatingStatusSensor(coordinator))
    sensors.append(RelaysFiltrationHeatingGpioSensor(coordinator))
    sensors.append(RelaysFiltrationGpioSensor(coordinator))

    # relays.backwash
    sensors.append(RelaysBackwashGpioSensor(coordinator))

    # relays.io
    sensors.append(RelaysIoGpioSensor(coordinator))

    # relays.rx
    sensors.append(RelaysRxGpioSensor(coordinator))

    # relays.light
    sensors.append(RelaysLightGpioSensor(coordinator))

    # relays.cl
    sensors.append(RelaysClGpioSensor(coordinator))

    # relays.cd
    sensors.append(RelaysCdGpioSensor(coordinator))

    # relays.ph (acid/base)
    sensors.append(RelaysPhAcidGpioSensor(coordinator))
    sensors.append(RelaysPhBaseGpioSensor(coordinator))

    # relayX (1..4) + uv
    sensors.append(RelaysUvGpioSensor(coordinator))

    sensors.append(RelaysRelay4NameSensor(coordinator))
    sensors.append(RelaysRelay4InfoFromSensor(coordinator))
    sensors.append(RelaysRelay4InfoDelaySensor(coordinator))
    # ... en zo voort voor elk veld in relay4.info ...
    sensors.append(RelaysRelay4InfoOnOffSensor(coordinator))
    sensors.append(RelaysRelay4InfoFreq2Sensor(coordinator))
    sensors.append(RelaysRelay4InfoManAutoTempSensor(coordinator))
    sensors.append(RelaysRelay4InfoSignalSensor(coordinator))
    sensors.append(RelaysRelay4InfoFrom2Sensor(coordinator))
    sensors.append(RelaysRelay4InfoPolaritySensor(coordinator))
    sensors.append(RelaysRelay4InfoStatusSensor(coordinator))
    sensors.append(RelaysRelay4InfoFreqSensor(coordinator))
    sensors.append(RelaysRelay4InfoToSensor(coordinator))
    sensors.append(RelaysRelay4InfoTo2Sensor(coordinator))
    sensors.append(RelaysRelay4InfoTiempoOnSensor(coordinator))
    sensors.append(RelaysRelay4InfoKeySensor(coordinator))

    # relay1, relay2, relay3 -> name + info
    sensors.append(RelaysRelay1NameSensor(coordinator))
    sensors.extend(make_relay_info_sensors(coordinator, relay_number=1))
    sensors.append(RelaysRelay2NameSensor(coordinator))
    sensors.extend(make_relay_info_sensors(coordinator, relay_number=2))
    sensors.append(RelaysRelay3NameSensor(coordinator))
    sensors.extend(make_relay_info_sensors(coordinator, relay_number=3))

    #
    # ============ FORM KEYS ============
    #
    sensors.append(FormLngSensor(coordinator))
    sensors.append(FormCountrySensor(coordinator))
    sensors.append(FormCitySensor(coordinator))
    sensors.append(FormNameSensor(coordinator))
    sensors.append(FormZipcodeSensor(coordinator))
    sensors.append(FormLatSensor(coordinator))
    sensors.append(FormStreetSensor(coordinator))

    async_add_entities(sensors)


#
# ==================== HELPER FOR RELAY INFO ====================
#

def make_relay_info_sensors(coordinator, relay_number: int):
    """
    Hulpfunctie die de SensorEntity's voor relay{N}.info.* teruggeeft.
    Om code-herhaling te vermijden. Je ziet dat relay4 exact hetzelfde struct heeft,
    dus we doen hier generiek.
    """
    base = f"relay{relay_number}"
    # Return een lijst van sensor classes. Evt. als je alles expliciet wilt, kun je het uitschrijven.
    # Hier even beknopt ter illustratie:
    return [
        RelayInfoGenericSensor(coordinator, relay_number, "from"),
        RelayInfoGenericSensor(coordinator, relay_number, "delay"),
        RelayInfoGenericSensor(coordinator, relay_number, "onoff"),
        RelayInfoGenericSensor(coordinator, relay_number, "freq2"),
        RelayInfoGenericSensor(coordinator, relay_number, "manAutoTemp"),
        RelayInfoGenericSensor(coordinator, relay_number, "signal"),
        RelayInfoGenericSensor(coordinator, relay_number, "from2"),
        RelayInfoGenericSensor(coordinator, relay_number, "polarity"),
        RelayInfoGenericSensor(coordinator, relay_number, "status"),
        RelayInfoGenericSensor(coordinator, relay_number, "freq"),
        RelayInfoGenericSensor(coordinator, relay_number, "to"),
        RelayInfoGenericSensor(coordinator, relay_number, "to2"),
        RelayInfoGenericSensor(coordinator, relay_number, "tiempoOn"),
        RelayInfoGenericSensor(coordinator, relay_number, "key"),
    ]


class RelayInfoGenericSensor(CoordinatorEntity, SensorEntity):
    """
    Reads relays.relay{N}.info.<field>.
    e.g. relays.relay1.info.freq
    """

    def __init__(self, coordinator, relay_number, field):
        super().__init__(coordinator)
        self._relay_number = relay_number
        self._field = field
        self._attr_name = f"Relay{relay_number} Info {field}"
        self._attr_unique_id = f"{coordinator.api._pool_id}_relay{relay_number}_info_{field}"

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
# Het principe is bij alle hetzelfde: je pakt het pad in data en returnt dat
# Alle devices krijg elk hun eigen device_info(...) => categorie in HA
#

#
# --------------- GLOBAL / TOP-LEVEL ---------------
#

class GlobalSensorBase(CoordinatorEntity, SensorEntity):
    """Top-level info (isAWS, wifi, id, ...)."""
    @property
    def device_info(self):
        return {
            "identifiers": {(DOMAIN, f"{self.coordinator.api._pool_id}_global")},
            "name": "Algemeen (Global)",
            "manufacturer": "Vistapool",
            "model": "Vistapool Controller"
        }

class GlobalIsAWSSensor(GlobalSensorBase):
    def __init__(self, coordinator):
        super().__init__(coordinator)
        self._attr_name = "isAWS"
        self._attr_unique_id = f"{coordinator.api._pool_id}_isaws"

    @property
    def native_value(self):
        return self.coordinator.data.get("isAWS", None)


class GlobalWifiSensor(GlobalSensorBase):
    def __init__(self, coordinator):
        super().__init__(coordinator)
        self._attr_name = "Wifi"
        self._attr_unique_id = f"{coordinator.api._pool_id}_wifi"

    @property
    def native_value(self):
        return self.coordinator.data.get("wifi", None)


class GlobalIdSensor(GlobalSensorBase):
    def __init__(self, coordinator):
        super().__init__(coordinator)
        self._attr_name = "Pool ID"
        self._attr_unique_id = f"{coordinator.api._pool_id}_id"

    @property
    def native_value(self):
        return self.coordinator.data.get("id", None)


class GlobalCompanySensor(GlobalSensorBase):
    def __init__(self, coordinator):
        super().__init__(coordinator)
        self._attr_name = "Company"
        self._attr_unique_id = f"{coordinator.api._pool_id}_company"

    @property
    def native_value(self):
        return self.coordinator.data.get("company", None)


class GlobalUpdatedAtSensor(GlobalSensorBase):
    def __init__(self, coordinator):
        super().__init__(coordinator)
        self._attr_name = "Updated At"
        self._attr_unique_id = f"{coordinator.api._pool_id}_updated_at"

    @property
    def native_value(self):
        return self.coordinator.data.get("updatedAt", None)


class GlobalCreatedAtSensor(GlobalSensorBase):
    def __init__(self, coordinator):
        super().__init__(coordinator)
        self._attr_name = "Created At"
        self._attr_unique_id = f"{coordinator.api._pool_id}_created_at"

    @property
    def native_value(self):
        return self.coordinator.data.get("createdAt", None)


class GlobalPresentSensor(GlobalSensorBase):
    def __init__(self, coordinator):
        super().__init__(coordinator)
        self._attr_name = "Present"
        self._attr_unique_id = f"{coordinator.api._pool_id}_present"

    @property
    def native_value(self):
        return self.coordinator.data.get("present", None)


#
# --------------- BACKWASH ---------------
#

class BackwashSensorBase(CoordinatorEntity, SensorEntity):
    """backwash.* => Filtratie/Backwash device."""
    @property
    def device_info(self):
        return {
            "identifiers": {(DOMAIN, f"{self.coordinator.api._pool_id}_filtratie")},
            "name": "Filtratie",
            "manufacturer": "Vistapool",
            "model": "Vistapool Controller"
        }

class BackwashIntervalSensor(BackwashSensorBase):
    def __init__(self, coordinator):
        super().__init__(coordinator)
        self._attr_name = "Backwash Interval"
        self._attr_unique_id = f"{coordinator.api._pool_id}_backwash_interval"

    @property
    def native_value(self):
        return self.coordinator.data.get("backwash", {}).get("interval", None)

class BackwashModeSensor(BackwashSensorBase):
    def __init__(self, coordinator):
        super().__init__(coordinator)
        self._attr_name = "Backwash Mode"
        self._attr_unique_id = f"{coordinator.api._pool_id}_backwash_mode"

    @property
    def native_value(self):
        return self.coordinator.data.get("backwash", {}).get("mode", None)

class BackwashRemainingTimeSensor(BackwashSensorBase):
    def __init__(self, coordinator):
        super().__init__(coordinator)
        self._attr_name = "Backwash Remaining Time"
        self._attr_unique_id = f"{coordinator.api._pool_id}_backwash_remainingTime"

    @property
    def native_value(self):
        return self.coordinator.data.get("backwash", {}).get("remainingTime", None)

class BackwashStatusSensor(BackwashSensorBase):
    def __init__(self, coordinator):
        super().__init__(coordinator)
        self._attr_name = "Backwash Status"
        self._attr_unique_id = f"{coordinator.api._pool_id}_backwash_status"

    @property
    def native_value(self):
        return self.coordinator.data.get("backwash", {}).get("status", None)

class BackwashFrequencySensor(BackwashSensorBase):
    def __init__(self, coordinator):
        super().__init__(coordinator)
        self._attr_name = "Backwash Frequency"
        self._attr_unique_id = f"{coordinator.api._pool_id}_backwash_frequency"

    @property
    def native_value(self):
        return self.coordinator.data.get("backwash", {}).get("frequency", None)

class BackwashStartAtSensor(BackwashSensorBase):
    def __init__(self, coordinator):
        super().__init__(coordinator)
        self._attr_name = "Backwash StartAt"
        self._attr_unique_id = f"{coordinator.api._pool_id}_backwash_startAt"

    @property
    def native_value(self):
        return self.coordinator.data.get("backwash", {}).get("startAt", None)


#
# --------------- LIGHT ---------------
#

class LightSensorBase(CoordinatorEntity, SensorEntity):
    """light.* => Filtratie/Light device? Of separate 'Lighting' device."""
    @property
    def device_info(self):
        return {
            "identifiers": {(DOMAIN, f"{self.coordinator.api._pool_id}_filtratie")},
            "name": "Filtratie",
            "manufacturer": "Vistapool",
            "model": "Vistapool Controller"
        }

class LightModeSensor(LightSensorBase):
    def __init__(self, coordinator):
        super().__init__(coordinator)
        self._attr_name = "Light Mode"
        self._attr_unique_id = f"{coordinator.api._pool_id}_light_mode"

    @property
    def native_value(self):
        return self.coordinator.data.get("light", {}).get("mode", None)

class LightFreqSensor(LightSensorBase):
    def __init__(self, coordinator):
        super().__init__(coordinator)
        self._attr_name = "Light Frequency"
        self._attr_unique_id = f"{coordinator.api._pool_id}_light_freq"

    @property
    def native_value(self):
        return self.coordinator.data.get("light", {}).get("freq", None)

class LightToSensor(LightSensorBase):
    def __init__(self, coordinator):
        super().__init__(coordinator)
        self._attr_name = "Light To"
        self._attr_unique_id = f"{coordinator.api._pool_id}_light_to"

    @property
    def native_value(self):
        return self.coordinator.data.get("light", {}).get("to", None)

class LightFromSensor(LightSensorBase):
    def __init__(self, coordinator):
        super().__init__(coordinator)
        self._attr_name = "Light From"
        self._attr_unique_id = f"{coordinator.api._pool_id}_light_from"

    @property
    def native_value(self):
        return self.coordinator.data.get("light", {}).get("from", None)

class LightStatusSensor(LightSensorBase):
    def __init__(self, coordinator):
        super().__init__(coordinator)
        self._attr_name = "Light Status"
        self._attr_unique_id = f"{coordinator.api._pool_id}_light_status"

    @property
    def native_value(self):
        return self.coordinator.data.get("light", {}).get("status", None)


#
# --------------- HIDRO ---------------
#

class HydrolyseSensorBase(CoordinatorEntity, SensorEntity):
    @property
    def device_info(self):
        return {
            "identifiers": {(DOMAIN, f"{self.coordinator.api._pool_id}_hydrolyse")},
            "name": "Hydrolyse",
            "manufacturer": "Vistapool",
            "model": "Vistapool Controller"
        }

class HidroClorationEnabledSensor(HydrolyseSensorBase):
    def __init__(self, coordinator):
        super().__init__(coordinator)
        self._attr_name = "Cloration Enabled"
        self._attr_unique_id = f"{coordinator.api._pool_id}_hidro_cloration_enabled"

    @property
    def native_value(self):
        return self.coordinator.data.get("hidro", {}).get("cloration_enabled", None)

# ... etc. Voor elke key in `hidro`:
class HidroTemperatureEnabledSensor(HydrolyseSensorBase):
    def __init__(self, coordinator):
        super().__init__(coordinator)
        self._attr_name = "Hidro Temperature Enabled"
        self._attr_unique_id = f"{coordinator.api._pool_id}_hidro_temperature_enabled"

    @property
    def native_value(self):
        return self.coordinator.data.get("hidro", {}).get("temperature_enabled", None)


class HidroControlSensor(HydrolyseSensorBase):
    def __init__(self, coordinator):
        super().__init__(coordinator)
        self._attr_name = "Hidro Control"
        self._attr_unique_id = f"{coordinator.api._pool_id}_hidro_control"
    @property
    def native_value(self):
        return self.coordinator.data.get("hidro", {}).get("control", None)

class HidroFl1Sensor(HydrolyseSensorBase):
    def __init__(self, coordinator):
        super().__init__(coordinator)
        self._attr_name = "Hidro fl1"
        self._attr_unique_id = f"{coordinator.api._pool_id}_hidro_fl1"
    @property
    def native_value(self):
        return self.coordinator.data.get("hidro", {}).get("fl1", None)

# Enzovoort – hetzelfde patroon voor elk veld in `hidro`.

#
# --------------- FILTRATION ---------------
#
class FiltrationSensorBase(CoordinatorEntity, SensorEntity):
    @property
    def device_info(self):
        return {
            "identifiers": {(DOMAIN, f"{self.coordinator.api._pool_id}_filtratie")},
            "name": "Filtratie",
            "manufacturer": "Vistapool",
            "model": "Vistapool Controller"
        }

# interval1.from
class FiltrationInterval1FromSensor(FiltrationSensorBase):
    def __init__(self, coordinator):
        super().__init__(coordinator)
        self._attr_name = "Filtration Interval1 From"
        self._attr_unique_id = f"{coordinator.api._pool_id}_filtration_interval1_from"

    @property
    def native_value(self):
        return self.coordinator.data.get("filtration", {}) \
                   .get("interval1", {}) \
                   .get("from", None)

# Enzovoort voor 'to', 'interval2', 'interval3' etc.

# Filtration.intel.time
class FiltrationIntelTimeSensor(FiltrationSensorBase):
    def __init__(self, coordinator):
        super().__init__(coordinator)
        self._attr_name = "Filtration Intel Time"
        self._attr_unique_id = f"{coordinator.api._pool_id}_filtration_intel_time"

    @property
    def native_value(self):
        return self.coordinator.data.get("filtration", {}) \
                   .get("intel", {}) \
                   .get("time", None)

# ... etc.
# Je herhaalt dit voor elk veld: timerVel2, hasSmart, heating.temp, heating.clima, ...
# mode, status, manVel, pumpType, etc.

#
# --------------- MAIN ---------------
#
class MainSensorBase(CoordinatorEntity, SensorEntity):
    @property
    def device_info(self):
        return {
            "identifiers": {(DOMAIN, f"{self.coordinator.api._pool_id}_main")},
            "name": "Algemeen (Main)",
            "manufacturer": "Vistapool",
            "model": "Vistapool Controller"
        }

class MainHideRelaysSensor(MainSensorBase):
    def __init__(self, coordinator):
        super().__init__(coordinator)
        self._attr_name = "Hide Relays"
        self._attr_unique_id = f"{coordinator.api._pool_id}_main_hideRelays"

    @property
    def native_value(self):
        return self.coordinator.data.get("main", {}).get("hideRelays", None)

# Enzovoort voor elk veld in 'main' (hasUV, RSSI, hasLED, etc.)

#
# --------------- MODULES ---------------
#
class ModulesSensorBase(CoordinatorEntity, SensorEntity):
    @property
    def device_info(self):
        return {
            "identifiers": {(DOMAIN, f"{self.coordinator.api._pool_id}_modules")},
            "name": "Modules",
            "manufacturer": "Vistapool",
            "model": "Vistapool Controller"
        }

class ModulesRxPumpStatusSensor(ModulesSensorBase):
    def __init__(self, coordinator):
        super().__init__(coordinator)
        self._attr_name = "Modules rx pump_status"
        self._attr_unique_id = f"{coordinator.api._pool_id}_modules_rx_pump_status"

    @property
    def native_value(self):
        return self.coordinator.data \
                   .get("modules", {}) \
                   .get("rx", {}) \
                   .get("pump_status", None)

# ... Idem voor alle velden in modules.rx, modules.ph, modules.cl, modules.cd, modules.uv, modules.io.

#
# --------------- RELAYS ---------------
#
class RelaysSensorBase(CoordinatorEntity, SensorEntity):
    @property
    def device_info(self):
        return {
            "identifiers": {(DOMAIN, f"{self.coordinator.api._pool_id}_relays")},
            "name": "Relays",
            "manufacturer": "Vistapool",
            "model": "Vistapool Controller"
        }

class RelaysFiltrationHeatingStatusSensor(RelaysSensorBase):
    def __init__(self, coordinator):
        super().__init__(coordinator)
        self._attr_name = "Relays Filtration Heating Status"
        self._attr_unique_id = f"{coordinator.api._pool_id}_relays_filtration_heating_status"

    @property
    def native_value(self):
        return self.coordinator.data.get("relays", {}) \
                   .get("filtration", {}) \
                   .get("heating", {}) \
                   .get("status", None)

# ... etc. net zoals we deden in 'make_relay_info_sensors'.


#
# --------------- FORM ---------------
#
class FormSensorBase(CoordinatorEntity, SensorEntity):
    @property
    def device_info(self):
        return {
            "identifiers": {(DOMAIN, f"{self.coordinator.api._pool_id}_form")},
            "name": "Form",
            "manufacturer": "Vistapool",
            "model": "Vistapool Controller"
        }

class FormLngSensor(FormSensorBase):
    def __init__(self, coordinator):
        super().__init__(coordinator)
        self._attr_name = "Form lng"
        self._attr_unique_id = f"{coordinator.api._pool_id}_form_lng"

    @property
    def native_value(self):
        return self.coordinator.data.get("form", {}).get("lng", None)

class FormCountrySensor(FormSensorBase):
    def __init__(self, coordinator):
        super().__init__(coordinator)
        self._attr_name = "Form country"
        self._attr_unique_id = f"{coordinator.api._pool_id}_form_country"

    @property
    def native_value(self):
        return self.coordinator.data.get("form", {}).get("country", "")

# ... en zo verder voor city, name, zipcode, lat, street

class RelaysRelay4NameSensor(RelaysSensorBase):
    def __init__(self, coordinator):
        super().__init__(coordinator)
        self._attr_name = "Relay4 Name"
        self._attr_unique_id = f"{coordinator.api._pool_id}_relay4_name"

    @property
    def native_value(self):
        return self.coordinator.data \
                   .get("relays", {}) \
                   .get("relay4", {}) \
                   .get("name", "")

# ... etc. herhaald voor alle relays


#
# Klaar! :-)
#
