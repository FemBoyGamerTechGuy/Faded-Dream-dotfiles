#!/bin/bash
# [12/13] Waybar Config Selection

echo ""
echo -e "${BOLD}${CYAN}  Which Waybar layout would you like to use for your device?${RESET}"
echo -e "  1) Laptop  — includes battery and backlight modules"
echo -e "  2) PC      — standard layout"
echo ""
read -rp "  Enter choice [1/2]: " WAYBAR_CHOICE

case "$WAYBAR_CHOICE" in
1)
  info "Laptop Waybar selected — deploying laptop waybar config."
  mkdir -p "${HOME}/.config/waybar"
  cp "$DOTFILES_DIR/waybar laptop/config-laptop.jsonc" "${HOME}/.config/waybar/config.jsonc"
  cp "$DOTFILES_DIR/waybar laptop/style-laptop.css"    "${HOME}/.config/waybar/style.css"
  success "Laptop Waybar config deployed."
  ;;
2)
  info "PC Waybar selected — deploying desktop waybar config."
  mkdir -p "${HOME}/.config/waybar"
  cp "$DOTFILES_DIR/waybar pc/config-pc.jsonc" "${HOME}/.config/waybar/config.jsonc"
  cp "$DOTFILES_DIR/waybar pc/style-pc.css"    "${HOME}/.config/waybar/style.css"
  success "PC Waybar config deployed."
  ;;
*)
  warn "Invalid choice, defaulting to PC Waybar config."
  mkdir -p "${HOME}/.config/waybar"
  cp "$DOTFILES_DIR/waybar pc/config-pc.jsonc" "${HOME}/.config/waybar/config.jsonc"
  cp "$DOTFILES_DIR/waybar pc/style-pc.css"    "${HOME}/.config/waybar/style.css"
  ;;
esac