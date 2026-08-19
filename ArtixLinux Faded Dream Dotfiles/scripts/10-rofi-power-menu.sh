#!/bin/bash
# [10/13] Rofi Power Menu

POWER_MENU_TMP=$(mktemp -d)

git clone --branch master \
  https://github.com/FemBoyGamerTechGuy/rofi-power-menu-for-non-systemd-users.git \
  "$POWER_MENU_TMP/rofi-power-menu" ||
  die "Failed to clone rofi-power-menu."

PKGBUILD_DIR="$POWER_MENU_TMP/rofi-power-menu/rofi-power-menu-PKG"

[[ -d "$PKGBUILD_DIR" ]] || die "rofi-power-menu-PKG folder not found in repo."
[[ -f "$PKGBUILD_DIR/PKGBUILD" ]] || die "PKGBUILD not found in rofi-power-menu-PKG."

(cd "$PKGBUILD_DIR" && makepkg -si --noconfirm) ||
  die "Failed to build rofi-power-menu."

rm -rf "$POWER_MENU_TMP"
success "rofi-power-menu installed."
