# 🔧 Vistapool Troubleshooting Guide

Complete gids voor het oplossen van problemen met de Vistapool integratie.

---

## 📋 Inhoudsopgave

1. [Installatie Problemen](#installatie-problemen)
2. [Configuratie Fouten](#configuratie-fouten)
3. [Verbindings Problemen](#verbindings-problemen)
4. [Entity Problemen](#entity-problemen)
5. [Commando Fouten](#commando-fouten)
6. [Performance Issues](#performance-issues)
7. [Data Synchronisatie](#data-synchronisatie)
8. [Geavanceerde Debug](#geavanceerde-debug)

---

## 🚀 Installatie Problemen

### Probleem 1: Integratie Verschijnt Niet in Lijst

**Symptomen:**
- "Vistapool" niet zichtbaar bij "Add Integration"
- Zoeken geeft geen resultaten

**Oplossing:**

**Stap 1:** Check installatie locatie
```bash
# SSH naar Home Assistant
cd /config/custom_components/
ls -la vistapool/

# Moet tonen:
# __init__.py
# manifest.json
# sensor.py
# switch.py
# ... etc
```

**Stap 2:** Valideer manifest.json
```bash
cat /config/custom_components/vistapool/manifest.json
```

Moet valide JSON zijn met:
```json
{
  "domain": "vistapool",
  "name": "Vistapool / Sugar Valley Oxilife",
  ...
}
```

**Stap 3:** Check logs voor Python errors
```bash
grep -i "vistapool" /config/home-assistant.log | grep -i "error"
```

**Stap 4:** Herstart Home Assistant
- Settings → System → Restart
- Wacht 2-3 minuten
- Try opnieuw

**Als het nog steeds niet werkt:**
1. Verwijder `/config/custom_components/vistapool/`
2. Herstart HA
3. Kopieer bestanden opnieuw
4. Check bestandsrechten: `chmod -R 755 /config/custom_components/vistapool/`
5. Herstart opnieuw

---

### Probleem 2: Import Errors bij Opstarten

**Symptomen:**
```
ERROR (MainThread) [homeassistant.setup] Error during setup of component vistapool
ModuleNotFoundError: No module named 'requests'
```

**Oplossing:**

**Optie A:** Requests library ontbreekt
```bash
# In Home Assistant container/venv
pip install requests
```

**Optie B:** Update manifest.json
```json
{
  "requirements": ["requests>=2.31.0"],
  ...
}
```

**Optie C:** Herinstalleer integratie via HACS
- HACS → Integrations
- Vistapool → Reinstall
- Restart HA

---

### Probleem 3: Version Mismatch

**Symptomen:**
```
WARNING Setup of vistapool is taking over 10 seconds
```

**Oplossing:**

Check Home Assistant versie:
```bash
ha core info
```

Minimum vereiste: **2024.1.0**

Update indien nodig:
- Settings → System → Updates
- Update Core

---

## ⚙️ Configuratie Fouten

### Probleem 4: "Ongeldige inloggegevens"

**Symptomen:**
- Error bij configuratie
- "invalid_auth" message

**Diagnose Checklist:**
- [ ] Email correct gespeld?
- [ ] Wachtwoord correct (let op hoofdletters)?
- [ ] Kan je inloggen op Vistapool website/app?
- [ ] 2FA actief op account?

**Oplossing:**

**Stap 1:** Test login handmatig
```python
# In Developer Tools → Template
import requests
url = "https://www.googleapis.com/identitytoolkit/v3/relyingparty/verifyPassword?key=YOUR_API_KEY"
payload = {
    "email": "YOUR_EMAIL",
    "password": "YOUR_PASSWORD",
    "returnSecureToken": True
}
response = requests.post(url, json=payload)
print(response.status_code, response.text)
```

**Verwacht:** Status 200 + idToken in response

**Stap 2:** Reset wachtwoord
1. Ga naar Vistapool website
2. Wachtwoord vergeten
3. Gebruik nieuw wachtwoord in HA

**Stap 3:** Check API Key
- API key moet 39 karakters zijn
- Format: `AIza...`
- Geen spaties voor/achter

---

### Probleem 5: "Cannot connect"

**Symptomen:**
- Configuratie faalt met connection error
- Timeout errors

**Oplossing:**

**Stap 1:** Test internet connectie
```bash
# Vanuit HA container
ping -c 3 8.8.8.8
ping -c 3 firestore.googleapis.com
```

**Stap 2:** Check firewall/proxy
- Port 443 (HTTPS) open?
- Geen proxy blocking Google APIs?

**Stap 3:** DNS probleem?
```bash
nslookup firestore.googleapis.com
```

Moet IP adres teruggeven.

**Stap 4:** Tijdelijke network issue
- Wacht 5 minuten
- Probeer opnieuw

---

### Probleem 6: Wrong Pool ID / Gateway ID

**Symptomen:**
- Configuratie werkt maar geen data
- Entities blijven "unknown"

**Vind Correcte IDs:**

**Methode 1:** Browser Developer Tools
1. Log in op Vistapool web app
2. Open Developer Tools (F12)
3. Network tab
4. Filter op "pools"
5. Zoek naar request URL:
   ```
   https://firestore.googleapis.com/.../pools/005E00464E43501320343337
                                              ^^^^^^^^^^^^^^^^^^^^^^^^
                                              Dit is je Pool ID (24 chars)
   ```

**Methode 2:** Check Config Entry
```bash
cd /config/.storage/
cat core.config_entries | grep vistapool -A 20
```

Zoek naar:
```json
"pool_id": "005E00464E43501320343337",
"gateway": "P32202209190043"
```

**Methode 3:** API Response
```python
# Pool ID staat ook in data response
# Check sensor.vistapool_id value
```

---

## 🌐 Verbindings Problemen

### Probleem 7: "Token Expired" Errors

**Symptomen:**
```
ERROR VistapoolApiClient: HTTP 401 Unauthorized
WARNING Token refresh gefaald, voer volledige login uit
```

**Dit is NORMAAL gedrag!** Token expires na 1 uur.

**Check of auto-refresh werkt:**
```bash
grep "token" /config/home-assistant.log | tail -20
```

Moet tonen:
```
DEBUG Vernieuw Vistapool token
DEBUG Token succesvol vernieuwd
```

**Als refresh faalt:**
1. Check internet verbinding
2. Herstart integratie:
   - Settings → Devices & Services
   - Vistapool → Reload

---

### Probleem 8: "Rate Limited" / 429 Errors

**Symptomen:**
```
ERROR HTTP 429: Too Many Requests
```

**Oorzaken:**
- Te frequent API calls
- Update interval te kort (<10 sec)
- Veel automations tegelijk

**Oplossing:**

**Stap 1:** Verhoog update interval
- Settings → Devices & Services
- Vistapool → Configure
- Update interval: 30-60 sec

**Stap 2:** Batch commando's
Gebruik services ipv individuele calls:
```yaml
# GOED
service: vistapool.set_timer_intervals
data:
  interval1_from: 28800
  interval1_to: 61200

# SLECHT (3 aparte API calls)
service: number.set_value
target:
  entity_id: number.vistapool_interval1_from
data:
  value: 28800
```

**Stap 3:** Debounce automations
```yaml
automation:
  trigger:
    - platform: ...
  action:
    - delay:
        seconds: 5  # Wacht 5 sec tussen commands
    - service: ...
```

---

### Probleem 9: Entities "Unavailable"

**Symptomen:**
- Alle/sommige entities grijs
- State = "unavailable"

**Diagnose:**

**Check 1:** Is integratie geladen?
```bash
ha core info | grep vistapool
```

**Check 2:** Is coordinator updating?
```bash
grep "Pool data succesvol" /config/home-assistant.log | tail -5
```

Moet recent zijn (< 60 sec).

**Check 3:** Specific entity unavailable?
Sommige entities hebben availability checks:
- Smart temp: alleen in Smart mode
- Backwash freq: alleen in Auto mode
- Hydrolyse: alleen als enabled

**Oplossing:**

**Voor alle entities unavailable:**
1. Check internet connectie
2. Check API credentials nog geldig
3. Reload integratie
4. Herstart HA

**Voor specifieke entities:**
Check of voorwaarden kloppen:
```yaml
# Developer Tools → States
# Filter op entity
# Check "available" attribute
```

---

## 🎛️ Entity Problemen

### Probleem 10: Entity Waarden Kloppen Niet

**Symptomen:**
- Sensor toont verkeerde waarde
- Waarde matcht niet met Vistapool app

**Diagnose:**

**Stap 1:** Check raw data
```yaml
# Developer Tools → States
# Zoek: sensor.vistapool_modules_ph_current
# Check attributes → raw value
```

**Stap 2:** Vergelijk met app
- Open Vistapool app
- Check dezelfde waarde
- Noteer verschil

**Stap 3:** Check data transform
Sommige waarden worden getransformeerd:
- pH: 710 → 7.10 (/ 100)
- Hydrolyse: 1000 → 100% (/ 10)
- Tijd: 28800 → 08:00:00 (seconds to time)

**Oplossing:**

**Voor pH waarden:**
```python
# Raw API: "710"
# Sensor: 7.10
# Transform: int(value) / 100
```

Check `sensor_helpers.py` → `ph_to_float()` functie.

**Voor tijd waarden:**
```python
# Raw API: 28800 (seconden sinds middernacht)
# Sensor: "08:00:00"
# Transform: seconds_to_time()
```

**Als waarde echt fout is:**
1. Check Vistapool app voor correcte waarde
2. Update in app
3. Wacht 30-60 sec voor sync
4. Reload HA entity

---

### Probleem 11: Entity Niet Updaten

**Symptomen:**
- Waarde verandert niet
- Blijft op oude waarde steken

**Oplossing:**

**Check 1:** Coordinator refresh
```bash
grep "async_request_refresh" /config/home-assistant.log | tail -10
```

**Check 2:** Force manual refresh
```yaml
# Developer Tools → Services
service: homeassistant.update_entity
target:
  entity_id: sensor.vistapool_main_temperature
```

**Check 3:** Reload integratie
- Settings → Devices & Services
- Vistapool → ... → Reload

**Check 4:** Cache issue
```bash
# Stop HA
ha core stop

# Clear cache
rm -rf /config/.storage/core.entity_registry

# Start HA
ha core start
```

⚠️ **Waarschuwing:** Dit verwijdert entity customizations!

---

### Probleem 12: Duplicate Entities

**Symptomen:**
- Entity bestaat 2x
- `sensor.vistapool_temperature` + `sensor.vistapool_temperature_2`

**Oorzaak:**
- Integratie 2x toegevoegd
- Upgrade van oude versie

**Oplossing:**

**Stap 1:** Check config entries
```bash
cd /config/.storage/
cat core.config_entries | grep vistapool -c
```

Moet 1 zijn.

**Stap 2:** Verwijder duplicate
- Settings → Devices & Services
- Vistapool → ... → Delete
- Voeg integratie 1x toe

**Stap 3:** Verwijder oude entities
- Settings → Entities
- Filter: "vistapool"
- Verwijder duplicates met `_2`, `_3` suffix

**Stap 4:** Clear entity registry
Zie Probleem 11, Check 4.

---

## 🎮 Commando Fouten

### Probleem 13: Switch Schakelt Niet

**Symptomen:**
- Switch toggle maar werkt niet
- Geen effect op zwembad
- Switch keert terug naar vorige state

**Diagnose:**

**Check logs:**
```bash
grep "Zet.*aan\|uit" /config/home-assistant.log | tail -10
```

Verwacht:
```
DEBUG Zet Zwembadpomp aan met changes: {'filtration': {'status': 1}}
INFO Pool commando WRP succesvol verzonden
```

**Check API response:**
```bash
grep "Pool commando" /config/home-assistant.log | tail -5
```

**Mogelijke oorzaken:**

1. **Mode mismatch**
   - Pomp manual switch werkt alleen in Manual mode
   - Fix: Zet `select.vistapool_filtration_mode` naar "Manual"

2. **Hydrolyse disabled**
   - Chloorshock werkt niet als hydrolyse uit is
   - Fix: Zet `switch.vistapool_hydrolyse_ingeschakeld` aan

3. **Availability issue**
   - Entity is unavailable (grijs)
   - Check voorwaarden (zie Probleem 9)

**Oplossing:**

**Test commando direct:**
```yaml
# Developer Tools → Services
service: switch.turn_on
target:
  entity_id: switch.vistapool_zwembadpomp
```

Check logs voor errors.

**Manual API test:**
```yaml
# Developer Tools → Services
service: vistapool.set_timer_intervals
data:
  interval1_from: 28800
  interval1_to: 61200
```

Als dit werkt maar switch niet → switch bug.

---

### Probleem 14: Number Wijzigingen Niet Doorgevoerd

**Symptomen:**
- Number waarde instellen
- Waarde keert terug naar oud
- Geen effect in app

**Diagnose:**

**Check command:**
```bash
grep "Set.*naar" /config/home-assistant.log | tail -10
```

Verwacht:
```
DEBUG Set pH Setpoint Hoog naar 7.2 (API: 720)
INFO Pool commando WRP succesvol verzonden
```

**Check multiplier:**
Sommige numbers hebben multiplier:
- pH: x100 (7.2 → 720)
- Hydrolyse: x10 (50 → 500)

**Oplossing:**

**Test met service call:**
```yaml
# Developer Tools → Services
service: number.set_value
target:
  entity_id: number.vistapool_ph_setpoint_high
data:
  value: 7.2
```

Check logs:
```bash
tail -f /config/home-assistant.log | grep "pH Setpoint"
```

**Verify in app:**
1. Set waarde in HA
2. Wacht 30 sec
3. Check Vistapool app
4. Waarde moet matchen

**Als waarde niet blijft:**
- Mogelijk Vistapool systeem override
- Check physical controller instellingen
- Mogelijk range limiet (te hoog/laag)

---

### Probleem 15: Select Optie Niet Toegepast

**Symptomen:**
- Dropdown keuze gemaakt
- Geen effect
- Valt terug naar vorige optie

**Oplossing:**

**Check mapping:**
```python
# const.py
FILTRATION_MODE_MAP = {
    "Manual": 0,
    "Auto": 1,
    "Smart": 3
}
```

**Verify API call:**
```bash
grep "Selecteer.*voor" /config/home-assistant.log | tail -5
```

**Test direct:**
```yaml
service: select.select_option
target:
  entity_id: select.vistapool_filtration_mode
data:
  option: "Auto"
```

**Common issue:** Case sensitive
- Use exact name: "Auto" not "auto"
- Check dropdown options in UI

---

## ⚡ Performance Issues

### Probleem 16: Hoge CPU Usage

**Symptomen:**
- Home Assistant traag
- CPU constant hoog (>50%)
- Vistapool in top processen

**Diagnose:**

```bash
# Check CPU usage
top -p $(pgrep -f "hass") -n 1

# Check wat integratie doet
grep "vistapool" /config/home-assistant.log | tail -50
```

**Mogelijke oorzaken:**

1. **Te frequent updates**
   - Default: 30 sec
   - Met 160 entities × 30 sec = veel updates

2. **Infinite loop in automation**
   - Automation triggert zichzelf
   - Command → state change → trigger → command

3. **Memory leak**
   - Na lang draaien steeds meer geheugen

**Oplossing:**

**1. Verhoog update interval:**
```yaml
# Configuration → Integrations → Vistapool → Configure
Update interval: 60 seconds (ipv 30)
```

**2. Disable unused entities:**
```yaml
# Settings → Entities
# Filter: vistapool
# Disable entities je niet gebruikt
```

**3. Check automations:**
```yaml
# Zoek naar loops:
automation:
  trigger:
    - platform: state
      entity_id: switch.vistapool_zwembadpomp
  action:
    - service: switch.turn_on  # ← Loop!
      target:
        entity_id: switch.vistapool_zwembadpomp
```

Fix: Add condition
```yaml
condition:
  - condition: state
    entity_id: switch.vistapool_zwembadpomp
    state: "off"
```

---

### Probleem 17: Slow Response Times

**Symptomen:**
- Commands duren lang (>5 sec)
- UI hangt bij switch toggle
- Timeout errors

**Diagnose:**

**Measure response time:**
```bash
time curl -X POST https://europe-west1-hayward-europe.cloudfunctions.net/sendCommand
```

Should be < 3 seconds.

**Check logs:**
```bash
grep "succesvol verzonden" /config/home-assistant.log | tail -20
```

Note time between "Set" and "succesvol".

**Oplossing:**

**1. Network latency:**
- Check internet speed
- Ping Google servers: `ping firestore.googleapis.com`
- Traceroute: `traceroute firestore.googleapis.com`

**2. API slow:**
- Vistapool API can be slow (3-5 sec normal)
- Not much you can do
- Wait for response

**3. Async issue:**
All commands are async in code, so shouldn't block UI.

Check code in `coordinator.py`:
```python
await self.hass.async_add_executor_job(
    self.coordinator.api.send_pool_command, "WRP", changes
)
```

---

## 📊 Data Synchronisatie

### Probleem 18: HA vs App Mismatch

**Symptomen:**
- Waarde in HA ≠ waarde in app
- HA toont oud
- App toont actueel

**Oorzaak:**
Cache / sync timing

**Oplossing:**

**1. Force refresh:**
```yaml
# Developer Tools → Services
service: homeassistant.reload_config_entry
data:
  entry_id: "YOUR_ENTRY_ID"
```

Find entry_id:
```bash
cat /config/.storage/core.config_entries | grep vistapool -B 5 | grep entry_id
```

**2. Check update interval:**
- Default: 30 sec
- App might update faster
- Increase refresh rate to 15 sec (not recommended for battery)

**3. Manual sync:**
```yaml
automation:
  - alias: "Force Pool Sync"
    trigger:
      - platform: state
        entity_id: switch.vistapool_zwembadpomp
    action:
      - delay:
          seconds: 5
      - service: homeassistant.update_entity
        target:
          entity_id: sensor.vistapool_filtration_status
```

---

### Probleem 19: Delayed State Updates

**Symptomen:**
- Command sent
- State updates 30-60 sec later

**Dit is NORMAAL:**
- API command: instant
- State refresh: next coordinator update (30 sec default)

**Oplossing (optioneel):**

Add immediate refresh after command:
```python
# switch.py - async_turn_on()
await self.coordinator.async_send_pool_command("WRP", changes)
await self.coordinator.async_request_refresh()  # Already in code!
```

This is already implemented!

If still slow:
- Check network latency
- Coordinator might be rate limited
- Increase priority: Not possible without code change

---

## 🔬 Geavanceerde Debug

### Debug 20: Enable Full Debug Logging

**configuration.yaml:**
```yaml
logger:
  default: warning
  logs:
    custom_components.vistapool: debug
    custom_components.vistapool.api: debug
    custom_components.vistapool.coordinator: debug
    custom_components.vistapool.switch: debug
    custom_components.vistapool.number: debug
    custom_components.vistapool.select: debug
    custom_components.vistapool.sensor: debug
```

Restart HA.

**View logs:**
```bash
tail -f /config/home-assistant.log | grep -i vistapool
```

---

### Debug 21: API Request Tracing

**Test API manually:**

```python
import requests
import json

# 1. Login
login_url = "https://www.googleapis.com/identitytoolkit/v3/relyingparty/verifyPassword?key=YOUR_API_KEY"
login_data = {
    "email": "YOUR_EMAIL",
    "password": "YOUR_PASSWORD",
    "returnSecureToken": True
}
r = requests.post(login_url, json=login_data)
token = r.json()["idToken"]

# 2. Get pool data
pool_url = "https://firestore.googleapis.com/v1/projects/hayward-europe/databases/(default)/documents/pools/YOUR_POOL_ID"
headers = {"Authorization": f"Bearer {token}"}
r = requests.get(pool_url, headers=headers)
print(json.dumps(r.json(), indent=2))

# 3. Send command
cmd_url = "https://europe-west1-hayward-europe.cloudfunctions.net/sendPoolCommand"
cmd_data = {
    "gateway": "YOUR_GATEWAY",
    "poolId": "YOUR_POOL_ID",
    "operation": "WRP",
    "changes": json.dumps({"filtration": {"status": 1}}),
    "source": "test"
}
r = requests.post(cmd_url, json=cmd_data, headers=headers)
print(r.status_code, r.text)
```

---

### Debug 22: Packet Capture

**Advanced users:**

```bash
# Install tcpdump
apk add tcpdump

# Capture HTTPS traffic
tcpdump -i eth0 -w /config/vistapool.pcap host firestore.googleapis.com

# Analyze with Wireshark
```

---

### Debug 23: Check Entity Registry

```bash
cd /config/.storage/

# View all Vistapool entities
cat core.entity_registry | jq '.data.entities[] | select(.platform=="vistapool")'

# Count entities
cat core.entity_registry | jq '[.data.entities[] | select(.platform=="vistapool")] | length'

# Find duplicates
cat core.entity_registry | jq '.data.entities[] | select(.platform=="vistapool") | .unique_id' | sort | uniq -d
```

---

## 🆘 Last Resort Solutions

### Nuclear Option 1: Complete Reset

```bash
# 1. Stop HA
ha core stop

# 2. Backup
cp -r /config/.storage /config/.storage.backup

# 3. Remove Vistapool
rm -rf /config/custom_components/vistapool/
rm /config/.storage/core.config_entries  # ⚠️ Removes ALL integrations!

# 4. Start HA
ha core start

# 5. Re-add integration
```

---

### Nuclear Option 2: Fresh Install

1. Export automations
2. Backup configuration
3. Remove Vistapool completely
4. Restart HA
5. Install from HACS fresh
6. Re-configure
7. Import automations

---

## 📞 Getting Help

### Before Asking for Help

Collect this info:

1. **Version Info:**
```bash
ha core info
ha supervisor info
```

2. **Integration Info:**
```bash
cat /config/custom_components/vistapool/manifest.json
```

3. **Logs:**
```bash
# Last 100 lines with Vistapool
grep -i vistapool /config/home-assistant.log | tail -100 > vistapool_log.txt
```

4. **Config (censored):**
```bash
cat /config/.storage/core.config_entries | grep vistapool -A 30
# Remove sensitive data (passwords, IDs)
```

5. **Screenshots:**
- Settings → Devices & Services → Vistapool
- Developer Tools → States (filter: vistapool)
- Any error messages

### Where to Ask

1. **GitHub Issues:** https://github.com/MatthiasVanDE/Vistapool/issues
2. **Home Assistant Community:** https://community.home-assistant.io
3. **Discord:** Home Assistant Discord → #custom-components

---

## ✅ Preventive Maintenance

### Weekly Checks
- [ ] Check logs for warnings
- [ ] Verify entities updating
- [ ] Test critical automations
- [ ] Backup configuration

### Monthly Checks
- [ ] Update to latest version (if available)
- [ ] Review automation performance
- [ ] Clean up old logs
- [ ] Test API credentials still valid

### Seasonal Checks
- [ ] Adjust filter timing for season
- [ ] Review automation schedules
- [ ] Update temperature thresholds
- [ ] Test winter/summer mode switches

---

**Hopelijk lost dit je problemen op! 🛠️**

Als je problemen blijft houden, maak een GitHub issue aan met bovenstaande info.
