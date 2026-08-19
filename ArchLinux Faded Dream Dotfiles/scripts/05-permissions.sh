#!/bin/bash
# [5/13] User Permissions

INIT_CACHE="/tmp/.faded-dream-init"

if [[ -f "$INIT_CACHE" ]]; then
  INIT_SYSTEM="$(cat "$INIT_CACHE")"
  info "Init system: ${BOLD}${INIT_SYSTEM}${RESET}"
else
  warn "Init system not found — please re-run from the beginning."
  exit 1
fi

# --- Group membership --------------------------------------------------------
info "Adding $USER to storage, input, and video groups."
sudo usermod -aG storage "$USER" || warn "Could not add $USER to storage group."
sudo usermod -aG input "$USER" || warn "Could not add $USER to input group."
sudo usermod -aG video "$USER" || warn "Could not add $USER to video group."
success "Group membership updated (storage, input, video)."
warn "Group changes take effect on next login."
