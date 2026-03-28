#!/bin/bash
# [3/11] Core Packages

PACKAGES=(
  # Desktop / WM
  hyprland
  xorg-server
  xorg-xwayland
  waybar
  swaync
  nwg-look

  # Audio
  pipewire
  pipewire-pulse
  pipewire-alsa
  pipewire-jack
  pavucontrol

  # Polkit
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
  ffmpeg

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

  # Faded Dream (GTK4 app)
  gtk4
  libadwaita
  python-gobject
  python-cairo

  # VoidDream (TUI file manager)
  chafa
  unrar
  unzip
  p7zip
  zstd
)

sudo pacman -S --noconfirm --needed "${PACKAGES[@]}" ||
  die "Package installation failed."

success "Core packages installed."
