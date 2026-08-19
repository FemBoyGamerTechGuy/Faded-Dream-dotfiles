#!/bin/bash
# [7/13] AUR Helper (paru)

if command -v paru &>/dev/null; then
  warn "paru already installed, skipping build."
else
  PARU_TMP=$(mktemp -d)
  git clone https://aur.archlinux.org/paru.git "$PARU_TMP/paru" ||
    die "Failed to clone paru."
  (cd "$PARU_TMP/paru" && makepkg -si --noconfirm) ||
    die "Failed to build paru."
  rm -rf "$PARU_TMP"
fi

success "paru installed."
