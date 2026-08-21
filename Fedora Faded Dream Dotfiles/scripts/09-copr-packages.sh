#!/bin/bash
# [9/13] COPR / Flatpak Packages (Fedora)
# These packages have no official Fedora/RPM Fusion build, so they go through COPR or Flatpak.

# Packages from COPR repos (enabled in 07-copr.sh)
COPR_PACKAGES=(
  waypaper
  clipse
  rofimoji
)

info "Installing COPR packages..."
sudo dnf install -y "${COPR_PACKAGES[@]}" ||
  warn "Some COPR packages may not be available yet."

# Flatpak packages
FLATPAK_PACKAGES=(
  "org.vinegarhq.Sober"           # Sober (Roblox client)
  "io.github.aandrew_me.ytdn"     # YT Downloader
)

if command -v flatpak &>/dev/null; then
  info "Installing Flatpak packages..."
  for pkg in "${FLATPAK_PACKAGES[@]}"; do
    flatpak install --noninteractive flathub "$pkg" || warn "Failed to install $pkg"
  done
else
  warn "flatpak not available, skipping Flatpak packages."
fi

success "COPR/Flatpak packages installation attempted."