# 🤖 Vistapool Automatisering Voorbeelden

Complete collectie van handige automatiseringen voor je Vistapool zwembad.

---

## 📋 Inhoudsopgave

1. [Basis Automatiseringen](#basis-automatiseringen)
2. [Temperatuur Gebaseerd](#temperatuur-gebaseerd)
3. [Seizoen & Weer](#seizoen--weer)
4. [Energie Optimalisatie](#energie-optimalisatie)
5. [Waterkwaliteit](#waterkwaliteit)
6. [Veiligheid & Alarms](#veiligheid--alarms)
7. [Geavanceerde Scenarios](#geavanceerde-scenarios)

---

## 🎯 Basis Automatiseringen

### Auto 1: Pomp Timer (Eenvoudig)
**Doel:** Pomp loopt van 8:00 tot 17:00

```yaml
automation:
  - alias: "Zwembad: Pomp Schema"
    description: "Pomp aan om 8:00, uit om 17:00"
    trigger:
      - platform: time
        at: "08:00:00"
        id: "start"
      - platform: time
        at: "17:00:00"
        id: "stop"
    action:
      - choose:
          - conditions:
              - condition: trigger
                id: "start"
            sequence:
              - service: switch.turn_on
                target:
                  entity_id: switch.vistapool_zwembadpomp
          - conditions:
              - condition: trigger
                id: "stop"
            sequence:
              - service: switch.turn_off
                target:
                  entity_id: switch.vistapool_zwembadpomp
```

---

### Auto 2: Licht bij Zonsondergang
**Doel:** Licht aan na zonsondergang, uit om middernacht

```yaml
automation:
  - alias: "Zwembad: Licht Automatisch"
    description: "Zwembadlicht aan bij zonsondergang"
    trigger:
      - platform: sun
        event: sunset
        offset: "+00:30:00"  # 30 min na zonsondergang
        id: "on"
      - platform: time
        at: "00:00:00"
        id: "off"
    condition:
      # Alleen in zomer (april-september)
      - condition: template
        value_template: "{{ now().month >= 4 and now().month <= 9 }}"
    action:
      - choose:
          - conditions:
              - condition: trigger
                id: "on"
            sequence:
              - service: switch.turn_on
                target:
                  entity_id: switch.vistapool_zwembadlicht
              - service: notify.mobile_app
                data:
                  message: "Zwembadlicht is aangegaan 💡"
          - conditions:
              - condition: trigger
                id: "off"
            sequence:
              - service: switch.turn_off
                target:
                  entity_id: switch.vistapool_zwembadlicht
```

---

### Auto 3: Weekendstand
**Doel:** Langere pomptijd in weekend

```yaml
automation:
  - alias: "Zwembad: Weekend Extra Filtratie"
    description: "Pomp loopt langer in weekend"
    trigger:
      - platform: time
        at: "08:00:00"
    condition:
      - condition: time
        weekday:
          - sat
          - sun
    action:
      - service: number.set_value
        target:
          entity_id: number.vistapool_interval1_to
        data:
          value: 68400  # 19:00 (ipv 17:00)
      - service: switch.turn_on
        target:
          entity_id: switch.vistapool_zwembadpomp
```

---

## 🌡️ Temperatuur Gebaseerd

### Auto 4: Hoge Temperatuur = Meer Filtreren
**Doel:** Bij hoge watertemp meer filtreren

```yaml
automation:
  - alias: "Zwembad: Extra Filtratie bij Hitte"
    description: "Schakel naar Smart mode bij >26°C"
    trigger:
      - platform: numeric_state
        entity_id: sensor.vistapool_main_temperature
        above: 26
        for:
          minutes: 30
    condition:
      # Alleen overdag
      - condition: sun
        after: sunrise
        before: sunset
    action:
      - service: select.select_option
        target:
          entity_id: select.vistapool_filtration_mode
        data:
          option: "Smart"
      - service: select.select_option
        target:
          entity_id: select.vistapool_pump_speed_timer1
        data:
          option: "High"
      - service: notify.mobile_app
        data:
          title: "🏊 Zwembad Hitte Modus"
          message: "Temperatuur {{ states('sensor.vistapool_main_temperature') }}°C - Smart mode geactiveerd"
```

---

### Auto 5: Vorstbeveiliging
**Doel:** Bescherm zwembad bij vorst

```yaml
automation:
  - alias: "Zwembad: Vorstbeveiliging"
    description: "Pomp aan bij temperatuur < 2°C"
    trigger:
      - platform: numeric_state
        entity_id: sensor.vistapool_main_temperature
        below: 2
    action:
      - service: switch.turn_on
        target:
          entity_id: switch.vistapool_smart_mode_vorstbeveiliging
      - service: switch.turn_on
        target:
          entity_id: switch.vistapool_zwembadpomp
      - service: notify.mobile_app
        data:
          title: "❄️ VORSTBEVEILIGING ACTIEF"
          message: "Zwembadpomp draait continu - Temp: {{ states('sensor.vistapool_main_temperature') }}°C"
          data:
            priority: high
            ttl: 0
```

---

### Auto 6: Verwarming Slim Regelen
**Doel:** Verwarm alleen als nodig

```yaml
automation:
  - alias: "Zwembad: Slimme Verwarming"
    description: "Verwarming aan bij zon + temp < gewenst"
    trigger:
      - platform: time_pattern
        minutes: "/15"  # Check elk kwartier
    condition:
      - condition: sun
        after: sunrise
        before: sunset
      - condition: numeric_state
        entity_id: sensor.vistapool_main_temperature
        below: 24  # Gewenste temp
      - condition: numeric_state
        entity_id: sensor.vistapool_main_temperature
        above: 20  # Minimale temp
    action:
      - service: switch.turn_on
        target:
          entity_id: switch.vistapool_verwarming
      - service: number.set_value
        target:
          entity_id: number.vistapool_heating_temp
        data:
          value: 26
```

---

## 🌦️ Seizoen & Weer

### Auto 7: Zomer/Winter Modus
**Doel:** Automatisch schakelen tussen seizoenen

```yaml
automation:
  - alias: "Zwembad: Zomer Modus"
    description: "Activeer zomer instellingen in mei"
    trigger:
      - platform: time
        at: "08:00:00"
    condition:
      - condition: template
        value_template: "{{ now().month == 5 and now().day == 1 }}"
    action:
      - service: select.select_option
        target:
          entity_id: select.vistapool_filtration_mode
        data:
          option: "Auto"
      - service: vistapool.set_timer_intervals
        data:
          interval1_from: 28800  # 08:00
          interval1_to: 72000    # 20:00 (langer in zomer)
          interval2_from: 0
          interval2_to: 0
      - service: switch.turn_on
        target:
          entity_id: switch.vistapool_hydrolyse_ingeschakeld
      - service: notify.mobile_app
        data:
          title: "🏖️ Zomer Modus Actief"
          message: "Zwembad omgeschakeld naar zomer instellingen"

  - alias: "Zwembad: Winter Modus"
    description: "Activeer winter instellingen in oktober"
    trigger:
      - platform: time
        at: "08:00:00"
    condition:
      - condition: template
        value_template: "{{ now().month == 10 and now().day == 1 }}"
    action:
      - service: select.select_option
        target:
          entity_id: select.vistapool_filtration_mode
        data:
          option: "Manual"
      - service: vistapool.set_timer_intervals
        data:
          interval1_from: 32400  # 09:00
          interval1_to: 54000    # 15:00 (korter in winter)
          interval2_from: 0
          interval2_to: 0
      - service: switch.turn_off
        target:
          entity_id: switch.vistapool_hydrolyse_ingeschakeld
      - service: notify.mobile_app
        data:
          title: "❄️ Winter Modus Actief"
          message: "Zwembad omgeschakeld naar winter instellingen"
```

---

### Auto 8: Regen = Geen Licht
**Doel:** Licht uit bij regen

```yaml
automation:
  - alias: "Zwembad: Licht Uit bij Regen"
    description: "Schakel licht uit als het regent"
    trigger:
      - platform: state
        entity_id: weather.home
        to: "rainy"
    condition:
      - condition: state
        entity_id: switch.vistapool_zwembadlicht
        state: "on"
    action:
      - service: switch.turn_off
        target:
          entity_id: switch.vistapool_zwembadlicht
      - service: notify.mobile_app
        data:
          message: "Zwembadlicht uitgezet - het regent 🌧️"
```

---

## ⚡ Energie Optimalisatie

### Auto 9: Goedkope Uren (Dynamische Prijzen)
**Doel:** Filtreer tijdens goedkope stroom

```yaml
automation:
  - alias: "Zwembad: Filtreren bij Goedkope Stroom"
    description: "Gebruik dynamische energieprijzen"
    trigger:
      - platform: time_pattern
        hours: "*"
    condition:
      # Alleen als prijs < €0.15/kWh
      - condition: numeric_state
        entity_id: sensor.energy_current_hour_price
        below: 0.15
      # En tussen 6:00 - 22:00
      - condition: time
        after: "06:00:00"
        before: "22:00:00"
    action:
      - service: switch.turn_on
        target:
          entity_id: switch.vistapool_zwembadpomp
      - service: select.select_option
        target:
          entity_id: select.vistapool_pump_speed_manual
        data:
          option: "High"
```

---

### Auto 10: Zonnepanelen Overschot
**Doel:** Gebruik zonne-energie voor zwembad

```yaml
automation:
  - alias: "Zwembad: Extra Filtreren met Zon"
    description: "Pomp op vol vermogen bij zonne-overschot"
    trigger:
      - platform: numeric_state
        entity_id: sensor.solar_power_export
        above: 2000  # Meer dan 2kW export
        for:
          minutes: 15
    condition:
      - condition: sun
        after: sunrise
        before: sunset
      - condition: numeric_state
        entity_id: sensor.vistapool_main_temperature
        above: 18  # Alleen als water warm genoeg
    action:
      - service: switch.turn_on
        target:
          entity_id: switch.vistapool_zwembadpomp
      - service: switch.turn_on
        target:
          entity_id: switch.vistapool_verwarming
      - service: select.select_option
        target:
          entity_id: select.vistapool_pump_speed_manual
        data:
          option: "High"
      - service: notify.mobile_app
        data:
          message: "☀️ Zwembad verwarmt met zonne-energie!"
```

---

## 💧 Waterkwaliteit

### Auto 11: pH Te Hoog Alarm
**Doel:** Notificatie bij verkeerde pH

```yaml
automation:
  - alias: "Zwembad: pH Alarm"
    description: "Waarschuwing bij abnormale pH"
    trigger:
      - platform: numeric_state
        entity_id: sensor.vistapool_modules_ph_current
        above: 7.6
        for:
          minutes: 30
        id: "hoog"
      - platform: numeric_state
        entity_id: sensor.vistapool_modules_ph_current
        below: 7.0
        for:
          minutes: 30
        id: "laag"
    action:
      - service: notify.mobile_app
        data:
          title: "⚠️ pH Waarde Abnormaal"
          message: >
            pH is {% if trigger.id == 'hoog' %}te hoog{% else %}te laag{% endif %}: 
            {{ states('sensor.vistapool_modules_ph_current') }}
          data:
            priority: high
            actions:
              - action: "VIEW_POOL"
                title: "Bekijk Zwembad"
```

---

### Auto 12: Chloorshock Schema
**Doel:** Automatische chloorshock wekelijks

```yaml
automation:
  - alias: "Zwembad: Wekelijkse Chloorshock"
    description: "Chloorshock elke zondag avond"
    trigger:
      - platform: time
        at: "22:00:00"
    condition:
      - condition: time
        weekday:
          - sun
      - condition: numeric_state
        entity_id: sensor.vistapool_main_temperature
        above: 20  # Alleen als water warm genoeg
    action:
      - service: switch.turn_on
        target:
          entity_id: switch.vistapool_chloorshock
      - delay:
          hours: 4  # 4 uur shock
      - service: switch.turn_off
        target:
          entity_id: switch.vistapool_chloorshock
      - service: notify.mobile_app
        data:
          message: "✅ Wekelijkse chloorshock voltooid"
```

---

### Auto 13: Redox Waarschuwing
**Doel:** Alert bij lage redox waarde

```yaml
automation:
  - alias: "Zwembad: Lage Redox Waarschuwing"
    description: "Waarschuwing bij te lage desinfectie"
    trigger:
      - platform: numeric_state
        entity_id: sensor.vistapool_modules_rx_current
        below: 600
        for:
          hours: 2
    action:
      - service: notify.mobile_app
        data:
          title: "⚠️ Zwembad Desinfectie Laag"
          message: "Redox: {{ states('sensor.vistapool_modules_rx_current') }} mV - Controleer zwembad"
          data:
            priority: high
      - service: switch.turn_on
        target:
          entity_id: switch.vistapool_chloorshock
```

---

## 🚨 Veiligheid & Alarms

### Auto 14: Offline Detectie
**Doel:** Waarschuwing bij verbindingsverlies

```yaml
automation:
  - alias: "Zwembad: Offline Alarm"
    description: "Alert als zwembad controller offline gaat"
    trigger:
      - platform: state
        entity_id: sensor.vistapool_present
        to: "False"
        for:
          minutes: 10
    action:
      - service: notify.mobile_app
        data:
          title: "🔴 Zwembad Controller Offline"
          message: "Geen verbinding met zwembad controller sinds 10 minuten"
          data:
            priority: high
            ttl: 0
```

---

### Auto 15: Pomp Storing Detectie
**Doel:** Alert bij pomp probleem

```yaml
automation:
  - alias: "Zwembad: Pomp Storing"
    description: "Detecteer als pomp niet start wanneer hij zou moeten"
    trigger:
      - platform: time_pattern
        minutes: "/5"
    condition:
      # Pomp switch is aan
      - condition: state
        entity_id: switch.vistapool_zwembadpomp
        state: "on"
      # Maar status is off
      - condition: state
        entity_id: sensor.vistapool_filtration_status
        state: "Off"
        for:
          minutes: 5
    action:
      - service: notify.mobile_app
        data:
          title: "🚨 ZWEMBAD POMP STORING"
          message: "Pomp reageert niet - controleer apparatuur!"
          data:
            priority: high
            ttl: 0
            tag: "pump_error"
```

---

### Auto 16: Lekdetectie (Geschat)
**Doel:** Detecteer mogelijk lek via verbruik

```yaml
automation:
  - alias: "Zwembad: Mogelijk Lek Detectie"
    description: "Waarschuwing bij abnormaal hoog stroomverbruik"
    trigger:
      - platform: numeric_state
        entity_id: sensor.vistapool_hidro_current
        above: 8000  # mA - abnormaal hoog
        for:
          hours: 2
    action:
      - service: notify.mobile_app
        data:
          title: "⚠️ Mogelijk Zwembad Lek"
          message: "Abnormaal hoog hydrolyse verbruik: {{ states('sensor.vistapool_hidro_current') }} mA"
          data:
            actions:
              - action: "DISABLE_HYDRO"
                title: "Hydrolyse Uitschakelen"
```

---

## 🎓 Geavanceerde Scenarios

### Auto 17: Vakantie Modus
**Doel:** Minimale onderhoud tijdens afwezigheid

```yaml
automation:
  - alias: "Zwembad: Vakantie Modus Activeren"
    description: "Schakel naar spaarzame instellingen"
    trigger:
      - platform: state
        entity_id: input_boolean.vacation_mode
        to: "on"
    action:
      # Minimale filtratie
      - service: vistapool.set_timer_intervals
        data:
          interval1_from: 43200  # 12:00
          interval1_to: 50400    # 14:00 (2 uur per dag)
          interval2_from: 0
          interval2_to: 0
      # Lage pomp snelheid
      - service: select.select_option
        target:
          entity_id: select.vistapool_pump_speed_timer1
        data:
          option: "Slow"
      # Hydrolyse op minimum
      - service: number.set_value
        target:
          entity_id: number.vistapool_hydrolyse_level
        data:
          value: 30
      # Verwarming uit
      - service: switch.turn_off
        target:
          entity_id: switch.vistapool_verwarming
      # Licht uit
      - service: switch.turn_off
        target:
          entity_id: switch.vistapool_licht_automatische_modus
      - service: notify.mobile_app
        data:
          message: "🏖️ Zwembad vakantie modus geactiveerd"

  - alias: "Zwembad: Vakantie Modus Deactiveren"
    description: "Herstel normale instellingen"
    trigger:
      - platform: state
        entity_id: input_boolean.vacation_mode
        to: "off"
    action:
      # Normale filtratie
      - service: vistapool.set_timer_intervals
        data:
          interval1_from: 28800  # 08:00
          interval1_to: 61200    # 17:00
          interval2_from: 0
          interval2_to: 0
      # Normale snelheid
      - service: select.select_option
        target:
          entity_id: select.vistapool_pump_speed_timer1
        data:
          option: "Medium"
      # Hydrolyse normaal
      - service: number.set_value
        target:
          entity_id: number.vistapool_hydrolyse_level
        data:
          value: 100
      # Licht automatisch
      - service: switch.turn_on
        target:
          entity_id: switch.vistapool_licht_automatische_modus
      - service: notify.mobile_app
        data:
          message: "🏠 Zwembad normale modus hersteld"
```

---

### Auto 18: Feest Modus
**Doel:** Optimale instellingen voor zwembad party

```yaml
automation:
  - alias: "Zwembad: Feest Modus"
    description: "Activeer party instellingen"
    trigger:
      - platform: state
        entity_id: input_boolean.pool_party_mode
        to: "on"
    action:
      # Pomp op vol vermogen voor optimale water kwaliteit
      - service: switch.turn_on
        target:
          entity_id: switch.vistapool_zwembadpomp
      - service: select.select_option
        target:
          entity_id: select.vistapool_pump_speed_manual
        data:
          option: "High"
      # Extra chloorshock voor gebruik
      - service: switch.turn_on
        target:
          entity_id: switch.vistapool_chloorshock
      # Licht aan voor sfeer
      - service: switch.turn_on
        target:
          entity_id: switch.vistapool_zwembadlicht
      # Verwarming aan
      - service: switch.turn_on
        target:
          entity_id: switch.vistapool_verwarming
      - service: notify.mobile_app
        data:
          message: "🎉 Zwembad feest modus actief - Geniet ervan!"
```

---

### Auto 19: Adaptieve Filtratie
**Doel:** Zelf-lerend filtratie schema obv gebruik

```yaml
automation:
  - alias: "Zwembad: Adaptieve Filtratie"
    description: "Pas filtratie aan op basis van temperatuur en seizoen"
    trigger:
      - platform: time
        at: "06:00:00"
    variables:
      temp: "{{ states('sensor.vistapool_main_temperature') | float }}"
      month: "{{ now().month }}"
    action:
      - choose:
          # Zomer + Hoge Temp (> 26°C)
          - conditions:
              - "{{ temp > 26 }}"
              - "{{ month >= 6 and month <= 8 }}"
            sequence:
              - service: vistapool.set_timer_intervals
                data:
                  interval1_from: 25200  # 07:00
                  interval1_to: 75600    # 21:00 (14 uur)
                  interval2_from: 0
                  interval2_to: 0
              - service: select.select_option
                target:
                  entity_id: select.vistapool_pump_speed_timer1
                data:
                  option: "High"
          
          # Zomer + Normale Temp (20-26°C)
          - conditions:
              - "{{ temp >= 20 and temp <= 26 }}"
              - "{{ month >= 5 and month <= 9 }}"
            sequence:
              - service: vistapool.set_timer_intervals
                data:
                  interval1_from: 28800  # 08:00
                  interval1_to: 68400    # 19:00 (11 uur)
                  interval2_from: 0
                  interval2_to: 0
              - service: select.select_option
                target:
                  entity_id: select.vistapool_pump_speed_timer1
                data:
                  option: "Medium"
          
          # Tussenseizoen (15-20°C)
          - conditions:
              - "{{ temp >= 15 and temp < 20 }}"
            sequence:
              - service: vistapool.set_timer_intervals
                data:
                  interval1_from: 32400  # 09:00
                  interval1_to: 61200    # 17:00 (8 uur)
                  interval2_from: 0
                  interval2_to: 0
              - service: select.select_option
                target:
                  entity_id: select.vistapool_pump_speed_timer1
                data:
                  option: "Medium"
          
          # Winter (< 15°C)
          - conditions:
              - "{{ temp < 15 }}"
            sequence:
              - service: vistapool.set_timer_intervals
                data:
                  interval1_from: 43200  # 12:00
                  interval1_to: 54000    # 15:00 (3 uur)
                  interval2_from: 0
                  interval2_to: 0
              - service: select.select_option
                target:
                  entity_id: select.vistapool_pump_speed_timer1
                data:
                  option: "Slow"
```

---

### Auto 20: Dashboard Notificatie Samenvatting
**Doel:** Dagelijkse status update

```yaml
automation:
  - alias: "Zwembad: Dagelijkse Status Rapport"
    description: "Stuur dagelijks overzicht om 20:00"
    trigger:
      - platform: time
        at: "20:00:00"
    action:
      - service: notify.mobile_app
        data:
          title: "📊 Zwembad Dagrapport"
          message: |
            🌡️ Temperatuur: {{ states('sensor.vistapool_main_temperature') }}°C
            💧 pH: {{ states('sensor.vistapool_modules_ph_current') }}
            ⚡ Redox: {{ states('sensor.vistapool_modules_rx_current') }} mV
            ⏱️ Filtratie: {{ states('sensor.vistapool_filtration_status') }}
            💊 Hydrolyse: {{ states('sensor.vistapool_hidro_level') }}%
            🔋 Cel Tijd: {{ (states('sensor.vistapool_hidro_cell_total') | int / 3600) | round(1) }}h
          data:
            actions:
              - action: "VIEW_POOL"
                title: "Open Dashboard"
```

---

## 📱 Bonus: Dashboard Card Voorbeeld

```yaml
type: vertical-stack
cards:
  - type: entities
    title: Zwembad Controle
    entities:
      - entity: switch.vistapool_zwembadpomp
        name: Pomp
      - entity: switch.vistapool_zwembadlicht
        name: Licht
      - entity: select.vistapool_filtration_mode
        name: Modus
      - entity: number.vistapool_hydrolyse_level
        name: Hydrolyse %

  - type: glance
    title: Waterkwaliteit
    entities:
      - entity: sensor.vistapool_main_temperature
        name: Temp
      - entity: sensor.vistapool_modules_ph_current
        name: pH
      - entity: sensor.vistapool_modules_rx_current
        name: Redox
      - entity: sensor.vistapool_filtration_status
        name: Status

  - type: history-graph
    title: Temperatuur Verloop
    hours_to_show: 24
    entities:
      - entity: sensor.vistapool_main_temperature
```

---

## 🎯 Tips voor Beste Resultaten

1. **Start Klein**: Begin met 2-3 basis automatiseringen
2. **Test Grondig**: Test elke automatisering apart
3. **Monitor Gedrag**: Check logs eerste week
4. **Pas Geleidelijk Aan**: Wijzig instellingen stapsgewijs
5. **Documenteer**: Noteer wat werkt voor jouw situatie

---

**Veel plezier met je slimme zwembad! 🏊‍♂️💙**
