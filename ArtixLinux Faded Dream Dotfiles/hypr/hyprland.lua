-- =====================================================================================
-- Faded Dream — Hyprland Lua Configuration
-- https://wiki.hypr.land/Configuring/
-- =====================================================================================

-- ── Programs ──────────────────────────────────────────────────────────────────────────

local terminal      = "kitty"
local fileManager   = "kitty VoidDream"
local menu          = "rofi -show drun -show-icons"
local emojilauncher = "rofimoji -a copy"
local mainMod       = "SUPER"

-- Default browser — auto-patched by faded-dream-setup on first login.
-- To change manually: edit the line below or re-run the setup app.
local browser = "librewolf"

-- ── Monitors ──────────────────────────────────────────────────────────────────────────

hl.monitor({
    output   = "",
    mode     = "preferred",
    position = "auto",
    scale    = "auto",
})

-- ── Environment Variables ─────────────────────────────────────────────────────────────

hl.env("XCURSOR_SIZE",   "24")
hl.env("HYPRCURSOR_SIZE","24")

-- ── Autostart ─────────────────────────────────────────────────────────────────────────

hl.on("hyprland.start", function()
    hl.exec_cmd("/usr/lib/polkit-gnome/polkit-gnome-authentication-agent-1")
    hl.exec_cmd("~/.config/autostart/pipewire.sh")
    hl.exec_cmd("waypaper --restore")
    hl.exec_cmd("clipse -listen")
    hl.exec_cmd("/usr/lib/xdg-desktop-portal-gtk")

    -- First-run setup — controlled by sentinel file ~/.config/faded-dream-autostart
    hl.exec_cmd("bash -c '[ -f \"$HOME/.config/faded-dream-autostart\" ] && [ -f \"$HOME/Faded-Dream-dotfiles/ArtixLinux Faded Dream Dotfiles/Faded Dream welcome app/faded-dream-setup.py\" ] && python3 \"$HOME/Faded-Dream-dotfiles/ArtixLinux Faded Dream Dotfiles/Faded Dream welcome app/faded-dream-setup.py\"'")
end)

-- ── Look and Feel ─────────────────────────────────────────────────────────────────────

hl.config({
    general = {
        gaps_in          = 5,
        gaps_out         = 20,
        border_size      = 2,
        resize_on_border = false,
        allow_tearing    = true,

        col = {
            active_border   = { colors = { "rgba(33ccffee)", "rgba(00ff99ee)" }, angle = 45 },
            inactive_border = "rgba(595959aa)",
        },
    },

    decoration = {
        rounding         = 10,
        rounding_power   = 2,
        active_opacity   = 1.0,
        inactive_opacity = 0.8,

        shadow = {
            enabled      = true,
            range        = 4,
            render_power = 3,
            color        = "rgba(1a1a1aee)",
        },

        blur = {
            enabled  = true,
            size     = 3,
            passes   = 1,
            vibrancy = 0.1696,
        },
    },

    animations = {
        enabled = true,
    },

    misc = {
        force_default_wallpaper = 0,
        disable_hyprland_logo   = true,
    },
})

-- ── Animations ────────────────────────────────────────────────────────────────────────

--         NAME          X0      Y0     X1     Y1
hl.curve("popIn",       { type = "bezier", points = { { 0.34, 1.56 }, { 0.64,  1     } } })
hl.curve("popOut",      { type = "bezier", points = { { 0.36, 0    }, { 0.66, -0.56  } } })
hl.curve("smoothSlide", { type = "bezier", points = { { 0.25, 1    }, { 0.5,   1     } } })

--                        NAME               ENABLED  SPEED  CURVE         STYLE
hl.animation({ leaf = "global",        enabled = true,  speed = 10,  bezier = "default"     })
hl.animation({ leaf = "border",        enabled = true,  speed = 5,   bezier = "smoothSlide" })

hl.animation({ leaf = "windows",       enabled = true,  speed = 4,   bezier = "popIn",       style = "popin 60%" })
hl.animation({ leaf = "windowsIn",     enabled = true,  speed = 4,   bezier = "popIn",       style = "popin 60%" })
hl.animation({ leaf = "windowsOut",    enabled = true,  speed = 3,   bezier = "popOut",      style = "popin 60%" })

hl.animation({ leaf = "fade",          enabled = true,  speed = 3,   bezier = "smoothSlide" })
hl.animation({ leaf = "fadeIn",        enabled = true,  speed = 3,   bezier = "smoothSlide" })
hl.animation({ leaf = "fadeOut",       enabled = true,  speed = 2,   bezier = "smoothSlide" })
hl.animation({ leaf = "layers",        enabled = true,  speed = 3,   bezier = "smoothSlide" })
hl.animation({ leaf = "layersIn",      enabled = true,  speed = 3,   bezier = "smoothSlide" })
hl.animation({ leaf = "fadeLayersIn",  enabled = true,  speed = 2,   bezier = "smoothSlide" })
hl.animation({ leaf = "fadeLayersOut", enabled = true,  speed = 2,   bezier = "smoothSlide" })

hl.animation({ leaf = "workspaces",    enabled = true,  speed = 5,   bezier = "popIn",       style = "slide" })
hl.animation({ leaf = "workspacesIn",  enabled = true,  speed = 5,   bezier = "popIn",       style = "slide" })
hl.animation({ leaf = "workspacesOut", enabled = true,  speed = 4,   bezier = "popOut",      style = "slide" })

-- ── Layouts ───────────────────────────────────────────────────────────────────────────

hl.config({
    dwindle = {
        preserve_split = true,
    },
})

-- ── Input ─────────────────────────────────────────────────────────────────────────────

hl.config({
    input = {
        kb_layout  = "us,ro",              -- Change to fit your needs
        kb_variant = ",std",               -- Change to fit your needs
        kb_model   = "",
        kb_options = "grp:win_space_toggle",
        kb_rules   = "",

        follow_mouse = 1,
        sensitivity  = 0,                  -- -1.0 to 1.0, 0 = no modification

        touchpad = {
            natural_scroll = false,
        },
    },
})

-- ── Keybindings ───────────────────────────────────────────────────────────────────────

-- — Apps
hl.bind(mainMod .. " + return", hl.dsp.exec_cmd(terminal))
hl.bind(mainMod .. " + E",      hl.dsp.exec_cmd(fileManager))
hl.bind(mainMod .. " + B",      hl.dsp.exec_cmd(browser))
hl.bind("ALT + space",          hl.dsp.exec_cmd(menu))
hl.bind(mainMod .. " + C",      hl.dsp.exec_cmd("kitty --class clipse -e 'clipse'"))
hl.bind("PRINT",                hl.dsp.exec_cmd("hyprshot -m region"))
hl.bind(mainMod .. " + I",      hl.dsp.exec_cmd(emojilauncher))
hl.bind(mainMod .. " + F",      hl.dsp.window.fullscreen())

-- — Window management
hl.bind(mainMod .. " + Q", hl.dsp.window.close())
hl.bind(mainMod .. " + V", hl.dsp.window.float({ action = "toggle" }))
hl.bind(mainMod .. " + P", hl.dsp.window.pseudo())
hl.bind(mainMod .. " + J", hl.dsp.layout("togglesplit"))
hl.bind(mainMod .. " + M", hl.dsp.exec_cmd("command -v hyprshutdown >/dev/null 2>&1 && hyprshutdown || hyprctl dispatch exit"))
hl.bind(mainMod .. " + W", hl.dsp.exec_cmd("pkill waybar || waybar &"))

-- — Focus
hl.bind(mainMod .. " + left",  hl.dsp.focus({ direction = "left"  }))
hl.bind(mainMod .. " + right", hl.dsp.focus({ direction = "right" }))
hl.bind(mainMod .. " + up",    hl.dsp.focus({ direction = "up"    }))
hl.bind(mainMod .. " + down",  hl.dsp.focus({ direction = "down"  }))

-- — Workspaces
for i = 1, 9 do
    hl.bind(mainMod .. " + " .. i,           hl.dsp.focus({ workspace = i }))
    hl.bind(mainMod .. " + SHIFT + " .. i,   hl.dsp.window.move({ workspace = i }))
end
hl.bind(mainMod .. " + 0",         hl.dsp.focus({ workspace = 10 }))
hl.bind(mainMod .. " + SHIFT + 0", hl.dsp.window.move({ workspace = 10 }))

-- — Scratchpad
hl.bind(mainMod .. " + S",         hl.dsp.workspace.toggle_special("magic"))
hl.bind(mainMod .. " + SHIFT + S", hl.dsp.window.move({ workspace = "special:magic" }))

-- — Mouse
hl.bind(mainMod .. " + mouse_down", hl.dsp.focus({ workspace = "e+1" }))
hl.bind(mainMod .. " + mouse_up",   hl.dsp.focus({ workspace = "e-1" }))
hl.bind(mainMod .. " + mouse:272",  hl.dsp.window.drag(),   { mouse = true })
hl.bind(mainMod .. " + mouse:273",  hl.dsp.window.resize(), { mouse = true })

-- — Volume
hl.bind("XF86AudioRaiseVolume", hl.dsp.exec_cmd("wpctl set-volume -l 1 @DEFAULT_AUDIO_SINK@ 5%+"), { locked = true, repeating = true })
hl.bind("XF86AudioLowerVolume", hl.dsp.exec_cmd("wpctl set-volume @DEFAULT_AUDIO_SINK@ 5%-"),      { locked = true, repeating = true })
hl.bind("XF86AudioMute",        hl.dsp.exec_cmd("wpctl set-mute @DEFAULT_AUDIO_SINK@ toggle"),     { locked = true, repeating = true })
hl.bind("XF86AudioMicMute",     hl.dsp.exec_cmd("wpctl set-mute @DEFAULT_AUDIO_SOURCE@ toggle"),   { locked = true, repeating = true })

-- — Brightness
hl.bind("XF86MonBrightnessUp",   hl.dsp.exec_cmd("brightnessctl -e4 -n2 set 5%+"), { locked = true, repeating = true })
hl.bind("XF86MonBrightnessDown", hl.dsp.exec_cmd("brightnessctl -e4 -n2 set 5%-"), { locked = true, repeating = true })

-- — Media
hl.bind("XF86AudioNext",  hl.dsp.exec_cmd("playerctl next"),        { locked = true })
hl.bind("XF86AudioPrev",  hl.dsp.exec_cmd("playerctl previous"),    { locked = true })
hl.bind("XF86AudioPlay",  hl.dsp.exec_cmd("playerctl play-pause"),  { locked = true })
hl.bind("XF86AudioPause", hl.dsp.exec_cmd("playerctl play-pause"),  { locked = true })

-- ── Window Rules ──────────────────────────────────────────────────────────────────────

hl.window_rule({
    name           = "suppress-maximize-events",
    match          = { class = ".*" },
    suppress_event = "maximize",
})

hl.window_rule({
    name  = "fix-xwayland-drags",
    match = {
        class      = "^$",
        title      = "^$",
        xwayland   = true,
        float      = true,
        fullscreen = false,
        pin        = false,
    },
    no_focus = true,
})

hl.window_rule({
    name  = "move-hyprland-run",
    match = { class = "hyprland-run" },
    move  = "20 monitor_h-120",
    float = true,
})

