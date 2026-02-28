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
TOTAL_STEPS=11

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

# --- [1/11] Arch Repositories ------------------------------------------------
step "[1/${TOTAL_STEPS}] Setting up Arch Linux repositories"

sudo pacman -S --noconfirm --needed archlinux-keyring archlinux-mirrorlist artix-archlinux-support ||
  die "Failed to install repository packages."

[[ -f "$DOTFILES_DIR/pacman.conf" ]] || die "pacman.conf not found in dotfiles."
sudo cp /etc/pacman.conf /etc/pacman.conf.bak && info "Backed up existing pacman.conf"
sudo cp "$DOTFILES_DIR/pacman.conf" /etc/pacman.conf

sudo pacman-key --populate archlinux
sudo pacman -Sy --noconfirm

success "Arch repositories configured."

# --- [2/11] Directory Structure ----------------------------------------------
step "[2/${TOTAL_STEPS}] Creating directory structure"

mkdir -p \
  "${HOME}/.config" \
  "${HOME}/.local/share" \
  "${HOME}/.config/autostart" \
  "${HOME}/.config/waypaper" \
  "${HOME}/.icons/default" \
  "${HOME}/Live&NON Live Wallpapers"

success "Directories ready."

# --- [3/11] Core Packages ----------------------------------------------------
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

# --- [4/11] Device Type ------------------------------------------------------
step "[4/${TOTAL_STEPS}] Device type selection"

echo ""
echo -e "${BOLD}${CYAN}  What type of device are you installing on?${RESET}"
echo -e "  1) Laptop"
echo -e "  2) PC"
echo ""
read -rp "  Enter choice [1/2]: " DEVICE_CHOICE

if [[ "$DEVICE_CHOICE" == "1" ]]; then
  info "Laptop selected — installing laptop specific packages."
  sudo pacman -S --noconfirm --needed \
    tlp-runit brightnessctl acpi acpid \
    bluez bluez-utils cpupower powertop ||
    die "Failed to install laptop packages."
  sudo ln -s /etc/runit/sv/tlp /run/runit/service 2>/dev/null || warn "tlp service link already exists."
  sv up tlp || warn "Could not start tlp — it will start on next boot."
  success "Laptop packages installed."
else
  info "PC selected — skipping laptop specific packages."
fi

# --- [5/11] Set zsh as default shell -----------------------------------------
step "[5/${TOTAL_STEPS}] Setting zsh as default shell"

ZSH_PATH="$(command -v zsh)"
[[ -z "$ZSH_PATH" ]] && die "zsh not found after installation, something went wrong."

if [[ "$(getent passwd "$USER" | cut -d: -f7)" == "$ZSH_PATH" ]]; then
  warn "zsh is already the default shell for $USER, skipping."
else
  sudo chsh -s "$ZSH_PATH" "$USER" ||
    die "Failed to change default shell to zsh."
  success "Default shell changed to zsh for $USER."
fi

# --- [6/11] AUR Helper (paru) ------------------------------------------------
step "[6/${TOTAL_STEPS}] Installing paru"

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

success "paru installed."

# --- [7/11] GPU Drivers ------------------------------------------------------
step "[7/${TOTAL_STEPS}] Installing GPU drivers"

KERNEL=$(uname -r)
case "$KERNEL" in
*zen*) HEADERS="linux-zen-headers" ;;
*lts*) HEADERS="linux-lts-headers" ;;
*hardened*) HEADERS="linux-hardened-headers" ;;
*) HEADERS="linux-headers" ;;
esac
info "Detected kernel: $KERNEL — will install $HEADERS"

echo ""
echo -e "${BOLD}${CYAN}  Which GPU do you have?${RESET}"
echo -e "  1) AMD (discrete + iGPU / Ryzen APU)"
echo -e "  2) Nvidia RTX 50 series - GTX 16 series"
echo -e "  3) Nvidia GTX 1080 Ti - GTX 1010"
echo -e "  4) Nvidia GTX 700 - GTX 600 series"
echo -e "  5) Nvidia GTX 500 - GTX 400 series"
echo -e "  6) Nvidia GeForce 8/9/100/200/300 series"
echo -e "  7) Intel (discrete + iGPU)"
echo -e "  8) Skip (no drivers needed)"
echo ""
read -rp "  Enter choice [1-8]: " GPU_CHOICE

case "$GPU_CHOICE" in
1)
  info "AMD selected — installing AMD drivers."
  sudo pacman -S --noconfirm --needed \
    mesa vulkan-radeon xf86-video-amdgpu dkms "$HEADERS" ||
    die "Failed to install AMD drivers."
  success "AMD drivers installed."
  ;;
2)
  info "Nvidia RTX 50 - GTX 16 series selected — installing drivers."
  sudo pacman -S --noconfirm --needed dkms "$HEADERS" ||
    die "Failed to install dkms and headers."
  sudo pacman -S --noconfirm --needed \
    nvidia-open-dkms nvidia-utils lib32-nvidia-utils \
    lib32-opencl-nvidia opencl-nvidia nvidia-settings ||
    die "Failed to install Nvidia drivers."
  success "Nvidia drivers installed."
  ;;
3)
  info "Nvidia GTX 1080 Ti - GTX 1010 selected — installing drivers."
  sudo pacman -S --noconfirm --needed dkms "$HEADERS" ||
    die "Failed to install dkms and headers."
  sudo pacman -S --noconfirm --needed \
    nvidia-580xx-dkms nvidia-580xx-utils lib32-nvidia-580xx-utils \
    opencl-nvidia-580xx lib32-opencl-nvidia-580xx nvidia-580xx-settings ||
    die "Failed to install Nvidia 580xx drivers."
  success "Nvidia 580xx drivers installed."
  ;;
4)
  info "Nvidia GTX 700 - GTX 600 series selected — installing drivers."
  sudo pacman -S --noconfirm --needed dkms "$HEADERS" ||
    die "Failed to install dkms and headers."
  paru -S --noconfirm --needed \
    nvidia-470xx-dkms nvidia-470xx-utils nvidia-470xx-settings \
    opencl-nvidia-470xx lib32-nvidia-470xx-utils lib32-opencl-nvidia-470xx ||
    die "Failed to install Nvidia 470xx drivers."
  success "Nvidia 470xx drivers installed."
  ;;
5)
  info "Nvidia GTX 500 - GTX 400 series selected — installing drivers."
  sudo pacman -S --noconfirm --needed dkms "$HEADERS" ||
    die "Failed to install dkms and headers."
  paru -S --noconfirm --needed \
    nvidia-390xx-dkms nvidia-390xx-utils nvidia-390xx-settings \
    opencl-nvidia-390xx lib32-nvidia-390xx-utils lib32-opencl-nvidia-390xx ||
    die "Failed to install Nvidia 390xx drivers."
  success "Nvidia 390xx drivers installed."
  ;;
6)
  info "Nvidia GeForce 8/9/100/200/300 series selected — installing drivers."
  sudo pacman -S --noconfirm --needed dkms "$HEADERS" ||
    die "Failed to install dkms and headers."
  paru -S --noconfirm --needed \
    nvidia-340xx-dkms nvidia-340xx-utils nvidia-340xx-settings \
    opencl-nvidia-340xx lib32-nvidia-340xx-utils lib32-opencl-nvidia-340xx ||
    die "Failed to install Nvidia 340xx drivers."
  success "Nvidia 340xx drivers installed."
  ;;
7)
  info "Intel selected — installing Intel drivers."
  sudo pacman -S --noconfirm --needed \
    mesa vulkan-intel libva-intel-driver xf86-video-intel \
    dkms "$HEADERS" ||
    die "Failed to install Intel drivers."
  success "Intel drivers installed."
  ;;
8)
  warn "Skipping GPU driver installation."
  ;;
*)
  warn "Invalid choice, skipping GPU driver installation."
  ;;
esac

# --- [8/11] AUR Packages -----------------------------------------------------
step "[8/${TOTAL_STEPS}] Installing AUR packages"

paru -S --noconfirm --needed waypaper mpvpaper clipse-wayland-bin ||
  die "Failed to install AUR packages."

success "AUR packages installed."

# --- [9/11] Rofi Power Menu --------------------------------------------------
step "[9/${TOTAL_STEPS}] Installing rofi-power-menu (non-systemd)"

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

# --- [10/11] LazyVim ---------------------------------------------------------
step "[10/${TOTAL_STEPS}] Installing LazyVim starter config"

if [[ -d "${HOME}/.config/nvim" ]]; then
  warn "~/.config/nvim already exists, skipping LazyVim clone."
else
  git clone https://github.com/LazyVim/starter "${HOME}/.config/nvim" ||
    die "Failed to clone LazyVim starter."
  success "LazyVim starter cloned to ~/.config/nvim."
fi

# --- [11/11] Dotfile Deployment + Autostart ----------------------------------
step "[11/${TOTAL_STEPS}] Deploying dotfiles and autostart scripts"

deploy() {
  local src="$1" dst="$2"
  if [[ ! -e "$src" ]]; then
    warn "Source not found, skipping: $src"
    return
  fi
  mkdir -p "$(dirname "$dst")"
  cp -r "$src" "$dst" && info "Deployed: $(basename "$src") → $dst"
}

# Waybar config selection
echo ""
echo -e "${BOLD}${CYAN}  Which Waybar layout would you like to use for your device?${RESET}"
echo -e "  1) Laptop  — includes battery and backlight modules"
echo -e "  2) PC      — standard layout"
echo ""
read -rp "  Enter choice [1/2]: " WAYBAR_CHOICE

case "$WAYBAR_CHOICE" in
1)
  info "Laptop Waybar selected — deploying laptop waybar config."
  mkdir -p "${HOME}/.config/waybar"
  cp "$DOTFILES_DIR/waybar laptop/config-laptop.jsonc" "${HOME}/.config/waybar/config.jsonc"
  cp "$DOTFILES_DIR/waybar laptop/style-laptop.css" "${HOME}/.config/waybar/style.css"
  success "Laptop Waybar config deployed."
  ;;
2)
  info "PC Waybar selected — deploying desktop waybar config."
  mkdir -p "${HOME}/.config/waybar"
  cp "$DOTFILES_DIR/waybar pc/config-pc.jsonc" "${HOME}/.config/waybar/config.jsonc"
  cp "$DOTFILES_DIR/waybar pc/style-pc.css" "${HOME}/.config/waybar/style.css"
  success "PC Waybar config deployed."
  ;;
*)
  warn "Invalid choice, defaulting to PC Waybar config."
  mkdir -p "${HOME}/.config/waybar"
  cp "$DOTFILES_DIR/waybar pc/config-pc.jsonc" "${HOME}/.config/waybar/config.jsonc"
  cp "$DOTFILES_DIR/waybar pc/style-pc.css" "${HOME}/.config/waybar/style.css"
  ;;
esac

# Config folder deployments
deploy "$DOTFILES_DIR/hypr" "${HOME}/.config/hypr"
deploy "$DOTFILES_DIR/kitty" "${HOME}/.config/kitty"
deploy "$DOTFILES_DIR/rofi for .config" "${HOME}/.config/rofi"
deploy "$DOTFILES_DIR/rofi for local then share" "${HOME}/.local/share/rofi"
deploy "$DOTFILES_DIR/fastfetch" "${HOME}/.config/fastfetch"
deploy "$DOTFILES_DIR/gtk configs/gtk-3.0" "${HOME}/.config/gtk-3.0"
deploy "$DOTFILES_DIR/gtk configs/gtk-4.0" "${HOME}/.config/gtk-4.0"
deploy "$DOTFILES_DIR/gtk configs/xsettingsd" "${HOME}/.config/xsettingsd"
deploy "$DOTFILES_DIR/config.ini for waypaper" "${HOME}/.config/waypaper/config.ini"

# Home directory deployments
deploy "$DOTFILES_DIR/.zshrc" "${HOME}/.zshrc"
deploy "$DOTFILES_DIR/.zsh" "${HOME}/.zsh"
deploy "$DOTFILES_DIR/gtk configs/.gtkrc-2.0" "${HOME}/.gtkrc-2.0"
deploy "$DOTFILES_DIR/.themes" "${HOME}/.themes"
cp -r "$DOTFILES_DIR/.icons/." "${HOME}/.icons/" && info "Deployed: .icons → ${HOME}/.icons"

success "Dotfiles deployed."

# PipeWire autostart
PIPEWIRE_SCRIPT="${HOME}/.config/autostart/pipewire.sh"

cat >"$PIPEWIRE_SCRIPT" <<'EOF'
#!/bin/bash
/usr/bin/pipewire &
/usr/bin/pipewire-pulse &
/usr/bin/wireplumber &
EOF

chmod +x "$PIPEWIRE_SCRIPT"
success "PipeWire autostart configured."

# Nemo terminal autostart (runs once on first login then deletes itself)
NEMO_TERMINAL_SCRIPT="${HOME}/.config/autostart/set-nemo-terminal.sh"

cat >"$NEMO_TERMINAL_SCRIPT" <<'EOF'
#!/bin/bash
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
gsettings set org.gnome.desktop.interface gtk-theme "Nordic-bluish-accent-v40"
gsettings set org.gnome.desktop.interface icon-theme "Papirus"
gsettings set org.gnome.desktop.interface cursor-theme "ArcDusk-cursors"
gsettings set org.gnome.desktop.interface cursor-size 24
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
