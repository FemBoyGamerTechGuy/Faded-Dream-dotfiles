#!/bin/bash

# =============================================================================
# Faded Dream Dotfiles - Install Script
# =============================================================================

echo ""
echo "============================================="
echo "   Faded Dream Dotfiles - Install Script"
echo "============================================="
echo ""

# --- Arch Linux Repository Setup ---------------------------------------------

echo "[1/6] Setting up Arch Linux repositories..."

sudo pacman -S archlinux-keyring archlinux-mirrorlist artix-archlinux-support --noconfirm
sudo rm -rf /etc/pacman.conf
sudo cp $HOME/Faded-Dream-dotfiles/pacman.conf /etc/
sudo pacman-key --populate archlinux
sudo pacman -Sy --noconfirm

echo "[1/6] Done."
echo ""

# --- Directory Structure -----------------------------------------------------

echo "[2/6] Creating directory structure..."

mkdir -p $HOME/.config
mkdir -p $HOME/.local/share
mkdir -p $HOME/.config/autostart

echo "[2/6] Done."
echo ""

# --- Package Installation ----------------------------------------------------

echo "[3/6] Installing core packages..."

sudo pacman -S \
    nemo \
    polkit-gnome \
    rofi \
    git \
    rust \
    hyprland \
    xorg-server \
    xorg-xwayland \
    pipewire \
    pipewire-pulse \
    pipewire-alsa \
    pipewire-jack \
    noto-fonts \
    noto-fonts-cjk \
    noto-fonts-emoji \
    waybar \
    swaync \
    neovim \
    hyprshot \
    --noconfirm

echo "[3/6] Done."
echo ""

# --- AUR Helper (paru) -------------------------------------------------------

echo "[4/6] Installing paru AUR helper and AUR packages..."

git clone https://aur.archlinux.org/paru.git
cd paru && makepkg -si
paru -S waypaper mpvpaper clipse-wayland-bin --noconfirm

echo "[4/6] Done."
echo ""

# --- Dotfile Deployment ------------------------------------------------------

echo "[5/6] Deploying dotfiles..."

cp -r $HOME/Faded-Dream-dotfiles/hypr $HOME/.config
cp -r "$HOME/Faded-Dream-dotfiles/rofi for .config" "$HOME/.config/rofi"
cp -r "$HOME/Faded-Dream-dotfiles/rofi for local then share" "$HOME/.local/share/rofi"
cp -r "$HOME/Faded-Dream-dotfiles/fastfetch" "$HOME/.config/fastfetch"

echo "[5/6] Done."
echo ""

# --- Autostart Services ------------------------------------------------------

echo "[6/6] Setting up PipeWire autostart service..."

cat > $HOME/.config/autostart/pipewire.sh << 'EOF'
#!/bin/bash

# Wait for XDG_RUNTIME_DIR to be available before starting audio services.
while [ ! -d "/run/user/$(id -u)" ]; do
    sleep 0.5
done

sleep 3

/usr/bin/pipewire &
/usr/bin/pipewire-pulse &
/usr/bin/wireplumber &
EOF

chmod +x $HOME/.config/autostart/pipewire.sh

echo "[6/6] Done."
echo ""

echo "============================================="
echo "   Installation complete! Rebooting in 10"
echo "   seconds. Press CTRL+C to cancel."
echo "============================================="
echo ""

sleep 10
sudo reboot
