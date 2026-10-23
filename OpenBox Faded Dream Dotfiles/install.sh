#!/bin/bash
# =============================================================================
# Faded Dream Dotfiles - Install Script - OpenBox (X11) variant
#
# Ports FemBoyGamerTechGuy/Faded-Dream-dotfiles (Hyprland) to OpenBox.
# Self-contained like the per-distro installers: everything needed for a
# full Faded Dream OpenBox session lives in this folder.
#
# Layout of what gets deployed:
#   openbox/            → ~/.config/openbox/          (WM: rc/menu/env/autostart)
#   themes/             → ~/.themes/Faded-Dream/      (gradient OB3 theme)
#   picom/              → ~/.config/picom/            (blur/rounding/animation)
#   dunst/              → ~/.config/dunst/             (rofi-styled notifications)
#   waybar pc|laptop/   → ~/.config/waybar/            (X11 port, your choice)
#   kitty/              → ~/.config/kitty/             (verbatim from upstream)
#   rofi for .config/   → ~/.config/rofi/              (verbatim from upstream)
#   rofi for local then share/ → ~/.local/share/rofi/  (verbatim from upstream)
#   fastfetch/          → ~/.config/fastfetch/        (verbatim from upstream)
#   config.ini for waypaper → ~/.config/waypaper/      (backend=feh for X11)
#   .zshrc / .zsh/      → $HOME/                       (verbatim from upstream)
#   helpers/            → ~/.local/bin/                (scratchpad, pager, bell…)
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

DOTFILES_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

deploy() {
  # Idempotent deploy: re-running never nests folders (unlike a bare `cp -r
  # src dst`, which puts src INSIDE dst when dst already exists).
  local src="$1" dst="$2"
  [[ ! -e "$src" ]] && { warn "Source not found, skipping: $src"; return; }
  mkdir -p "$(dirname "$dst")"
  if [[ -d "$src" ]]; then
    mkdir -p "$dst"
    cp -r "$src"/. "$dst"/
  else
    cp -r "$src" "$dst"
  fi
  success "Deployed: $(basename "$src") → $dst"
}

# --- Preflight Checks --------------------------------------------------------
[[ "$(id -u)" -eq 0 ]] && die "Do not run this script as root."
[[ ! -d "$DOTFILES_DIR/openbox" ]] && die "OpenBox variant files not found in: $DOTFILES_DIR"

echo ""
echo -e "${BOLD}${CYAN}"
echo "  ╔══════════════════════════════════════╗"
echo "  ║  Faded Dream  -  OpenBox  Installer  ║"
echo "  ╚══════════════════════════════════════╝"
echo -e "${RESET}"

# --- [1/5] Directory structure (mirrors upstream 02-dirs.sh) -----------------
step "[1/5] Directory structure"
mkdir -p \
  "${HOME}/.config" \
  "${HOME}/.local/share" \
  "${HOME}/.local/bin" \
  "${HOME}/.config/autostart" \
  "${HOME}/.config/waypaper" \
  "${HOME}/.icons/default" \
  "${HOME}/.themes" \
  "${HOME}/Live&NON Live Wallpapers"
success "Directories ready."

# --- [2/5] Packages (optional) ------------------------------------------------
step "[2/5] Packages"

# Official Arch repos — the Hyprland list translated to X11.
#   hyprland      → openbox + picom
#   swaync        → dunst (+ libnotify for notify-send)
#   hyprshot      → flameshot
#   mpvpaper      → feh            (waypaper X11 backend)
#   (new)         → xdotool wmctrl (scratchpad/pager helpers)
#   (new)         → xclip          (clipse clipboard on X11)
#   (new)         → ttf-jetbrains-mono-nerd (waybar/dunst font — upstream gap)
#   (new)         → brightnessctl playerctl  (media/laptop keybinds)
#   (new)         → obconf nwg-look (GUI theme / GTK+cursor pickers)
CORE_PKGS=(
  openbox picom obconf nwg-look
  xorg-server xorg-xrandr
  waybar dunst libnotify
  xdg-desktop-portal-gtk
  kitty zsh bat fastfetch btop calcurse neovim wget git
  rofi flameshot xdotool wmctrl xclip feh
  brightnessctl playerctl
  noto-fonts noto-fonts-cjk noto-fonts-emoji ttf-firacode-nerd ttf-jetbrains-mono-nerd
  polkit polkit-gnome
  pipewire pipewire-pulse pipewire-alsa wireplumber pavucontrol
  mpv yt-dlp imagemagick ffmpeg
  gtk4 libadwaita python-gobject python-cairo
  chafa unrar unzip p7zip zstd
)

# AUR — upstream AUR list translated to X11:
#   clipse-wayland-bin → clipse-bin   (X11 build uses xclip, not wl-clipboard)
#   waypaper, rofimoji-git, rofi-power-menu unchanged
AUR_PKGS=(
  waypaper
  clipse-bin
  rofimoji-git
  rofi-power-menu
  librewolf-bin
)

if command -v pacman &>/dev/null; then
  echo ""
  echo -e "  ${BOLD}Install core packages from the official repos now?${RESET}"
  echo -e "  (${#CORE_PKGS[@]} packages — openbox, picom, waybar, dunst, kitty, rofi, …)"
  read -rp  "  Install now? [y/N]: " PKG_CHOICE
  if [[ "${PKG_CHOICE,,}" == "y" ]]; then
    sudo pacman -S --noconfirm --needed "${CORE_PKGS[@]}" ||
      warn "Some core packages failed — fix manually, then re-run."
    success "Core packages installed."
  else
    info "Skipping core packages (get them from README.md if needed)."
  fi

  echo ""
  echo -e "  ${BOLD}Install AUR packages?${RESET}"
  echo -e "  (${#AUR_PKGS[@]} packages via paru — waypaper, clipse-bin, rofimoji,"
  echo -e "   rofi-power-menu, librewolf-bin)"
  read -rp  "  Install now? [y/N]: " AUR_CHOICE
  if [[ "${AUR_CHOICE,,}" == "y" ]]; then
    if command -v paru &>/dev/null; then
      paru -S --noconfirm --needed "${AUR_PKGS[@]}" ||
        warn "Some AUR packages failed — fix manually, then re-run."
      success "AUR packages installed."
    else
      warn "paru not found — install an AUR helper first, then run:"
      warn "  paru -S --needed ${AUR_PKGS[*]}"
    fi
  else
    info "Skipping AUR packages."
  fi
else
  warn "pacman not found — assuming a non-Arch system."
  warn "Install the equivalents listed in README.md yourself, then continue."
  read -rp "  Continue with config deployment anyway? [y/N]: " CONT
  [[ "${CONT,,}" == "y" ]] || die "Aborted — install packages first (see README.md)."
fi

# --- [3/5] Waybar layout choice (mirrors upstream 12-waybar.sh) --------------
step "[3/5] Waybar layout"
echo ""
echo -e "  ${BOLD}${CYAN}Which Waybar layout would you like to use for your device?${RESET}"
echo -e "  1) Laptop  — includes battery and backlight modules"
echo -e "  2) PC      — standard layout"
echo ""
read -rp "  Enter choice [1/2]: " WAYBAR_CHOICE

case "$WAYBAR_CHOICE" in
  1) info "Laptop Waybar selected." ;;
  *) info "PC Waybar selected (default)." ;;
esac

# --- [4/5] Deploy configs ------------------------------------------------------
step "[4/5] Deploying configs"

mkdir -p "${HOME}/.config/openbox"
cp "$DOTFILES_DIR/openbox/rc.xml"        "${HOME}/.config/openbox/"
cp "$DOTFILES_DIR/openbox/menu.xml"      "${HOME}/.config/openbox/"
cp "$DOTFILES_DIR/openbox/environment"   "${HOME}/.config/openbox/"
cp "$DOTFILES_DIR/openbox/autostart"     "${HOME}/.config/openbox/"
chmod +x "${HOME}/.config/openbox/autostart"
success "OpenBox config deployed (rc.xml, menu.xml, environment, autostart)."

deploy "$DOTFILES_DIR/themes/Faded-Dream"                       "${HOME}/.themes/Faded-Dream"
deploy "$DOTFILES_DIR/picom/picom.conf"                         "${HOME}/.config/picom/picom.conf"
deploy "$DOTFILES_DIR/dunst/dunstrc"                            "${HOME}/.config/dunst/dunstrc"

mkdir -p "${HOME}/.config/waybar"
if [[ "$WAYBAR_CHOICE" == "1" ]]; then
  cp "$DOTFILES_DIR/waybar laptop/config-laptop.jsonc" "${HOME}/.config/waybar/config.jsonc"
  cp "$DOTFILES_DIR/waybar laptop/style-laptop.css"     "${HOME}/.config/waybar/style.css"
else
  cp "$DOTFILES_DIR/waybar pc/config-pc.jsonc"          "${HOME}/.config/waybar/config.jsonc"
  cp "$DOTFILES_DIR/waybar pc/style-pc.css"              "${HOME}/.config/waybar/style.css"
fi
success "Waybar (X11 port, $([[ "$WAYBAR_CHOICE" == "1" ]] && echo laptop || echo PC)) deployed."

deploy "$DOTFILES_DIR/kitty"                                    "${HOME}/.config/kitty"
deploy "$DOTFILES_DIR/rofi for .config/config.rasi"             "${HOME}/.config/rofi/config.rasi"
deploy "$DOTFILES_DIR/rofi for local then share"               "${HOME}/.local/share/rofi"
deploy "$DOTFILES_DIR/fastfetch"                                "${HOME}/.config/fastfetch"
deploy "$DOTFILES_DIR/config.ini for waypaper"                  "${HOME}/.config/waypaper/config.ini"

# Home-directory deployments (shell config — verbatim from upstream)
deploy "$DOTFILES_DIR/.zshrc"                                   "${HOME}/.zshrc"
deploy "$DOTFILES_DIR/.zsh"                                     "${HOME}/.zsh"

# Helper scripts → ~/.local/bin (scratchpad, workspace pager, window title, bell)
for s in faded-scratchpad faded-workspaces faded-window-title faded-notifications; do
  cp "$DOTFILES_DIR/helpers/$s" "${HOME}/.local/bin/$s"
  chmod +x "${HOME}/.local/bin/$s"
done
success "Helper scripts deployed → ~/.local/bin (faded-*)."

# --- [5/5] Default shell -------------------------------------------------------
step "[5/5] Default shell"
ZSH_PATH="$(command -v zsh || true)"
if [[ -n "$ZSH_PATH" ]]; then
  if [[ "$(getent passwd "$USER" | cut -d: -f7)" == "$ZSH_PATH" ]]; then
    warn "zsh is already the default shell for $USER, skipping."
  else
    read -rp "  Make zsh your default shell? [Y/n]: " ZSH_CHOICE
    if [[ ! "${ZSH_CHOICE,,}" == "n" ]]; then
      sudo chsh -s "$ZSH_PATH" "$USER" && success "Default shell changed to zsh." ||
        warn "Could not change shell — run 'chsh -s $(which zsh)' manually."
    else
      info "Keeping current shell."
    fi
  fi
else
  warn "zsh not installed — skipping shell change."
fi

# --- Done -----------------------------------------------------------------------
echo ""
echo -e "${GREEN}${BOLD}"
echo "  ╔══════════════════════════════════════╗"
echo "  ║      Installation complete!           ║"
echo "  ╚══════════════════════════════════════╝"
echo -e "${RESET}"
echo -e "  Next steps:"
echo -e "   1. Log out, pick the ${BOLD}Openbox${RESET} session on your display manager"
echo -e "      (or add 'exec openbox-session' to ~/.xinitrc / startx)."
echo -e "   2. Win+Enter opens kitty; Win+Space... use Alt+Space for rofi."
echo -e "   3. Set your wallpaper: run ${BOLD}waypaper${RESET} once (feh backend, static only)."
echo -e "   4. VoidDream (file manager, Win+E) installs from its own repo:"
echo -e "      https://github.com/FemBoyGamerTechGuy/VoidDream"
echo -e "   5. GTK theme / cursors: nwg-look → Nordic + ArcDusk (see README.md)."
echo ""
