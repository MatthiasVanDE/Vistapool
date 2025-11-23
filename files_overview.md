# 📁 Vistapool Bestandsstructuur

Overzicht van alle bestanden in de integratie en hun functie.

---

## 📦 Verplichte Bestanden (Integratie Code)

### `manifest.json` (15 regels)
**Doel:** Metadata voor Home Assistant  
**Bevat:**
- Domain naam: `vistapool`
- Versie: `2.0.0`
- Requirements: `requests>=2.31.0`
- Codeowners, documentation links

**Belangrijk:** Zonder dit bestand wordt integratie niet herkend!

---

### `__init__.py` (150 regels)
**Doel:** Entry point van de integratie  
**Functionaliteit:**
- Setup integratie via config flow
- Platform forwarding (sensor, switch, number, select)
- Service registratie (`set_timer_intervals`)
- Options flow support (update interval)
- Cleanup bij unload

**Key functions:**
- `async_setup()` - YAML setup (optioneel)
- `async_setup_entry()` - UI config setup
- `async_unload_entry()` - Cleanup
- `async_reload_entry()` - Options reload

---

### `config_flow.py` (120 regels)
**Doel:** UI configuratie wizard  
**Functionaliteit:**
- Formulier voor API credentials
- Input validatie
- Test connectie voordat entry wordt aangemaakt
- Error handling (invalid auth, cannot connect)
- Options flow (update interval)

**Key classes:**
- `VistapoolConfigFlow` - Main flow
- `VistapoolOptionsFlow` - Options
- `validate_input()` - Validation helper

---

### `coordinator.py` (100 regels)
**Doel:** Data update coordinator  
**Functionaliteit:**
- Periodieke data refresh (default 30 sec)
- API login management
- Error handling en recovery
- Async command sending
- State management

**Key class:**
- `VistapoolDataUpdateCoordinator`
  - `_async_update_data()` - Fetch pool data
  - `async_send_command()` - Send simple commands
  - `async_send_pool_command()` - Send configuration

---

### `api.py` (250 regels)
**Doel:** API client voor Vistapool  
**Functionaliteit:**
- Firebase authentication
- Token management (1 uur geldig)
- Automatic token refresh
- Firestore document fetching
- Command sending (WRP operations)
- HTTP session reuse
- Custom exceptions

**Key class:**
- `VistapoolApiClient`
  - `login()` - Email/password auth
  - `refresh_id_token()` - Token refresh
  - `get_pool_document()` - Fetch data
  - `send_pool_command()` - Send commands

**Custom Exceptions:**
- `VistapoolApiError` - Base exception
- `VistapoolAuthError` - Auth failures
- `VistapoolConnectionError` - Network issues

---

### `const.py` (100 regels)
**Doel:** Constanten en mappings  
**Bevat:**
- Domain: `"vistapool"`
- Enum mappings (modes, speeds, frequencies)
- Device type constanten
- Device info templates
- Helper function: `get_device_info()`

**Key mappings:**
- `FILTRATION_MODE_MAP` - Manual/Auto/Smart
- `BACKWASH_MODE_MAP` - Manual/Automatic
- `PUMP_SPEED_MAP` - Slow/Medium/High
- `BACKWASH_FREQ_MAP` - Frequentie presets
- `TRUE_FALSE_MAP` - Boolean mappings

---

### `switch.py` (200 regels)
**Doel:** Switch entities (aan/uit)  
**Aantal entities:** 14 switches  
**Features:**
- Generieke `VistapoolSwitch` class
- Configureerbare data/command paths
- Lambda availability checks
- Inverted logic support

**Switches:**
- Pomp, Licht, Licht auto mode
- Backwash actief
- Chloorshock, Hydrolyse, Temp sensor, Dekzeil
- Relay 1-4
- Verwarming, Freeze protection

---

### `number.py` (450 regels)
**Doel:** Number entities (instelbare waarden)  
**Aantal entities:** 38 numbers  
**Features:**
- Generieke `VistapoolNumber` class
- Multiplier support (pH x100, Hydrolyse x10)
- Min/max/step configureerbaar
- Slider/Box mode
- Availability logic

**Categories:**
- Set Points (5): pH high/low, Redox, CL, CD
- Hydrolyse (3): Level, Reduction, Max
- Filtratie (5): Temps, heating
- Intervals (6): Timer 1-3 from/to
- Backwash (3): Interval, Frequency, StartAt
- Licht (3): From, To, Frequency
- Relays (12): 4 relays × 3 settings

---

### `select.py` (180 regels)
**Doel:** Select entities (dropdowns)  
**Aantal entities:** 8 selects  
**Features:**
- Generieke `VistapoolSelect` class
- Mapping dictionaries
- Availability checks

**Selects:**
- Filtratie modus
- Pomp snelheid (Manual + Timer 1-3)
- Pomp type
- Backwash modus + frequentie preset
- pH type (ACID/BASE)

---

### `sensor.py` (450 regels)
**Doel:** Sensor entities (read-only)  
**Aantal entities:** 100+ sensors  
**Features:**
- Factory pattern voor alle sensors
- Generieke `VistapoolSensor` class
- Value transformations (pH, tijd, temp)
- Value mappings (modes naar strings)

**Categories:**
- Global (7): isAWS, wifi, ID, timestamps
- Backwash (6): interval, mode, status, frequency
- Light (5): mode, freq, timing, status
- Hidro (19): cloration, temp, current, cell time
- Filtration (23): intervals, speeds, modes, temps
- Main (24): has* flags, version, network
- Modules (24): pH, Rx, CL, CD, UV, IO
- Relays (70+): GPIOs, relay info
- Form (7): Location data

---

### `firestore_parser.py` (40 regels)
**Doel:** Parse Firestore JSON format  
**Functionaliteit:**
- Convert Firestore types naar Python types
- Recursive parsing van nested objects
- Support voor mapValue, arrayValue, stringValue, etc.

**Key function:**
- `parse_firestore_doc()` - Main parser

---

### `strings.json` (60 regels)
**Doel:** UI translations (Nederlands)  
**Bevat:**
- Config flow teksten
- Error messages
- Service descriptions
- Field labels

---

### `services.yaml` (10 regels)
**Doel:** Service definities  
**Services:**
- `set_timer_intervals` - Bulk interval setting

---

## 📚 Documentatie Bestanden

### `README.md` (400 regels) ⭐
**Voor:** Gebruikers  
**Bevat:**
- Feature overzicht
- Installatie instructies (HACS + Manual)
- Configuratie uitleg
- Gebruik voorbeelden
- Services documentatie
- Automatisering voorbeelden
- Tips & tricks

---

### `QUICK_START.md` (100 regels) ⚡
**Voor:** Snelle start  
**Bevat:**
- 5-stappen installatie
- Eerste automatisering
- Dashboard voorbeeld
- Belangrijkste entities
- Troubleshooting basics

---

### `INSTALLATION_CHECKLIST.md` (200+ stappen) 📋
**Voor:** Gedetailleerde installatie  
**Bevat:**
- Pre-installatie checklist
- Stap-voor-stap instructies
- Verificatie checkpoints
- Test procedures
- Post-installatie setup
- Dashboard configuratie

---

### `ENTITIES_OVERVIEW.md` (200 regels) 📊
**Voor:** Entity reference  
**Bevat:**
- Volledige lijst van alle 160+ entities
- Tabellen per type (switches, numbers, selects, sensors)
- Apparaat indeling
- Entity ID's en beschrijvingen
- Handig tips voor zoeken

---

### `TEST_SCENARIOS.md` (800 regels) 🧪
**Voor:** Testing & QA  
**Bevat:**
- 23 gedetailleerde test scenarios
- Pre-test checklist
- Test categories:
  - Installatie (3 tests)
  - Switches (4 tests)
  - Numbers (6 tests)
  - Selects (4 tests)
  - Services (1 test)
  - Availability (3 tests)
  - Integration (2 tests)
  - Error handling (3 tests)
  - Performance (2 tests)
  - Stability (2 tests)
- Test report template
- Troubleshooting commands

---

### `AUTOMATIONS.md` (700 regels) 🤖
**Voor:** Automatisering voorbeelden  
**Bevat:**
- 20 complete automatiseringen:
  - Basis (3): Timer, licht, weekend
  - Temperatuur (3): Hitte, vorst, verwarming
  - Seizoen (2): Zomer/winter, regen
  - Energie (2): Goedkope uren, zonnepanelen
  - Waterkwaliteit (3): pH, chloorshock, redox
  - Veiligheid (3): Offline, storing, lek
  - Geavanceerd (4): Vakantie, feest, adaptief, rapport
- Dashboard card voorbeelden
- Tips voor beste resultaten

---

### `TROUBLESHOOTING.md` (900 regels) 🔧
**Voor:** Probleem oplossing  
**Bevat:**
- Installatie problemen (3)
- Configuratie fouten (3)
- Verbindings problemen (3)
- Entity problemen (3)
- Commando fouten (3)
- Performance issues (2)
- Data synchronisatie (2)
- Geavanceerde debug (4)
- Last resort solutions (2)
- Getting help sectie
- Preventive maintenance

---

### `CHANGELOG.md` (150 regels) 📝
**Voor:** Versie historie  
**Bevat:**
- Volledige changelog v1.0 → v2.0
- Breaking changes documentatie
- Migratie gids
- Toekomstige features (roadmap)
- Contributors en dankwoord

---

### `FILES_OVERVIEW.md` (Dit bestand) 📁
**Voor:** Developer reference  
**Bevat:**
- Overzicht alle bestanden
- Doel en functionaliteit per bestand
- Code structuur uitleg
- Dependencies

---

## 📊 Statistieken

### Code Bestanden
```
13 Python/JSON bestanden:
- manifest.json       15 regels
- __init__.py        150 regels
- config_flow.py     120 regels
- coordinator.py     100 regels
- api.py             250 regels
- const.py           100 regels
- switch.py          200 regels
- number.py          450 regels
- select.py          180 regels
- sensor.py          450 regels
- firestore_parser    40 regels
- strings.json        60 regels
- services.yaml       10 regels
━━━━━━━━━━━━━━━━━━━━━━━━━━━━
TOTAAL            ~2,125 regels
```

### Documentatie Bestanden
```
8 Markdown bestanden:
- README.md                  400 regels
- QUICK_START.md            100 regels
- INSTALLATION_CHECKLIST    200 regels
- ENTITIES_OVERVIEW         200 regels
- TEST_SCENARIOS            800 regels
- AUTOMATIONS               700 regels
- TROUBLESHOOTING           900 regels
- CHANGELOG                 150 regels
- FILES_OVERVIEW            100 regels
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
TOTAAL                   ~3,550 regels
```

### Grand Total
```
21 bestanden
~5,675 regels code + documentatie
160+ entities
20 automatisering voorbeelden
23 test scenarios
```

---

## 🗂️ Bestandsstructuur in Repository

```
vistapool/
├── custom_components/
│   └── vistapool/
│       ├── __init__.py
│       ├── api.py
│       ├── config_flow.py
│       ├── const.py
│       ├── coordinator.py
│       ├── firestore_parser.py
│       ├── manifest.json
│       ├── number.py
│       ├── select.py
│       ├── sensor.py
│       ├── services.yaml
│       ├── strings.json
│       └── switch.py
│
├── docs/
│   ├── README.md
│   ├── QUICK_START.md
│   ├── INSTALLATION_CHECKLIST.md
│   ├── ENTITIES_OVERVIEW.md
│   ├── TEST_SCENARIOS.md
│   ├── AUTOMATIONS.md
│   ├── TROUBLESHOOTING.md
│   ├── CHANGELOG.md
│   └── FILES_OVERVIEW.md
│
├── .github/
│   ├── ISSUE_TEMPLATE/
│   ├── workflows/
│   └── FUNDING.yml
│
├── LICENSE
└── .gitignore
```

---

## 🔗 Dependencies

### Python Libraries
```
requests >= 2.31.0  (HTTP client)
```

### Home Assistant
```
homeassistant >= 2024.1.0
```

### External APIs
```
- Firebase Authentication API
- Google Firestore API
- Hayward Cloud Functions
```

---

## 🎯 Gebruik per Bestand

### Voor Eindgebruikers:
1. `README.md` - Start hier
2. `QUICK_START.md` - Snel aan de slag
3. `AUTOMATIONS.md` - Inspiratie
4. `TROUBLESHOOTING.md` - Bij problemen

### Voor Installatie:
1. Alle bestanden in `custom_components/vistapool/`
2. `INSTALLATION_CHECKLIST.md` - Volg stappen

### Voor Developers:
1. Alle code bestanden
2. `FILES_OVERVIEW.md` - Dit bestand
3. `CHANGELOG.md` - Versie info
4. `TEST_SCENARIOS.md` - Testing

### Voor Testers:
1. `TEST_SCENARIOS.md` - Volledige test suite
2. `ENTITIES_OVERVIEW.md` - Wat te testen
3. `TROUBLESHOOTING.md` - Issue reporting

---

## 💡 Best Practices

### Code Organisatie
- ✅ Elk platform heeft eigen bestand (switch, number, select, sensor)
- ✅ Helpers in `const.py`
- ✅ API logic gescheiden in `api.py`
- ✅ Config flow gescheiden van setup

### Documentatie
- ✅ Elke functie heeft docstring
- ✅ Type hints overal
- ✅ Comments waar nodig
- ✅ README voor gebruikers
- ✅ Technical docs voor developers

### Testing
- ✅ Volledige test coverage in TEST_SCENARIOS.md
- ✅ Voorbeeld data in documentatie
- ✅ Error scenarios gedocumenteerd

---

## 📞 Support Files

Mist een bestand? Check:
- GitHub Issues template
- Contributing guidelines
- Code of Conduct
- GitHub Actions workflows

Deze worden typisch apart beheerd in `.github/` folder.

---

**Dit overzicht helpt je snel te vinden wat je nodig hebt! 📚**
