#!/bin/bash
# [7/13] COPR Repositories (Fedora equivalent of AUR helper)
# Enable COPR repositories for packages not in official Fedora/RPM Fusion repos.
# We don't build an AUR helper; we use COPR + Flatpak instead.

info "Enabling COPR repositories for additional packages..."

# COPR repos for packages not in Fedora/RPM Fusion
COPR_REPOS=(
  "solopasha/hyprland"              # Hyprland ecosystem
  "atim/lazygit"                    # lazygit
  "atim/starship"                   # starship (if needed)
  "wezfurlong/wezterm-nightly"      # wezterm (if needed)
)

for repo in "${COPR_REPOS[@]}"; do
  sudo dnf copr enable -y "$repo" || warn "Could not enable COPR repo: $repo"
done

# Refresh metadata after enabling COPR repos
sudo dnf makecache || warn "Failed to refresh DNF cache after enabling COPR repos."

success "COPR repositories enabled."