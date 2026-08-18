# Faded Dream Dotfiles — Changelog

All notable changes to this project will be documented here.

---

## [Unreleased]

### Added

- **Arch Linux (systemd) variant** added alongside the existing Artix Linux builds; each now lives in its own self-contained folder under the repo root (`ArchLinux Faded Dream Dotfiles/` and `ArtixLinux Faded Dream Dotfiles/`).
- `packages.py` package classification switched to the Arch package DB — fixes AUR/[extra] sourcing (librewulf, vivaldi, obsidian, warpinator, system-config-printer returned to [extra]; android-tools and superfile corrected).

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
