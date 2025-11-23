# 🧪 Vistapool Test Scenarios

Complete test guide om de integratie te valideren.

## 📋 Pre-Test Checklist

- [ ] Backup van je Home Assistant configuratie gemaakt
- [ ] Alle bestanden gekopieerd naar `custom_components/vistapool/`
- [ ] Home Assistant herstart
- [ ] Logs zichtbaar gemaakt (Settings → System → Logs)
- [ ] Integratie toegevoegd via UI

---

## 1️⃣ Basis Installatie Tests

### Test 1.1: Configuratie Setup
**Doel:** Valideer dat de integratie correct configureert

**Stappen:**
1. Ga naar Settings → Devices & Services
2. Klik op "Add Integration"
3. Zoek "Vistapool"
4. Vul je credentials in
5. Klik Submit

**Verwacht resultaat:**
- ✅ Geen errors in logs
- ✅ Integratie verschijnt in lijst
- ✅ Status is "Loaded"

**Troubleshooting:**
```bash
# Check logs voor errors
grep -i "vistapool" /config/home-assistant.log
grep -i "error" /config/home-assistant.log | grep vistapool
```

---

### Test 1.2: Entity Discovery
**Doel:** Controleer of alle entities zijn aangemaakt

**Stappen:**
1. Ga naar Developer Tools → States
2. Filter op "vistapool"
3. Tel aantal entities

**Verwacht resultaat:**
- ✅ ~160 entities gevonden
- ✅ Geen entities met status "unavailable" (tenzij verwacht)
- ✅ Entities verdeeld over 8 apparaten

**Apparaten checklist:**
- [ ] Filtratie (groen indien pomp actief)
- [ ] Hydrolyse (groen indien actief)
- [ ] Set points
- [ ] Relays
- [ ] Algemeen (Global)
- [ ] Algemeen (Main)
- [ ] Modules
- [ ] Form

---

### Test 1.3: Data Refresh
**Doel:** Valideer dat data wordt bijgewerkt

**Stappen:**
1. Noteer een sensor waarde (bijv. temperatuur)
2. Wacht 30 seconden (default interval)
3. Refresh de pagina
4. Check of waarde is bijgewerkt

**Verwacht resultaat:**
- ✅ "Updated At" sensor toont recente tijd
- ✅ Alle sensor waarden zijn actueel
- ✅ Geen "unknown" waarden (tenzij verwacht)

---

## 2️⃣ Switch Tests

### Test 2.1: Pomp Aan/Uit
**Doel:** Test basis pomp besturing

**Pre-conditie:**
- Filtratie mode = Manual (0)

**Stappen:**
1. Zet `switch.vistapool_zwembadpomp` AAN
2. Wacht 5 seconden
3. Check status in Vistapool app
4. Zet switch UIT
5. Check status opnieuw

**Verwacht resultaat:**
- ✅ Switch state verandert direct
- ✅ `sensor.vistapool_filtration_status` toont "On"
- ✅ Status in app komt overeen
- ✅ Geen errors in logs

**Logs checken:**
```
DEBUG Zet Zwembadpomp aan met changes: {'filtration': {'status': 1}}
INFO Pool commando WRP succesvol verzonden
```

---

### Test 2.2: Licht Besturing
**Doel:** Test licht aan/uit

**Stappen:**
1. Zet `switch.vistapool_zwembadlicht` AAN
2. Wacht 5 seconden
3. Check `sensor.vistapool_light_status`
4. Zet switch UIT

**Verwacht resultaat:**
- ✅ Licht gaat aan
- ✅ Sensor update naar "On"
- ✅ Switch blijft synchroniseren met status

---

### Test 2.3: Chloorshock
**Doel:** Test hydrolyse chloorshock

**Pre-conditie:**
- Hydrolyse moet enabled zijn (disable=0)

**Stappen:**
1. Check `switch.vistapool_hydrolyse_ingeschakeld` is AAN
2. Zet `switch.vistapool_chloorshock` AAN
3. Wacht 10 seconden
4. Check `sensor.vistapool_hidro_cloration` = 1

**Verwacht resultaat:**
- ✅ Chloorshock activeert
- ✅ Hydrolyse level blijft actief
- ✅ Sensor toont "On"

**Waarschuwing:**
Als hydrolyse disabled is, moet switch unavailable zijn (grijs).

---

### Test 2.4: Relay Besturing
**Doel:** Test configureerbare relays

**Stappen:**
1. Zet `switch.vistapool_relay_1` AAN
2. Check `sensor.vistapool_relay1_status`
3. Zet UIT

**Verwacht resultaat:**
- ✅ Relay schakelt
- ✅ Status sensor update
- ✅ `sensor.vistapool_relay1_onoff` = 1/0

---

## 3️⃣ Number Tests

### Test 3.1: pH Setpoint Aanpassen
**Doel:** Test setpoint wijziging

**Stappen:**
1. Noteer huidige `number.vistapool_ph_setpoint_high`
2. Wijzig naar 7.20
3. Wacht 10 seconden
4. Check `sensor.vistapool_modules_ph_high`

**Verwacht resultaat:**
- ✅ Waarde verandert naar 7.20
- ✅ Sensor toont 720 (internal format)
- ✅ Vistapool app toont 7.20

**Logs:**
```
DEBUG Set pH Setpoint Hoog naar 7.2 (API: 720)
INFO Pool commando WRP succesvol verzonden
```

---

### Test 3.2: Hydrolyse Level
**Doel:** Test hydrolyse vermogen aanpassing

**Pre-conditie:**
- Hydrolyse enabled

**Stappen:**
1. Zet `number.vistapool_hydrolyse_level` naar 50
2. Wacht 10 seconden
3. Check `sensor.vistapool_hidro_level`

**Verwacht resultaat:**
- ✅ Waarde = 500 (50 * 10)
- ✅ Hydrolyse past vermogen aan
- ✅ Geen overload errors

---

### Test 3.3: Timer Interval Instellen
**Doel:** Test filtratie timer

**Pre-conditie:**
- Filtratie mode = Auto (1) of Smart (3)

**Stappen:**
1. Zet `number.vistapool_interval1_from` naar 28800 (08:00)
2. Zet `number.vistapool_interval1_to` naar 61200 (17:00)
3. Check sensors

**Verwacht resultaat:**
- ✅ `sensor.vistapool_filtration_int1_from` = "08:00:00"
- ✅ `sensor.vistapool_filtration_int1_to` = "17:00:00"
- ✅ Pomp start om 08:00

**Tijd Conversie Test:**
```python
# 08:00 = 8 * 3600 = 28800 seconden
# 17:00 = 17 * 3600 = 61200 seconden
```

---

### Test 3.4: Backwash Timing
**Doel:** Test backwash configuratie

**Stappen:**
1. Zet `number.vistapool_backwash_interval` naar 180 (3 min)
2. Zet `number.vistapool_backwash_frequency` naar 10080 (1 week)
3. Check sensors

**Verwacht resultaat:**
- ✅ Interval = 180 min
- ✅ Frequency = 10080 min (7 dagen)
- ✅ Backwash scheduled correct

---

### Test 3.5: Licht Timing
**Doel:** Test licht timer

**Stappen:**
1. Zet `number.vistapool_light_from` naar 72000 (20:00)
2. Zet `number.vistapool_light_to` naar 79200 (22:00)
3. Check `sensor.vistapool_light_from/to`

**Verwacht resultaat:**
- ✅ From = "20:00:00"
- ✅ To = "22:00:00"
- ✅ Licht gaat automatisch aan/uit

---

### Test 3.6: Relay Timing
**Doel:** Test relay timer configuratie

**Stappen:**
1. Zet `number.vistapool_relay1_from` naar 32400 (09:00)
2. Zet `number.vistapool_relay1_to` naar 64800 (18:00)
3. Zet `number.vistapool_relay1_delay` naar 60 (1 min vertraging)

**Verwacht resultaat:**
- ✅ Relay 1 start om 09:01 (delay)
- ✅ Relay 1 stopt om 18:00
- ✅ Sensors tonen correcte waarden

---

## 4️⃣ Select Tests

### Test 4.1: Filtratie Modus Wisselen
**Doel:** Test mode switching

**Stappen:**
1. Zet `select.vistapool_filtration_mode` naar "Manual"
2. Wacht 5 sec, check `sensor.vistapool_filtration_mode`
3. Zet naar "Auto"
4. Wacht 5 sec, check sensor
5. Zet naar "Smart"

**Verwacht resultaat:**
- ✅ Mode = 0, 1, 3 in sensor
- ✅ Numbers voor intervals verschijnen/verdwijnen
- ✅ Pomp gedrag past aan per mode

**Manual Mode:**
- Pomp blijft aan/uit zoals ingesteld
- Timer intervals unavailable

**Auto Mode:**
- Pomp volgt interval timers
- Timer intervals beschikbaar

**Smart Mode:**
- Pomp volgt temperatuur
- Smart temp numbers beschikbaar

---

### Test 4.2: Pomp Snelheid
**Doel:** Test pomp snelheid aanpassingen

**Stappen:**
1. Zet mode naar "Manual"
2. Zet `select.vistapool_pump_speed_manual` naar "Slow"
3. Check `sensor.vistapool_filtration_manvel` = 0
4. Zet naar "High"
5. Check sensor = 2

**Verwacht resultaat:**
- ✅ Snelheid verandert
- ✅ Pomp past RPM aan
- ✅ Energieverbruik wijzigt

---

### Test 4.3: Backwash Mode
**Doel:** Test backwash automatisering

**Stappen:**
1. Zet `select.vistapool_backwash_mode` naar "Automatic"
2. Check `number.vistapool_backwash_frequency` beschikbaar
3. Zet mode naar "Manual"
4. Check number unavailable

**Verwacht resultaat:**
- ✅ Automatic: frequency number zichtbaar
- ✅ Manual: frequency hidden
- ✅ Sensor toont correcte mode

---

### Test 4.4: Backwash Frequentie Select
**Doel:** Test preset frequenties

**Pre-conditie:**
- Backwash mode = Automatic

**Stappen:**
1. Zet `select.vistapool_backwash_frequency_select` naar "Elke week"
2. Check `sensor.vistapool_backwash_frequency` = 10080

**Mapping tabel:**
- Elke dag = 1440 min
- Elke twee dagen = 2880 min
- Elke week = 10080 min
- Elke vier weken = 40320 min

---

## 5️⃣ Service Tests

### Test 5.1: Set Timer Intervals Service
**Doel:** Test bulk interval setting

**Stappen:**
1. Ga naar Developer Tools → Services
2. Selecteer `vistapool.set_timer_intervals`
3. Vul in:
```yaml
service: vistapool.set_timer_intervals
data:
  interval1_from: 28800  # 08:00
  interval1_to: 61200    # 17:00
  interval2_from: 0
  interval2_to: 0
  interval3_from: 0
  interval3_to: 0
```
4. Run service
5. Check sensors

**Verwacht resultaat:**
- ✅ Alle intervals ingesteld
- ✅ Sensors tonen nieuwe waarden
- ✅ Service completes zonder errors

---

## 6️⃣ Availability Tests

### Test 6.1: Smart Mode Features
**Doel:** Valideer availability logic

**Stappen:**
1. Zet filtratie mode naar "Manual"
2. Check `number.vistapool_smart_temp_min` - moet unavailable zijn
3. Zet mode naar "Smart"
4. Check number - moet beschikbaar zijn

**Verwacht resultaat:**
- ✅ Smart features alleen in Smart mode
- ✅ Entities grijs wanneer unavailable
- ✅ Geen errors bij unavailable entities

---

### Test 6.2: Hydrolyse Disable
**Doel:** Test hydrolyse enable/disable

**Stappen:**
1. Zet `switch.vistapool_hydrolyse_ingeschakeld` UIT
2. Check `number.vistapool_hydrolyse_level` unavailable
3. Check `switch.vistapool_chloorshock` unavailable
4. Zet switch weer AAN
5. Check entities beschikbaar

---

### Test 6.3: Backwash Auto Features
**Doel:** Test backwash availability

**Stappen:**
1. Zet backwash mode naar "Manual"
2. Check frequency number/select unavailable
3. Zet naar "Automatic"
4. Check beschikbaar

---

## 7️⃣ Integration Tests

### Test 7.1: Complete Scenario - Dagelijkse Routine
**Scenario:** Pomp loopt 8:00-17:00, licht 20:00-22:00, backwash elke week

**Setup:**
```yaml
# Filtratie
select.vistapool_filtration_mode: "Auto"
number.vistapool_interval1_from: 28800  # 08:00
number.vistapool_interval1_to: 61200   # 17:00
select.vistapool_pump_speed_timer1: "High"

# Licht
switch.vistapool_licht_automatische_modus: on
number.vistapool_light_from: 72000  # 20:00
number.vistapool_light_to: 79200    # 22:00

# Backwash
select.vistapool_backwash_mode: "Automatic"
select.vistapool_backwash_frequency_select: "Elke week"
number.vistapool_backwash_interval: 180  # 3 min
```

**Test over 24 uur:**
- ✅ 08:00: Pomp start
- ✅ 17:00: Pomp stopt
- ✅ 20:00: Licht aan
- ✅ 22:00: Licht uit
- ✅ Elke week: Backwash 3 min

---

### Test 7.2: Smart Mode Scenario
**Scenario:** Smart filtratie op basis van temperatuur

**Setup:**
```yaml
select.vistapool_filtration_mode: "Smart"
number.vistapool_smart_temp_min: 10  # Onder 10°C: minimale filtering
number.vistapool_smart_temp_high: 28  # Boven 28°C: maximale filtering
switch.vistapool_smart_mode_vorstbeveiliging: on
```

**Test:**
- ✅ Temperatuur < 10°C: Pomp op laag
- ✅ Temperatuur 10-28°C: Normale filtratie
- ✅ Temperatuur > 28°C: Pomp op hoog
- ✅ Temperatuur < 2°C: Freeze protection actief

---

## 8️⃣ Error Handling Tests

### Test 8.1: Invalid Credentials
**Doel:** Test error handling bij foute login

**Stappen:**
1. Verwijder integratie
2. Voeg toe met fout wachtwoord
3. Check error message

**Verwacht resultaat:**
- ✅ Error: "Ongeldige inloggegevens"
- ✅ Geen crash
- ✅ Retry mogelijk

---

### Test 8.2: Network Timeout
**Doel:** Test timeout handling

**Simulatie:**
1. Blokkeer internet tijdelijk (firewall regel)
2. Wacht op update interval
3. Check logs

**Verwacht resultaat:**
- ✅ Warning log: "Verbindingsfout met Vistapool API"
- ✅ Entities blijven available (laatste waarden)
- ✅ Auto-recovery bij herstel

---

### Test 8.3: Invalid Commands
**Doel:** Test command validation

**Stappen:**
1. Probeer hydrolyse level te zetten terwijl disabled
2. Check log voor warning

**Verwacht resultaat:**
- ✅ Warning: "Hydrolyse is disabled; ignoring level change"
- ✅ Geen crash
- ✅ Entity state onveranderd

---

## 9️⃣ Performance Tests

### Test 9.1: Update Interval Performance
**Doel:** Test verschillende update intervals

**Stappen:**
1. Configureer interval op 10 sec
2. Monitor CPU/Memory voor 5 min
3. Verhoog naar 60 sec
4. Monitor opnieuw

**Verwacht resultaat:**
- ✅ 10 sec: ~6 updates/min, acceptabel CPU gebruik
- ✅ 60 sec: 1 update/min, minimaal gebruik
- ✅ Geen memory leaks

**Monitor commando:**
```bash
top -p $(pgrep -f "hass")
```

---

### Test 9.2: Multiple Command Burst
**Doel:** Test rapid command sending

**Stappen:**
1. Stuur 5 commands snel achter elkaar:
   - Pomp aan
   - Licht aan
   - pH setpoint wijzigen
   - Hydrolyse level wijzigen
   - Mode wijzigen
2. Check alle commands succesvol

**Verwacht resultaat:**
- ✅ Alle commands verwerkt
- ✅ Geen rate limit errors
- ✅ States correct bijgewerkt

---

## 🔟 Long-term Stability Tests

### Test 10.1: 24-Hour Uptime
**Doel:** Test stabiliteit over 24 uur

**Monitoring:**
- Check om de 4 uur:
  - [ ] Entities still available
  - [ ] No errors in logs
  - [ ] Memory usage stable
  - [ ] API token refreshed correctly

**Success criteria:**
- ✅ 0 crashes
- ✅ <5 minor warnings
- ✅ All automations triggered correctly

---

### Test 10.2: Token Refresh
**Doel:** Test automatische token vernieuwing

**Stappen:**
1. Start integratie
2. Wacht 60 minuten (token expires na 1 uur)
3. Check logs voor refresh
4. Verify entities blijven werken

**Expected log:**
```
DEBUG Vernieuw Vistapool token
DEBUG Token succesvol vernieuwd
```

---

## ✅ Test Checklist Summary

### Must Pass (Critical)
- [ ] 1.1 Configuratie Setup
- [ ] 1.2 Entity Discovery
- [ ] 2.1 Pomp Aan/Uit
- [ ] 3.1 pH Setpoint
- [ ] 4.1 Filtratie Modus
- [ ] 8.1 Invalid Credentials
- [ ] 10.2 Token Refresh

### Should Pass (Important)
- [ ] Alle switch tests
- [ ] Alle number tests
- [ ] Alle select tests
- [ ] Service tests
- [ ] Availability tests

### Nice to Have (Optional)
- [ ] Performance tests
- [ ] Long-term stability
- [ ] Integration scenarios

---

## 📊 Test Report Template

```markdown
# Vistapool Test Report

**Date:** YYYY-MM-DD
**Version:** 2.0.0
**Tester:** [Name]

## Environment
- Home Assistant Version: 
- Python Version:
- Installation Method: HACS / Manual

## Test Results

### Critical Tests: X/7 Passed
- [ ] Configuration Setup
- [ ] Entity Discovery
- [ ] Pomp Control
- [ ] pH Setpoint
- [ ] Mode Switching
- [ ] Error Handling
- [ ] Token Refresh

### All Tests: X/50 Passed

## Issues Found
1. [Issue description]
2. [Issue description]

## Performance Notes
- Average CPU: X%
- Memory usage: X MB
- Update latency: X sec

## Conclusion
[ ] Ready for production
[ ] Needs fixes
[ ] Requires further testing
```

---

## 🆘 Troubleshooting Commands

```bash
# Volledige log voor Vistapool
grep -i "vistapool" /config/home-assistant.log

# Alleen errors
grep -i "error" /config/home-assistant.log | grep -i "vistapool"

# API calls
grep "Pool commando" /config/home-assistant.log

# Token management
grep "token" /config/home-assistant.log | grep -i "vistapool"

# Laatste 50 regels live
tail -f /config/home-assistant.log | grep -i "vistapool"
```

---

**Succes met testen! 🎯**
