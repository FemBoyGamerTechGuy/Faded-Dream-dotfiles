#!/bin/bash
# [7/11] GPU Drivers

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
echo -e "  4) Nvidia GTX 700 - GTX 600 series"
echo -e "  5) Nvidia GTX 500 - GTX 400 series"
echo -e "  6) Nvidia GeForce 8/9/100/200/300 series"
echo -e "  7) Intel (discrete + iGPU)"
echo -e "  8) Skip (no drivers needed)"
echo ""
read -rp "  Enter choice [1-8]: " GPU_CHOICE

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
  sudo pacman -S --noconfirm --needed \
    nvidia-580xx-dkms nvidia-580xx-utils lib32-nvidia-580xx-utils \
    opencl-nvidia-580xx lib32-opencl-nvidia-580xx nvidia-580xx-settings ||
    die "Failed to install Nvidia 580xx drivers."
  success "Nvidia 580xx drivers installed."
  ;;
4)
  info "Nvidia GTX 700 - GTX 600 series selected — installing drivers."
  sudo pacman -S --noconfirm --needed dkms "$HEADERS" ||
    die "Failed to install dkms and headers."
  paru -S --noconfirm --needed \
    nvidia-470xx-dkms nvidia-470xx-utils nvidia-470xx-settings \
    opencl-nvidia-470xx lib32-nvidia-470xx-utils lib32-opencl-nvidia-470xx ||
    die "Failed to install Nvidia 470xx drivers."
  success "Nvidia 470xx drivers installed."
  ;;
5)
  info "Nvidia GTX 500 - GTX 400 series selected — installing drivers."
  sudo pacman -S --noconfirm --needed dkms "$HEADERS" ||
    die "Failed to install dkms and headers."
  paru -S --noconfirm --needed \
    nvidia-390xx-dkms nvidia-390xx-utils nvidia-390xx-settings \
    opencl-nvidia-390xx lib32-nvidia-390xx-utils lib32-opencl-nvidia-390xx ||
    die "Failed to install Nvidia 390xx drivers."
  success "Nvidia 390xx drivers installed."
  ;;
6)
  info "Nvidia GeForce 8/9/100/200/300 series selected — installing drivers."
  sudo pacman -S --noconfirm --needed dkms "$HEADERS" ||
    die "Failed to install dkms and headers."
  paru -S --noconfirm --needed \
    nvidia-340xx-dkms nvidia-340xx-utils nvidia-340xx-settings \
    opencl-nvidia-340xx lib32-nvidia-340xx-utils lib32-opencl-nvidia-340xx ||
    die "Failed to install Nvidia 340xx drivers."
  success "Nvidia 340xx drivers installed."
  ;;
7)
  info "Intel selected — installing Intel drivers."
  sudo pacman -S --noconfirm --needed \
    mesa vulkan-intel libva-intel-driver xf86-video-intel \
    dkms "$HEADERS" ||
    die "Failed to install Intel drivers."
  success "Intel drivers installed."
  ;;
8)
  warn "Skipping GPU driver installation."
  ;;
*)
  warn "Invalid choice, skipping GPU driver installation."
  ;;
esac
