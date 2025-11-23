# ⚡ Vistapool Quick Start

Snel aan de slag in 5 minuten!

---

## 🚀 In 5 Stappen

### 1. Verzamel Deze Gegevens
```
Email:       _______________
Password:    _______________
API Key:     AIza___________________________ (39 tekens)
Project:     hayward-europe
Gateway ID:  P_____________ (uit Vistapool app)
Pool ID:     ________________________ (24 hex tekens)
```

**API Key vinden:**
1. Open Vistapool web app
2. F12 → Network tab
3. Zoek `?key=` in URL

**Pool ID vinden:**
1. F12 → Network tab
2. Filter op "pools"
3. Laatste deel van URL

---

### 2. Installeer via HACS

```
HACS → Integrations → ⋮ Menu → Custom repositories

Repository: https://github.com/MatthiasVanDE/Vistapool
Category: Integration
→ ADD → Download
```

**Of handmatig:**
```bash
cd /config/custom_components/
mkdir vistapool
# Kopieer alle .py bestanden + manifest.json + strings.json
```

---

### 3. Herstart Home Assistant

```
Settings → System → Restart
```

Wacht 2-3 minuten.

---

### 4. Configureer Integratie

```
Settings → Devices & Services → + ADD INTEGRATION
→ Zoek "Vistapool"
→ Vul gegevens in
→ SUBMIT
```

✅ Succes = 8 apparaten + ~160 entities!

---

### 5. Test Het!

**Pomp aan/uit:**
```
1. select.vistapool_filtration_mode → "Manual"
2. switch.vistapool_zwembadpomp → AAN
3. Check Vistapool app → Pomp moet draaien
```

**pH aanpassen:**
```
number.vistapool_ph_setpoint_high → 7.20
```

---

## 🎯 Eerste Automatisering (30 seconden)

**Pomp timer 8:00-17:00:**

```yaml
automation:
  - alias: "Zwembad Pomp Timer"
    trigger:
      - platform: time
        at: "08:00:00"
        id: start
      - platform: time
        at: "17:00:00"
        id: stop
    action:
      - choose:
          - conditions: "{{ trigger.id == 'start' }}"
            sequence:
              - service: switch.turn_on
                target:
                  entity_id: switch.vistapool_zwembadpomp
          - conditions: "{{ trigger.id == 'stop' }}"
            sequence:
              - service: switch.turn_off
                target:
                  entity_id: switch.vistapool_zwembadpomp
```

Kopieer → Plak in **Settings → Automations & Scenes → + CREATE → Edit in YAML**

---

## 📊 Dashboard (1 minuut)

```yaml
type: entities
title: Zwembad
entities:
  - switch.vistapool_zwembadpomp
  - switch.vistapool_zwembadlicht
  - sensor.vistapool_main_temperature
  - sensor.vistapool_modules_ph_current
  - select.vistapool_filtration_mode
```

---

## 🎛️ Belangrijkste Entities

### Switches (Aan/Uit)
- `switch.vistapool_zwembadpomp` - Pomp
- `switch.vistapool_zwembadlicht` - Licht
- `switch.vistapool_chloorshock` - Chloorshock
- `switch.vistapool_verwarming` - Verwarming

### Sensors (Status)
- `sensor.vistapool_main_temperature` - Watertemp
- `sensor.vistapool_modules_ph_current` - pH waarde
- `sensor.vistapool_modules_rx_current` - Redox (ORP)
- `sensor.vistapool_filtration_status` - Pomp status

### Selects (Modi)
- `select.vistapool_filtration_mode` - Manual/Auto/Smart
- `select.vistapool_pump_speed_manual` - Slow/Medium/High
- `select.vistapool_backwash_mode` - Manual/Automatic

### Numbers (Instellingen)
- `number.vistapool_ph_setpoint_high` - pH doel (6.0-8.5)
- `number.vistapool_hydrolyse_level` - Hydrolyse % (0-100)
- `number.vistapool_interval1_from` - Timer start (sec)

---

## ⚠️ Problemen?

### Error: "Invalid auth"
→ Check email + wachtwoord, probeer inloggen op website

### Error: "Cannot connect"
→ Check internet, ping google.com

### Entities "unavailable"
→ Herstart HA, wacht 2 min

### Pomp reageert niet
→ Zet eerst `select.vistapool_filtration_mode` naar "Manual"

---

## 📚 Meer Lezen

- **INSTALLATION_CHECKLIST.md** - Gedetailleerde installatie
- **ENTITIES_OVERVIEW.md** - Alle 160+ entities uitgelegd
- **AUTOMATIONS.md** - 20 kant-en-klare automatiseringen
- **TEST_SCENARIOS.md** - Test alle functionaliteit
- **TROUBLESHOOTING.md** - Oplossingen voor problemen

---

## 🎉 Klaar!

Je bent nu klaar om je zwembad te beheren via Home Assistant!

**Volgende stappen:**
1. Experimenteer met entities
2. Maak automatiseringen
3. Geniet van je slimme zwembad! 🏊‍♂️

---

**Need help?** Open een issue op GitHub of check TROUBLESHOOTING.md
