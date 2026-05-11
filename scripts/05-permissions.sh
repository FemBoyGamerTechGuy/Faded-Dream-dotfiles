#!/bin/bash
# [5/13] Init System & User Permissions

INIT_CACHE="/tmp/.faded-dream-init"

# --- Ask init system ---------------------------------------------------------
echo ""
echo -e "${BOLD}${CYAN}  Which init system are you using?${RESET}"
echo -e "  1) runit"
echo -e "  2) openrc"
echo -e "  3) dinit"
echo -e "  4) s6"
echo ""
read -rp "  Enter choice [1-4]: " INIT_CHOICE

case "$INIT_CHOICE" in
  1) INIT_SYSTEM="runit"  ;;
  2) INIT_SYSTEM="openrc" ;;
  3) INIT_SYSTEM="dinit"  ;;
  4) INIT_SYSTEM="s6"     ;;
  *)
    warn "Invalid choice — defaulting to runit."
    INIT_SYSTEM="runit"
    ;;
esac

echo "$INIT_SYSTEM" > "$INIT_CACHE"
info "Init system set to: ${BOLD}${INIT_SYSTEM}${RESET}"

# --- Group membership --------------------------------------------------------
info "Adding $USER to storage, input, and video groups."
sudo usermod -aG storage "$USER" || warn "Could not add $USER to storage group."
sudo usermod -aG input   "$USER" || warn "Could not add $USER to input group."
sudo usermod -aG video   "$USER" || warn "Could not add $USER to video group."
success "Group membership updated (storage, input, video)."
warn "Group changes take effect on next login."
