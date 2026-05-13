#!/bin/bash
# [13/14] Dotfile Deployment + Autostart

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

# PipeWire autostart
cat >"${HOME}/.config/autostart/pipewire.sh" <<'AUTOEOF'
#!/bin/bash

kill_pipewire() {
  kill $PIPEWIRE_PID $PULSE_PID $WP_PID 2>/dev/null
  sleep 1
}

attempt=1

while true; do
  echo "[PipeWire] Starting audio services (attempt $attempt)..."

  /usr/bin/pipewire &
  PIPEWIRE_PID=$!
  /usr/bin/pipewire-pulse &
  PULSE_PID=$!
  /usr/bin/wireplumber &
  WP_PID=$!

  sleep 2

  fail=0
  kill -0 $PIPEWIRE_PID 2>/dev/null || fail=1
  kill -0 $PULSE_PID    2>/dev/null || fail=1
  kill -0 $WP_PID       2>/dev/null || fail=1

  if [[ $fail -eq 0 ]]; then
    echo "[PipeWire] Audio is ready."
    waybar &
    exit 0
  fi

  echo "[PipeWire] Audio did not start correctly, trying again..."
  kill_pipewire
  (( attempt++ ))
  sleep 2
done
AUTOEOF
chmod +x "${HOME}/.config/autostart/pipewire.sh"
success "PipeWire autostart configured."

# GTK settings — write directly into config files, no script needed
info "Writing GTK theme settings..."

mkdir -p "${HOME}/.config/gtk-3.0" "${HOME}/.config/gtk-4.0" "${HOME}/.icons/default"

cat > "${HOME}/.config/gtk-3.0/settings.ini" <<'EOF'
[Settings]
gtk-theme-name=Nordic-bluish-accent-v40
gtk-icon-theme-name=Papirus
gtk-cursor-theme-name=ArcDusk-cursors
gtk-cursor-theme-size=24
gtk-font-name=Sans 10
EOF

cat > "${HOME}/.config/gtk-4.0/settings.ini" <<'EOF'
[Settings]
gtk-theme-name=Nordic-bluish-accent-v40
gtk-icon-theme-name=Papirus
gtk-cursor-theme-name=ArcDusk-cursors
gtk-cursor-theme-size=24
gtk-font-name=Sans 10
EOF

cat > "${HOME}/.gtkrc-2.0" <<'EOF'
gtk-theme-name="Nordic-bluish-accent-v40"
gtk-icon-theme-name="Papirus"
gtk-cursor-theme-name="ArcDusk-cursors"
gtk-cursor-theme-size=24
gtk-font-name="Sans 10"
EOF

cat > "${HOME}/.icons/default/index.theme" <<'EOF'
[Icon Theme]
Name=ArcDusk-cursors
Inherits=ArcDusk-cursors
EOF

success "GTK theme settings written."

# D-Bus session startup script
cat >"${HOME}/start-dbus.sh" <<'AUTOEOF'
#!/bin/bash
# Start a D-Bus session and launch Hyprland within it.
# Usage: run this instead of calling Hyprland directly (e.g. from TTY login).
exec dbus-run-session start-hyprland
AUTOEOF
chmod +x "${HOME}/start-dbus.sh"
success "D-Bus session startup script created at ~/start-dbus.sh"
