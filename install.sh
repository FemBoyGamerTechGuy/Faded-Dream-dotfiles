#!/bin/bash
# =============================================================================
# Faded Dream Dotfiles - Universal Installer (entry point)
# Prompts for the distro, then delegates to that distro's own self-contained
# install.sh (which may further prompt for the init system).
# =============================================================================
set -euo pipefail

# Locate this script's directory (repo root) without depending on $PWD.
DOTFILES_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

# Resolve the distro folders by glob so their exact (long) names are always
# correct even if the folders are ever renamed/edited.
arch_dir="$(find "$DOTFILES_DIR" -maxdepth 1 -mindepth 1 -type d -name 'Arch*' -print -quit)"
artix_dir="$(find "$DOTFILES_DIR" -maxdepth 1 -mindepth 1 -type d -name 'Art*' -print -quit)"
fedora_dir="$(find "$DOTFILES_DIR" -maxdepth 1 -mindepth 1 -type d -name 'Fedora*' -print -quit)"

if [[ -z "${arch_dir:-}" || -z "${artix_dir:-}" || -z "${fedora_dir:-}" ]]; then
  echo "ERROR: distro folders ('Arch*' / 'Art*' / 'Fedora*') not found in: $DOTFILES_DIR" >&2
  echo "       Run this script from the repo root." >&2
  exit 1
fi

RED='\033[0;31m';  GREEN='\033[0;32m'; YELLOW='\033[1;33m'
CYAN='\033[0;36m'; BOLD='\033[1m';    RESET='\033[0m'

# --- Banner (matches the look of the per-distro install.sh banners) ---
echo ""
echo -e "${BOLD}${CYAN}══════════════════════════════════════════${RESET}"
echo -e "${BOLD}  Faded Dream Dotfiles  -  Installer${RESET}"
echo -e "${BOLD}${CYAN}══════════════════════════════════════════${RESET}"
echo ""

# --- Distro prompt (plain names only; init selection happens in each installer) ---
echo "  Which distro are you installing on?"
echo ""
echo -e "  ${BOLD}1${RESET})  Arch Linux"
echo -e "  ${BOLD}2${RESET})  Artix Linux"
echo -e "  ${BOLD}3${RESET})  Fedora Linux"
echo -e "  ${BOLD}q${RESET})  quit"
printf "\n  Choice [1]: "
read -r choice || { echo; echo -e "  ${BOLD}Aborted.${RESET}"; exit 0; }

case "$choice" in
  1|'')    target="$arch_dir"   ;;
  2)      target="$artix_dir"  ;;
  3)      target="$fedora_dir" ;;
  q|Q)    echo ""; echo -e "  ${BOLD}Aborted.${RESET}"; exit 0 ;;
  *)      echo -e "\n${RED}Invalid choice: $choice${RESET}" >&2; exit 1 ;;
esac

echo -e "\n  ${BOLD}Launching ${YELLOW}$(basename "$target")${RESET}${BOLD} installer...${RESET}\n"
cd "$target"
exec ./install.sh "$@"
