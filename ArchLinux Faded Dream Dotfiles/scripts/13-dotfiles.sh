#!/bin/bash
# [13/13] Dotfile Deployment + Autostart (Arch Linux)
# PipeWire is managed by systemd user units on Arch, so we don't need a
# pipewire.sh autostart script here. Waybar is autostarted via hyprland.lua
# after the XDG desktop portal comes up.

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

# Hyprland D-Bus launcher
cat >"${HOME}/start-hyprland.sh" <<'HLEOF'
#!/bin/bash
# Launch Hyprland under a D-Bus session so portals, tray apps,
# and systemd user services all get the correct environment.
exec dbus-run-session start-hyprland
HLEOF
chmod +x "${HOME}/start-hyprland.sh"
success "start-hyprland.sh created at ~/start-hyprland.sh"
