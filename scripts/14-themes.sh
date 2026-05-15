#!/bin/bash
# [14/14] Icon Themes & Cursors — cloned fresh from source

# ── Standalone helpers (no need to source install.sh) ─────────────────────────

BOLD="\e[1m"
RESET="\e[0m"
GREEN="\e[32m"
YELLOW="\e[33m"
CYAN="\e[36m"

info()    { echo -e "  ${CYAN}${BOLD}info:${RESET}  $*"; }
warn()    { echo -e "  ${YELLOW}${BOLD}warn:${RESET}  $*"; }
success() { echo -e "  ${GREEN}${BOLD}done:${RESET}  $*"; }

ICONS_DIR="${HOME}/.icons"
THEMES_DIR="${HOME}/.themes"
mkdir -p "$ICONS_DIR" "$THEMES_DIR"

# ── Helper ────────────────────────────────────────────────────────────────────

clone_theme() {
    local name="$1"
    local repo="$2"
    local dest="$3"

    if [[ -d "$dest" ]]; then
        info "$name already exists, pulling latest..."
        git -C "$dest" pull --ff-only && info "$name updated." || warn "$name update failed, skipping."
    else
        info "Cloning $name..."
        git clone --depth=1 "$repo" "$dest" && info "$name installed → $dest" || warn "$name clone failed."
    fi
}

# ── Nordic GTK Theme (v40) ────────────────────────────────────────────────────

info "Downloading Nordic GTK Theme v2.2.0..."
wget -q "https://github.com/EliverLara/Nordic/releases/download/v2.2.0/Nordic-bluish-accent-v40.tar.xz" \
    -O /tmp/Nordic-bluish-accent-v40.tar.xz && \
    tar -xf /tmp/Nordic-bluish-accent-v40.tar.xz -C "$THEMES_DIR/" && \
    rm /tmp/Nordic-bluish-accent-v40.tar.xz && \
    info "Nordic deployed → $THEMES_DIR/Nordic-bluish-accent-v40" || \
    warn "Nordic download failed."

# ── Sweet Dark GTK Theme (v40) ────────────────────────────────────────────────

info "Downloading Sweet Dark GTK Theme v6.0..."
wget -q "https://github.com/EliverLara/Sweet/releases/download/v6.0/Sweet-Dark-v40.tar.xz" \
    -O /tmp/Sweet-Dark-v40.tar.xz && \
    tar -xf /tmp/Sweet-Dark-v40.tar.xz -C "$THEMES_DIR/" && \
    rm /tmp/Sweet-Dark-v40.tar.xz && \
    info "Sweet Dark deployed → $THEMES_DIR/Sweet-Dark-v40" || \
    warn "Sweet Dark download failed."

success "GTK themes deployed."

# ── Papirus Icon Theme ────────────────────────────────────────────────────────

clone_theme \
    "Papirus Icon Theme" \
    "https://github.com/PapirusDevelopmentTeam/papirus-icon-theme.git" \
    "/tmp/papirus-icon-theme"

if [[ -d "/tmp/papirus-icon-theme/Papirus" ]]; then
    cp -r /tmp/papirus-icon-theme/Papirus "$ICONS_DIR/"
    rm -rf /tmp/papirus-icon-theme
    info "Papirus icons deployed → $ICONS_DIR"
else
    warn "Papirus source not found after clone, skipping deploy."
fi

# ── ArcDusk Cursors ───────────────────────────────────────────────────────────

clone_theme \
    "ArcDusk Cursors" \
    "https://github.com/yeyushengfan258/ArcDusk-Cursors.git" \
    "/tmp/arcdusk-cursors"

if [[ -d "/tmp/arcdusk-cursors/dist" ]]; then
    mkdir -p "$ICONS_DIR/ArcDusk-cursors"
    cp -r /tmp/arcdusk-cursors/dist/cursors  "$ICONS_DIR/ArcDusk-cursors/cursors"
    cp    /tmp/arcdusk-cursors/dist/index.theme "$ICONS_DIR/ArcDusk-cursors/index.theme"
    rm -rf /tmp/arcdusk-cursors
    info "ArcDusk Cursors deployed → $ICONS_DIR/ArcDusk-cursors"
else
    warn "ArcDusk Cursors dist/ not found after clone, skipping deploy."
fi

# ── Set default cursor ────────────────────────────────────────────────────────

mkdir -p "$ICONS_DIR/default"
cat > "$ICONS_DIR/default/index.theme" <<EOF
[Icon Theme]
Name=ArcDusk-cursors
Inherits=ArcDusk-cursors
EOF
info "Default cursor set to ArcDusk-cursors"

success "Themes & cursors installed."

# ── Apply GTK theme via gsettings + nwg-look ──────────────────────────────────
# Seed gsettings with the default theme so nwg-look has something to apply.
# After first login the user can open nwg-look, pick any theme, hit Apply,
# and it will work correctly from that point forward without any config files.

info "Seeding default GTK theme into gsettings..."

gsettings set org.gnome.desktop.interface gtk-theme    'Nordic-bluish-accent-v40'
gsettings set org.gnome.desktop.interface icon-theme   'Papirus'
gsettings set org.gnome.desktop.interface cursor-theme 'ArcDusk-cursors'
gsettings set org.gnome.desktop.interface cursor-size  24
gsettings set org.gnome.desktop.interface font-name    'Sans 10'

# Export the gsettings values to all GTK config files (gtk-3.0, gtk-4.0,
# .gtkrc-2.0) so apps that read files instead of dconf also get the theme.
nwg-look -x

success "GTK theme seeded and exported. Use nwg-look to change it anytime."
