### Status

> ⚠️ **UNTESTED / WORK IN PROGRESS**
> 
> The Fedora implementation is complete on paper but **has not been tested on actual Fedora hardware**. Known gaps:
> - Custom COPR repo name is a placeholder (`yourusername/faded-dream`)
> - Package availability in COPR/Fedora not fully verified
> - Installer flow, GPU detection, welcome app untested
> - Nvidia 580xx branch depends on RPM Fusion Nonfree having the packages
> - Need manual testing on Fedora 44/45

---

## [Released] — 2026-08-19
# Faded Dream Dotfiles — Changelog

All notable changes to this project will be documented here.

---

## [Released] — 2026-08-19

### Fixed

- **Faded Dream welcome screen not launching on login (both ArchLinux & ArtixLinux)**
  The `hyprland.lua` autostart handler was pointing to `$HOME/Faded-Dream-dotfiles/Faded Dream welcome app/faded-dream-setup.py`, but the welcome app lives inside the distribution-specific subdirectory (`ArchLinux Faded Dream Dotfiles/` or `ArtixLinux Faded Dream Dotfiles/`). Fixed the path in both `hyprland.lua` files to include the correct subdirectory, so the sentinel-triggered welcome screen now launches on first login.
  _Files:_ `ArchLinux Faded Dream Dotfiles/hypr/hyprland.lua`, `ArtixLinux Faded Dream Dotfiles/hypr/hyprland.lua`

- **Waybar not autostarting on ArchLinux**
  With the removal of `pipewire.sh` from the ArchLinux install, waybar lost its autostart. Added `hl.exec_cmd("waybar &")` to the `hyprland.start` autostart block in the ArchLinux `hyprland.lua`. PipeWire itself remains managed by systemd user units on Arch, so no manual launch is needed.
  _File:_ `ArchLinux Faded Dream Dotfiles/hypr/hyprland.lua`

- **Stale comment in faded-dream-setup.py pointing to wrong directory (both ArchLinux & ArtixLinux)**
  The `# Lives in ~/Faded-Dream-dotfiles/...` header comment was updated to reflect the actual repo subdirectory path.
  _Files:_ `ArchLinux Faded Dream Dotfiles/Faded Dream welcome app/faded-dream-setup.py`, `ArtixLinux Faded Dream Dotfiles/Faded Dream welcome app/faded-dream-setup.py`

### Removed

- **pipewire.sh autostart script creation removed from ArchLinux install**
  The `13-dotfiles.sh` script was generating `~/.config/autostart/pipewire.sh` on ArchLinux, but on systemd-based Arch the PipeWire daemons are already started by user units. Removed the heredoc block and `chmod`/`success` lines from the ArchLinux `13-dotfiles.sh` only. The ArtixLinux variant retains `pipewire.sh` creation, since Artix uses OpenRC/runit and still relies on it to start both PipeWire and waybar.
  _File:_ `ArchLinux Faded Dream Dotfiles/scripts/13-dotfiles.sh`

### Fixed

- **Nvidia 580xx drivers failing to install on Arch Linux**
  The `08-gpu.sh` script (option 3 — GTX 1080 Ti / GTX 1010) was installing all `580xx` packages via `sudo pacman`, but these are AUR-only on Arch Linux (official support dropped for pre-GTX1650 cards). `pacman` could not resolve them, causing a fatal error under `set -euo pipefail` that aborted the entire dotfiles installation. Switched the `580xx` package install from `pacman` to `paru` (the AUR helper built in step `07-aur.sh`, which runs immediately before this script). `dkms` and kernel headers remain on `pacman` as they are still official-repo packages.
  _File:_ `ArchLinux Faded Dream Dotfiles/scripts/08-gpu.sh`

### Removed

- **Pipewire autostart line removed from hyprland.lua (ArchLinux only)**
  `hl.exec_cmd("~/.config/autostart/pipewire.sh")` was removed from the Autostart block. On Arch Linux pipewire is now managed by the system directly, so the manual invocation is no longer needed. The ArtixLinux variant retains the line until an alternative solution is found.
  _File:_ `ArchLinux Faded Dream Dotfiles/hypr/hyprland.lua`

---

## [Released] — 2026-08-18

### Added

- **Arch Linux (systemd) variant** added alongside the existing Artix Linux builds; each now lives in its own self-contained folder under the repo root (`ArchLinux Faded Dream Dotfiles/` and `ArtixLinux Faded Dream Dotfiles/`).
- `packages.py` package classification switched to the Arch package DB — fixes AUR/[extra] sourcing (librewulf, vivaldi, obsidian, warpinator, system-config-printer returned to [extra]; android-tools and superfile corrected).

### Removed

- **KOCMOC welcome-app easter-egg** removed. Typing `KOCMOC` used to stream a YouTube video (`https://www.youtube.com/watch?v=eMDu1byE45A`) via `yt-dlp` piped into `mpv`, but the stream fetch returned **HTTP 403 Forbidden** for this video/network (`yt-dlp -g` resolved, but the data fetch failed in both `yt-dlp -o -` and `mpv`), so the video never opened. `yt-dlp` and `mpv` are not part of the default package set, so they would have to be installed manually regardless.
  _Files:_ `Faded Dream welcome app/faded-dream-setup.py` (`ArchLinux Faded Dream Dotfiles/` and `ArtixLinux Faded Dream Dotfiles/`)

---

## [Released] — 2026-05-13

### Fixed

- **Startup toggle writing invalid syntax to hyprland.lua**
  The welcome app toggle was appending a raw `exec-once = ...` line (old `.conf` syntax) to the Lua config, causing a syntax error on line 238. Fixed by updating `EXEC_LINE` in `packages.py` to proper Lua `hl.exec_cmd(...)` syntax, and rewriting the toggle logic to insert/remove the line inside the `hl.on("hyprland.start", ...)` block instead of appending to the end of the file.
  _Files:_ `Faded Dream welcome app/packages.py`, `Faded Dream welcome app/faded-dream-setup.py`, `hypr/hyprland.lua`

- **Cursor theme not applying (ArcDusk)**
  The `14-themes.sh` script was looking for the wrong folder structure in the ArcDusk repo. Fixed to correctly copy from `dist/cursors/` and `dist/index.theme` into `~/.icons/ArcDusk-cursors/`.
  _File:_ `scripts/14-themes.sh`

- **Init system defaulting to runit silently**
  `04-device.sh` was reading from a cache file and falling back to runit if not found. Removed the autodetect entirely — the user is now prompted to pick their init system explicitly. `05-permissions.sh` updated to read from the cache written by `04-device.sh` and exit cleanly if missing.
  _Files:_ `scripts/04-device.sh`, `scripts/05-permissions.sh`

### Changed

- **Bundled `.icons` and `.themes` replaced with cloned sources**
  Removed the 43k+ SVG Papirus icon files and bundled GTK themes from the repo. A new script `14-themes.sh` now clones them fresh from their official repos at install time: Papirus (base only), Nordic v40 variants, Sweet Dark v40, and ArcDusk Cursors.
  _Files:_ `scripts/13-dotfiles.sh`, `scripts/14-themes.sh`, `install.sh`

- **Removed gtk configs and .themes from dotfile deployment**
  GTK theme files are now handled entirely by `14-themes.sh` so the deploy lines for `gtk configs/` and `.themes` have been removed from `13-dotfiles.sh`.
  _File:_ `scripts/13-dotfiles.sh`

---

## [Released] — 2026-05-12

### Fixed

- **File Manager — unable to patch on install**
  The welcome setup app was failing to update `local fileManager` in the Hyprland config because the `sed` pattern didn't account for the extra whitespace around the `=` in the Lua file. Pattern updated to use `[[:space:]]*` to match any spacing.
  _File:_ `Faded Dream welcome app/faded-dream-setup.py`

### Changed

- **Hyprland config migrated from `.conf` to `.lua`**
  Hyprland now uses a Lua-based config (`hypr/hyprland.lua`) instead of the old `hypr/hyprland.conf`. The welcome setup app has been updated in two places to reflect this:

  - `HYPRLAND_CONF` path updated from `~/.config/hypr/hyprland.conf` → `~/.config/hypr/hyprland.lua`
  - Browser patch `sed` pattern updated from `$Browser = ...` (conf syntax) → `local browser = "..."` (Lua syntax)
  - File manager patch `sed` pattern updated from `$fileManager = ...` (conf syntax) → `local fileManager = "..."` (Lua syntax)

  _Files:_ `Faded Dream welcome app/packages.py`, `Faded Dream welcome app/faded-dream-setup.py`
