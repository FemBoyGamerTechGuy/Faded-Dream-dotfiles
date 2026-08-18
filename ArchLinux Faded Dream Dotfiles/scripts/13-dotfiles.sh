#!/bin/bash
# [13/13] Dotfile Deployment + Autostart (Arch Linux)
# PipeWire is normally started by systemd user units on Arch, so this autostart
# script is made idempotent: it only launches PipeWire when it isn't already
# running, then starts waybar. Keeps compatibility with non-systemd setups too.

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
deploy "$DOTFILES_DIR/hypr"                        "${HOME}/.config/hypr"
deploy "$DOTFILES_DIR/kitty"                       "${HOME}/.config/kitty"
deploy "$DOTFILES_DIR/rofi for .config"            "${HOME}/.config/rofi"
deploy "$DOTFILES_DIR/rofi for local then share"   "${HOME}/.local/share/rofi"
deploy "$DOTFILES_DIR/fastfetch"                   "${HOME}/.config/fastfetch"
deploy "$DOTFILES_DIR/config.ini for waypaper"     "${HOME}/.config/waypaper/config.ini"

# Home directory deployments
deploy "$DOTFILES_DIR/.zshrc"                      "${HOME}/.zshrc"
deploy "$DOTFILES_DIR/.zsh"                        "${HOME}/.zsh"

success "Dotfiles deployed."

# Create sentinel so the welcome app runs on first login
touch "${HOME}/.config/faded-dream-autostart"
success "Autostart sentinel created."

# PipeWire autostart (systemd-aware / idempotent)
cat >"${HOME}/.config/autostart/pipewire.sh" <<'AUTOEOF'
#!/bin/bash
# Launch PipeWire + Waybar on login.
# Under systemd, PipeWire user units usually start automatically; we still make
# sure the services are up so audio and the bar are ready under any init.

# Only start the daemons if they are not already running.
if ! pgrep -x pipewire >/dev/null 2>&1; then
  /usr/bin/pipewire &
  /usr/bin/pipewire-pulse &
  if command -v wireplumber >/dev/null 2>&1; then
    /usr/bin/wireplumber &
  elif command -v pipewire-media-session >/dev/null 2>&1; then
    /usr/bin/pipewire-media-session &
  fi
  # Give the daemons a moment to come up.
  sleep 2
else
  echo "[PipeWire] Already running — skipping launch."
fi

# (Re)start waybar
pkill waybar 2>/dev/null
sleep 0.3
waybar &
AUTOEOF
chmod +x "${HOME}/.config/autostart/pipewire.sh"
success "PipeWire autostart configured."

# Hyprland D-Bus launcher
cat >"${HOME}/start-hyprland.sh" <<'HLEOF'
#!/bin/bash
# Launch Hyprland under a D-Bus session so portals, tray apps,
# and systemd user services all get the correct environment.
exec dbus-run-session start-hyprland
HLEOF
chmod +x "${HOME}/start-hyprland.sh"
success "start-hyprland.sh created at ~/start-hyprland.sh"
