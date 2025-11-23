# 📋 Vistapool Entities Overzicht

Volledig overzicht van alle beschikbare entities in de Vistapool integratie.

## 🔀 Switches (14 stuks)

| Entity ID | Naam | Apparaat | Beschrijving |
|-----------|------|----------|--------------|
| `switch.vistapool_zwembadpomp` | Zwembadpomp | Filtratie | Hoofdpomp aan/uit |
| `switch.vistapool_zwembadlicht` | Zwembadlicht | Filtratie | Zwembadverlichting |
| `switch.vistapool_licht_automatische_modus` | Licht Automatische Modus | Filtratie | Auto timer voor licht |
| `switch.vistapool_backwash_actief` | Backwash Actief | Filtratie | Terugspoel systeem |
| `switch.vistapool_chloorshock` | Chloorshock | Hydrolyse | Chloor boost functie |
| `switch.vistapool_hydrolyse_ingeschakeld` | Hydrolyse Ingeschakeld | Hydrolyse | Hoofdschakelaar hydrolyse |
| `switch.vistapool_hydrolyse_temperatuur_sensor` | Hydrolyse Temperatuur Sensor | Hydrolyse | Temp sensor activatie |
| `switch.vistapool_hydrolyse_dekzeil_detectie` | Hydrolyse Dekzeil Detectie | Hydrolyse | Cover detection |
| `switch.vistapool_relay_1` | Relay 1 | Relays | Configureerbare relay 1 |
| `switch.vistapool_relay_2` | Relay 2 | Relays | Configureerbare relay 2 |
| `switch.vistapool_relay_3` | Relay 3 | Relays | Configureerbare relay 3 |
| `switch.vistapool_relay_4` | Relay 4 | Relays | Configureerbare relay 4 |
| `switch.vistapool_verwarming` | Verwarming | Filtratie | Verwarmingssysteem |
| `switch.vistapool_smart_mode_vorstbeveiliging` | Smart Mode Vorstbeveiliging | Filtratie | Freeze protection |

## 🔢 Numbers (38 stuks)

### Set Points (5)
| Entity ID | Naam | Min | Max | Step | Eenheid |
|-----------|------|-----|-----|------|---------|
| `number.vistapool_ph_setpoint_hoog` | pH Setpoint Hoog | 6.0 | 8.5 | 0.01 | pH |
| `number.vistapool_ph_setpoint_laag` | pH Setpoint Laag | 6.0 | 8.5 | 0.01 | pH |
| `number.vistapool_redox_setpoint` | Redox Setpoint | 300 | 900 | 1 | mV |
| `number.vistapool_cl_setpoint` | Chloor Setpoint | 0 | 300 | 1 | - |
| `number.vistapool_cd_setpoint` | CD Setpoint | 0 | 10000 | 1 | - |

### Hydrolyse (3)
| Entity ID | Naam | Min | Max | Step | Eenheid |
|-----------|------|-----|-----|------|---------|
| `number.vistapool_hydrolyse_level` | Hydrolyse Level | 0 | 100 | 1 | % |
| `number.vistapool_hydrolyse_reductie` | Hydrolyse Reductie | 0 | 100 | 1 | % |
| `number.vistapool_hydrolyse_max_allowed` | Hydrolyse Max Toegestaan | 0 | 1000 | 10 | - |

### Filtratie (5)
| Entity ID | Naam | Min | Max | Step | Eenheid |
|-----------|------|-----|-----|------|---------|
| `number.vistapool_water_temp_setpoint` | Watertemperatuur Setpoint | 0 | 40 | 0.5 | °C |
| `number.vistapool_heating_temp` | Verwarming Temperatuur | 0 | 40 | 0.5 | °C |
| `number.vistapool_heating_temp_hi` | Verwarming Max Temperatuur | 0 | 45 | 0.5 | °C |
| `number.vistapool_smart_temp_min` | Smart Mode Min Temp | 0 | 30 | 1 | °C |
| `number.vistapool_smart_temp_high` | Smart Mode Max Temp | 15 | 40 | 1 | °C |

### Timer Intervals (6)
| Entity ID | Naam | Min | Max | Step | Eenheid |
|-----------|------|-----|-----|------|---------|
| `number.vistapool_interval1_from` | Interval 1 Start | 0 | 86400 | 60 | sec |
| `number.vistapool_interval1_to` | Interval 1 Einde | 0 | 86400 | 60 | sec |
| `number.vistapool_interval2_from` | Interval 2 Start | 0 | 86400 | 60 | sec |
| `number.vistapool_interval2_to` | Interval 2 Einde | 0 | 86400 | 60 | sec |
| `number.vistapool_interval3_from` | Interval 3 Start | 0 | 86400 | 60 | sec |
| `number.vistapool_interval3_to` | Interval 3 Einde | 0 | 86400 | 60 | sec |

### Backwash (3)
| Entity ID | Naam | Min | Max | Step | Eenheid |
|-----------|------|-----|-----|------|---------|
| `number.vistapool_backwash_interval` | Backwash Interval | 1 | 1440 | 1 | min |
| `number.vistapool_backwash_frequency` | Backwash Frequentie | 1440 | 43200 | 1440 | min |
| `number.vistapool_backwash_startat` | Backwash StartAt | 0 | 9999999999 | 3600 | epoch |

### Verlichting (3)
| Entity ID | Naam | Min | Max | Step | Eenheid |
|-----------|------|-----|-----|------|---------|
| `number.vistapool_light_from` | Licht Start Tijd | 0 | 86400 | 60 | sec |
| `number.vistapool_light_to` | Licht Eind Tijd | 0 | 86400 | 60 | sec |
| `number.vistapool_light_freq` | Licht Frequentie | 3600 | 604800 | 3600 | sec |

### Relays (12 - 3 per relay)
Elk van de 4 relays heeft:
- Vertraging (0-3600 sec, step 1)
- Start Tijd (0-86400 sec, step 60)
- Eind Tijd (0-86400 sec, step 60)

## 📊 Selects (8 stuks)

| Entity ID | Naam | Opties |
|-----------|------|--------|
| `select.vistapool_filtration_mode` | Filtratie Modus | Manual, Auto, Smart |
| `select.vistapool_pump_speed_manual` | Pomp Snelheid (Manueel) | Slow, Medium, High |
| `select.vistapool_pump_speed_timer1` | Pomp Snelheid Interval 1 | Slow, Medium, High |
| `select.vistapool_pump_speed_timer2` | Pomp Snelheid Interval 2 | Slow, Medium, High |
| `select.vistapool_pump_speed_timer3` | Pomp Snelheid Interval 3 | Slow, Medium, High |
| `select.vistapool_pump_type` | Pomp Type | Enkel-snelheid, Variabel |
| `select.vistapool_backwash_mode` | Backwash Modus | Manual, Automatic |
| `select.vistapool_backwash_frequency_select` | Backwash Frequentie | Elke dag, Elke twee dagen, ..., Elke vier weken |
| `select.vistapool_ph_type` | pH Dosering Type | ACID, BASE |

## 📡 Sensors (100+ stuks)

### Global (7)
- isAWS
- Wifi
- Pool ID
- Company
- Updated At
- Created At
- Present

### Backwash (6)
- Interval
- Mode
- Remaining Time
- Status
- Frequency
- StartAt

### Light (5)
- Mode
- Frequency
- To
- From
- Status

### Hidro/Hydrolyse (19)
- Cloration Enabled
- Temperature Enabled
- Control
- fl1, fl2
- Temperature Value
- al4
- HasHidroControl
- Cover
- Current
- CellPartialTime
- is_electrolysis
- CellTotalTime
- Reduction
- Level
- MaxAllowedValue
- Low
- cover_enabled
- measure

### Filtration (23)
- Interval 1/2/3 From/To
- Intel Time/Temp
- TimerVel 1/2/3
- HasSmart
- Heating Temp/Clima/TempHi
- ManVel
- HasHeat
- PumpType
- Status
- Mode
- Smart tempMin/tempHigh/freeze

### Main (25)
- HideRelays, HasUV, RSSI, HasLED, LEDPulse
- HasIO, HasLinkedAuto, HideTemperature
- HideLighting, FWU_enabled, NetworkPresent
- Version, HasPH, HasBackwash, HasWifi
- HasCD, HideFiltration, HasCL, HasRX
- Temperature, WifiVersion, LocalTime
- HasLinked, HasHidro

### Modules (20)
**rx:** pump_status, current, tank, status.value  
**ph:** type, tank, current, pump_high_on, pump_low_on, status.high_value, status.low_value, al3  
**cl:** pump_status, current, status.value, tank  
**cd:** current, status.value, tank  
**uv:** total, partial, status  
**io:** activation, status, level

### Relays (30+)
- Filtration heating status/gpio
- Filtration gpio
- Backwash gpio
- IO gpio, RX gpio, Light gpio
- CL gpio, CD gpio, UV gpio
- pH acid/base gpio
- Relay 1/2/3/4: name + 14 info fields elk

### Form (7)
- lng, lat
- country, city
- name, street, zipcode

## 📈 Totaal Overzicht

| Type | Aantal | Beschrijving |
|------|--------|--------------|
| **Switches** | 14 | On/off besturing |
| **Numbers** | 38 | Instelbare waarden |
| **Selects** | 8 | Dropdown keuzes |
| **Sensors** | 100+ | Status monitoring |
| **TOTAAL** | **160+** | **Volledige controle!** |

## 🎯 Apparaat Indeling

### Filtratie
- Pomp, backwash, intervals
- Verlichting
- Verwarming
- 22 switches/numbers/selects

### Hydrolyse
- Elektrolyse controle
- Chloorshock
- Temperatuur monitoring
- 5 switches/numbers

### Set points
- pH, Redox, CL, CD
- 5 numbers

### Relays
- 4 configureerbare relays
- 16 entities

### Algemeen (Global/Main)
- Systeem informatie
- Netwerk status
- 32 sensors

### Modules
- pH, Rx, CL, CD, UV, IO
- 20 sensors

### Form
- Locatie informatie
- 7 sensors

---

💡 **Tip**: Gebruik de zoekfunctie in Home Assistant om snel entities te vinden: zoek op "vistapool"
