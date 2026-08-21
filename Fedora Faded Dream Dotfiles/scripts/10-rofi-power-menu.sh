#!/bin/bash
# [10/13] Rofi Power Menu (Fedora / systemd)
# On systemd we use the rofi-power-menu package from COPR, which ships a
# script that talks to loginctl/systemd for power management.

if command -v rofi-power-menu &>/dev/null; then
  warn "rofi-power-menu already installed, skipping."
else
  info "Installing rofi-power-menu from COPR..."
  sudo dnf install -y rofi-power-menu ||
    die "Failed to install rofi-power-menu."
fi

success "rofi-power-menu installed."