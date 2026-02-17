sudo pacman -S archlinux-keyring archlinux-mirrorlist artix-archlinux-support --noconfirm
sudo rm -rf /etc/pacman.conf
sudo cp $HOME/Faded-Dream-dotfiles/pacman.conf /etc/
sudo pacman -S nautilus rofi git rust hyprland xorg-server xorg-xwayland pipewire pipewire-pulse pipewire-alsa pipewire-jack noto-fonts noto-fonts-cjk noto-fonts-emoji waybar swaync neovim hyprshot --noconfirm
git clone https://aur.archlinux.org/paru.git
cd paru
makepkg -si
paru -S waypaper
