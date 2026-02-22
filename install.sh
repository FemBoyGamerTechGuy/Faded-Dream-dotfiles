#!/bin/bash

# Install Arch Linux keyring, mirrorlist, and support packages to enable Arch repos on Artix.
sudo pacman -S archlinux-keyring archlinux-mirrorlist artix-archlinux-support --noconfirm

# Remove the existing pacman.conf so it can be replaced with the one from the repo.
sudo rm -rf /etc/pacman.conf

# Create the .config directory if it doesn't already exist.
mkdir $HOME/.config

# Create the .local/share directory if it doesn't already exist.
mkdir -p $HOME/.local/share

# Create the autostart directory for scripts that run on login.
mkdir -p $HOME/.config/autostart

# Copy the Hyprland config into .config.
cp -r $HOME/Faded-Dream-dotfiles/hypr $HOME/.config

# Replace pacman.conf with the custom one from the repo that includes Arch repos.
sudo cp $HOME/Faded-Dream-dotfiles/pacman.conf /etc/

# Populate the Arch Linux keyring to trust Arch packages.
sudo pacman-key --populate archlinux

# Sync the package databases with the newly added repos.
sudo pacman -Sy --noconfirm

# Install all core packages including Hyprland, audio, fonts, and utilities.
sudo pacman -S nemo polkit-gnome rofi git rust hyprland xorg-server xorg-xwayland pipewire pipewire-pulse pipewire-alsa pipewire-jack noto-fonts noto-fonts-cjk noto-fonts-emoji waybar swaync neovim hyprshot --noconfirm

# Clone the paru AUR helper source from the AUR.
git clone https://aur.archlinux.org/paru.git

# Enter the paru directory to build it.
cd paru

# Build and install paru.
makepkg -si

# Install optional AUR packages for wallpaper and clipboard management.
paru -S waypaper mpvpaper clipse-wayland-bin --noconfirm

# Copy the Rofi config into .config.
cp -r "$HOME/Faded-Dream-dotfiles/rofi for .config" "$HOME/.config/rofi"

# Copy the Rofi theme files into .local/share.
cp -r "$HOME/Faded-Dream-dotfiles/rofi for local then share" "$HOME/.local/share/rofi"

# Copy the Fastfetch config into .config.
cp -r "$HOME/Faded-Dream-dotfiles/fastfetch" "$HOME/.config/fastfetch"

# Write a pipewire autostart script to .config/autostart so audio starts correctly on login.
cat > $HOME/.config/autostart/pipewire.sh << 'EOF'
#!/bin/bash
# Wait for XDG_RUNTIME_DIR to be available
while [ ! -d "/run/user/$(id -u)" ]; do
  sleep 0.5
done
sleep 3
/usr/bin/pipewire &
/usr/bin/pipewire-pulse &
/usr/bin/wireplumber &
EOF

# Make the pipewire autostart script executable.
chmod +x $HOME/.config/autostart/pipewire.sh
