#!/bin/bash
# [9/13] AUR Packages (Arch Linux)
# These packages have no official Arch build, so they go through paru.

paru -S --noconfirm --needed \
  waypaper \
  mpvpaper \
  clipse-wayland-bin \
  rofimoji-git ||
  die "Failed to install AUR packages."

success "AUR packages installed."
