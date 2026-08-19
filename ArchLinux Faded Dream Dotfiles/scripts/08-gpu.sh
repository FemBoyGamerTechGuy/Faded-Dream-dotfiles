#!/bin/bash
# [8/13] GPU Drivers

KERNEL=$(uname -r)
case "$KERNEL" in
*zen*)      HEADERS="linux-zen-headers" ;;
*lts*)      HEADERS="linux-lts-headers" ;;
*hardened*) HEADERS="linux-hardened-headers" ;;
*)          HEADERS="linux-headers" ;;
esac
info "Detected kernel: $KERNEL — will install $HEADERS"

echo ""
echo -e "${BOLD}${CYAN}  Which GPU do you have?${RESET}"
echo -e "  1) AMD (discrete + iGPU / Ryzen APU)"
echo -e "  2) Nvidia RTX 50 series - GTX 16 series"
echo -e "  3) Nvidia GTX 1080 Ti - GTX 1010"
echo -e "  4) Intel (discrete + iGPU)"
echo -e "  5) Skip (no drivers needed)"
echo ""
read -rp "  Enter choice [1-5]: " GPU_CHOICE

case "$GPU_CHOICE" in
1)
  info "AMD selected — installing AMD drivers."
  sudo pacman -S --noconfirm --needed \
    mesa vulkan-radeon xf86-video-amdgpu dkms "$HEADERS" ||
    die "Failed to install AMD drivers."
  success "AMD drivers installed."
  ;;
2)
  info "Nvidia RTX 50 - GTX 16 series selected — installing drivers."
  sudo pacman -S --noconfirm --needed dkms "$HEADERS" ||
    die "Failed to install dkms and headers."
  sudo pacman -S --noconfirm --needed \
    nvidia-open-dkms nvidia-utils lib32-nvidia-utils \
    lib32-opencl-nvidia opencl-nvidia nvidia-settings ||
    die "Failed to install Nvidia drivers."
  success "Nvidia drivers installed."
  ;;
3)
  info "Nvidia GTX 1080 Ti - GTX 1010 selected — installing drivers."
  sudo pacman -S --noconfirm --needed dkms "$HEADERS" ||
    die "Failed to install dkms and headers."
  paru -S --noconfirm --needed \
    nvidia-580xx-dkms nvidia-580xx-utils lib32-nvidia-580xx-utils \
    opencl-nvidia-580xx lib32-opencl-nvidia-580xx nvidia-580xx-settings ||
    die "Failed to install Nvidia 580xx drivers."
  success "Nvidia 580xx drivers installed."
  ;;
4)
  info "Intel selected — installing Intel drivers."
  sudo pacman -S --noconfirm --needed \
    mesa vulkan-intel libva-intel-driver xf86-video-intel \
    dkms "$HEADERS" ||
    die "Failed to install Intel drivers."
  success "Intel drivers installed."
  ;;
5)
  warn "Skipping GPU driver installation."
  ;;
*)
  warn "Invalid choice, skipping GPU driver installation."
  ;;
esac
