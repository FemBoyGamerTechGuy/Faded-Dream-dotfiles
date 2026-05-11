#!/bin/bash
# [4/13] Device Type

INIT_CACHE="/tmp/.faded-dream-init"

if [[ -f "$INIT_CACHE" ]]; then
  INIT_SYSTEM="$(cat "$INIT_CACHE")"
  info "Using init system: ${BOLD}${INIT_SYSTEM}${RESET}"
else
  warn "Init system not detected from previous step — defaulting to runit."
  INIT_SYSTEM="runit"
fi

echo ""
echo -e "${BOLD}${CYAN}  What type of device are you installing on?${RESET}"
echo -e "  1) Laptop"
echo -e "  2) PC"
echo ""
read -rp "  Enter choice [1/2]: " DEVICE_CHOICE

if [[ "$DEVICE_CHOICE" == "1" ]]; then
  info "Laptop selected — installing laptop specific packages."

  # Build package list based on init system
  LAPTOP_PKGS=(brightnessctl acpi powertop bluez-utils)

  case "$INIT_SYSTEM" in
    runit)  LAPTOP_PKGS+=(tlp-runit  acpid-runit  bluez-runit  cpupower-runit)  ;;
    openrc) LAPTOP_PKGS+=(tlp-openrc acpid-openrc bluez-openrc cpupower-openrc) ;;
    dinit)  LAPTOP_PKGS+=(tlp-dinit  acpid-dinit  bluez-dinit  cpupower-dinit)  ;;
    s6)     LAPTOP_PKGS+=(tlp-s6     acpid-s6     bluez-s6     cpupower-s6)     ;;
  esac

  sudo pacman -S --noconfirm --needed "${LAPTOP_PKGS[@]}" ||
    die "Failed to install laptop packages."

  # Enable & start services
  case "$INIT_SYSTEM" in
    runit)
      sudo ln -s /etc/runit/sv/tlp        /run/runit/service 2>/dev/null || warn "tlp service link already exists."
      sudo ln -s /etc/runit/sv/acpid      /run/runit/service 2>/dev/null || warn "acpid service link already exists."
      sudo ln -s /etc/runit/sv/bluetoothd /run/runit/service 2>/dev/null || warn "bluetoothd service link already exists."
      sudo ln -s /etc/runit/sv/cpupower   /run/runit/service 2>/dev/null || warn "cpupower service link already exists."
      sudo sv up tlp        2>&1 | grep -qiE "fail|error" && warn "Could not start tlp — it will start on next boot."        || true
      sudo sv up acpid      2>&1 | grep -qiE "fail|error" && warn "Could not start acpid — it will start on next boot."      || true
      sudo sv up bluetoothd 2>&1 | grep -qiE "fail|error" && warn "Could not start bluetoothd — it will start on next boot." || true
      sudo sv up cpupower   2>&1 | grep -qiE "fail|error" && warn "Could not start cpupower — it will start on next boot."   || true
      ;;
    openrc)
      sudo rc-update add tlp        default || warn "Could not enable tlp."
      sudo rc-update add acpid      default || warn "Could not enable acpid."
      sudo rc-update add bluetoothd default || warn "Could not enable bluetoothd."
      sudo rc-update add cpupower   default || warn "Could not enable cpupower."
      sudo rc-service tlp        start || warn "Could not start tlp — it will start on next boot."
      sudo rc-service acpid      start || warn "Could not start acpid — it will start on next boot."
      sudo rc-service bluetoothd start || warn "Could not start bluetoothd — it will start on next boot."
      sudo rc-service cpupower   start || warn "Could not start cpupower — it will start on next boot."
      ;;
    dinit)
      sudo dinitctl enable tlp        || warn "Could not enable tlp."
      sudo dinitctl enable acpid      || warn "Could not enable acpid."
      sudo dinitctl enable bluetoothd || warn "Could not enable bluetoothd."
      sudo dinitctl enable cpupower   || warn "Could not enable cpupower."
      sudo dinitctl start tlp        || warn "Could not start tlp — it will start on next boot."
      sudo dinitctl start acpid      || warn "Could not start acpid — it will start on next boot."
      sudo dinitctl start bluetoothd || warn "Could not start bluetoothd — it will start on next boot."
      sudo dinitctl start cpupower   || warn "Could not start cpupower — it will start on next boot."
      ;;
    s6)
      sudo s6-rc-bundle-update add default tlp        || warn "Could not enable tlp."
      sudo s6-rc-bundle-update add default acpid      || warn "Could not enable acpid."
      sudo s6-rc-bundle-update add default bluetoothd || warn "Could not enable bluetoothd."
      sudo s6-rc-bundle-update add default cpupower   || warn "Could not enable cpupower."
      sudo s6-rc change -u tlp        || warn "Could not start tlp — it will start on next boot."
      sudo s6-rc change -u acpid      || warn "Could not start acpid — it will start on next boot."
      sudo s6-rc change -u bluetoothd || warn "Could not start bluetoothd — it will start on next boot."
      sudo s6-rc change -u cpupower   || warn "Could not start cpupower — it will start on next boot."
      ;;
  esac

  # --- Brightness persistence ---
  case "$INIT_SYSTEM" in
    s6)
      info "Installing brightness persistence for s6 (backlight-s6)."
      sudo pacman -S --noconfirm --needed backlight-s6 ||
        die "Failed to install backlight-s6."
      success "backlight-s6 installed."
      ;;
    openrc)
      info "Installing brightness persistence for openrc (backlight-openrc)."
      sudo pacman -S --noconfirm --needed backlight-openrc ||
        die "Failed to install backlight-openrc."
      sudo rc-update add backlight default ||
        warn "Could not enable backlight service — enable manually: rc-update add backlight default"
      success "backlight-openrc installed and enabled."
      ;;
    runit|dinit)
      info "No backlight persistence package available for ${INIT_SYSTEM} — skipping."
      info "Brightness will be managed by brightnessctl at session start."
      ;;
  esac

  success "Laptop packages installed."
else
  info "PC selected — skipping laptop specific packages."
fi
