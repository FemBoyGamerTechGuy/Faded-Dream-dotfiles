<div align="center">

# Faded Dream Dotfiles

> A straightforward [Hyprland](https://github.com/hyprwm/Hyprland) configuration focused on simplicity, compatibility, and daily usability.  
> Built and tested on [Artix Linux](https://artixlinux.org/) (runit) with reliable XWayland support.

</div>

---

## Previews

<div align="center">

[![Screenshot 1](https://github.com/FemBoyGamerTechGuy/Faded-Dream-dotfiles/raw/main/Previews/2026-02-22-192101_hyprshot.png)](https://github.com/FemBoyGamerTechGuy/Faded-Dream-dotfiles/blob/main/Previews/2026-02-22-192101_hyprshot.png)
[![Screenshot 2](https://github.com/FemBoyGamerTechGuy/Faded-Dream-dotfiles/raw/main/Previews/2026-02-22-193220_hyprshot.png)](https://github.com/FemBoyGamerTechGuy/Faded-Dream-dotfiles/blob/main/Previews/2026-02-22-193220_hyprshot.png)
[![Screenshot 3](https://github.com/FemBoyGamerTechGuy/Faded-Dream-dotfiles/raw/main/Previews/2026-02-22-193353_hyprshot.png)](https://github.com/FemBoyGamerTechGuy/Faded-Dream-dotfiles/blob/main/Previews/2026-02-22-193353_hyprshot.png)

</div>

---

## Video Demonstration

<!-- Replace with actual video link when ready -->
> Video coming soon.

---

## Features

- **Single central config** — one `hyprland.conf` to rule them all *(may split in the future)*
- **XWayland compatibility** — Xorg apps run smoothly under Wayland
- **Lightweight** — works on most hardware including integrated GPUs
- **[Rofi](https://github.com/davatorium/rofi)** — application launcher
- **[mpvpaper](https://github.com/GhostNaN/mpvpaper)** — video wallpaper support
- **[swaync](https://github.com/ErikReider/SwayNotificationCenter)** — notifications
- **[Catppuccin Macchiato](https://github.com/catppuccin/catppuccin)** — theme across terminal and GTK apps
- **Designed for daily use** — no fluff, just a setup that works

---

## Environment

| Component | Tool |
|-----------|------|
| Compositor | [Hyprland](https://github.com/hyprwm/Hyprland) |
| Distribution | [Artix Linux](https://artixlinux.org/) |
| Init System | runit |
| Shell | [zsh](https://www.zsh.org/) |
| Terminal | [Kitty](https://github.com/kovidgoyal/kitty) |
| Editor | [Neovim](https://neovim.io/) + [LazyVim](https://www.lazyvim.org/) |
| Launcher | [Rofi](https://github.com/davatorium/rofi) |
| Notifications | [swaync](https://github.com/ErikReider/SwayNotificationCenter) |
| Wallpaper | [mpvpaper](https://github.com/GhostNaN/mpvpaper) / [waypaper](https://github.com/anufrievroman/waypaper) |
| File Manager | [Nemo](https://github.com/linuxmint/nemo) |
| Browser | [LibreWolf](https://librewolf.net/) |
| Theme | [Catppuccin Macchiato](https://github.com/catppuccin/catppuccin) |

---

## Keybinds

| Keybind | Action |
|---------|--------|
| `Super + Enter` | Open terminal (Kitty) |
| `Super + Q` | Close active window |
| `Super + E` | Open file manager (Nemo) |
| `Super + B` | Open browser (LibreWolf) |
| `Super + V` | Toggle floating |
| `Super + C` | Open clipboard manager (clipse) |
| `Super + W` | Restart Waybar |
| `Super + M` | Exit Hyprland |
| `Alt + Space` | Open Rofi launcher |
| `Print` | Screenshot region |
| `Super + Arrow keys` | Move focus |
| `Super + [1-0]` | Switch workspace |
| `Super + Shift + [1-0]` | Move window to workspace |

---

## Installation

> Tested on a fresh Artix Linux (runit) install.
```bash
git clone https://github.com/FemBoyGamerTechGuy/Faded-Dream-dotfiles.git ~/Faded-Dream-dotfiles
cd ~/Faded-Dream-dotfiles
chmod +x install.sh
./install.sh
```

The install script will handle everything including packages, AUR helpers, dotfile deployment, and shell setup. A reboot is triggered automatically at the end.

---

## Project Structure
```bash
Faded-Dream-dotfiles/
├── hypr/
│   └── hyprland.conf
├── waybar/
├── rofi for .config/
├── rofi for local then share/
├── fastfetch/
├── gtk configs/
│   ├── gtk-3.0/
│   ├── gtk-4.0/
│   ├── xsettingsd/
│   └── .gtkrc-2.0
├── .zsh/
├── .zshrc
├── .themes/
├── .icons/
├── pacman.conf
└── install.sh
```

---

<div align="center">
<sub>Built with 💜 on Artix Linux</sub>
</div>My configuration Simple xorg support configuration made to work with any apps 
