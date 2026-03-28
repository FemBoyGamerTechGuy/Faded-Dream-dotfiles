<div align="center">

<img src="https://github.com/FemBoyGamerTechGuy/Faded-Dream-dotfiles/raw/main/faded-dream-logo.svg" alt="Faded Dream Logo" width="600"/>

# Faded Dream Dotfiles

> A straightforward [Hyprland](https://github.com/hyprwm/Hyprland) configuration focused on simplicity, compatibility, and daily usability.  
> Built and tested on [Artix Linux](https://artixlinux.org/) (runit) with reliable XWayland support.

</div>

> [!WARNING]
> **🔨 Massive rework in progress.** The current version is stable and fully usable, but the project is being significantly redesigned under the hood. Things may change without notice. If you want something rock-solid right now, use the latest release tag.

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
- **[First-run setup GUI](Faded%20Dream%20welcome%20app/faded-dream-setup.py)** — launches on first login to let you choose your browser, file manager, and optional packages (gaming, peripherals, office, media, comms). Can be re-opened at any time via the startup toggle.
- **[Rofi](https://github.com/davatorium/rofi)** — application launcher
- **[rofimoji](https://github.com/fdw/rofimoji)** — emoji picker with recent history
- **[mpvpaper](https://github.com/GhostNaN/mpvpaper)** — wallpaper support (video and static)
- **[swaync](https://github.com/ErikReider/SwayNotificationCenter)** — notifications
- **Your choice of file manager** — selected at first login via the setup GUI
- **[Catppuccin Macchiato](https://github.com/catppuccin/catppuccin)** — theme across terminal and GTK apps
- **[Oh My Posh](https://ohmyposh.dev/)** — shell prompt with custom `if_tea` theme
- **Designed for daily use** — no fluff, just a setup that works

---

## Environment

| Component | Tool |
|-----------|------|
| Compositor | [Hyprland](https://github.com/hyprwm/Hyprland) |
| Distribution | [Artix Linux](https://artixlinux.org/) *(multi-distro support planned)* |
| Init System | runit |
| Shell | [zsh](https://www.zsh.org/) |
| Prompt | [Oh My Posh](https://ohmyposh.dev/) |
| Terminal | [Kitty](https://github.com/kovidgoyal/kitty) |
| Editor | [Neovim](https://neovim.io/) + [LazyVim](https://www.lazyvim.org/) |
| Launcher | [Rofi](https://github.com/davatorium/rofi) |
| Notifications | [swaync](https://github.com/ErikReider/SwayNotificationCenter) |
| Wallpaper | [mpvpaper](https://github.com/GhostNaN/mpvpaper) / [waypaper](https://github.com/anufrievroman/waypaper) |
| File Manager | chosen at first login via setup GUI |
| Browser | chosen at first login via setup GUI |
| Emoji Picker | [rofimoji](https://github.com/fdw/rofimoji) |
| Theme | [Catppuccin Macchiato](https://github.com/catppuccin/catppuccin) |

---

## Keybinds

| Keybind | Action |
|---------|--------|
| `Super + Enter` | Open terminal (Kitty) |
| `Super + Q` | Close active window |
| `Super + E` | Open file manager (chosen at first login) |
| `Super + B` | Open browser (chosen at first login) |
| `Super + V` | Toggle floating |
| `Super + C` | Open clipboard manager (clipse) |
| `Super + I` | Emoji picker (rofimoji) |
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

> `cat` alias requires `bat` to be installed — handled automatically by `install.sh`

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

## Notes

- On first login after install, the **Faded Dream Setup** GUI launches automatically — pick your browser, file manager, and any optional packages, then hit Install.
- To re-open the setup at any time: `python3 ~/Faded-Dream-dotfiles/Faded\ Dream\ welcome\ app/faded-dream-setup.py`
- Use the startup toggle inside the app to control whether it launches on login
- On first boot after install, PipeWire may take a few seconds to start — this is normal
- `bat` must be installed for the `cat` alias to work — handled automatically by `install.sh`
- The `if_tea` Oh My Posh theme requires the FiraCode Nerd Font to render correctly
- GTK theming is managed via `nwg-look` — run it after first login to apply the theme
- Keyboard layout is set to `us,ro` by default — change `kb_layout` and `kb_variant` in `hyprland.conf` to match your layout

---

## Installation

> Tested on a fresh Artix Linux (runit) install.
```bash
git clone https://github.com/FemBoyGamerTechGuy/Faded-Dream-dotfiles.git ~/Faded-Dream-dotfiles
cd ~/Faded-Dream-dotfiles
chmod +x install.sh
./install.sh
```

The install script handles packages, AUR helper, GPU drivers, dotfile deployment, and shell setup. A reboot is triggered automatically at the end. On first Hyprland login the setup GUI launches to let you choose your browser, file manager, and optional packages. You can re-open it at any time.

---

## Project Structure

```
Faded-Dream-dotfiles/
├── Previews/
│   └── ... (screenshots)
├── Faded Dream welcome app/
│   ├── faded-dream-setup.py
│   ├── packages.py
│   ├── i18n.py
│   └── widgets.py
├── hypr/
│   └── hyprland.conf
├── kitty/
│   ├── kitty.conf
│   └── current-theme.conf
├── waybar laptop/
│   ├── config-laptop.jsonc
│   └── style-laptop.css
├── waybar pc/
│   ├── config-pc.jsonc
│   └── style-pc.css
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
│   ├── Nordic-bluish-accent-v40/
│   └── Sweet-Dark-v40/
├── .icons/
│   ├── ArcDusk-cursors/
│   ├── Papirus/
│   └── default/
├── config.ini for waypaper
├── pacman.conf
└── install.sh
```

---

## Third-Party Credits

The following third-party projects are included or used in Faded-Dream-dotfiles.
They are **not** covered by this repository's GPL v3 license and remain under their own respective licenses.

| Project | License | Source |
|---------|---------|--------|
| zsh-syntax-highlighting | BSD-3 Clause | [github.com/zsh-users/zsh-syntax-highlighting](https://github.com/zsh-users/zsh-syntax-highlighting) |
| zsh-autosuggestions | MIT | [github.com/zsh-users/zsh-autosuggestions](https://github.com/zsh-users/zsh-autosuggestions) |
| Papirus Icon Theme | GPL v3 | [github.com/PapirusDevelopmentTeam/papirus-icon-theme](https://github.com/PapirusDevelopmentTeam/papirus-icon-theme) |
| Oh My Posh | MIT | [github.com/JanDeDobbeleer/oh-my-posh](https://github.com/JanDeDobbeleer/oh-my-posh) |
| Nordic | GPL v3 | [github.com/EliverLara/Nordic](https://github.com/EliverLara/Nordic) |
| FastCat | MIT | [github.com/m3tozz/FastCat](https://github.com/m3tozz/FastCat) |
| ArcDusk-Cursors | GPL v3 | [github.com/yeyushengfan258/ArcDusk-Cursors](https://github.com/yeyushengfan258/ArcDusk-Cursors) |
| Sweet | GPL v3 | [github.com/EliverLara/Sweet](https://github.com/EliverLara/Sweet) |

---

## Contributing

Contributions are welcome! Please read the [CONTRIBUTING.md](CONTRIBUTING.md)
before submitting a pull request.

---

## License

Copyright (C) 2026 FemBoyGamerTechGuy

This project is licensed under the **GNU General Public License v3.0**.
You are free to use, modify, and distribute this project, but any derivative work must also be open source under the same license. Nobody can take this project and release it under a different or proprietary license.

See the [LICENSE](LICENSE) file for the full license text.

---

<div align="center">
<sub>Built with 💜 on Artix Linux</sub>
<br>
<sub>Almost all of this repository was vibe coded with <a href="https://claude.ai">Claude.ai</a></sub>
</div>
