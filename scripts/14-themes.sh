#!/bin/bash
# [14/14] Icon Themes & Cursors — cloned fresh from source

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

clone_theme \
    "Nordic GTK Theme" \
    "https://github.com/EliverLara/Nordic.git" \
    "/tmp/nordic-theme"

if [[ -d "/tmp/nordic-theme" ]]; then
    # Copy v40 variants
    for variant in Nordic-v40 Nordic-darker-v40 Nordic-bluish-accent-v40 \
                   Nordic-standard-buttons-v40 Nordic-darker-standard-buttons-v40; do
        [[ -d "/tmp/nordic-theme/$variant" ]] && \
            cp -r "/tmp/nordic-theme/$variant" "$THEMES_DIR/" && \
            info "Deployed $variant → $THEMES_DIR"
    done
    rm -rf /tmp/nordic-theme
else
    warn "Nordic source not found after clone, skipping."
fi

# ── Sweet Dark GTK Theme (v40) ────────────────────────────────────────────────

clone_theme \
    "Sweet Dark GTK Theme" \
    "https://github.com/EliverLara/Sweet.git" \
    "/tmp/sweet-theme"

if [[ -d "/tmp/sweet-theme" ]]; then
    for variant in Sweet-Dark-v40 Sweet-v40; do
        [[ -d "/tmp/sweet-theme/$variant" ]] && \
            cp -r "/tmp/sweet-theme/$variant" "$THEMES_DIR/" && \
            info "Deployed $variant → $THEMES_DIR"
    done
    rm -rf /tmp/sweet-theme
else
    warn "Sweet source not found after clone, skipping."
fi

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
