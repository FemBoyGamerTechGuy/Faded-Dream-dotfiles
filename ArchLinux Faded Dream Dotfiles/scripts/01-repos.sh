#!/bin/bash
# [1/13] Arch Linux Repositories

# Copy the Faded Dream pacman.conf to replace the user's original configuration
[[ -f "$DOTFILES_DIR/pacman.conf" ]] || die "pacman.conf not found in dotfiles."
sudo cp /etc/pacman.conf /etc/pacman.conf.bak && info "Backed up existing pacman.conf"
sudo cp "$DOTFILES_DIR/pacman.conf" /etc/pacman.conf

success "Arch pacman.conf installed (replaced original user configuration)."