#!/bin/bash
# [10/13] Rofi Power Menu (Arch Linux / systemd)
# On systemd we use the upstream rofi-power-menu AUR package, which ships a
# script that talks to loginctl/systemd for power management.
if command -v rofi-power-menu &>/dev/null; then
  warn "rofi-power-menu already installed, skipping."
else
  paru -S --noconfirm --needed rofi-power-menu ||
    die "Failed to build/install rofi-power-menu."
fi

success "rofi-power-menu installed."
