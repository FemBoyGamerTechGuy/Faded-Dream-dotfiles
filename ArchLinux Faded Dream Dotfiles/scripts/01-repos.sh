#!/bin/bash
# [1/13] Arch Linux Repositories

[[ -f "$DOTFILES_DIR/pacman.conf" ]] || die "pacman.conf not found in dotfiles."
sudo cp /etc/pacman.conf /etc/pacman.conf.bak && info "Backed up existing pacman.conf"
sudo cp "$DOTFILES_DIR/pacman.conf" /etc/pacman.conf

# Ensure the Arch keyring is present and populated (safe on ISOs / fresh installs)
sudo pacman -Sy --noconfirm --needed archlinux-keyring || warn "archlinux-keyring sync failed."

sudo pacman-key --populate archlinux 2>/dev/null || true
sudo pacman -Sy --noconfirm

success "Arch repositories configured (extra + multilib)."
