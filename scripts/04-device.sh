#!/bin/bash
# [4/11] Device Type

echo ""
echo -e "${BOLD}${CYAN}  What type of device are you installing on?${RESET}"
echo -e "  1) Laptop"
echo -e "  2) PC"
echo ""
read -rp "  Enter choice [1/2]: " DEVICE_CHOICE

if [[ "$DEVICE_CHOICE" == "1" ]]; then
  info "Laptop selected — installing laptop specific packages."
  sudo pacman -S --noconfirm --needed \
    tlp-runit brightnessctl acpi acpid-runit \
    bluez-runit bluez-utils cpupower-runit powertop ||
    die "Failed to install laptop packages."
  sudo ln -s /etc/runit/sv/tlp      /run/runit/service 2>/dev/null || warn "tlp service link already exists."
  sudo ln -s /etc/runit/sv/acpid    /run/runit/service 2>/dev/null || warn "acpid service link already exists."
  sudo ln -s /etc/runit/sv/bluetoothd /run/runit/service 2>/dev/null || warn "bluetoothd service link already exists."
  sudo ln -s /etc/runit/sv/cpupower /run/runit/service 2>/dev/null || warn "cpupower service link already exists."
  sudo sv up tlp       || warn "Could not start tlp — it will start on next boot."
  sudo sv up acpid     || warn "Could not start acpid — it will start on next boot."
  sudo sv up bluetoothd || warn "Could not start bluetoothd — it will start on next boot."
  sudo sv up cpupower  || warn "Could not start cpupower — it will start on next boot."
  success "Laptop packages installed."
else
  info "PC selected — skipping laptop specific packages."
fi
