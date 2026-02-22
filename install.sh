sudo pacman -S archlinux-keyring archlinux-mirrorlist artix-archlinux-support --noconfirm
sudo rm -rf /etc/pacman.conf
rm -rf .config
sudo cp $HOME/Faded-Dream-dotfiles/pacman.conf /etc/
sudo pacman-key --populate archlinux
sudo pacman -Sy --noconfirm
sudo pacman -S nautilus polkit-gnome rofi git rust hyprland xorg-server xorg-xwayland pipewire pipewire-pulse pipewire-alsa pipewire-jack noto-fonts noto-fonts-cjk noto-fonts-emoji waybar swaync neovim hyprshot --noconfirm
git clone https://aur.archlinux.org/paru.git
cd paru
makepkg -si
paru -S waypaper --noconfirm
paru -S mpvpaper --noconfirm
paru -S clipse-wayland-bin --noconfirm
