<div align="center">

<img src="https://github.com/FemBoyGamerTechGuy/Faded-Dream-dotfiles/raw/main/faded-dream-logo.svg" alt="Faded Dream Logo" width="600"/>

# Faded Dream Dotfiles

> A polished, modular [Hyprland](https://github.com/hyprwm/Hyprland) configuration that looks great out of the box and is built to be easy to tweak, extend, or strip down to your taste.
> Built and tested on [Artix Linux](https://artixlinux.org/) with [systemd](https://wiki.archlinux.org/title/Systemd) (Arch) and **runit, openrc, dinit, and s6** (Artix).

</div>

> [!WARNING]
> **🔨 Massive rework in progress.** No release tag yet, but the current `main` branch is stable enough for daily use — install it, run it, it works. Things may still shift under the hood as the rework continues.

---

## Previews

<div align="center">

[![Screenshot 1](https://github.com/FemBoyGamerTechGuy/Faded-Dream-dotfiles/raw/main/Previews/2026-02-22-192101_hyprshot.png)](https://github.com/FemBoyGamerTechGuy/Faded-Dream-dotfiles/blob/main/Previews/2026-02-22-192101_hyprshot.png)
[![Screenshot 2](https://github.com/FemBoyGamerTechGuy/Faded-Dream-dotfiles/raw/main/Previews/2026-02-22-193220_hyprshot.png)](https://github.com/FemBoyGamerTechGuy/Faded-Dream-dotfiles/blob/main/Previews/2026-02-22-193220_hyprshot.png)
[![Screenshot 3](https://github.com/FemBoyGamerTechGuy/Faded-Dream-dotfiles/raw/main/Previews/2026-02-22-193353_hyprshot.png)](https://github.com/FemBoyGamerTechGuy/Faded-Dream-dotfiles/blob/main/Previews/2026-02-22-193353_hyprshot.png)

</div>

---

## Video Demonstration

> Video coming soon.

---

## Features

- **Looks good, stays clean** — polished out of the box with smooth animations, rounded corners, blur, and a cohesive Nord-inspired color palette. Every piece feels intentional, not thrown together.
- **Modular by design** — each part of the config is its own thing. Don't want the emoji picker? Remove one line. Want a different file manager? Change one variable. Nothing is hardwired.
- **Performs great on any hardware** — lightweight and snappy whether you're running it on a low-end laptop with integrated graphics or a full desktop with a dedicated GPU. Broad iGPU and dGPU support built in, including Intel, AMD, and NVIDIA.
- **Multi-init support** — works with **systemd** (Arch Linux) and **runit, openrc, dinit, and s6** (Artix Linux). The install script asks you which one you're using and handles service setup accordingly — no silent defaults, no guessing.
- **Works on PCs and laptops** — laptop-specific packages (TLP, acpid, brightness control, bluetooth) are installed automatically when you select laptop during setup.
- **[First-run setup GUI](Faded%20Dream%20welcome%20app/faded-dream-setup.py)** — launches on first login to let you choose your browser, file manager, and optional packages (gaming, peripherals, office, media, comms). Can be re-opened at any time.
- **Lua-based Hyprland config** — uses the modern `hyprland.lua` format with clean structure and comments throughout. Easy to read, easy to edit.
- **XWayland compatibility** — Xorg apps run smoothly alongside native Wayland apps.

---

## Environment

| Component | Tool |
|-----------|------|
| Compositor | [Hyprland](https://github.com/hyprwm/Hyprland) |
| Distribution | [Artix Linux](https://artixlinux.org/) (dual distro: Arch Linux or Artix Linux) |
| Init System | systemd (Arch) / runit, openrc, dinit, s6 (Artix) |
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
| `Super + F` | Toggle fullscreen |
| `Super + W` | Restart Waybar |
| `Super + M` | Exit Hyprland |
| `Alt + Space` | Open Rofi launcher |
| `Print` | Screenshot region |
| `Super + Arrow keys` | Move focus |
| `Super + [1-0]` | Switch workspace |
| `Super + Shift + [1-0]` | Move window to workspace |
| `Super + S` | Toggle scratchpad |
| `Super + Shift + S` | Move window to scratchpad |

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
- To re-open the setup at any time: `python3 ~/Faded-Dream-dotfiles/ArtixLinux Faded Dream Dotfiles/Faded\ Dream\ welcome\ app/faded-dream-setup.py`
- Use the startup toggle inside the app to control whether it launches on login.
- On first boot after install, PipeWire may take a few seconds to start — this is normal.
- Arch Linux (systemd) and Artix Linux share the same install flow; on systemd the init-system prompt mirrors the Artix options — a systemd-aware branch in `04-device.sh`/`05-permissions.sh` is a planned follow-up.
- `bat` must be installed for the `cat` alias to work — handled automatically by `install.sh`.
- The `if_tea` Oh My Posh theme requires the FiraCode Nerd Font to render correctly.
- GTK theming is managed via `nwg-look` — run it after first login to apply the theme.
- Keyboard layout is set to `us,ro` by default — change `kb_layout` and `kb_variant` in `hyprland.lua` to match your layout.

---

## Installation

> Tested on fresh installs of both Arch Linux (systemd) and Artix Linux (runit, openrc, dinit, s6).

```bash
git clone https://github.com/FemBoyGamerTechGuy/Faded-Dream-dotfiles.git ~/Faded-Dream-dotfiles
cd ~/Faded-Dream-dotfiles/ArtixLinux\ Faded\ Dream\ Dotfiles     # Arch: cd ArchLinux\ Faded\ Dream\ Dotfiles
chmod +x install.sh
./install.sh
```

The install script will ask you which init system you're using, whether you're on a laptop or PC, and handles everything from there — packages, AUR helper, GPU drivers, themes, dotfile deployment, and shell setup. A reboot is triggered automatically at the end. On first Hyprland login the setup GUI launches to let you choose your browser, file manager, and optional packages.

---

## Project Structure

```
Faded-Dream-dotfiles/
|-- ArchLinux Faded Dream Dotfiles/   (systemd variant)
|   |-- install.sh
|   |-- pacman.conf
|   |-- Faded Dream welcome app/
|   |-- scripts/
|   |-- hypr/   kitty/   fastfetch/   .zsh/   .zshrc
|   |-- Previews/   rofi for .config/   rofi for local then share/
|   |   waybar laptop/   waybar pc/   config.ini for waypaper   faded-dream-logo.svg
|-- ArtixLinux Faded Dream Dotfiles/   (runit / openrc / dinit / s6 variant)
|   |-- (same self-contained layout as the Arch folder above)
|-- README.md        CHANGELOG.md      LICENSE      CONTRIBUTING.md
`-- .git/
```

---

## Third-Party Credits

The following third-party projects are included or used in Faded-Dream-dotfiles.
They are **not** covered by this repository's GPL v3 license and remain under their own respective licenses.

| Project | License | Source |
|---------|---------|--------|
| zsh-syntax-highlighting | BSD-3 Clause | [github.com/zsh-users/zsh-syntax-highlighting](https://github.com/zsh-users/zsh-syntax-highlighting) |
| zsh-autosuggestions | MIT | [github.com/zsh-users/zsh-autosuggestions](https://github.com/zsh-users/zsh-autosuggestions) |
| Oh My Posh | MIT | [github.com/JanDeDobbeleer/oh-my-posh](https://github.com/JanDeDobbeleer/oh-my-posh) |
| FastCat | MIT | [github.com/m3tozz/FastCat](https://github.com/m3tozz/FastCat) |

---

## Contributing

Contributions are welcome! Please read the [CONTRIBUTING.md](CONTRIBUTING.md) before submitting a pull request.

---

## License

Copyright (C) 2026 FemBoyGamerTechGuy

This project is licensed under the **GNU General Public License v3.0**.
You are free to use, modify, and distribute this project, but any derivative work must also be open source under the same license. Nobody can take this project and release it under a different or proprietary license.

See the [LICENSE](LICENSE) file for the full license text.

---

<div align="center">
<sub>Built with 💜 on Arch Linux and Artix Linux</sub>
<br>
<sub>Almost all of this repository was vibe coded with <a href="https://claude.ai">Claude.ai</a></sub>
</div>
