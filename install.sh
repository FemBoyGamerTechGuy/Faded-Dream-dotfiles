sudo pacman -S archlinux-keyring archlinux-mirrorlist artix-archlinux-support --noconfirm
sudo rm -rf /etc/pacman.conf
mkdir $HOME/.config #This creates a ".config" folder if not alredy created
mkdir -p $HOME/.local/share #This also creates a folder with the path "USER/.local/share" if non existent 
cp -r $HOME/Faded-Dream-dotfiles/hypr $HOME/.config
sudo cp $HOME/Faded-Dream-dotfiles/pacman.conf /etc/
sudo pacman-key --populate archlinux
sudo pacman -Sy --noconfirm
sudo pacman -S nemo polkit-gnome rofi git rust hyprland xorg-server xorg-xwayland pipewire pipewire-pulse pipewire-alsa pipewire-jack noto-fonts noto-fonts-cjk noto-fonts-emoji waybar swaync neovim hyprshot --noconfirm
git clone https://aur.archlinux.org/paru.git
cd paru
makepkg -si
paru -S waypaper mpvpaper clipse-wayland-bin --noconfirm
cp -r "$HOME/Faded-Dream-dotfiles/rofi for .config" "$HOME/.config/rofi" # This copys the needed files for rofi into .config
cp -r "$HOME/Faded-Dream-dotfiles/rofi for local then share" "$HOME/.local/share/rofi" # This copys the needed files for .local/share
cp -r "$HOME/Faded-Dream-dotfiles/fastfetch" "$HOME/.config/fastfetch" # This copys fastfetch config into .config
