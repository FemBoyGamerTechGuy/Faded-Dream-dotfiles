#!/bin/bash
# [8/13] GPU Drivers (Fedora)

KERNEL=$(uname -r)
case "$KERNEL" in
*rt*)       HEADERS="kernel-rt-devel" ;;
*debug*)    HEADERS="kernel-debug-devel" ;;
*)          HEADERS="kernel-devel" ;;
esac
info "Detected kernel: $KERNEL — will install $HEADERS"

echo ""
echo -e "${BOLD}${CYAN}  Which GPU do you have?${RESET}"
echo -e "  1) AMD (discrete + iGPU / Ryzen APU)"
echo -e "  2) Nvidia RTX 50 series - GTX 16 series"
echo -e "  3) Nvidia GTX 1080 Ti - GTX 1010 (580xx legacy)"
echo -e "  4) Intel (discrete + iGPU)"
echo -e "  5) Skip (no drivers needed)"
echo ""
read -rp "  Enter choice [1-5]: " GPU_CHOICE

case "$GPU_CHOICE" in
1)
  info "AMD selected — installing AMD drivers."
  sudo dnf install -y \
    mesa-vulkan-drivers \
    mesa-dri-drivers \
    xorg-x11-drv-amdgpu \
    dkms \
    "$HEADERS" ||
    die "Failed to install AMD drivers."
  success "AMD drivers installed."
  ;;
2)
  info "Nvidia RTX 50 - GTX 16 series selected — installing drivers."
  # Enable RPM Fusion nonfree (should already be enabled from 01-repos.sh)
  sudo dnf install -y dkms "$HEADERS" ||
    die "Failed to install dkms and headers."
  
  # Install Nvidia drivers from RPM Fusion nonfree
  sudo dnf install -y \
    akmod-nvidia \
    xorg-x11-drv-nvidia-cuda \
    nvidia-settings \
    nvidia-vaapi-driver \
    libva-nvidia-driver \
    vulkan-loader \
    nvidia-vulkan-driver ||
    die "Failed to install Nvidia drivers."
  
  # Enable Nvidia services
  sudo systemctl enable --now nvidia-persistenced 2>/dev/null || true
  
  success "Nvidia drivers installed."
  ;;
3)
  info "Nvidia GTX 1080 Ti - GTX 1010 (580xx) selected — installing drivers."
  sudo dnf install -y dkms "$HEADERS" ||
    die "Failed to install dkms and headers."
  
  # Install Nvidia 580xx legacy drivers from RPM Fusion nonfree
  sudo dnf install -y \
    akmod-nvidia-580xx \
    xorg-x11-drv-nvidia-580xx \
    xorg-x11-drv-nvidia-580xx-cuda \
    nvidia-settings-580xx \
    xorg-x11-drv-nvidia-580xx-libs \
    xorg-x11-drv-nvidia-580xx-cuda-libs ||
    die "Failed to install Nvidia 580xx drivers."
  
  # Enable Nvidia services
  sudo systemctl enable --now nvidia-persistenced 2>/dev/null || true
  
  success "Nvidia 580xx drivers installed."
  ;;
4)
  info "Intel selected — installing Intel drivers."
  sudo dnf install -y \
    mesa-vulkan-drivers \
    mesa-dri-drivers \
    intel-media-driver \
    libva-intel-driver \
    xorg-x11-drv-intel \
    dkms \
    "$HEADERS" ||
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