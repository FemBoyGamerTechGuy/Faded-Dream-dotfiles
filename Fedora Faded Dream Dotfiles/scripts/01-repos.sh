#!/bin/bash
# [1/13] Fedora Repositories
# Enable RPM Fusion, Flathub, and configure DNF

# Backup original dnf config
[[ -f "$DOTFILES_DIR/dnf.conf" ]] || die "dnf.conf not found in dotfiles."
sudo cp /etc/dnf/dnf.conf /etc/dnf/dnf.conf.bak && info "Backed up existing dnf.conf"
sudo cp "$DOTFILES_DIR/dnf.conf" /etc/dnf/dnf.conf

# Enable RPM Fusion free and nonfree
info "Enabling RPM Fusion repositories..."
sudo dnf install -y \
  "https://mirrors.rpmfusion.org/free/fedora/rpmfusion-free-release-$(rpm -E %fedora).noarch.rpm" \
  "https://mirrors.rpmfusion.org/nonfree/fedora/rpmfusion-nonfree-release-$(rpm -E %fedora).noarch.rpm" ||
  die "Failed to enable RPM Fusion repositories."

# Enable COPR repos for additional packages
info "Enabling COPR repositories..."
sudo dnf copr enable -y sneexy/zen-browser || warn "Could not enable sneexy/zen-browser COPR."
sudo dnf copr enable -y sdegler/hyprland || warn "Could not enable sdegler/hyprland COPR."
sudo dnf copr enable -y dejan/lazygit || warn "Could not enable dejan/lazygit COPR."

# Add official third-party browser repositories
info "Adding official browser repositories..."
# LibreWolf
sudo dnf config-manager --add-repo https://repo.librewolf.net/librewolf.repo || warn "Could not add LibreWolf repo."
# Vivaldi
sudo dnf config-manager --add-repo https://repo.vivaldi.com/archive/vivaldi-fedora.repo || warn "Could not add Vivaldi repo."
# Google Chrome
cat <<'EOF' | sudo tee /etc/yum.repos.d/google-chrome.repo > /dev/null
[google-chrome]
name=google-chrome
baseurl=https://dl.google.com/linux/chrome/rpm/stable/x86_64
enabled=1
gpgcheck=1
gpgkey=https://dl.google.com/linux/linux_signing_key.pub
EOF
# Microsoft Edge
cat <<'EOF' | sudo tee /etc/yum.repos.d/microsoft-edge.repo > /dev/null
[microsoft-edge-stable]
name=microsoft-edge-stable
baseurl=https://packages.microsoft.com/yumrepos/edge-stable/
enabled=1
gpgcheck=1
gpgkey=https://packages.microsoft.com/keys/microsoft.asc
EOF

# Enable Flathub
info "Enabling Flathub..."
flatpak remote-add --if-not-exists flathub https://dl.flathub.org/repo/flathub.flatpakrepo ||
  warn "Could not add Flathub remote (flatpak may not be installed yet)."

# Update system
info "Updating system..."
sudo dnf upgrade --refresh -y || die "System upgrade failed."

success "Fedora repositories configured and system updated."