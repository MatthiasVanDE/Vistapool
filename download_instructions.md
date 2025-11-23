# 📥 Vistapool Code Download Guide

Stap-voor-stap instructies om alle code te downloaden en te installeren.

---

## 🎯 Wat Je Nodig Hebt

- [ ] SSH toegang tot Home Assistant
- [ ] Terminal/File Editor add-on (optioneel)
- [ ] 15-20 minuten tijd

---

## 📋 Bestandenlijst

Je moet **13 bestanden** aanmaken in `/config/custom_components/vistapool/`:

### Python Bestanden (10)
1. `__init__.py`
2. `api.py`
3. `coordinator.py`
4. `switch.py`
5. `number.py`
6. `select.py`
7. `sensor.py`
8. `config_flow.py`
9. `const.py`
10. `firestore_parser.py`

### Config Bestanden (3)
11. `manifest.json`
12. `strings.json`
13. `services.yaml`

---

## 🚀 Methode 1: Via SSH (Aanbevolen)

### Stap 1: Maak Directory
```bash
ssh root@homeassistant.local
# Of via Terminal add-on

cd /config
mkdir -p custom_components/vistapool
cd custom_components/vistapool
```

### Stap 2: Maak Elk Bestand

**Voor elk bestand hieronder:**
1. Kopieer de content uit de artifact
2. Maak bestand aan: `nano BESTANDSNAAM`
3. Plak content (Ctrl+Shift+V)
4. Sla op (Ctrl+O, Enter, Ctrl+X)

---

### Bestand 1: `__init__.py`
```bash
nano __init__.py
```
→ Kopieer uit artifact "vistapool_init"

---

### Bestand 2: `api.py`
```bash
nano api.py
```
→ Kopieer uit artifact "vistapool_api"

---

### Bestand 3: `coordinator.py`
```bash
nano coordinator.py
```
→ Kopieer uit artifact "vistapool_coordinator"

---

### Bestand 4: `switch.py`
```bash
nano switch.py
```
→ Kopieer uit artifact "vistapool_switch_complete"

---

### Bestand 5: `number.py`
```bash
nano number.py
```
→ Kopieer uit artifact "vistapool_number_complete"

---

### Bestand 6: `select.py`
```bash
nano select.py
```
→ Kopieer uit artifact "vistapool_select_complete"

---

### Bestand 7: `sensor.py`
```bash
nano sensor.py
```
→ Kopieer uit artifact "vistapool_sensor_refactored"

---

### Bestand 8: `config_flow.py`
```bash
nano config_flow.py
```
→ Kopieer uit artifact "vistapool_config_flow"

---

### Bestand 9: `const.py`
```bash
nano const.py
```
→ Kopieer uit artifact "vistapool_const"

---

### Bestand 10: `firestore_parser.py`
```bash
nano firestore_parser.py
```
→ Dit is je ORIGINELE bestand (document #8 uit je upload)

---

### Bestand 11: `manifest.json`
```bash
nano manifest.json
```
→ Kopieer uit artifact "vistapool_manifest"

---

### Bestand 12: `strings.json`
```bash
nano strings.json
```
→ Kopieer uit artifact "vistapool_strings"

---

### Bestand 13: `services.yaml`
```bash
nano services.yaml
```
→ Dit is je ORIGINELE bestand (document #2 uit je upload)

---

### Stap 3: Verificatie
```bash
cd /config/custom_components/vistapool
ls -la
```

**Moet tonen:**
```
total XX
-rw-r--r-- 1 root root  XXXX __init__.py
-rw-r--r-- 1 root root  XXXX api.py
-rw-r--r-- 1 root root  XXXX config_flow.py
-rw-r--r-- 1 root root  XXXX const.py
-rw-r--r-- 1 root root  XXXX coordinator.py
-rw-r--r-- 1 root root  XXXX firestore_parser.py
-rw-r--r-- 1 root root  XXXX manifest.json
-rw-r--r-- 1 root root  XXXX number.py
-rw-r--r-- 1 root root  XXXX select.py
-rw-r--r-- 1 root root  XXXX sensor.py
-rw-r--r-- 1 root root  XXXX services.yaml
-rw-r--r-- 1 root root  XXXX strings.json
-rw-r--r-- 1 root root  XXXX switch.py
```

**Check aantal:** `ls -1 | wc -l` moet **13** zijn

---

## 🖥️ Methode 2: Via File Editor Add-on

### Stap 1: Installeer File Editor
```
Settings → Add-ons → Add-on Store
Zoek: "File editor"
Installeer → Start
```

### Stap 2: Open File Editor
```
Settings → Add-ons → File Editor → OPEN WEB UI
```

### Stap 3: Maak Directory
Klik op folder icoon → Nieuw → Folder:
```
config/custom_components/vistapool
```

### Stap 4: Maak Bestanden
Voor elk bestand:
1. Klik op 📄 nieuw bestand icoon
2. Naam: `__init__.py` (etc.)
3. Kopieer content uit artifact
4. Plak in editor
5. Sla op (💾 icoon)

Herhaal voor alle 13 bestanden.

---

## 💾 Methode 3: Via Samba Share

### Stap 1: Activeer Samba
```
Settings → Add-ons → Samba share
Start → Open Web UI
```

### Stap 2: Verbind vanaf Computer
**Windows:**
```
\\HOMEASSISTANT\config\custom_components\
```

**Mac:**
```
smb://homeassistant.local/config/custom_components/
```

### Stap 3: Maak Folder
```
Maak folder: vistapool
```

### Stap 4: Kopieer Bestanden
Maak elk bestand op je computer en kopieer naar de folder.

---

## 📦 Methode 4: Via ZIP Upload (Makkelijkst!)

Als je alle bestanden in 1 ZIP wilt:

### Stap 1: Download ZIP Maken
Op je computer:
1. Maak folder `vistapool`
2. Kopieer alle 13 bestanden erin
3. ZIP de folder

### Stap 2: Upload naar HA
Via File Editor of Samba:
1. Upload `vistapool.zip`
2. Unzip in `/config/custom_components/`

**Of via SSH:**
```bash
cd /config/custom_components/
unzip vistapool.zip
```

---

## ✅ Verificatie Checklist

Na installatie, check:

```bash
cd /config/custom_components/vistapool

# Check aantal bestanden
ls -1 | wc -l
# Moet 13 zijn

# Check Python syntax
python3 -m py_compile *.py
# Geen errors

# Check manifest
cat manifest.json | python3 -m json.tool
# Moet valide JSON zijn

# Check bestandsrechten
chmod 644 *.py *.json *.yaml
```

---

## 🔄 Na Installatie

### Stap 1: Herstart Home Assistant
```
Settings → System → Restart
```

### Stap 2: Check Logs
```bash
tail -f /config/home-assistant.log | grep vistapool
```

Of via UI:
```
Settings → System → Logs
Filter: "vistapool"
```

### Stap 3: Voeg Integratie Toe
```
Settings → Devices & Services → + ADD INTEGRATION
Zoek: "Vistapool"
```

---

## 🐛 Troubleshooting Download

### Probleem: Permission Denied
```bash
chmod -R 755 /config/custom_components/vistapool/
chown -R root:root /config/custom_components/vistapool/
```

### Probleem: Bestand Corrupt
- Re-download artifact
- Check copy-paste (hele content?)
- Vergelijk bestandsgrootte

### Probleem: Niet Alle Bestanden
```bash
# Lijst verwachte bestanden
cat > /tmp/expected_files.txt << 'EOF'
__init__.py
api.py
config_flow.py
const.py
coordinator.py
firestore_parser.py
manifest.json
number.py
select.py
sensor.py
services.yaml
strings.json
switch.py
EOF

# Check welke ontbreken
cd /config/custom_components/vistapool
diff <(ls -1 | sort) <(sort /tmp/expected_files.txt)
```

---

## 📋 Quick Checklist

Vink af terwijl je bezig bent:

- [ ] Directory gemaakt: `/config/custom_components/vistapool/`
- [ ] `__init__.py` (150 regels)
- [ ] `api.py` (250 regels)
- [ ] `coordinator.py` (100 regels)
- [ ] `switch.py` (200 regels)
- [ ] `number.py` (450 regels)
- [ ] `select.py` (180 regels)
- [ ] `sensor.py` (450 regels)
- [ ] `config_flow.py` (120 regels)
- [ ] `const.py` (100 regels)
- [ ] `firestore_parser.py` (40 regels)
- [ ] `manifest.json` (15 regels)
- [ ] `strings.json` (60 regels)
- [ ] `services.yaml` (10 regels)
- [ ] Bestandsrechten gezet (755)
- [ ] Python syntax check OK
- [ ] Home Assistant herstart
- [ ] Integratie verschijnt in lijst

---

## 🎯 Alternatief: Ik Kan ZIP Maken

Als je wilt kan ik ook:
1. Een compleet install script maken
2. GitHub repository setup helpen
3. HACS manifest voorbereiden

Zeg maar wat je het makkelijkst vindt! 😊

---

**Succes met downloaden!** 📥✨
