#!/bin/bash
# [9/13] AUR Packages

paru -S --noconfirm --needed waypaper mpvpaper clipse-wayland-bin rofimoji-git ||
  die "Failed to install AUR packages."

success "AUR packages installed."
