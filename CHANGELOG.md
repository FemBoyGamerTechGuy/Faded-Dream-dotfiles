# Faded Dream Dotfiles — Changelog

All notable changes to this project will be documented here.

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

  _Files changed:_
  - `Faded Dream welcome app/packages.py`
  - `Faded Dream welcome app/faded-dream-setup.py`
