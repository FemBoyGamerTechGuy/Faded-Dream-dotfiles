#!/bin/bash
# [4/13] Device Type + systemd services
# Arch Linux uses systemd unconditionally — there is no init-system prompt.

INIT_SYSTEM="systemd"
echo "$INIT_SYSTEM" >/tmp/.faded-dream-init
info "Init system set to: ${BOLD}${INIT_SYSTEM}${RESET}"

echo ""
echo -e "${BOLD}${CYAN}  What type of device are you installing on?${RESET}"
echo -e "  1) Laptop"
echo -e "  2) PC"
echo ""
read -rp "  Enter choice [1/2]: " DEVICE_CHOICE

if [[ "$DEVICE_CHOICE" == "1" ]]; then
  info "Laptop selected — installing laptop specific packages."

  # Standard Arch packages (no init-system suffixes needed under systemd)
  LAPTOP_PKGS=(brightnessctl acpi powertop bluez-utils tlp acpid cpupower)

  sudo pacman -S --noconfirm --needed "${LAPTOP_PKGS[@]}" ||
    die "Failed to install laptop packages."

  # Enable & start systemd services
  for svc in tlp acpid bluetooth cpupower; do
    sudo systemctl enable --now "${svc}.service" 2>/dev/null \
      || warn "Could not enable/start ${svc}.service — it will start on next boot."
  done

  # --- Brightness persistence (systemd-native) ---
  info "Brightness persistence is handled automatically by systemd-backlight (no extra package needed)."

  success "Laptop packages installed and systemd services enabled."
else
  info "PC selected — skipping laptop specific packages."
fi
