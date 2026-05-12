#!/bin/bash
# [14/14] Icon Themes & Cursors — cloned fresh from source

ICONS_DIR="${HOME}/.icons"
mkdir -p "$ICONS_DIR"

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

# ── Papirus Icon Theme ────────────────────────────────────────────────────────

clone_theme \
    "Papirus Icon Theme" \
    "https://github.com/PapirusDevelopmentTeam/papirus-icon-theme.git" \
    "/tmp/papirus-icon-theme"

if [[ -d "/tmp/papirus-icon-theme/Papirus" ]]; then
    cp -r /tmp/papirus-icon-theme/Papirus           "$ICONS_DIR/"
    cp -r /tmp/papirus-icon-theme/Papirus-Dark      "$ICONS_DIR/" 2>/dev/null || true
    cp -r /tmp/papirus-icon-theme/Papirus-Light     "$ICONS_DIR/" 2>/dev/null || true
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

if [[ -d "/tmp/arcdusk-cursors" ]]; then
    # Run the upstream install script if present, otherwise copy manually
    if [[ -f "/tmp/arcdusk-cursors/install.sh" ]]; then
        bash /tmp/arcdusk-cursors/install.sh && info "ArcDusk Cursors installed via install.sh"
    else
        cp -r /tmp/arcdusk-cursors/ArcDusk-cursors "$ICONS_DIR/" 2>/dev/null || \
        cp -r /tmp/arcdusk-cursors               "$ICONS_DIR/ArcDusk-cursors"
        info "ArcDusk Cursors deployed → $ICONS_DIR"
    fi
    rm -rf /tmp/arcdusk-cursors
else
    warn "ArcDusk Cursors source not found after clone, skipping deploy."
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
