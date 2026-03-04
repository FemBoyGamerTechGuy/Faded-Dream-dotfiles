#!/bin/bash
# =============================================================================
# Faded Dream — rEFInd Theme Installer
# =============================================================================

ESP="/efi/EFI/refind"
THEME_DIR="$ESP/themes/faded-dream"
SCRIPT_DIR="$(cd "$(dirname "$(realpath "$0")")" && pwd)"

echo ""
echo "  ╔══════════════════════════════════════╗"
echo "  ║   Faded Dream — rEFInd Theme Install  ║"
echo "  ╚══════════════════════════════════════╝"
echo ""
echo "  Source: $SCRIPT_DIR"
echo ""

# Check ESP is accessible
[[ ! -d "$ESP" ]] && echo "[FAIL] $ESP not found. Is /dev/sdd1 mounted at /efi?" && exit 1

# Create theme directories
sudo mkdir -p "$THEME_DIR/icons"

# Copy theme assets
sudo cp "$SCRIPT_DIR/theme.conf"          "$THEME_DIR/" && echo "[ OK ]  theme.conf"
sudo cp "$SCRIPT_DIR/background.png"      "$THEME_DIR/" && echo "[ OK ]  background.png"
sudo cp "$SCRIPT_DIR/selection_big.png"   "$THEME_DIR/" && echo "[ OK ]  selection_big.png"
sudo cp "$SCRIPT_DIR/selection_small.png" "$THEME_DIR/" && echo "[ OK ]  selection_small.png"
sudo cp "$SCRIPT_DIR/icons/"*.png         "$THEME_DIR/icons/" && echo "[ OK ]  icons/"

# Copy refind.conf
sudo cp "$SCRIPT_DIR/refind.conf" "$ESP/refind.conf" && echo "[ OK ]  refind.conf"

echo ""
echo "  Done! Reboot to see the theme."
echo "  Don't forget to update PARTUUID in $ESP/refind.conf"
echo ""
