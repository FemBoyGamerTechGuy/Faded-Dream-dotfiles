#!/bin/bash
# [11/13] LazyVim

if [[ -d "${HOME}/.config/nvim" ]]; then
  warn "~/.config/nvim already exists, skipping LazyVim clone."
else
  git clone https://github.com/LazyVim/starter "${HOME}/.config/nvim" ||
    die "Failed to clone LazyVim starter."
  success "LazyVim starter cloned to ~/.config/nvim."
fi