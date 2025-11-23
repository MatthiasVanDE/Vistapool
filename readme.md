# 🏊 Vistapool / Sugar Valley Oxilife - Home Assistant Integratie

Complete Home Assistant integratie voor Vistapool / Sugar Valley Oxilife zwembad controllers.

## ✨ Features

### 📊 Monitoring (100+ sensors)
- **Temperatuur**: Water, lucht, hydrolyse
- **pH & Redox**: Actuele waarden en alarmen
- **Hydrolyse**: Level, stroomverbruik, celtijd
- **Modules**: CL, CD, UV, IO status
- **Relays**: Status van alle relays
- **Systeem**: WiFi, firmware, netwerk info

### 🎛️ Volledige Controle

#### Switches (14 switches)
- ✅ Zwembadpomp aan/uit
- ✅ Zwembadlicht aan/uit
- ✅ Licht automatische modus
- ✅ Backwash actief
- ✅ Chloorshock
- ✅ Hydrolyse in-/uitschakelen
- ✅ Hydrolyse temperatuur sensor
- ✅ Hydrolyse dekzeil detectie
- ✅ Relay 1-4 aan/uit
- ✅ Verwarming aan/uit
- ✅ Smart mode vorstbeveiliging

#### Numbers (35+ instelbare waarden)
**Set Points:**
- pH setpoint (hoog/laag)
- Redox setpoint
- Chloor setpoint
- CD setpoint

**Hydrolyse:**
- Level (0-100%)
- Reductie percentage
- Max toegestane waarde

**Filtratie:**
- Watertemperatuur setpoint
- Verwarming temperatuur (normaal/max)
- Smart mode temperaturen (min/max)
- Timer intervals 1-3 (start/eind)

**Backwash:**
- Interval duur
- Frequentie
- Start tijd

**Verlichting:**
- Start tijd
- Eind tijd
- Frequentie

**Relays (per relay 1-4):**
- Vertraging
- Start tijd
- Eind tijd

#### Selects (8 dropdowns)
- Filtratie modus (Manual/Auto/Smart)
- Pomp snelheid (Slow/Medium/High)
  - Manuele modus
  - Per interval (1-3)
- Pomp type
- Backwash modus (Manual/Automatic)
- Backwash frequentie (dag/week/maand)
- pH dosering type (ACID/BASE)

## 📥 Installatie

### Optie 1: HACS (Aanbevolen)

1. Open HACS in Home Assistant
2. Ga naar "Integrations"
3. Klik op het menu (3 puntjes) rechts boven
4. Selecteer "Custom repositories"
5. Voeg toe:
   - **Repository**: `https://github.com/MatthiasVanDE/Vistapool`
   - **Category**: Integration
6. Klik op "Vistapool" in de lijst
7. Klik op "Download"
8. Herstart Home Assistant

### Optie 2: Manueel

1. Download de `custom_components/vistapool` folder
2. Kopieer naar `config/custom_components/vistapool` in je Home Assistant installatie
3. Herstart Home Assistant

## ⚙️ Configuratie

### Benodigde Gegevens

Je hebt de volgende informatie nodig:

1. **Email & Password**: Je Vistapool account inloggegevens
2. **API Key**: Firebase API key
3. **Project ID**: Firebase project (meestal `hayward-europe`)
4. **Gateway ID**: Je gateway ID (bijv. `P32202209190043`)
5. **Pool ID**: Je pool ID (24 karakters hexadecimaal)

### API Key Vinden

De Firebase API key kan je vinden door:

1. Inloggen op de Vistapool app
2. Developer tools in je browser openen
3. Network tab bekijken
4. Zoeken naar requests met `?key=` in de URL
5. De key na `?key=` is je API key

### Gateway ID en Pool ID Vinden

Je kan deze vinden in de network logs van de Vistapool web app of mobiele app.

### Setup in Home Assistant

1. Ga naar **Instellingen** → **Apparaten & Services**
2. Klik op **Integratie toevoegen**
3. Zoek naar **Vistapool**
4. Vul de gevraagde gegevens in
5. Klik op **Verzenden**

De integratie zal automatisch alle beschikbare entities aanmaken.

## 🎯 Gebruik

### Apparaten

De integratie maakt de volgende apparaten aan:

- **Filtratie**: Pomp, backwash, intervals, timers
- **Hydrolyse**: Elektrolyse, chloorshock, temperatuur
- **Set points**: pH, Redox, Chloor, CD setpoints
- **Relays**: Configureerbare relays 1-4
- **Algemeen (Global)**: Top-level systeem info
- **Algemeen (Main)**: Main controller info
- **Modules**: pH, Rx, CL, CD, UV, IO modules
- **Form**: Locatie en configuratie info

### Services

#### `vistapool.set_timer_intervals`

Stel meerdere filtratie timer intervals in één keer in.

**Parameters:**
- `interval1_from`: Start tijd interval 1 (seconden sinds middernacht)
- `interval1_to`: Eind tijd interval 1
- `interval2_from`: Start tijd interval 2 (optioneel)
- `interval2_to`: Eind tijd interval 2 (optioneel)
- `interval3_from`: Start tijd interval 3 (optioneel)
- `interval3_to`: Eind tijd interval 3 (optioneel)

**Voorbeeld:**
```yaml
service: vistapool.set_timer_intervals
data:
  interval1_from: 28800  # 8:00
  interval1_to: 61200    # 17:00
  interval2_from: 0
  interval2_to: 0
```

### Automatiseringen

**Voorbeeld: Pomp inschakelen bij hoge temperatuur**
```yaml
automation:
  - alias: "Pomp aan bij hoge temperatuur"
    trigger:
      - platform: numeric_state
        entity_id: sensor.vistapool_main_temperature
        above: 28
    action:
      - service: switch.turn_on
        target:
          entity_id: switch.vistapool_zwembadpomp
```

**Voorbeeld: Chloorshock 's nachts**
```yaml
automation:
  - alias: "Chloorshock 's nachts"
    trigger:
      - platform: time
        at: "23:00:00"
    condition:
      - condition: numeric_state
        entity_id: sensor.vistapool_main_temperature
        above: 20
    action:
      - service: switch.turn_on
        target:
          entity_id: switch.vistapool_chloorshock
```

## 🔧 Geavanceerde Configuratie

### Update Interval

Standaard update interval is 30 seconden. Je kan dit aanpassen:

1. Ga naar **Instellingen** → **Apparaten & Services**
2. Klik op **Vistapool**
3. Klik op **Opties configureren**
4. Pas het update interval aan (10-300 seconden)

### Debug Logging

Voeg toe aan `configuration.yaml`:

```yaml
logger:
  default: info
  logs:
    custom_components.vistapool: debug
```

## 📝 Tijdformaten

De integratie gebruikt verschillende tijdformaten:

- **Seconden sinds middernacht**: Voor intervals (0-86400)
  - Voorbeeld: 28800 = 08:00, 61200 = 17:00
- **UNIX timestamp**: Voor absolute tijdstippen
- **HH:MM:SS**: Voor weergave in sensors

**Handige conversies:**
- 1 uur = 3600 seconden
- 8:00 = 28800 seconden
- 17:00 = 61200 seconden

## 🐛 Problemen Oplossen

### Integratie start niet

1. Check de logs: **Instellingen** → **Systeem** → **Logs**
2. Controleer of alle gegevens correct zijn
3. Test je login op de Vistapool website
4. Check je netwerk connectie

### Entities worden niet aangemaakt

1. Herstart Home Assistant
2. Verwijder en voeg de integratie opnieuw toe
3. Check de logs voor errors

### Commando's werken niet

1. Check of de switch/sensor beschikbaar is (niet grijs)
2. Bekijk de logs voor API errors
3. Test of de Vistapool app nog werkt
4. Check je internet verbinding

### Waarden kloppen niet

1. Vergelijk met de Vistapool app
2. Check of de coordinator data refresht (bekijk logs)
3. Pas het update interval aan indien nodig

## 🤝 Bijdragen

Bijdragen zijn welkom! 

1. Fork de repository
2. Maak een feature branch
3. Commit je wijzigingen
4. Push naar de branch
5. Open een Pull Request

## 📄 Licentie

MIT License - zie LICENSE file voor details

## 🙏 Credits

- Ontwikkeld door [@MatthiasVanDE](https://github.com/MatthiasVanDE)
- Gebaseerd op reverse engineering van de Vistapool/Hayward API
- Dank aan de Home Assistant community

## 📞 Support

- **Issues**: [GitHub Issues](https://github.com/MatthiasVanDE/Vistapool/issues)
- **Discussies**: [GitHub Discussions](https://github.com/MatthiasVanDE/Vistapool/discussions)

## 🔄 Updates

### Versie 2.0.0 (Nieuw!)

✨ **Nieuwe features:**
- 14 switches voor volledige controle
- 35+ instelbare waarden (numbers)
- 8 dropdown selecties (selects)
- Relay configuratie
- Geavanceerde filtratie opties
- Hydrolyse uitgebreide controle

🔧 **Verbeteringen:**
- Complete refactoring voor betere onderhoudbaarheid
- Betere error handling
- Uitgebreide logging
- Type hints overal
- Configureerbaar update interval

📚 **Documentatie:**
- Complete README
- Service documentatie
- Voorbeelden en automatiseringen

---

**Geniet van je slimme zwembad! 🏊‍♂️💧**
