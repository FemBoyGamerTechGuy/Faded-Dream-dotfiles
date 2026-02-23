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
- **[Oh My Posh](https://ohmyposh.dev/)** — shell prompt with custom `if_tea` theme
- **Designed for daily use** — no fluff, just a setup that works

---

## Environment

| Component | Tool |
|-----------|------|
| Compositor | [Hyprland](https://github.com/hyprwm/Hyprland) |
| Distribution | [Artix Linux](https://artixlinux.org/) |
| Init System | runit |
| Shell | [zsh](https://www.zsh.org/) |
| Prompt | [Oh My Posh](https://ohmyposh.dev/) |
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

## Aliases

| Alias | Command | Description |
|-------|---------|-------------|
| `ls` | `ls --color=auto` | Colored output |
| `ll` | `ls -lah --color=auto` | Detailed list with hidden files |
| `la` | `ls -A --color=auto` | List hidden files |
| `grep` | `grep --color=auto` | Colored grep |
| `cls` | `clear` | Clear terminal |
| `update` | `sudo pacman -Syu --noconfirm` | Full system update |
| `paru` | `paru --noconfirm` | AUR helper without confirmation |
| `vim` | `nvim` | Use Neovim instead of Vim |
| `cat` | `bat --style=plain` | Better cat with syntax highlighting |

> `cat` alias requires `bat` to be installed: `sudo pacman -S bat`

---

## Oh My Posh Themes

All official Oh My Posh themes are included in `.zsh/themes/`. The default is `if_tea.omp.json` — a custom theme with PM/AM clock and day names.

> Two custom `if_tea` variants are included:
> - `if_tea.omp.json` — Romanian day names
> - `if_tea-enghlis.omp.json` — English day names

To switch themes edit this line in your `.zshrc`:
```bash
eval "$($HOME/.zsh/posh-linux-amd64 init zsh --config $HOME/.zsh/themes/if_tea.omp.json)"
```

Replace `if_tea.omp.json` with any theme name from the list below. To preview all themes run:
```bash
$HOME/.zsh/posh-linux-amd64 themes --config $HOME/.zsh/themes/if_tea.omp.json
```

<details>
<summary>Click to see all available themes</summary>
```
1_shell                   gruvbox                   plague
M365Princess              half-life                 poshmon
agnoster.minimal          honukai                   powerlevel10k_classic
agnoster                  hotstick.minimal          powerlevel10k_lean
agnosterplus              hul10                     powerlevel10k_modern
aliens                    hunk                      powerlevel10k_rainbow
amro                      huvix                     powerline
atomic                    if_tea                    probua.minimal
atomicBit                 if_tea-enghlis            pure
avit                      illusi0n                  quick-term
blue-owl                  iterm2                    remk
blueish                   jandedobbeleer            robbyrussell
bubbles                   jblab_2021                rudolfs-dark
bubblesextra              jonnychipz                rudolfs-light
bubblesline               json                      sim-web
capr4n                    jtracey93                 slim
catppuccin                jv_sitecorian             slimfat
catppuccin_frappe         kali                      smoothie
catppuccin_latte          kushal                    sonicboom_dark
catppuccin_macchiato      lambda                    sonicboom_light
catppuccin_mocha          lambdageneration          sorin
cert                      larserikfinholt           space
chips                     lightgreen                spaceship
cinnamon                  marcduiker                star
clean-detailed            markbull                  stelbent-compact.minimal
cloud-context             material                  stelbent.minimal
cloud-native-azure        microverse-power          takuya
cobalt2                   mojada                    the-unnamed
craver                    montys                    thecyberden
darkblood                 mt                        tiwahu
devious-diamonds          multiverse-neon           tokyo
di4am0nd                  negligible                tokyonight_storm
dracula                   neko                      tonybaloney
easy-term                 night-owl                 uew
emodipt-extend            nordtron                  unicorn
emodipt                   nu4a                      velvet
fish                      onehalf.minimal           wholespace
free-ukraine              paradox                   wopian
froczh                    pararussel                xtoys
glowsticks                patriksvensson            ys
gmay                      peru                      zash
grandpa-style             pixelrobots
```

</details>

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
├── kitty/
│   ├── kitty.conf
│   └── current-theme.conf
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
│   ├── themes/
│   │   ├── if_tea.omp.json
│   │   ├── if_tea-enghlis.omp.json
│   │   └── ... (all official Oh My Posh themes)
│   ├── zsh-autosuggestions/
│   └── zsh-syntax-highlighting/
├── .zshrc
├── .themes/
├── .icons/
├── pacman.conf
└── install.sh
```

---

<div align="center">
<sub>Built with 💜 on Artix Linux</sub>
</div>
