#!/bin/bash
# =============================================================================
# Faded Dream Dotfiles - Install Script
# =============================================================================

set -euo pipefail

# --- Colors & Helpers --------------------------------------------------------
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
CYAN='\033[0;36m'
BOLD='\033[1m'
RESET='\033[0m'

info()    { echo -e "${CYAN}${BOLD}[INFO]${RESET}  $*"; }
success() { echo -e "${GREEN}${BOLD}[ OK ]${RESET}  $*"; }
warn()    { echo -e "${YELLOW}${BOLD}[WARN]${RESET}  $*"; }
die()     { echo -e "${RED}${BOLD}[FAIL]${RESET}  $*" >&2; exit 1; }

step() {
  echo ""
  echo -e "${BOLD}${CYAN}══════════════════════════════════════════${RESET}"
  echo -e "${BOLD}  $1${RESET}"
  echo -e "${BOLD}${CYAN}══════════════════════════════════════════${RESET}"
}

export -f info success warn die step
export RED GREEN YELLOW CYAN BOLD RESET

DOTFILES_DIR="${HOME}/Faded-Dream-dotfiles"
export DOTFILES_DIR

SCRIPTS_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/scripts" && pwd)"
TOTAL_STEPS=13

# --- Preflight Checks --------------------------------------------------------
[[ "$(id -u)" -eq 0 ]] && die "Do not run this script as root."
[[ ! -d "$DOTFILES_DIR" ]] && die "Dotfiles directory not found: $DOTFILES_DIR"
command -v pacman &>/dev/null || die "pacman not found. Is this Artix/Arch Linux?"

echo ""
echo -e "${BOLD}${CYAN}"
echo "  ╔══════════════════════════════════════╗"
echo "  ║   Faded Dream Dotfiles  -  Installer  ║"
echo "  ╚══════════════════════════════════════╝"
echo -e "${RESET}"

# --- Run each step -----------------------------------------------------------
steps=(
  "01-repos.sh"
  "02-dirs.sh"
  "03-packages.sh"
  "04-device.sh"
  "05-permissions.sh"
  "06-shell.sh"
  "07-aur.sh"
  "08-gpu.sh"
  "09-aur-packages.sh"
  "10-rofi-power-menu.sh"
  "11-lazyvim.sh"
  "12-waybar.sh"
  "13-dotfiles.sh"
)

for i in "${!steps[@]}"; do
  step "[$(( i + 1 ))/${TOTAL_STEPS}] Running ${steps[$i]%.sh}"
  bash "$SCRIPTS_DIR/${steps[$i]}" || die "Step ${steps[$i]} failed."
done

# --- Done --------------------------------------------------------------------
echo ""
echo -e "${GREEN}${BOLD}"
echo "  ╔══════════════════════════════════════╗"
echo "  ║      Installation complete!           ║"
echo "  ╚══════════════════════════════════════╝"
echo -e "${RESET}"
echo -e "  Rebooting in ${BOLD}10 seconds${RESET}. Press ${BOLD}Ctrl+C${RESET} to cancel."
echo ""

sleep 10
sudo reboot
