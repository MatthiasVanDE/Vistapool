#!/bin/bash
#
# Vistapool Automatic Installation Script
# Versie: 2.0.0
#
# Gebruik: bash install.sh
#

set -e  # Stop bij errors

echo "=================================================="
echo "  Vistapool Home Assistant Integratie Installer"
echo "  Versie 2.0.0"
echo "=================================================="
echo ""

# Kleuren voor output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Functies
print_success() {
    echo -e "${GREEN}✓${NC} $1"
}

print_error() {
    echo -e "${RED}✗${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}⚠${NC} $1"
}

print_info() {
    echo -e "ℹ $1"
}

# Check of we in Home Assistant draaien
if [ ! -d "/config" ]; then
    print_error "Geen /config directory gevonden!"
    print_info "Dit script moet draaien op Home Assistant"
    exit 1
fi

print_success "Home Assistant detectie OK"

# Maak directory
TARGET_DIR="/config/custom_components/vistapool"

if [ -d "$TARGET_DIR" ]; then
    print_warning "Directory $TARGET_DIR bestaat al"
    read -p "Wil je de bestaande installatie overschrijven? (y/n): " -n 1 -r
    echo
    if [[ ! $REPLY =~ ^[Yy]$ ]]; then
        print_info "Installatie geannuleerd"
        exit 0
    fi
    print_info "Backup maken van bestaande installatie..."
    mv "$TARGET_DIR" "${TARGET_DIR}.backup.$(date +%s)"
    print_success "Backup gemaakt"
fi

print_info "Aanmaken directory $TARGET_DIR..."
mkdir -p "$TARGET_DIR"
print_success "Directory aangemaakt"

cd "$TARGET_DIR"

# Download bestanden
print_info "Bestanden downloaden..."

# Je moet de bestanden handmatig kopiëren uit de artifacts
# Dit script maakt de structuur aan

cat > __init__.py << 'HEREDOC_INIT'
# KOPIEER HIER DE CONTENT VAN ARTIFACT: vistapool_init
# Of download via de artifact download knop
HEREDOC_INIT

cat > api.py << 'HEREDOC_API'
# KOPIEER HIER DE CONTENT VAN ARTIFACT: vistapool_api
HEREDOC_API

cat > coordinator.py << 'HEREDOC_COORD'
# KOPIEER HIER DE CONTENT VAN ARTIFACT: vistapool_coordinator
HEREDOC_COORD

cat > switch.py << 'HEREDOC_SWITCH'
# KOPIEER HIER DE CONTENT VAN ARTIFACT: vistapool_switch_complete
HEREDOC_SWITCH

cat > number.py << 'HEREDOC_NUMBER'
# KOPIEER HIER DE CONTENT VAN ARTIFACT: vistapool_number_complete
HEREDOC_NUMBER

cat > select.py << 'HEREDOC_SELECT'
# KOPIEER HIER DE CONTENT VAN ARTIFACT: vistapool_select_complete
HEREDOC_SELECT

cat > sensor.py << 'HEREDOC_SENSOR'
# KOPIEER HIER DE CONTENT VAN ARTIFACT: vistapool_sensor_refactored
HEREDOC_SENSOR

cat > config_flow.py << 'HEREDOC_CONFIG'
# KOPIEER HIER DE CONTENT VAN ARTIFACT: vistapool_config_flow
HEREDOC_CONFIG

cat > const.py << 'HEREDOC_CONST'
# KOPIEER HIER DE CONTENT VAN ARTIFACT: vistapool_const
HEREDOC_CONST

cat > firestore_parser.py << 'HEREDOC_PARSER'
# KOPIEER HIER DE CONTENT VAN JE ORIGINELE firestore_parser.py
HEREDOC_PARSER

cat > manifest.json << 'HEREDOC_MANIFEST'
# KOPIEER HIER DE CONTENT VAN ARTIFACT: vistapool_manifest
HEREDOC_MANIFEST

cat > strings.json << 'HEREDOC_STRINGS'
# KOPIEER HIER DE CONTENT VAN ARTIFACT: vistapool_strings
HEREDOC_STRINGS

cat > services.yaml << 'HEREDOC_SERVICES'
# KOPIEER HIER DE CONTENT VAN JE ORIGINELE services.yaml
HEREDOC_SERVICES

print_info "Placeholder bestanden aangemaakt"
print_warning "Je moet nu de artifact content handmatig kopiëren!"

# Set permissions
print_info "Bestandsrechten instellen..."
chmod 644 *.py *.json *.yaml
print_success "Permissions gezet"

# Verificatie
print_info "Verificatie..."
FILE_COUNT=$(ls -1 | wc -l)

if [ "$FILE_COUNT" -eq 13 ]; then
    print_success "Alle 13 bestanden aanwezig"
else
    print_error "Verwacht 13 bestanden, gevonden $FILE_COUNT"
fi

# Python syntax check (optioneel)
if command -v python3 &> /dev/null; then
    print_info "Python syntax check..."
    for file in *.py; do
        if python3 -m py_compile "$file" 2>/dev/null; then
            print_success "$file syntax OK"
        else
            print_error "$file heeft syntax errors!"
        fi
    done
fi

# Samenvatting
echo ""
echo "=================================================="
echo "  Installatie Voltooid!"
echo "=================================================="
echo ""
print_info "Volgende stappen:"
echo "  1. Kopieer de artifact content in elk bestand"
echo "  2. Herstart Home Assistant"
echo "  3. Ga naar Settings → Devices & Services"
echo "  4. Klik + ADD INTEGRATION"
echo "  5. Zoek 'Vistapool'"
echo ""
print_warning "Vergeet niet om de placeholder content te vervangen!"
echo ""
