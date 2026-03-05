#!/bin/bash
# [3/11] Core Packages

PACKAGES=(
  # Desktop / WM
  hyprland
  xorg-server
  xorg-xwayland
  waybar
  swaync
  rofi
  nwg-look
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
  yt-dlp
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
  # ── Faded Dream Setup (faded-dream-setup-gtk.py) ──────────────────────────
  # GTK4 + libadwaita UI toolkit
  gtk4
  libadwaita
  # Python GTK4 bindings
  python-gobject          # gi.repository (Gtk, Adw, GLib, Pango)
  python-cairo            # cairo drawing for animations
)

sudo pacman -S --noconfirm --needed "${PACKAGES[@]}" ||
  die "Package installation failed."

success "Core packages installed."
