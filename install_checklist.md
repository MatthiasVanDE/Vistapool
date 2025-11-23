# 📋 Vistapool Installatie Checklist

Stap-voor-stap gids om de Vistapool integratie te installeren en te configureren.

---

## ✅ Pre-Installatie Checklist

### Benodigdheden
- [ ] Home Assistant 2024.1.0 of nieuwer
- [ ] SSH/Terminal toegang tot Home Assistant
- [ ] Vistapool/Sugar Valley Oxilife account
- [ ] Actieve internet verbinding
- [ ] 15-30 minuten tijd

### Verzamel Deze Gegevens
- [ ] **Email**: _________________
- [ ] **Wachtwoord**: _________________
- [ ] **API Key**: `AIza________________________` (39 tekens)
- [ ] **Project ID**: `hayward-europe` (meestal)
- [ ] **Gateway ID**: `P________________` (bijv. P32202209190043)
- [ ] **Pool ID**: `________________________` (24 hexadecimale tekens)

### API Gegevens Vinden

#### Firebase API Key
1. Open Vistapool web app in browser
2. Open Developer Tools (F12)
3. Ga naar Network tab
4. Filter op "key="
5. Zoek in URL: `?key=AIza...`

#### Gateway ID
- Staat in je Vistapool app
- Of in Network requests naar `sendCommand`

#### Pool ID
1. Developer Tools → Network
2. Filter op "pools"
3. URL eindigt op: `.../pools/005E00464E43501320343337`

---

## 📦 Stap 1: Backup Maken

### 1.1 Backup via UI
```
Settings → System → Backups → Create Backup
```
Selecteer:
- [x] Configuration
- [x] Add-ons (optioneel)
- [x] Home Assistant

### 1.2 Backup via CLI
```bash
ha backups new --name "pre-vistapool-install"
```

✅ **Checkpoint:** Backup succesvol gemaakt

---

## 💾 Stap 2: Bestanden Installeren

### Optie A: Via HACS (Aanbevolen)

#### 2.1 HACS Installeren (als nog niet gedaan)
```
https://hacs.xyz/docs/setup/download
```

#### 2.2 Custom Repository Toevoegen
1. HACS → Integrations
2. Menu (⋮) rechts boven → Custom repositories
3. Repository: `https://github.com/MatthiasVanDE/Vistapool`
4. Category: Integration
5. Klik ADD

#### 2.3 Installeren
1. Zoek "Vistapool" in HACS
2. Klik op de kaart
3. Klik DOWNLOAD
4. Selecteer laatste versie
5. Klik DOWNLOAD

✅ **Checkpoint:** Vistapool verschijnt in HACS installed

### Optie B: Handmatige Installatie

#### 2.1 SSH Verbinding
```bash
ssh root@homeassistant.local
# Of via Terminal add-on
```

#### 2.2 Bestanden Kopiëren
```bash
# Maak directory
cd /config
mkdir -p custom_components/vistapool

# Download bestanden (voorbeeld met wget)
cd custom_components/vistapool

# Download alle Python bestanden
wget https://raw.githubusercontent.com/MatthiasVanDE/Vistapool/main/__init__.py
wget https://raw.githubusercontent.com/MatthiasVanDE/Vistapool/main/api.py
wget https://raw.githubusercontent.com/MatthiasVanDE/Vistapool/main/coordinator.py
wget https://raw.githubusercontent.com/MatthiasVanDE/Vistapool/main/switch.py
wget https://raw.githubusercontent.com/MatthiasVanDE/Vistapool/main/number.py
wget https://raw.githubusercontent.com/MatthiasVanDE/Vistapool/main/select.py
wget https://raw.githubusercontent.com/MatthiasVanDE/Vistapool/main/sensor.py
wget https://raw.githubusercontent.com/MatthiasVanDE/Vistapool/main/config_flow.py
wget https://raw.githubusercontent.com/MatthiasVanDE/Vistapool/main/const.py
wget https://raw.githubusercontent.com/MatthiasVanDE/Vistapool/main/firestore_parser.py
wget https://raw.githubusercontent.com/MatthiasVanDE/Vistapool/main/manifest.json
wget https://raw.githubusercontent.com/MatthiasVanDE/Vistapool/main/strings.json
wget https://raw.githubusercontent.com/MatthiasVanDE/Vistapool/main/services.yaml
```

#### 2.3 Check Bestanden
```bash
ls -la /config/custom_components/vistapool/
```

Moet tonen:
```
__init__.py
api.py
coordinator.py
switch.py
number.py
select.py
sensor.py
config_flow.py
const.py
firestore_parser.py
manifest.json
strings.json
services.yaml
```

✅ **Checkpoint:** Alle 13 bestanden aanwezig

---

## 🔄 Stap 3: Home Assistant Herstarten

### 3.1 Restart via UI
```
Settings → System → Restart → Restart Home Assistant
```

### 3.2 Restart via CLI
```bash
ha core restart
```

### 3.3 Wacht op Opstart
- Wacht 2-3 minuten
- Check dat HA volledig opgestart is
- Dashboard moet bereikbaar zijn

✅ **Checkpoint:** Home Assistant draait opnieuw

---

## ⚙️ Stap 4: Integratie Configureren

### 4.1 Integratie Toevoegen
1. Ga naar `Settings → Devices & Services`
2. Klik op `+ ADD INTEGRATION` (rechts onder)
3. Zoek: `vistapool`
4. Klik op `Vistapool / Sugar Valley Oxilife`

### 4.2 Vul Configuratie In
Vul de verzamelde gegevens in:

| Veld | Waarde | Voorbeeld |
|------|--------|-----------|
| Email | Je Vistapool email | `user@example.com` |
| Password | Je wachtwoord | `********` |
| Firebase API Key | 39 tekens key | `AIzaSyC...` |
| Firebase Project ID | Project naam | `hayward-europe` |
| Gateway ID | Je gateway | `P32202209190043` |
| Pool ID | 24 hex tekens | `005E00464E43501320343337` |

### 4.3 Submit
Klik `SUBMIT`

### 4.4 Mogelijke Errors

#### Error: "Ongeldige inloggegevens"
- ✅ Check email spelling
- ✅ Check wachtwoord (hoofdletters!)
- ✅ Probeer inloggen op Vistapool website
- ✅ Geen 2FA op account?

#### Error: "Cannot connect"
- ✅ Check internet verbinding
- ✅ Ping test: `ping 8.8.8.8`
- ✅ Firewall blokkeert Google APIs?
- ✅ Wacht 5 min en probeer opnieuw

#### Error: "Unknown"
- ✅ Check logs: `Settings → System → Logs`
- ✅ Zoek naar "vistapool" en "error"
- ✅ Zie TROUBLESHOOTING.md

✅ **Checkpoint:** Integratie gelukt zonder errors

---

## 🎛️ Stap 5: Entities Verifiëren

### 5.1 Check Apparaten
```
Settings → Devices & Services → Vistapool
```

Moet 8 apparaten tonen:
- [ ] Filtratie
- [ ] Hydrolyse
- [ ] Set points
- [ ] Relays
- [ ] Algemeen (Global)
- [ ] Algemeen (Main)
- [ ] Modules
- [ ] Form

### 5.2 Check Entities
```
Developer Tools → States
Filter: "vistapool"
```

Verwacht aantal entities:
- ~14 switches
- ~38 numbers
- ~8 selects
- ~100 sensors
- **Totaal: ~160 entities**

### 5.3 Check Entity Status
In Developer Tools → States:
- [ ] Geen "unavailable" (tenzij verwacht)
- [ ] Geen "unknown" waarden
- [ ] Temperatuur sensors tonen waarden
- [ ] pH en Redox hebben waarden

✅ **Checkpoint:** Alle entities beschikbaar

---

## 🧪 Stap 6: Basis Functionaliteit Testen

### Test 1: Pomp Aan/Uit
1. Zet eerst filtratie mode naar "Manual":
   ```
   select.vistapool_filtration_mode → Manual
   ```
2. Toggle `switch.vistapool_zwembadpomp` AAN
3. Wacht 10 seconden
4. Check in Vistapool app → Pomp moet aanstaan
5. Toggle UIT
6. Check app → Pomp moet uitstaan

✅ **Test 1 geslaagd**

### Test 2: pH Setpoint Wijzigen
1. Open `number.vistapool_ph_setpoint_high`
2. Wijzig naar 7.20
3. Wacht 10 seconden
4. Check `sensor.vistapool_modules_ph_high` = 7.2
5. Check in app → pH setpoint = 7.20

✅ **Test 2 geslaagd**

### Test 3: Mode Switching
1. Zet `select.vistapool_filtration_mode` naar "Auto"
2. Wacht 5 sec
3. Check `sensor.vistapool_filtration_mode` = "Auto"
4. Zet naar "Smart"
5. Check sensor = "Smart"

✅ **Test 3 geslaagd**

### Test 4: Data Refresh
1. Noteer `sensor.vistapool_main_temperature`
2. Wacht 30 seconden (update interval)
3. Check `sensor.vistapool_updated_at` is recent (< 1 min)

✅ **Test 4 geslaagd**

---

## 📊 Stap 7: Logs Controleren

### 7.1 Check voor Errors
```bash
# Via Terminal
grep -i "error" /config/home-assistant.log | grep -i "vistapool"
```

Of via UI:
```
Settings → System → Logs
Filter: "vistapool"
```

### 7.2 Normale Log Output
Moet zien:
```
INFO Vistapool login succesvol
DEBUG Pool data succesvol opgehaald en geparst
```

### 7.3 Warnings OK
Deze warnings zijn normaal:
```
DEBUG Vernieuw Vistapool token
DEBUG Token succesvol vernieuwd
```

✅ **Checkpoint:** Geen kritieke errors in logs

---

## 🔧 Stap 8: Opties Configureren (Optioneel)

### 8.1 Update Interval Aanpassen
```
Settings → Devices & Services → Vistapool
Klik op "CONFIGURE"
Update interval: 30-60 seconden
```

Aanbevolen:
- Normaal: 30 sec
- Performance save: 60 sec
- Actief gebruik: 15 sec (niet aanbevolen)

✅ **Checkpoint:** Opties ingesteld

---

## 🎨 Stap 9: Dashboard Maken

### 9.1 Nieuwe Dashboard
```
Settings → Dashboards → + ADD DASHBOARD
Naam: "Zwembad"
Icon: mdi:pool
```

### 9.2 Basis Kaart Toevoegen
```yaml
type: entities
title: Zwembad Controle
entities:
  - entity: switch.vistapool_zwembadpomp
    name: Pomp
  - entity: switch.vistapool_zwembadlicht
    name: Licht
  - entity: sensor.vistapool_main_temperature
    name: Temperatuur
  - entity: sensor.vistapool_modules_ph_current
    name: pH Waarde
  - entity: select.vistapool_filtration_mode
    name: Modus
```

### 9.3 Meer Voorbeelden
Zie **AUTOMATIONS.md** → "Bonus: Dashboard Card"

✅ **Checkpoint:** Dashboard werkt

---

## 🤖 Stap 10: Eerste Automatisering

### 10.1 Eenvoudige Pomp Timer
```yaml
# configuration.yaml of via UI
automation:
  - alias: "Zwembad: Pomp Timer"
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

### 10.2 Test Automatisering
```
Developer Tools → Automations
Zoek: "Zwembad: Pomp Timer"
Klik: RUN
```

✅ **Checkpoint:** Eerste automatisering werkt

---

## 📱 Stap 11: Mobiele App (Optioneel)

### 11.1 Notificaties Instellen
Installeer Home Assistant Companion app:
- iOS: App Store
- Android: Play Store

### 11.2 Test Notificatie
```yaml
service: notify.mobile_app_YOUR_PHONE
data:
  title: "Test Zwembad"
  message: "Vistapool integratie actief! 🏊"
```

✅ **Checkpoint:** Notificaties werken

---

## 🎓 Stap 12: Geavanceerde Features

### 12.1 Debug Logging (Optioneel)
```yaml
# configuration.yaml
logger:
  default: warning
  logs:
    custom_components.vistapool: debug
```

### 12.2 Service Calls Testen
```yaml
# Developer Tools → Services
service: vistapool.set_timer_intervals
data:
  interval1_from: 28800  # 08:00
  interval1_to: 61200    # 17:00
```

✅ **Checkpoint:** Services werken

---

## 🎯 Post-Installatie Checklist

### Verificatie
- [ ] Alle 160+ entities beschikbaar
- [ ] Geen errors in logs
- [ ] Basis tests geslaagd (pomp, pH, mode)
- [ ] Dashboard gemaakt
- [ ] Eerste automatisering actief
- [ ] Backup gemaakt na installatie

### Aanbevolen Volgende Stappen
1. [ ] Lees **ENTITIES_OVERVIEW.md** voor alle entities
2. [ ] Implementeer meer automatiseringen uit **AUTOMATIONS.md**
3. [ ] Voer **TEST_SCENARIOS.md** uit
4. [ ] Configureer seizoen instellingen
5. [ ] Setup notificaties voor alarmen

### Troubleshooting
Als iets niet werkt:
1. Check **TROUBLESHOOTING.md**
2. Bekijk logs: `grep -i vistapool /config/home-assistant.log`
3. Herstart HA
4. Herstart integratie
5. Maak GitHub issue als probleem blijft

---

## 📞 Support

### Bronnen
- 📖 **README.md** - Complete documentatie
- 📋 **ENTITIES_OVERVIEW.md** - Alle entities uitgelegd
- 🧪 **TEST_SCENARIOS.md** - Test alle functionaliteit
- 🤖 **AUTOMATIONS.md** - 20 automatiseringen
- 🔧 **TROUBLESHOOTING.md** - Oplossing voor problemen

### Community
- **GitHub Issues**: [Link naar repository]/issues
- **Home Assistant Forum**: community.home-assistant.io
- **Discord**: Home Assistant Discord

---

## ✅ Installatie Compleet!

**Gefeliciteerd!** 🎉

Je Vistapool integratie is nu volledig geïnstalleerd en geconfigureerd.

### Wat Nu?
1. **Experimenteer** met de verschillende entities
2. **Bouw** automatiseringen die bij jouw gebruik passen
3. **Monitor** je zwembad 24/7 vanuit Home Assistant
4. **Geniet** van je slimme zwembad!

---

**Veel plezier met je geautomatiseerde zwembad! 🏊‍♂️💙**
