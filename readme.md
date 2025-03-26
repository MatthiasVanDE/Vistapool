# 📊 Read-Only Parameters (Sensoren)

| 🔢 Categorie              | 🧩 Parameter                       | 🗂️ JSON Pad                                 | 📝 Beschrijving                                       |
|--------------------------|------------------------------------|---------------------------------------------|-------------------------------------------------------|
| ✅ Systeemstatus          | `present`                          | `present`                                   | Apparaat online (true/false)                         |
|                          | `updatedAt`                        | `updatedAt`                                 | Tijdstip laatste update (UNIX)                       |
|                          | `createdAt`                        | `createdAt`                                 | Tijdstip creatie                                     |
| 🌡️ Temperatuur           | `main.temperature`                 | `main.temperature`                          | Buitentemperatuur                                    |
|                          | `hidro.temperature_value`          | `hidro.temperature_value`                   | Watertemperatuur via Hidro-module                    |
|                          | `hidro.temperature_enabled`        | `hidro.temperature_enabled`                 | Sensor aan/uit                                       |
| 🌐 Netwerk & Firmware     | `main.wifiVersion`                 | `main.wifiVersion`                          | Versie WiFi-module                                   |
|                          | `main.version`                     | `main.version`                              | Firmwareversie bord                                  |
|                          | `main.networkPresent`              | `main.networkPresent`                       | Netwerkstatus (1 = aanwezig)                         |
|                          | `main.RSSI`                        | `main.RSSI`                                 | WiFi signaalsterkte (dBm)                            |
| ⚗️ pH                    | `ph.current`                       | `modules.ph.current`                        | Actuele pH-waarde                                    |
|                          | `ph.status.high_value`             | `modules.ph.status.high_value`              | Bovenste alarmgrens                                  |
|                          | `ph.status.low_value`              | `modules.ph.status.low_value`               | Onderste alarmgrens                                  |
| ⚡ Redox / Rx             | `rx.current`                       | `modules.rx.current`                        | Actuele redoxwaarde (ORP)                            |
|                          | `rx.status.value`                  | `modules.rx.status.value`                   | Doelwaarde ORP                                       |
| 🧪 Chloor (CL)            | `cl.current`                       | `modules.cl.current`                        | Actuele stroom chloorcel                             |
|                          | `cl.status.value`                  | `modules.cl.status.value`                   | Status/alarmwaarde                                   |
| 📦 CD-module              | `cd.current`                       | `modules.cd.current`                        | Stroomverbruik (CD)                                  |
| 🧠 IO-module              | `io.level`                         | `modules.io.level`                          | Analoge waarde IO                                    |
|                          | `io.status`                        | `modules.io.status`                         | Bitmask statuswaarde                                 |
| 💧 Elektrolyse (Hidro)    | `hidro.level`                      | `hidro.level`                               | Huidig vermogen elektrolyse (0-1000 = 0-100%)         |
|                          | `hidro.cellPartialTime`            | `hidro.cellPartialTime`                     | Tijd actief sinds laatste reset                      |
|                          | `hidro.cellTotalTime`              | `hidro.cellTotalTime`                       | Totale looptijd van cel                              |
|                          | `hidro.current`                    | `hidro.current`                             | Stroom door de cel (mA)                              |
|                          | `hidro.fl1`, `hidro.fl2`           | `hidro.fl1`, `hidro.fl2`                    | Digitale inputs (1/0)                                |
|                          | `hidro.al4`                        | `hidro.al4`                                 | Alarmstatus bit                                      |
|                          | `hidro.cover`                      | `hidro.cover`                               | Dekzeilstatus (0 = open, 1 = gesloten)               |
| 💡 Verlichting            | `light.status`                     | `light.status`                              | 0 = uit, 1 = aan                                     |
|                          | `light.mode`                       | `light.mode`                                | 0 = manueel, 1 = automatisch                         |
|                          | `light.freq`                       | `light.freq`                                | Herhaalinterval (seconden)                           |
|                          | `light.from`                       | `light.from`                                | Starttijd (seconden sinds middernacht)              |
|                          | `light.to`                         | `light.to`                                  | Eindtijd (idem)                                      |
| ♻️ Backwash              | `backwash.mode`                    | `backwash.mode`                             | 0 = manueel, 1 = automatisch                         |
|                          | `backwash.status`                  | `backwash.status`                           | Status actief                                        |
|                          | `backwash.interval`                | `backwash.interval`                         | Duur in seconden                                     |
|                          | `backwash.frequency`               | `backwash.frequency`                        | Herhaalinterval in seconden                          |
|                          | `backwash.startAt`                 | `backwash.startAt`                          | Starttijd (seconden sinds middernacht)              |
| ⚙️ Relais (statussen)     | `relays.relayX.info.status`        | `relays.relay1..4.info.status`              | Aan/uit status van relais                            |
|                          | `relays.relayX.info.onoff`         | `relays.relay1..4.info.onoff`               | Manuele status (1 = aan, 0 = uit)                    |
|                          | `relays.relayX.name`               | `relays.relayX.name`                        | Naam van relais                                      |


# ✍️ Writable Parameters (Instelbare waarden)

| 🧩 Pad in JSON                         | 📝 Beschrijving                                                             | 🛠️ Mogelijke waarden / Structuur                           |
|---------------------------------------|----------------------------------------------------------------------------|------------------------------------------------------------|
| filtration.mode                       | Filtratiemodus                                                             | `0` = Manueel, `1` = Auto, `3` = Smart, `2` = Timer (onbekend) |
| filtration.status                     | Huidige pompstatus                                                         | `1` = Aan, `0` = Uit                                        |
| filtration.manVel                     | Manuele snelheid pomp (bij mode = 0)                                       | `0` = laag, `1` = hoog                                      |
| filtration.timerVel1                 | Snelheid tijdens interval1                                                 | `0` = laag, `1` = hoog, `2` = onbekend                      |
| filtration.timerVel2                 | Snelheid tijdens interval2                                                 | idem                                                       |
| filtration.timerVel3                 | Snelheid tijdens interval3                                                 | idem                                                       |
| filtration.interval1.from            | Starttijd interval1 (seconden sinds middernacht)                           | bijv. `28800` = 8:00                                        |
| filtration.interval1.to              | Eindtijd interval1                                                         | bijv. `61200` = 17:00                                       |
| filtration.interval2.from            | Starttijd interval2                                                        | idem                                                       |
| filtration.interval2.to              | Eindtijd interval2                                                         | idem                                                       |
| filtration.interval3.from            | Starttijd interval3                                                        | idem                                                       |
| filtration.interval3.to              | Eindtijd interval3                                                         | idem                                                       |
| filtration.smart.tempMin             | Minimum temperatuur voor smart-mode filtering                              | in graden Celsius                                          |
| filtration.smart.tempHigh            | Maximum temperatuur waarop gefilterd moet worden                           | idem                                                       |
| filtration.smart.freeze              | Vorstbeveiliging                                                           | `1` = aan, `0` = uit                                       |
| filtration.heating.temp              | Gewenste temperatuur in verwarmingsinstelling                              | in graden Celsius                                          |
| filtration.heating.tempHi            | Bovenlimiet temperatuur (alleen als gebruikt)                              | in graden Celsius                                          |
| filtration.heating.clima             | Onbekende functie (meestal `0`)                                            | `0`                                                        |
| filtration.intel.temp                | Temperatuurinstelling in intel-mode                                        | idem                                                       |
| filtration.intel.time                | Tijd in minuten (bijv. `"480"` = 8 uur)                                    | string!                                                    |
| backwash.mode                        | Backwashmodus                                                              | `0` = manueel, `1` = automatisch                           |
| backwash.status                      | Actieve status                                                             | `0` = uit, `1` = actief                                    |
| backwash.interval                    | Duur van backwash (seconden)                                               | bijv. `180`                                                |
| backwash.frequency                   | Frequentie in seconden                                                     | bijv. `30240` = 3 weken                                    |
| backwash.startAt                     | Starttijd in seconden sinds middernacht                                    | bijv. `39601` = 11:00:01                                   |
| light.mode                           | Lichtmodus                                                                 | `0` = manueel, `1` = automatisch                          |
| light.status                         | Licht aan/uit                                                              | `1` = aan, `0` = uit                                       |
| light.freq                           | Herhalingsfrequentie in seconden                                           | bijv. `86400` = dagelijks                                  |
| light.from                           | Starttijd verlichting (seconden sinds middernacht)                         | idem                                                       |
| light.to                             | Eindtijd verlichting                                                       | idem                                                       |
| relays.relay1..4.info.onoff          | Relais aan/uit                                                             | `1` = aan, `0` = uit                                       |
| relays.relay1..4.info.freq           | Frequentie (herhaling in seconden)                                         | bijv. `86400`                                              |
| relays.relay1..4.info.freq2          | Alternatieve frequentie                                                    | idem                                                       |
| relays.relay1..4.info.delay          | Vertraging in seconden voor inschakeling                                   | `0` tot `n`                                                |
| relays.relay1..4.info.from           | Starttijd (seconden sinds middernacht)                                     | idem                                                       |
| relays.relay1..4.info.to             | Eindtijd                                                                    | idem                                                       |
| relays.relay1..4.name                | Naam van relais                                                            | string                                                     |
| modules_web.ph.status.high_value     | Gewenste maximum pH-waarde                                                 | bijv. `710`                                                |
| modules_web.ph.status.low_value      | Gewenste minimum pH-waarde                                                 | bijv. `700`                                                |
| modules_web.rx.status.value          | Gewenste ORP waarde                                                        | bijv. `651`                                                |
| modules_web.cl.status.value          | Doelwaarde chloor (meestal `100`)                                          | onbekend functie                                           |
| modules_web.cd.status.value          | Doelwaarde voor CD (meestal `5000`)                                        | onbekend functie                                           |
| hidro.reduction                      | Percentage elektrolysevermindering (reduction)                             | `0` - `100` (in stappen van 1 tot max `1000`)              |
| hidro.cloration_enabled              | Chloorshock                                                                | `1` = aan, `0` = uit                                       |
| hidro.cover_enabled                  | Dekzeil detectie aan/uit                                                  | `1` = aan, `0` = uit                                       |
| hidro.disable                        | Hydrolyse uitzetten                                                        | `1` = uitschakelen                                         |

