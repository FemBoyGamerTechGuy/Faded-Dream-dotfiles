#!/bin/bash
# [1/13] Arch Linux Repositories

# Backup original user pacman configuration, replace with Faded Dream config,
# then run a full sync + upgrade.
[[ -f "$DOTFILES_DIR/pacman.conf" ]] || die "pacman.conf not found in dotfiles."
sudo cp /etc/pacman.conf /etc/pacman.conf.bak && info "Backed up existing pacman.conf"
sudo cp "$DOTFILES_DIR/pacman.conf" /etc/pacman.conf

sudo pacman -Syyu --noconfirm

success "Arch pacman.conf installed (replaced original user configuration)."