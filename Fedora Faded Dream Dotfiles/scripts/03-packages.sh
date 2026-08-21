#!/bin/bash
# [3/13] Core Packages (Fedora — official repos + RPM Fusion only)
# Packages with no official Fedora/RPM Fusion build are deferred to
# 09-copr-packages.sh, which runs after COPR repos are enabled.

PACKAGES=(
   # Desktop / WM
   hyprland
   xorg-x11-server-Xwayland
   waybar
   swaync
   nwg-look

  # Audio
  pipewire
  pipewire-pulseaudio
  pipewire-alsa
  pipewire-jack-audio-connection-kit
  pavucontrol

   # Polkit
   polkit
   polkit-gnome

  # Fonts
   google-noto-fonts
   google-noto-fonts-cjk
   google-noto-emoji-fonts
   fira-code-fonts

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
  ImageMagick
  ffmpeg

  # Languages & runtimes
  rust
  golang
  python3-pip
  java-21-openjdk
  julia
  php
  npm
  luarocks
  tectonic

  # Faded Dream (GTK4 app)
  gtk4
  libadwaita
  python3-gobject
  python3-cairo

  # VoidDream (TUI file manager)
  chafa
  unrar
  unzip
  p7zip
  zstd
)

sudo dnf install -y "${PACKAGES[@]}" ||
  die "Package installation failed."

success "Core packages installed."