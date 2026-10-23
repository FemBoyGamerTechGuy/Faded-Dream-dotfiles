# Faded Dream — OpenBox (X11) Edition

A port of **[FemBoyGamerTechGuy/Faded-Dream-dotfiles](https://github.com/FemBoyGamerTechGuy/Faded-Dream-dotfiles)** — a Hyprland (Wayland tiler) setup — to **OpenBox** on X11.

This folder is a full variant, self-contained exactly like the Arch/Fedora/Artix folders: it ships the translated window-manager stack (OpenBox, picom, dunst, X11 waybar, helper scripts) **plus** the upstream configs that run on X11 unchanged (kitty, rofi, fastfetch, zsh, waypaper). Its `install.sh` deploys everything and mirrors upstream's installer UX (packages prompt → Waybar PC/laptop choice → deployment → zsh).

## What gets translated vs. reused

| Piece | File | Upstream equivalent |
|---|---|---|
| WM config (keybinds, 10 desktops, mouse, app rules) | `openbox/rc.xml` | `hypr/hyprland.lua` |
| Root menu | `openbox/menu.xml` | rofi / Hyprland binds |
| Startup (picom, waybar, dunst, wallpaper, clipse, polkit) | `openbox/autostart` | `hl.on("hyprland.start")` block |
| Env vars (cursor size/theme, browser) | `openbox/environment` | `hl.env(...)` |
| Window theme (cyan→green gradient titlebar, pink menus) | `themes/Faded-Dream/openbox-3/themerc` | Hyprland border gradient + rofi palette |
| Compositor: blur, 10px rounding, pop-in animations, 80% inactive | `picom/picom.conf` | Hyprland `decoration` + `animations` |
| Bar, PC layout | `waybar pc/config-pc.jsonc` + `style-pc.css` | `waybar pc/*` |
| Bar, laptop layout (battery + backlight) | `waybar laptop/config-laptop.jsonc` + `style-laptop.css` | `waybar laptop/*` |
| Notifications | `dunst/dunstrc` | swaync |
| Scratchpad (special:magic emulator) | `helpers/faded-scratchpad` | Super+S / Super+Shift+S |
| X11 bar helpers | `helpers/faded-workspaces`, `faded-window-title`, `faded-notifications` | hyprland/workspaces, hyprland/window, swaync bell |
| Wallpaper picker | `config.ini for waypaper` (backend=**feh**) | `config.ini for waypaper` (backend=mpvpaper) |
| Terminal / launcher / fetch / shell | `kitty/`, `rofi for .config/`, `rofi for local then share/`, `fastfetch/`, `.zshrc`, `.zsh/` | identical files, X11-compatible |

## Packages (Arch)

`install.sh` offers to install these automatically; here's the full annotated list:

```bash
# Official repos — upstream's list translated to X11
sudo pacman -S --needed \
  openbox picom obconf nwg-look \
  xorg-server xorg-xrandr \
  waybar dunst libnotify \
  xdg-desktop-portal-gtk \
  kitty zsh bat fastfetch btop calcurse neovim wget git \
  rofi flameshot xdotool wmctrl xclip feh \
  brightnessctl playerctl \
  noto-fonts noto-fonts-cjk noto-fonts-emoji ttf-firacode-nerd ttf-jetbrains-mono-nerd \
  polkit polkit-gnome \
  pipewire pipewire-pulse pipewire-alsa wireplumber pavucontrol \
  mpv yt-dlp imagemagick ffmpeg \
  gtk4 libadwaita python-gobject python-cairo \
  chafa unrar unzip p7zip zstd

# AUR (paru/yay) — upstream AUR list translated to X11
paru -S --needed \
  waypaper \
  clipse-bin          # NOT clipse-wayland-bin — the X11 build uses xclip
  rofimoji-git \
  rofi-power-menu     # Waybar ⏻ button + Super+M power menu
  librewolf-bin
```

Notes:
- `picom` must be **v11+** for the `popin` animations block. On older picom, delete the `animations = (...)` block — everything else keeps working.
- **VoidDream** (Super+E file manager) builds from its own repo: <https://github.com/FemBoyGamerTechGuy/VoidDream>
- Upstream's visual stack: **Nordic** / **Sweet** GTK themes, **Papirus** icons, **ArcDusk** cursors — set them with `nwg-look` once installed.
- Upstream never installs `JetBrainsMono Nerd Font` even though the whole bar uses it; this port adds `ttf-jetbrains-mono-nerd` to the list (upstream gap fixed).

## Install

```bash
./install.sh        # prompts: packages? → Waybar PC or laptop? → deploys → zsh
# then log out and pick the "Openbox" session on your display manager
# (or: echo "exec openbox-session" >> ~/.xinitrc && startx)
```

Deployment destinations:

```
~/.config/openbox/{rc.xml,menu.xml,environment,autostart}
~/.themes/Faded-Dream/openbox-3/themerc
~/.config/picom/picom.conf
~/.config/waybar/{config.jsonc,style.css}     ← PC or laptop variant
~/.config/dunst/dunstrc
~/.config/kitty/  ~/.config/rofi/  ~/.local/share/rofi/
~/.config/fastfetch/  ~/.config/waypaper/config.ini
~/.zshrc  ~/.zsh/
~/.local/bin/faded-{scratchpad,workspaces,window-title,notifications}
```

Re-running the installer is safe (overwrites previous copies; back up if you customize).

## Keybind map (upstream → this port)

Everything below matches `hyprland.lua` 1:1 — `Super` is the same Mod4 (`W`), `Alt` the same (`A`):

| Upstream (Hyprland) | OpenBox port | Action |
|---|---|---|
| Super + Enter | `W-Return` | kitty |
| Super + Q | `W-q` | close window |
| Super + E | `W-e` | kitty VoidDream *(needs VoidDream TUI)* |
| Super + B | `W-b` | LibreWolf |
| Super + V | `W-v` | toggle float → **ToggleMaximize** (see notes) |
| Super + C | `W-c` | clipse clipboard manager (kitty `--class clipse`) |
| Super + I | `W-i` | rofimoji emoji picker |
| Super + F | `W-f` | fullscreen |
| Super + W | `W-w` | restart waybar |
| Super + M | `W-m` | **rofi power menu**, fallback `openbox --exit` (upstream: `hyprshutdown` else `hyprctl dispatch exit`) |
| Alt + Space | `A-space` | rofi app launcher (`-show drun -show-icons`) |
| Print | `Print` | region screenshot → **flameshot** |
| Super + ←/→/↑/↓ | `W-arrows` | directional focus |
| Super + 1..0 | `W-1..W-0` | desktops 1–10 |
| Super + Shift + 1..0 | `W-S-1..0` | move window to desktop (follows) |
| Super + S | `W-s` | scratchpad toggle |
| Super + Shift + S | `W-S-s` | stash focused window in scratchpad |
| Super + wheel | `W-wheel` on desktop/frame | desktop cycling (wraps, `e+1`/`e-1`) |
| Super + LMB drag | `W-Left` drag | move window |
| Super + RMB drag | `W-Right` drag | resize window |
| XF86 audio/brightness/media keys | same binds, same `wpctl` / `brightnessctl -e4 -n2` / `playerctl` commands | unchanged from upstream |
| Win + Space | `setxkbmap -layout us,ro -variant ,std -option grp:win_space_toggle` (autostart) | keyboard layout toggle (US↔RO) |

Added X11 conveniences (not upstream): `A-Tab`/`A-S-Tab` window cycling, desktop right/middle-click for root/window-list menus, plain wheel desktop cycling.

## Ported visual mapping

| Hyprland setting | OpenBox/X11 equivalent |
|---|---|
| `col.active_border` gradient `#33CCFF→#00FF99` @45°, `border_size 2` | Faded-Dream theme: **gradient titlebar** (Flat Gradient Diagonal) + solid `#33CCFF` active border, 2px |
| `col.inactive_border` `rgba(595959aa)` | inactive border `#595959` |
| `rounding = 10` | `picom corner-radius = 10` |
| `active_opacity 1.0 / inactive_opacity 0.8` | `picom active-opacity / inactive-opacity` |
| shadow `range 4, render_power 3, rgba(1a1a1aee)` | `picom` shadow (radius 8, `#1a1a1a` @93%) |
| blur `size 3, passes 1, vibrancy 0.1696` | `picom` kawase blur, strength 4 |
| `windows popin 60%` (popIn bezier speed 4 / popOut speed 3) | `picom` v11 `popin 60%`, 250ms overshoot / 333ms decel |
| rofi `rounded-pink-dark` (#212121 / #EC407A / #E6E6E6) | OpenBox menus + dunst styled with the same palette |
| Waybar transparent pills, JetBrainsMono Nerd Font | ported CSS verbatim + X11 module pills |
| `follow_mouse = 1` | `<focus><followMouse>yes</followMouse>` |
| `XCURSOR_SIZE=24` | `openbox/environment` |

## What cannot be ported 1:1 (and how it's handled)

- **Tiling** — OpenBox is a stacking WM. Upstream `Super+P` (pseudo) and `Super+J` (togglesplit) are tiling-only and intentionally unbound. `Super+V` "toggle float" becomes `ToggleMaximize` since windows float by default here (swap in `ToggleDecorations` in `rc.xml` if you prefer a decorations toggle).
- **Gaps (5/20)** — no gaps in a stacking WM; disabled rather than faked.
- **Workspace slide animations** — WM-level on Hyprland; picom covers open/close/minimize pop-in, which is the visually dominant part of the look.
- **Gradient borders** — OpenBox borders are solid color; the gradient lives on the titlebar/handle instead (the most recognizable surface).
- **hyprland/workspaces & hyprland/window modules** — no Hyprland IPC on X11; `faded-workspaces` (pango pager, scroll to switch) and `faded-window-title` fill in, styled as the same pills.
- **swaync → dunst** — the bell emits the same state names (`notification`, `none`, `dnd-*`) in waybar's `alt` field, so upstream's format-icons keep working. Left-click re-shows the last notification; right-click toggles DND (upstream: `swaync-client -d`).
- **hyprshot → flameshot** — region select on Print.
- **waypaper / mpvpaper → feh** — live (mp4) wallpapers are Wayland layer-shell only; on X11 you get static wallpapers. The shipped `config.ini` preselects the feh backend and keeps the upstream wallpaper folder.
- **clipse-wayland-bin → clipse-bin** — the X11 build of clipse uses `xclip` instead of `wl-clipboard`; everything else (the TUI, `-listen` daemon, `kitty --class clipse`) is identical.
- **Scratchpad** — `special:magic` is emulated with a `kitty --class faded-scratchpad` window (undecorated, always-on-top, centered, taskbar-hidden) toggled by `faded-scratchpad`, which also remembers windows you "send" into it.

## Tweaking

- **Keyboard layout**: edit the `setxkbmap` line in `~/.config/openbox/autostart` (upstream default: `us,ro` + `,std` variant, Win+Space toggles).
- **Apps**: `kitty VoidDream` in `rc.xml`/`menu.xml` assumes you have upstream's VoidDream TUI; otherwise replace with `thunar`/`yazi`/your pick.
- **Browser**: `openbox/environment` sets `BROWSER=librewolf`; upstream's welcome app patches `hyprland.lua` instead — on X11 edit this file.
- **Menu/theme edits**: run `openbox --reconfigure` after changing `menu.xml`/`themerc`.
- **Colors**: everything is commented with its upstream source value; grep `#33CCFF`, `#00FF99`, `#EC407A`, `#212121` across the files to re-skin consistently.

## Credits

- Upstream look & design: **FemBoyGamerTechGuy** — [Faded-Dream-dotfiles](https://github.com/FemBoyGamerTechGuy/Faded-Dream-dotfiles) (GPL-licensed; this port references its color values and app set)
- Rofi rounded theme by Newman Sanchez (upstream dependency)
- Catppuccin Macchiato (upstream kitty theme), Nordic / Sweet / Papirus / ArcDusk (upstream visual stack)
