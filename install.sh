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

info() { echo -e "${CYAN}${BOLD}[INFO]${RESET}  $*"; }
success() { echo -e "${GREEN}${BOLD}[ OK ]${RESET}  $*"; }
warn() { echo -e "${YELLOW}${BOLD}[WARN]${RESET}  $*"; }
die() {
  echo -e "${RED}${BOLD}[FAIL]${RESET}  $*" >&2
  exit 1
}

step() {
  echo ""
  echo -e "${BOLD}${CYAN}══════════════════════════════════════════${RESET}"
  echo -e "${BOLD}  $1${RESET}"
  echo -e "${BOLD}${CYAN}══════════════════════════════════════════${RESET}"
}

DOTFILES_DIR="${HOME}/Faded-Dream-dotfiles"
TOTAL_STEPS=9

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

# --- [1/9] Arch Repositories -------------------------------------------------
step "[1/${TOTAL_STEPS}] Setting up Arch Linux repositories"

sudo pacman -S --noconfirm --needed archlinux-keyring archlinux-mirrorlist artix-archlinux-support ||
  die "Failed to install repository packages."

[[ -f "$DOTFILES_DIR/pacman.conf" ]] || die "pacman.conf not found in dotfiles."
sudo cp /etc/pacman.conf /etc/pacman.conf.bak && info "Backed up existing pacman.conf"
sudo cp "$DOTFILES_DIR/pacman.conf" /etc/pacman.conf

sudo pacman-key --populate archlinux
sudo pacman -Sy --noconfirm

success "Arch repositories configured."

# --- [2/9] Directory Structure -----------------------------------------------
step "[2/${TOTAL_STEPS}] Creating directory structure"

mkdir -p \
  "${HOME}/.config" \
  "${HOME}/.local/share" \
  "${HOME}/.config/autostart" \
  "${HOME}/.icons/default"

success "Directories ready."

# --- [3/9] Core Packages -----------------------------------------------------
step "[3/${TOTAL_STEPS}] Installing core packages"

PACKAGES=(
  # Desktop / WM
  hyprland
  xorg-server
  xorg-xwayland
  waybar
  swaync
  rofi
  nwg-look
  # Browser
  librewolf
  # Audio
  pipewire
  pipewire-pulse
  pipewire-alsa
  pipewire-jack
  pavucontrol
  # File manager / Polkit
  nemo
  polkit-gnome
  # Fonts
  noto-fonts
  noto-fonts-cjk
  noto-fonts-emoji
  ttf-firacode-nerd
  # Terminal / Shell / Utilities
  kitty
  zsh
  bat
  fastfetch
  btop
  calcurse
  hyprshot
  neovim
  wget
  git
  # Media
  mpv
  imagemagick
  # Languages & runtimes
  rust
  go
  python-pip
  jdk-openjdk
  julia
  php
  npm
  luarocks
  tectonic
)

sudo pacman -S --noconfirm --needed "${PACKAGES[@]}" ||
  die "Package installation failed."

success "Core packages installed."

# --- [4/9] Set zsh as default shell ------------------------------------------
step "[4/${TOTAL_STEPS}] Setting zsh as default shell"

ZSH_PATH="$(command -v zsh)"
[[ -z "$ZSH_PATH" ]] && die "zsh not found after installation, something went wrong."

if [[ "$(getent passwd "$USER" | cut -d: -f7)" == "$ZSH_PATH" ]]; then
  warn "zsh is already the default shell for $USER, skipping."
else
  sudo chsh -s "$ZSH_PATH" "$USER" ||
    die "Failed to change default shell to zsh."
  success "Default shell changed to zsh for $USER."
fi

# --- [5/9] AUR Helper (paru) -------------------------------------------------
step "[5/${TOTAL_STEPS}] Installing paru and AUR packages"

if command -v paru &>/dev/null; then
  warn "paru already installed, skipping build."
else
  PARU_TMP=$(mktemp -d)
  git clone https://aur.archlinux.org/paru.git "$PARU_TMP/paru" ||
    die "Failed to clone paru."
  (cd "$PARU_TMP/paru" && makepkg -si --noconfirm) ||
    die "Failed to build paru."
  rm -rf "$PARU_TMP"
fi

paru -S --noconfirm --needed waypaper mpvpaper clipse-wayland-bin ||
  die "Failed to install AUR packages."

success "paru and AUR packages installed."

# --- [6/9] Rofi Power Menu ---------------------------------------------------
step "[6/${TOTAL_STEPS}] Installing rofi-power-menu (non-systemd)"

POWER_MENU_TMP=$(mktemp -d)

git clone --branch master \
  https://github.com/FemBoyGamerTechGuy/rofi-power-menu-for-non-systemd-users.git \
  "$POWER_MENU_TMP/rofi-power-menu" ||
  die "Failed to clone rofi-power-menu."

PKGBUILD_DIR="$POWER_MENU_TMP/rofi-power-menu/rofi-power-menu-PKG"

[[ -d "$PKGBUILD_DIR" ]] || die "rofi-power-menu-PKG folder not found in repo."
[[ -f "$PKGBUILD_DIR/PKGBUILD" ]] || die "PKGBUILD not found in rofi-power-menu-PKG."

(cd "$PKGBUILD_DIR" && makepkg -si --noconfirm) ||
  die "Failed to build rofi-power-menu."

rm -rf "$POWER_MENU_TMP"
success "rofi-power-menu installed."

# --- [7/9] LazyVim -----------------------------------------------------------
step "[7/${TOTAL_STEPS}] Installing LazyVim starter config"

if [[ -d "${HOME}/.config/nvim" ]]; then
  warn "~/.config/nvim already exists, skipping LazyVim clone."
else
  git clone https://github.com/LazyVim/starter "${HOME}/.config/nvim" ||
    die "Failed to clone LazyVim starter."
  success "LazyVim starter cloned to ~/.config/nvim."
fi

# --- [8/9] Dotfile Deployment ------------------------------------------------
step "[8/${TOTAL_STEPS}] Deploying dotfiles"

deploy() {
  local src="$1" dst="$2"
  if [[ ! -e "$src" ]]; then
    warn "Source not found, skipping: $src"
    return
  fi
  mkdir -p "$(dirname "$dst")"
  cp -r "$src" "$dst" && info "Deployed: $(basename "$src") → $dst"
}

# Config folder deployments
deploy "$DOTFILES_DIR/hypr" "${HOME}/.config/hypr"
deploy "$DOTFILES_DIR/waybar" "${HOME}/.config/waybar"
deploy "$DOTFILES_DIR/kitty" "${HOME}/.config/kitty"
deploy "$DOTFILES_DIR/rofi for .config" "${HOME}/.config/rofi"
deploy "$DOTFILES_DIR/rofi for local then share" "${HOME}/.local/share/rofi"
deploy "$DOTFILES_DIR/fastfetch" "${HOME}/.config/fastfetch"
deploy "$DOTFILES_DIR/gtk configs/gtk-3.0" "${HOME}/.config/gtk-3.0"
deploy "$DOTFILES_DIR/gtk configs/gtk-4.0" "${HOME}/.config/gtk-4.0"
deploy "$DOTFILES_DIR/gtk configs/xsettingsd" "${HOME}/.config/xsettingsd"

# Home directory deployments
deploy "$DOTFILES_DIR/.zshrc" "${HOME}/.zshrc"
deploy "$DOTFILES_DIR/.zsh" "${HOME}/.zsh"
deploy "$DOTFILES_DIR/gtk configs/.gtkrc-2.0" "${HOME}/.gtkrc-2.0"
deploy "$DOTFILES_DIR/.themes" "${HOME}/.themes"
deploy "$DOTFILES_DIR/.icons" "${HOME}/.icons"

success "Dotfiles deployed."

# --- [9/9] Autostart Scripts -------------------------------------------------
step "[9/${TOTAL_STEPS}] Setting up autostart scripts"

# PipeWire autostart
PIPEWIRE_SCRIPT="${HOME}/.config/autostart/pipewire.sh"

cat >"$PIPEWIRE_SCRIPT" <<'EOF'
#!/bin/bash
# Wait for XDG_RUNTIME_DIR before starting audio services.
until [[ -d "/run/user/$(id -u)" ]]; do
    sleep 0.5
done
sleep 1
/usr/bin/pipewire &
/usr/bin/pipewire-pulse &
/usr/bin/wireplumber &
# Wait for pipewire to be ready then restart waybar to pick up audio
sleep 2
pkill waybar || true
waybar &
EOF

chmod +x "$PIPEWIRE_SCRIPT"
success "PipeWire autostart configured."

# Nemo terminal autostart (runs once on first login then deletes itself)
NEMO_TERMINAL_SCRIPT="${HOME}/.config/autostart/set-nemo-terminal.sh"

cat >"$NEMO_TERMINAL_SCRIPT" <<'EOF'
#!/bin/bash
sleep 10
gsettings set org.cinnamon.desktop.default-applications.terminal exec kitty
gsettings set org.gnome.desktop.default-applications.terminal exec kitty
rm -- "$0"
EOF

chmod +x "$NEMO_TERMINAL_SCRIPT"
success "Nemo terminal autostart configured."

# GTK theme autostart (runs once on first login then kills itself)
GTK_THEME_SCRIPT="${HOME}/.config/autostart/set-gtk-theme.sh"

cat >"$GTK_THEME_SCRIPT" <<'EOF'
#!/bin/bash
sleep 10
gsettings set org.gnome.desktop.interface gtk-theme "Nordic-bluish-accent-v40"
gsettings set org.gnome.desktop.interface icon-theme "Papirus"
gsettings set org.gnome.desktop.interface cursor-theme "ArcDusk-cursors"
gsettings set org.gnome.desktop.interface cursor-size 24
# Fix cursor theme for all environments including XWayland
echo '[Icon Theme]' > ~/.icons/default/index.theme
echo 'Name=ArcDusk-cursors' >> ~/.icons/default/index.theme
echo 'Inherits=ArcDusk-cursors' >> ~/.icons/default/index.theme
rm -- "$0"
EOF

chmod +x "$GTK_THEME_SCRIPT"
success "GTK theme autostart configured."

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
