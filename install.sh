sudo pacman -S archlinux-keyring archlinux-mirrorlist artix-archlinux-support --noconfirm # This installs the archlinux repos.
sudo rm -rf /etc/pacman.conf # This removes the "pacman.conf" from "/etc/".
mkdir $HOME/.config # This creates a ".config" folder if not alredy created.
mkdir -p $HOME/.local/share # This also creates a folder with the path "USER/.local/share" if non existent .
cp -r $HOME/Faded-Dream-dotfiles/hypr $HOME/.config # This copys the "hypr" file into ".config".
sudo cp $HOME/Faded-Dream-dotfiles/pacman.conf /etc/ # This copys the "pacman.conf" from the repo into "/etc/".
sudo pacman-key --populate archlinux # This updates and repos with archlinux keeping up to date and syncronized.
sudo pacman -Sy --noconfirm # This updates the repos.
sudo pacman -S nemo polkit-gnome rofi git rust hyprland xorg-server xorg-xwayland pipewire pipewire-pulse pipewire-alsa pipewire-jack noto-fonts noto-fonts-cjk noto-fonts-emoji waybar swaync neovim hyprshot --noconfirm # This installs the needed apps and packages.
git clone https://aur.archlinux.org/paru.git # This clones the AUR helper "paru".
cd paru # This changes the directory into "paru".
makepkg -si # This installs "paru".
paru -S waypaper mpvpaper clipse-wayland-bin --noconfirm # This installs some apps not really needed but you may want them.
cp -r "$HOME/Faded-Dream-dotfiles/rofi for .config" "$HOME/.config/rofi" # This copys the needed files for rofi into ".config".
cp -r "$HOME/Faded-Dream-dotfiles/rofi for local then share" "$HOME/.local/share/rofi" # This copys the needed files for ".local/share".
cp -r "$HOME/Faded-Dream-dotfiles/fastfetch" "$HOME/.config/fastfetch" # This copys "fastfetch" config into ".config".
