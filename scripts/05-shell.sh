#!/bin/bash
# [5/11] Set zsh as default shell

ZSH_PATH="$(command -v zsh)"
[[ -z "$ZSH_PATH" ]] && die "zsh not found after installation, something went wrong."

if [[ "$(getent passwd "$USER" | cut -d: -f7)" == "$ZSH_PATH" ]]; then
  warn "zsh is already the default shell for $USER, skipping."
else
  sudo chsh -s "$ZSH_PATH" "$USER" ||
    die "Failed to change default shell to zsh."
  success "Default shell changed to zsh for $USER."
fi
