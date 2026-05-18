#!/bin/bash
# [1/13] Arch Linux Repositories

sudo pacman -S --noconfirm --needed archlinux-keyring archlinux-mirrorlist artix-archlinux-support lib32-artix-archlinux-support ||
  die "Failed to install repository packages."

[[ -f "$DOTFILES_DIR/pacman.conf" ]] || die "pacman.conf not found in dotfiles."
sudo cp /etc/pacman.conf /etc/pacman.conf.bak && info "Backed up existing pacman.conf"
sudo cp "$DOTFILES_DIR/pacman.conf" /etc/pacman.conf

sudo pacman-key --populate archlinux
sudo pacman -Sy --noconfirm

success "Arch repositories configured."
