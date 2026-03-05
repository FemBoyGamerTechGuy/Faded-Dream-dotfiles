#!/usr/bin/env python3
# =============================================================================
# Faded Dream — First Run Setup  (GTK4 + libadwaita)
# Ported from PyQt6 · sidebar nav · animated checkmarks · shimmer · glow
# Lives in ~/Faded-Dream-dotfiles/faded-dream-setup.py
# Launched via exec-once in hyprland.conf on first login.
# dep: sudo pacman -S python-gobject gtk4 libadwaita
# Easter egg: type KOCMOC
# =============================================================================

import sys, os, subprocess, threading, math, random, cairo

import gi
gi.require_version("Gtk",  "4.0")
gi.require_version("Adw",  "1")
from gi.repository import Gtk, Adw, GLib, Gio, Pango, Gdk, GObject

# ── Package data ──────────────────────────────────────────────────────────────
BROWSERS = [
    {"pkg":"librewolf",                 "exec":"librewolf",             "name":"LibreWolf",
     "desc":"Privacy-focused Firefox fork — no telemetry, hardened",
     "icon":"🦊","repo":"galaxy","aur":False,"recommended":True},
    {"pkg":"zen-browser-bin",           "exec":"zen-browser",           "name":"Zen Browser",
     "desc":"Beautiful Firefox-based browser with a modern UI",
     "icon":"🧘","repo":"AUR",   "aur":True, "recommended":False},
    {"pkg":"firefox",                   "exec":"firefox",               "name":"Firefox",
     "desc":"Mozilla's open source browser",
     "icon":"🔥","repo":"galaxy","aur":False,"recommended":False},
    {"pkg":"vivaldi",                   "exec":"vivaldi",               "name":"Vivaldi",
     "desc":"Feature-rich Chromium browser",
     "icon":"🎻","repo":"extra", "aur":False,"recommended":False},
    {"pkg":"google-chrome",             "exec":"google-chrome-stable",  "name":"Google Chrome",
     "desc":"Google's browser",
     "icon":"🌐","repo":"AUR",   "aur":True, "recommended":False},
    {"pkg":"microsoft-edge-stable-bin", "exec":"microsoft-edge-stable", "name":"Microsoft Edge",
     "desc":"Microsoft's Chromium browser",
     "icon":"🔷","repo":"AUR",   "aur":True, "recommended":False},
]

GAMING = [
    {"section":"Launchers","packages":[
        {"pkg":"steam",                     "name":"Steam",
         "desc":"Valve game platform","icon":"🎮","repo":"lib32","aur":False,"sub":[]},
        {"pkg":"heroic-games-launcher-bin", "name":"Heroic",
         "desc":"Epic &amp; GOG launcher","icon":"🦸","repo":"AUR","aur":True,"sub":[]},
    ]},
    {"section":"Compatibility","packages":[
        {"pkg":"wine","name":"Wine","desc":"Windows compatibility layer",
         "icon":"🍷","repo":"world","aur":False,"sub":[
            {"pkg":"winetricks","name":"Winetricks","repo":"world","aur":False},
            {"pkg":"wine-mono", "name":"Wine Mono", "repo":"extra","aur":False},
            {"pkg":"wine-gecko","name":"Wine Gecko","repo":"extra","aur":False},
        ]},
        {"pkg":"protonplus","name":"ProtonPlus","desc":"Proton version manager GUI",
         "icon":"⚗️","repo":"AUR","aur":True,"sub":[]},
    ]},
    {"section":"Performance","packages":[
        {"pkg":"gamemode","name":"GameMode","desc":"CPU/GPU performance optimizer",
         "icon":"⚡","repo":"world","aur":False,"sub":[
            {"pkg":"lib32-gamemode","name":"GameMode (32-bit)","repo":"lib32","aur":False},
        ]},
        {"pkg":"mangohud","name":"MangoHud","desc":"In-game FPS/stats overlay",
         "icon":"📊","repo":"world","aur":False,"sub":[
            {"pkg":"lib32-mangohud","name":"MangoHud (32-bit)","repo":"multilib","aur":False},
        ]},
        {"pkg":"mangojuice","name":"MangoJuice","desc":"GUI configurator for MangoHud",
         "icon":"🥭","repo":"AUR","aur":True,"sub":[]},
    ]},
]

LANG_LIST = [
    ("🇬🇧","English UK"),  ("🇷🇴","Romanian"),           ("🇫🇷","French"),    ("🇩🇪","German"),
    ("🇪🇸","Spanish"),     ("🇮🇹","Italian"),             ("🇵🇹","Portuguese"), ("🇷🇺","Russian"),
    ("🇯🇵","Japanese"),    ("🇨🇳","Chinese (Simplified)"), ("🇰🇷","Korean"),    ("🇸🇦","Arabic"),
]
LO_CODES = ["en-gb","ro","fr","de","es","it","pt","ru","ja","zh-cn","ko","ar"]
TB_CODES = ["en-gb","ro","fr","de","es-es","it","pt-pt","ru","ja","zh-cn","ko","ar"]

OFFICE_BASE = [
    {"pkg":"libreoffice-fresh","name":"LibreOffice Fresh",
     "desc":"Latest stable — Writer, Calc, Impress, Draw","icon":"📄","repo":"galaxy","aur":False},
]

MEDIA = [
    {"pkg":"mirage",             "name":"Mirage",
     "desc":"Feature-rich image viewer","icon":"🖼️","repo":"AUR","aur":True,"sub":[]},
    {"pkg":"gimp",               "name":"GIMP",
     "desc":"Image editor","icon":"🎨","repo":"world","aur":False,"sub":[]},
    {"pkg":"inkscape",           "name":"Inkscape",
     "desc":"Vector graphics editor","icon":"✏️","repo":"world","aur":False,"sub":[]},
    {"pkg":"kdenlive",           "name":"Kdenlive",
     "desc":"Video editor","icon":"🎬","repo":"world","aur":False,"sub":[]},
    {"pkg":"handbrake",          "name":"HandBrake",
     "desc":"Video converter/compressor","icon":"🔧","repo":"world","aur":False,"sub":[]},
    {"pkg":"obs-studio-liberty", "name":"OBS Liberty",
     "desc":"Streaming &amp; recording","icon":"🎙️","repo":"AUR","aur":True,"sub":[]},
]

COMMS = [
    {"section":"Messaging","packages":[
        {"pkg":"vesktop",          "name":"Vesktop",
         "desc":"Discord client (Vencord)","icon":"💬","repo":"AUR","aur":True,"sub":[]},
        {"pkg":"telegram-desktop", "name":"Telegram",
         "desc":"Messaging platform","icon":"📡","repo":"galaxy","aur":False,"sub":[]},
        {"pkg":"element-desktop",  "name":"Element",
         "desc":"Matrix decentralized chat","icon":"🔒","repo":"extra","aur":False,"sub":[]},
    ]},
    {"section":"Email","packages":[
        {"pkg":"thunderbird","name":"Thunderbird",
         "desc":"Email client with language packs","icon":"⚡","repo":"galaxy","aur":False,"sub":[]},
    ]},
    {"section":"Notes","packages":[
        {"pkg":"obsidian","name":"Obsidian",
         "desc":"Markdown note taking","icon":"💎","repo":"extra","aur":False,"sub":[]},
    ]},
]

PERIPHERALS = [
    {"section":"RGB / Razer","packages":[
        {"pkg":"openrazer-daemon","name":"OpenRazer Daemon",
         "desc":"Background service that communicates with Razer hardware",
         "icon":"🐍","repo":"extra","aur":False,"sub":[
            {"pkg":"openrazer-driver-dkms","name":"OpenRazer Driver","repo":"extra","aur":False},
            {"pkg":"python-openrazer",     "name":"Python OpenRazer","repo":"extra","aur":False},
        ]},
        {"pkg":"polychromatic","name":"Polychromatic",
         "desc":"OpenRazer GUI — per-key RGB, effects and DPI profiles",
         "icon":"🌈","repo":"AUR","aur":True,"sub":[]},
    ]},
    {"section":"Peripherals","packages":[
        {"pkg":"piper","name":"Piper",
         "desc":"Mouse &amp; keyboard configurator — DPI, buttons, polling rate. Multi-brand support",
         "icon":"🖱️","repo":"extra","aur":False,"sub":[]},
        {"pkg":"solaar","name":"Solaar",
         "desc":"Logitech device manager — Unifying/Bolt receiver pairing and battery levels",
         "icon":"⌨️","repo":"galaxy","aur":False,"sub":[]},
    ]},
]

FILE_TRANSFER = [
    {"section":"Android / MTP","packages":[
        {"pkg":"jmtpfs","name":"jmtpfs",
         "desc":"Mount Android phones via MTP — works with Android 4–14. Usage: jmtpfs ~/Phone",
         "icon":"📱","repo":"AUR","aur":True,"sub":[]},
        {"pkg":"go-mtpfs-git","name":"go-mtpfs",
         "desc":"Go implementation of MTP — faster for large file transfers",
         "icon":"🤖","repo":"AUR","aur":True,"sub":[]},
    ]},
    {"section":"Camera / PTP","packages":[
        {"pkg":"gphotofs","name":"gphotofs",
         "desc":"PTP mount via FUSE — works better with older devices and cameras",
         "icon":"📷","repo":"AUR","aur":True,"sub":[]},
        {"pkg":"gphoto2","name":"gphoto2",
         "desc":"Command-line tool for camera control and image download",
         "icon":"🎞️","repo":"world","aur":False,"sub":[]},
    ]},
    {"section":"Network / Wireless","packages":[
        {"pkg":"warpinator","name":"Warpinator",
         "desc":"LAN file sharing — send and receive files on the local network",
         "icon":"🌐","repo":"galaxy","aur":False,"sub":[]},
        {"pkg":"localsend-bin","name":"LocalSend",
         "desc":"Cross-platform AirDrop alternative — works with iOS, Android, Windows",
         "icon":"📡","repo":"AUR","aur":True,"sub":[]},
        {"pkg":"croc","name":"Croc",
         "desc":"Securely send files between any two computers — peer-to-peer, encrypted",
         "icon":"🐊","repo":"extra","aur":False,"sub":[]},
    ]},
    {"section":"USB / Serial","packages":[
        {"pkg":"android-tools","name":"Android Tools",
         "desc":"ADB and fastboot — sideloading, debugging, file transfer over USB",
         "icon":"🔧","repo":"world","aur":False,"sub":[]},
        {"pkg":"scrcpy","name":"Scrcpy",
         "desc":"Display and control Android devices over USB or Wi-Fi — no root needed",
         "icon":"📲","repo":"extra","aur":False,"sub":[]},
    ]},
]

# ── Repo badge style map ──────────────────────────────────────────────────────
REPO_STYLE = {
    "AUR":     ("#4fd9c4","#0e2e2e","#1a4040"),
    "extra":   ("#a89ff7","#18183a","#28285a"),
    "galaxy":  ("#f7b96a","#2e2200","#4a3800"),
    "world":   ("#6aaff7","#001a2e","#002a48"),
    "lib32":   ("#f76a6a","#2e0e0e","#4a1818"),
    "multilib":("#b46af7","#1e0e2e","#381848"),
}

ACCENT_COLOR  = (0.486, 0.416, 0.969)   # #7c6af7
ACCENT2_COLOR = (0.310, 0.851, 0.769)   # #4fd9c4

# ── Hyprland config ───────────────────────────────────────────────────────────
HYPRLAND_CONF = os.path.expanduser("~/.config/hypr/hyprland.conf")
EXEC_LINE = ("exec-once = bash -c '[ -f \"$HOME/Faded-Dream-dotfiles/faded-dream-setup.py\" ]"
             " && python3 \"$HOME/Faded-Dream-dotfiles/faded-dream-setup.py\"'")

# ── AUR map ───────────────────────────────────────────────────────────────────
def _build_aur_map():
    m = {}
    def idx(items):
        for it in items:
            m[it["pkg"]] = it.get("aur", False)
            for s in it.get("sub", []): m[s["pkg"]] = s.get("aur", False)
    for sec in GAMING:      idx(sec["packages"])
    for sec in PERIPHERALS: idx(sec["packages"])
    for sec in COMMS:       idx(sec["packages"])
    idx(MEDIA); idx(OFFICE_BASE)
    for sec in FILE_TRANSFER: idx(sec["packages"])
    for br in BROWSERS: m[br["pkg"]] = br.get("aur", False)
    return m

AUR_MAP = _build_aur_map()

# ── CSS ───────────────────────────────────────────────────────────────────────
APP_CSS = """
/* ═══════════════════════════════════════════════════════════════════════════
   FADED DREAM — BLACK HOLE / DEEP VOID THEME
   Palette:
     void       #07070d   absolute deep space
     surface    #0f0e1a   raised surface
     surface-hi #16152a   elevated card
     border     #1e1c30   subtle border
     text       #d8d4f0   soft lavender-white
     text-dim   #5a566e   dim mist
     event      #7c6af7   event horizon purple
     tidal      #4fd9c4   tidal teal
     corona     #c084fc   corona violet
     photon     #f7177a   photon ring pink
   ═══════════════════════════════════════════════════════════════════════════ */

window, .background { background-color: #07070d; color: #d8d4f0; }

headerbar {
    background-color: #0a0914; background-image: none;
    border-bottom: 1px solid #1e1c30;
    box-shadow: 0 1px 18px rgba(124,106,247,0.1);
    color: #d8d4f0; animation: fade-in 400ms ease both; min-height: 46px;
}
headerbar windowtitle title  { color: #d8d4f0; font-weight: bold; letter-spacing: 0.5px; }
headerbar windowtitle subtitle { color: #9490b0; font-size: 11px; }
headerbar button {
    background-color: transparent; background-image: none;
    border: 1px solid #1e1c30; border-radius: 6px; color: #9490b0;
    transition: all 150ms ease;
}
headerbar button:hover { background-color: #16152a; border-color: rgba(124,106,247,0.3); color: #d8d4f0; }

paned > separator { background-color: #1e1c30; min-width: 1px; }

.navigation-sidebar { background-color: #07070d; border: none; }
.navigation-sidebar row {
    background-color: transparent; border-radius: 10px; padding: 2px 4px;
    transition: background-color 200ms ease, box-shadow 200ms ease, padding-left 150ms ease;
    animation: sidebar-row-in 320ms cubic-bezier(0.34,1.56,0.64,1) both;
}
.navigation-sidebar row label {
    color: #7a7690; font-size: 12px; font-weight: bold;
    letter-spacing: 0.3px; transition: color 200ms ease;
}
.navigation-sidebar row:nth-child(1) { animation-delay:  30ms; }
.navigation-sidebar row:nth-child(2) { animation-delay:  70ms; }
.navigation-sidebar row:nth-child(3) { animation-delay: 110ms; }
.navigation-sidebar row:nth-child(4) { animation-delay: 150ms; }
.navigation-sidebar row:nth-child(5) { animation-delay: 190ms; }
.navigation-sidebar row:nth-child(6) { animation-delay: 230ms; }
.navigation-sidebar row:nth-child(7) { animation-delay: 270ms; }
.navigation-sidebar row:nth-child(8) { animation-delay: 310ms; }
.navigation-sidebar row:nth-child(9) { animation-delay: 350ms; }
.navigation-sidebar row:hover {
    background-color: rgba(124,106,247,0.07);
    box-shadow: inset 0 0 0 1px rgba(124,106,247,0.12);
    padding-left: 8px;
}
.navigation-sidebar row:hover label { color: #c4bef0; }
.navigation-sidebar row:selected {
    background-color: rgba(124,106,247,0.13);
    box-shadow: inset 3px 0 0 0 #7c6af7,
                inset 0 0 0 1px rgba(124,106,247,0.2),
                0 0 18px rgba(124,106,247,0.1);
    padding-left: 8px;
}
.navigation-sidebar row:selected label { color: #ffffff; }

stack, stack > * { background-color: #07070d; animation: fade-slide-in 240ms cubic-bezier(0.25,0.46,0.45,0.94) both; }
scrolledwindow, scrolledwindow > viewport { background-color: #07070d; border: none; }

.boxed-list { background-color: transparent; border: none; border-radius: 12px; margin-bottom: 12px; }
.boxed-list > row { background-color: #0f0e1a; border-bottom: 1px solid #1e1c30; }
.boxed-list > row:first-child { border-radius: 12px 12px 0 0; }
.boxed-list > row:last-child  { border-radius: 0 0 12px 12px; border-bottom: none; }
.boxed-list > row:only-child  { border-radius: 12px; border-bottom: none; }
.boxed-list > row:nth-child(1) { animation: fade-slide-in 200ms ease  20ms both; }
.boxed-list > row:nth-child(2) { animation: fade-slide-in 200ms ease  50ms both; }
.boxed-list > row:nth-child(3) { animation: fade-slide-in 200ms ease  80ms both; }
.boxed-list > row:nth-child(4) { animation: fade-slide-in 200ms ease 110ms both; }
.boxed-list > row:nth-child(5) { animation: fade-slide-in 200ms ease 140ms both; }
.boxed-list > row:nth-child(6) { animation: fade-slide-in 200ms ease 170ms both; }
.boxed-list > row:nth-child(7) { animation: fade-slide-in 200ms ease 200ms both; }
.boxed-list > row:nth-child(8) { animation: fade-slide-in 200ms ease 230ms both; }

row { background-color: transparent; color: #d8d4f0; }
row title   { color: #d8d4f0; font-size: 13px; font-weight: bold; background-color: transparent; }
row subtitle { color: #8884a0; font-size: 11px; background-color: transparent; }
row.activatable { transition: background-color 180ms ease, box-shadow 180ms ease; border-radius: 10px; }
row.activatable:hover {
    background-color: rgba(124,106,247,0.05);
    box-shadow: inset 0 0 0 1px rgba(124,106,247,0.09);
}

label { color: #d8d4f0; }
label.title-1 { color: #d8d4f0; font-size: 32px; font-weight: bold; animation: fade-in 400ms ease both; }
label.title-2 { color: #d8d4f0; font-size: 20px; }
label.title-3 { color: #d8d4f0; font-size: 16px; }
label.nav-icon { font-size: 20px; min-width: 28px; }
label.heading  { color: #d8d4f0; font-weight: bold; font-size: 14px; }
label.body     { color: #d8d4f0; font-size: 13px; }
label.caption  { color: #9490b0; font-size: 11px; }
label.dim-label { color: #7a7690; animation: void-breathe 5s ease-in-out infinite; }
label.success  { color: #4fd9c4; }
label.welcome-title {
    color: #d8d4f0; font-size: 28px; font-weight: bold; letter-spacing: 1px;
    animation: welcome-title-in 700ms cubic-bezier(0.34,1.56,0.64,1) 200ms both;
}
label.welcome-sub { color: #8884a0; font-size: 13px; animation: fade-in 600ms ease 450ms both; }
label.count-bump  { animation: count-bump 350ms cubic-bezier(0.34,1.56,0.64,1) both; }

.nav-count-badge {
    background-color: rgba(124,106,247,0.25);
    border: 1px solid rgba(124,106,247,0.45);
    border-radius: 10px;
    color: #c4bef0;
    font-size: 9px;
    font-weight: bold;
    padding: 1px 6px;
    min-width: 18px;
    transition: all 200ms cubic-bezier(0.34,1.56,0.64,1);
    animation: badge-pop-in 250ms cubic-bezier(0.34,1.56,0.64,1) both;
}
.navigation-sidebar row:selected .nav-count-badge {
    background-color: rgba(124,106,247,0.45);
    border-color: rgba(124,106,247,0.75);
    color: #ffffff;
}

.section-heading {
    color: #7a7690; font-size: 10px; font-weight: bold;
    letter-spacing: 2.5px; animation: header-slide-in 500ms ease both;
}

.row-icon {
    animation: icon-entrance 400ms cubic-bezier(0.34,1.56,0.64,1) both;
    transition: transform 220ms cubic-bezier(0.34,1.56,0.64,1);
}
row:hover .row-icon { transform: scale(1.18) rotate(6deg); }

.repo-badge {
    border-radius: 5px; padding: 1px 6px; font-weight: bold; font-size: 9px;
    letter-spacing: 0.3px; animation: fade-in 350ms ease both;
    transition: transform 200ms cubic-bezier(0.34,1.56,0.64,1);
}
row:hover .repo-badge { transform: scale(1.08); }
.repo-aur      { color: #4fd9c4; background-color: #071e1c; border: 1px solid #0e3530; }
.repo-extra    { color: #a89ff7; background-color: #100f28; border: 1px solid #1e1c48; }
.repo-galaxy   { color: #f59e0b; background-color: #1c1400; border: 1px solid #2e2200; }
.repo-world    { color: #6aaff7; background-color: #040e1e; border: 1px solid #081a32; }
.repo-lib32    { color: #f76a6a; background-color: #1c0808; border: 1px solid #2e1010; }
.repo-multilib { color: #c084fc; background-color: #110820; border: 1px solid #1e1034; }
.sub-bar { background-color: #7c6af7; border-radius: 1px; }

checkbutton { color: #d8d4f0; }
checkbutton check {
    background-color: #0f0e1a; background-image: none;
    border: 1.5px solid #2a2548; border-radius: 5px;
    min-width: 16px; min-height: 16px;
    transition: all 150ms cubic-bezier(0.34,1.56,0.64,1);
}
checkbutton check:hover {
    border-color: #7c6af7;
    box-shadow: 0 0 0 3px rgba(124,106,247,0.2), 0 0 12px rgba(124,106,247,0.3);
    transform: scale(1.12);
}
checkbutton check:checked {
    background-color: #7c6af7; background-image: none; border-color: #7c6af7;
    animation: check-bounce 300ms cubic-bezier(0.34,1.56,0.64,1) both;
    box-shadow: 0 0 0 2px rgba(124,106,247,0.25), 0 0 14px rgba(124,106,247,0.55);
}
checkbutton label { color: #d8d4f0; font-size: 12px; font-weight: bold; }

button {
    background-color: #0f0e1a; background-image: none;
    border: 1px solid #1e1c30; border-radius: 9px; color: #9490b0;
    padding: 5px 14px; font-size: 12px; font-weight: bold;
    transition: all 150ms cubic-bezier(0.34,1.56,0.64,1);
}
button:hover {
    background-color: #16152a; border-color: rgba(124,106,247,0.28);
    color: #d8d4f0; transform: translateY(-1px);
    box-shadow: 0 4px 16px rgba(0,0,0,0.6), 0 0 10px rgba(124,106,247,0.1);
}
button:active { background-color: #0a0914; transform: scale(0.95) translateY(1px); box-shadow: none; }
button:disabled { background-color: #0a0914; color: #1e1c30; border-color: #14121e; }
button.flat { background-color: transparent; background-image: none; border-color: transparent; color: #8884a0; box-shadow: none; }
button.flat:hover { background-color: rgba(124,106,247,0.08); border-color: transparent; color: #d8d4f0; transform: translateY(-1px); box-shadow: none; }

button.suggested-action,
button.suggested-action:link,
actionbar button.suggested-action {
    background-color: #f7177a; background-image: none;
    border-color: #f7177a; color: #fff; font-weight: bold;
    box-shadow: 0 0 16px rgba(247,23,122,0.4);
}
button.suggested-action:hover, actionbar button.suggested-action:hover {
    background-color: #ff3d94; background-image: none; border-color: #ff3d94;
    color: #fff; transform: translateY(-2px) scale(1.04);
    box-shadow: 0 4px 24px rgba(247,23,122,0.6), 0 0 50px rgba(247,23,122,0.2);
}
button.suggested-action:active, actionbar button.suggested-action:active {
    background-color: #c4005e; background-image: none;
    transform: scale(0.95) translateY(1px); box-shadow: none;
}
button.suggested-action:disabled, actionbar button.suggested-action:disabled {
    background-color: #1a1428; background-image: none;
    border-color: #1a1428; color: #2a2448; box-shadow: none;
}

switch, actionbar switch {
    background-color: #0a0e10; background-image: none;
    border: 1px solid #0e2824; border-radius: 14px;
    min-width: 40px; min-height: 22px; box-shadow: none; outline: none;
    transition: all 200ms ease;
}
switch:checked, actionbar switch:checked {
    background-color: #0d2e2a; background-image: none;
    border-color: #4fd9c4; box-shadow: 0 0 12px rgba(79,217,196,0.3);
}
switch:focus, switch:focus-visible { outline: none; box-shadow: none; }
switch slider, actionbar switch slider {
    background-color: #6a6488; background-image: none; border: none;
    border-radius: 50%; min-width: 16px; min-height: 16px; margin: 2px;
    transition: transform 220ms cubic-bezier(0.34,1.56,0.64,1),
                background-color 200ms ease, box-shadow 200ms ease;
    box-shadow: 0 1px 6px rgba(0,0,0,0.7);
}
switch:checked slider, actionbar switch:checked slider {
    background-color: #4fd9c4; background-image: none;
    transform: scale(1.1);
    box-shadow: 0 0 12px rgba(79,217,196,0.55), 0 1px 6px rgba(0,0,0,0.4);
}

progressbar { border-radius: 8px; }
progressbar trough {
    background-color: #0f0e1a; background-image: none;
    border: 1px solid #1e1c30; border-radius: 8px; min-height: 6px;
}
progressbar progress {
    background-color: #7c6af7; background-image: none; border-radius: 8px;
    animation: event-horizon-pulse 1.6s ease-in-out infinite;
    transition: all 300ms ease;
}
progressbar text { color: #7a7690; font-size: 10px; }

scrollbar { background-color: #07070d; border: none; min-width: 5px; }
scrollbar trough { background-color: #07070d; border: none; }
scrollbar slider {
    background-color: #1e1c30; border-radius: 8px; min-width: 3px; min-height: 20px;
    transition: background-color 150ms ease, min-width 150ms ease;
}
scrollbar slider:hover { background-color: #7c6af7; min-width: 6px; }
scrollbar.horizontal { min-height: 5px; }
scrollbar.horizontal slider { min-height: 3px; min-width: 20px; }

textview, textview > text {
    background-color: #050508; color: #8884a0;
    font-family: "JetBrainsMono Nerd Font","Noto Mono",monospace;
    font-size: 12px; border-radius: 10px; animation: fade-in 300ms ease both;
}

separator { background-color: #14121e; min-height: 1px; }

actionbar {
    background-color: #0a0914; background-image: none;
    border-top: 1px solid #1e1c30;
    box-shadow: 0 -1px 20px rgba(124,106,247,0.07);
    animation: fade-in 400ms ease both; padding: 8px 12px;
}
actionbar > revealer > box { background-color: transparent; border: none; }

.welcome-page { background-color: #07070d; }
.welcome-page flowbox { background-color: transparent; }
.welcome-page flowboxchild { background-color: transparent; border-radius: 12px; padding: 0; }
.welcome-page flowboxchild row {
    background-color: #0f0e1a; border: 1px solid #1e1c30; border-radius: 12px;
    transition: all 200ms cubic-bezier(0.34,1.56,0.64,1);
}
.welcome-page flowboxchild row *, .welcome-page flowboxchild row box,
.welcome-page flowboxchild row box * { background-color: transparent; }
.welcome-page flowboxchild row:hover {
    background-color: #16152a;
    border-color: rgba(124,106,247,0.4);
    box-shadow: 0 6px 28px rgba(124,106,247,0.18),
                inset 0 0 0 1px rgba(124,106,247,0.18);
    transform: translateY(-4px) scale(1.025);
}
.welcome-card-arrow { transition: opacity 180ms ease, transform 180ms cubic-bezier(0.34,1.56,0.64,1); opacity: 0; }
.welcome-page flowboxchild row:hover .welcome-card-arrow { opacity: 0.6; transform: translateX(4px); }

flowboxchild { background-color: transparent; border-radius: 12px; }

/* Welcome cards — staggered pop-in via named classes */
.wcard { animation: welcome-card-in 480ms cubic-bezier(0.34,1.56,0.64,1) both; opacity: 0; }
.wcard-0 { animation-delay:  60ms; }
.wcard-1 { animation-delay: 110ms; }
.wcard-2 { animation-delay: 165ms; }
.wcard-3 { animation-delay: 220ms; }
.wcard-4 { animation-delay: 280ms; }
.wcard-5 { animation-delay: 340ms; }
.wcard-6 { animation-delay: 400ms; }

tooltip { background-color: #0f0e1a; border: 1px solid #1e1c30; border-radius: 7px; color: #d8d4f0; }
popover  { background-color: #0f0e1a; border: 1px solid #1e1c30; border-radius: 9px; color: #d8d4f0; }

@keyframes fade-slide-in {
    from { opacity: 0; margin-top: 20px; } to { opacity: 1; margin-top: 0; }
}
@keyframes fade-in { from { opacity: 0; } to { opacity: 1; } }
@keyframes sidebar-row-in {
    from { opacity: 0; margin-left: -20px; } to { opacity: 1; margin-left: 0; }
}
@keyframes welcome-title-in {
    from { opacity: 0; transform: translateY(24px) scale(0.90); letter-spacing: 6px; }
    to   { opacity: 1; transform: translateY(0) scale(1.0); letter-spacing: 1px; }
}
@keyframes welcome-card-in {
    0%   { opacity: 0; transform: scale(0.78) translateY(28px); }
    60%  { opacity: 1; transform: scale(1.04) translateY(-4px); }
    80%  { opacity: 1; transform: scale(0.97) translateY(2px);  }
    100% { opacity: 1; transform: scale(1.00) translateY(0);    }
}
@keyframes header-slide-in {
    from { opacity: 0; letter-spacing: 8px; } to { opacity: 1; letter-spacing: 2.5px; }
}
@keyframes icon-entrance {
    from { transform: rotate(-18deg) scale(0.75); opacity: 0; }
    to   { transform: rotate(0) scale(1.0); opacity: 1; }
}
@keyframes check-bounce {
    0% { transform: scale(1.0); } 35% { transform: scale(1.35); }
    65% { transform: scale(0.9); } 100% { transform: scale(1.0); }
}
@keyframes event-horizon-pulse {
    0%   { box-shadow: 0 0 6px 2px rgba(124,106,247,0.25); }
    50%  { box-shadow: 0 0 22px 7px rgba(124,106,247,0.65),
                       0 0 55px 16px rgba(192,132,252,0.2); }
    100% { box-shadow: 0 0 6px 2px rgba(124,106,247,0.25); }
}
@keyframes badge-pop-in {
    from { opacity: 0; transform: scale(0.5); }
    to   { opacity: 1; transform: scale(1.0); }
}
@keyframes count-bump {
    0% { transform: scale(1.0); } 40% { transform: scale(1.28); } 100% { transform: scale(1.0); }
}
@keyframes void-breathe {
    0%, 100% { opacity: 0.55; } 50% { opacity: 1.0; }
}
"""

_CSS_INJECTED = False

def _inject_css(display):
    global _CSS_INJECTED
    if _CSS_INJECTED: return
    _CSS_INJECTED = True
    provider = Gtk.CssProvider()
    provider.load_from_data(APP_CSS.encode())
    # PRIORITY_USER (800) beats themes (600) and applications (400)
    Gtk.StyleContext.add_provider_for_display(
        display, provider, Gtk.STYLE_PROVIDER_PRIORITY_USER)

# ── Helpers ───────────────────────────────────────────────────────────────────
def _repo_badge(repo):
    lbl = Gtk.Label(label=repo)
    lbl.set_css_classes(["repo-badge", f"repo-{repo.lower()}"])
    lbl.set_valign(Gtk.Align.CENTER)
    return lbl

def _section_label(text):
    lbl = Gtk.Label(label=text.upper())
    lbl.add_css_class("section-heading")
    lbl.add_css_class("caption")
    lbl.set_halign(Gtk.Align.START)
    lbl.set_margin_top(14)
    lbl.set_margin_bottom(4)
    return lbl

def _sep():
    sep = Gtk.Separator(orientation=Gtk.Orientation.HORIZONTAL)
    sep.set_margin_bottom(6)
    return sep

def _scrolled(child):
    sw = Gtk.ScrolledWindow()
    sw.set_hexpand(True); sw.set_vexpand(True)
    sw.set_policy(Gtk.PolicyType.NEVER, Gtk.PolicyType.AUTOMATIC)
    sw.set_child(child)
    return sw

def _boxed_list():
    """Gtk.ListBox styled like Adw.PreferencesGroup but accepts any widget."""
    lb = Gtk.ListBox()
    lb.set_css_classes(["boxed-list"])
    lb.set_selection_mode(Gtk.SelectionMode.NONE)
    lb.set_margin_bottom(12)
    return lb

# ── Cairo-drawn animated checkmark widget ────────────────────────────────────
class CheckMarkWidget(Gtk.DrawingArea):
    """Animated checkmark: draws circle + progressive tick + particle burst."""

    def __init__(self, accent=None):
        super().__init__()
        self.set_size_request(24, 24)
        self.set_content_width(24)
        self.set_content_height(24)

        self._progress  = 0.0
        self._checked   = False
        self._accent    = accent or ACCENT_COLOR   # (r,g,b) tuple
        self._particles = []
        self._tick_id   = None

        self.set_draw_func(self._draw)

    # ── Particle system ───────────────────────────────────────────────────────
    def _spawn_particles(self):
        for _ in range(18):
            angle = random.uniform(0, math.tau)
            speed = random.uniform(1.5, 4.5)
            self._particles.append({
                "x": 12.0, "y": 12.0,
                "vx": math.cos(angle) * speed,
                "vy": math.sin(angle) * speed,
                "life": 1.0,
                "decay": random.uniform(0.04, 0.09),
                "r": random.uniform(2, 5),
            })

    def _tick_particles(self):
        live = []
        for p in self._particles:
            p["x"]    += p["vx"]
            p["y"]    += p["vy"]
            p["vy"]   += 0.12
            p["vx"]   *= 0.96
            p["life"] -= p["decay"]
            if p["life"] > 0:
                live.append(p)
        self._particles = live
        self.queue_draw()
        if not self._particles:
            if self._tick_id:
                GLib.source_remove(self._tick_id)
                self._tick_id = None
        return bool(self._particles)

    # ── State ─────────────────────────────────────────────────────────────────
    def set_checked(self, checked):
        if checked == self._checked:
            return
        self._checked = checked
        target = 1.0 if checked else 0.0
        start  = self._progress

        if checked:
            self._spawn_particles()
            if self._tick_id is None:
                self._tick_id = GLib.timeout_add(16, self._tick_particles)

        duration_ms = 360
        steps       = duration_ms // 16
        step_size   = (target - start) / max(steps, 1)
        step_count  = [0]

        def _animate():
            step_count[0] += 1
            self._progress = max(0.0, min(1.0, start + step_size * step_count[0]))
            self.queue_draw()
            if step_count[0] >= steps:
                self._progress = target
                self.queue_draw()
                return False
            return True

        GLib.timeout_add(16, _animate)

    # ── Draw ──────────────────────────────────────────────────────────────────
    def _draw(self, area, cr, w, h):
        cr.set_antialias(cairo.ANTIALIAS_BEST)
        r, g, b = self._accent

        # particles
        for p in self._particles:
            a = max(0.0, min(1.0, p["life"] * 0.85))
            cr.set_source_rgba(r, g, b, a)
            cr.arc(p["x"], p["y"], p["r"] * p["life"], 0, math.tau)
            cr.fill()

        prog = max(0.0, min(1.0, self._progress))

        if prog <= 0.01:
            cr.set_source_rgba(0.2, 0.2, 0.28, 1.0)
            cr.set_line_width(1.5)
            cr.arc(12, 12, 9, 0, math.tau)
            cr.stroke()
            return

        # filled bg circle
        cr.set_source_rgba(r, g, b, prog * 0.15)
        cr.arc(12, 12, 9, 0, math.tau)
        cr.fill()

        # border circle
        cr.set_source_rgba(r, g, b, prog)
        cr.set_line_width(1.5)
        cr.arc(12, 12, 9, 0, math.tau)
        cr.stroke()

        # progressive checkmark
        if prog > 0.05:
            p1x, p1y = 7.0,  12.0
            p2x, p2y = 10.5, 16.0
            p3x, p3y = 17.5,  8.0

            cr.set_source_rgba(r, g, b, 1.0)
            cr.set_line_width(2.0)
            cr.set_line_cap(cairo.LINE_CAP_ROUND)
            cr.set_line_join(cairo.LINE_JOIN_ROUND)
            cr.new_path()

            if prog < 0.4:
                t   = prog / 0.4
                mx  = p1x + (p2x - p1x) * t
                my  = p1y + (p2y - p1y) * t
                cr.move_to(p1x, p1y)
                cr.line_to(mx, my)
            else:
                t   = (prog - 0.4) / 0.6
                mx  = p2x + (p3x - p2x) * t
                my  = p2y + (p3y - p2y) * t
                cr.move_to(p1x, p1y)
                cr.line_to(p2x, p2y)
                cr.line_to(mx, my)

            cr.stroke()


# ── Shimmer drawing area ──────────────────────────────────────────────────────
class ShimmerWidget(Gtk.DrawingArea):
    """Paints a single left-to-right shimmer sweep; call play() to trigger."""

    def __init__(self):
        super().__init__()
        self.set_hexpand(True); self.set_vexpand(True)
        self.set_can_target(False)
        self._pos    = -1.0
        self._active = False
        self.set_draw_func(self._draw)

    def play(self):
        self._pos    = -0.3
        self._active = True
        GLib.timeout_add(16, self._tick)

    def _tick(self):
        self._pos += 0.06
        self.queue_draw()
        if self._pos > 1.3:
            self._active = False
            self._pos    = -1.0
            self.queue_draw()
            return False
        return True

    def _draw(self, area, cr, w, h):
        if not self._active or self._pos < 0: return
        cx = w * self._pos
        pat = cairo.LinearGradient(cx - 60, 0, cx + 60, 0)
        pat.add_color_stop_rgba(0.0, 1, 1, 1, 0.0)
        pat.add_color_stop_rgba(0.5, 1, 1, 1, 0.11)
        pat.add_color_stop_rgba(1.0, 1, 1, 1, 0.0)
        cr.set_source(pat)
        cr.rectangle(0, 0, w, h)
        cr.fill()


# ── GlowRow — overlay widget drawn over an ActionRow ─────────────────────────
class GlowOverlay(Gtk.DrawingArea):
    """Animated glow border drawn on top of a row; call set_selected()."""

    def __init__(self, accent=None, is_pill=False):
        super().__init__()
        self.set_hexpand(True); self.set_vexpand(True)
        self.set_can_target(False)
        self._accent   = accent or ACCENT_COLOR
        self._is_pill  = is_pill
        self._glow_op  = 0.0
        self._selected = False
        self._tick_id  = None
        self.set_draw_func(self._draw)

    def set_selected(self, sel):
        self._selected = sel
        target = 1.0 if sel else 0.0
        start  = self._glow_op
        steps  = 20
        sc     = [0]

        def _step():
            sc[0] += 1
            self._glow_op = max(0.0, min(1.0, start + (target - start) * sc[0] / steps))
            self.queue_draw()
            return sc[0] < steps

        GLib.timeout_add(16, _step)

    def _draw(self, area, cr, w, h):
        g = max(0.0, min(1.0, self._glow_op))
        if g < 0.01: return
        r, gb, b = self._accent
        radius   = h // 2 if self._is_pill else 10

        # glow rings
        for i in range(3):
            alpha = max(0.0, g * (0.28 - i * 0.08))
            lw    = 4.0 + i * 2
            cr.set_source_rgba(r, gb, b, alpha)
            cr.set_line_width(lw)
            off = 1.0 + i
            _rounded_rect(cr, off, off, w - off*2, h - off*2, radius)
            cr.stroke()

        # sharp border
        cr.set_source_rgba(r, gb, b, g)
        cr.set_line_width(2.0)
        _rounded_rect(cr, 0.75, 0.75, w - 1.5, h - 1.5, radius)
        cr.stroke()


def _rounded_rect(cr, x, y, w, h, r):
    cr.new_sub_path()
    cr.arc(x + w - r, y + r,     r, -math.pi/2, 0)
    cr.arc(x + w - r, y + h - r, r,  0,          math.pi/2)
    cr.arc(x + r,     y + h - r, r,  math.pi/2,  math.pi)
    cr.arc(x + r,     y + r,     r,  math.pi,    3*math.pi/2)
    cr.close_path()


# ── Animated row container (wraps an Adw.ActionRow with glow + shimmer) ───────
class AnimatedRow(Gtk.ListBoxRow):
    """
    Gtk.ListBoxRow containing a Gtk.Overlay that stacks:
      bottom layer : Adw.ActionRow (content)
      middle layer : GlowOverlay   (animated border glow)
      top layer    : ShimmerWidget (one-shot shimmer on select)
    Can be appended directly to a Gtk.ListBox.
    """

    def __init__(self, accent=None, is_pill=False):
        super().__init__()
        self.set_activatable(False)
        self._accent = accent or ACCENT_COLOR

        self._overlay = Gtk.Overlay()
        self.row      = Adw.ActionRow()
        self._glow    = GlowOverlay(accent=self._accent, is_pill=is_pill)
        self._shimmer = ShimmerWidget()

        self._overlay.set_child(self.row)
        self._overlay.add_overlay(self._glow)
        self._overlay.add_overlay(self._shimmer)
        self.set_child(self._overlay)

    def set_selected(self, sel):
        self._glow.set_selected(sel)
        if sel:
            self._shimmer.play()

    def add_controller(self, ctrl):
        # Route gesture controllers to the overlay so clicks hit the full area
        self._overlay.add_controller(ctrl)


# ── Faded Dream Hero — Black Hole / Void Scene ───────────────────────────────
class MoonHero(Gtk.DrawingArea):
    """
    Full-width Cairo hero drawing a coherent deep-space scene:
      • Absolute void background with subtle nebula colour washes
      • Black hole with animated accretion disk, photon ring, gravitational lensing
      • Crescent moon drifting in orbit to the left, casting a faint tidal glow
      • Star field — 160 stars twinkling and slowly drawn toward the black hole
      • Wispy gravitational dust streamers spiralling inward
      • Faint aurora ribbons (purple / teal / pink) — the color palette of the app
    60 fps via GLib.timeout_add(16, ...).
    """

    def __init__(self):
        super().__init__()
        self.set_hexpand(True)
        self.set_draw_func(self._draw)
        self._t       = 0.0
        self._rng     = random.Random(137)
        self._stars   = self._gen_stars(160)
        self._dust    = self._gen_dust(40)
        self._tick_id = GLib.timeout_add(16, self._tick)
        self.connect("unrealize", self._on_unrealize)

        # mouse interactivity
        self._mx    = 0.5
        self._my    = 0.5
        self._smx   = 0.5   # smoothed
        self._smy   = 0.5
        self._hover = False

        motion = Gtk.EventControllerMotion()
        motion.connect("motion", self._on_motion)
        motion.connect("enter",  self._on_enter)
        motion.connect("leave",  self._on_leave)
        self.add_controller(motion)

    # ── Mouse handlers ────────────────────────────────────────────────────────
    def _on_motion(self, ctrl, x, y):
        alloc = self.get_allocation()
        if alloc.width > 0 and alloc.height > 0:
            self._mx = x / alloc.width
            self._my = y / alloc.height

    def _on_enter(self, ctrl, x, y):
        self._hover = True

    def _on_leave(self, ctrl):
        self._hover = False

    # ── Data generators ───────────────────────────────────────────────────────
    def _gen_stars(self, n):
        r = self._rng
        return [{
            "x":     r.random(),
            "y":     r.random(),
            "rad":   r.uniform(0.5, 2.0),
            "phase": r.uniform(0, math.tau),
            "twink": r.uniform(0.2, 0.9),
            "drift": r.uniform(0.0001, 0.0004),   # slow pull toward BH
            "angle": r.uniform(0, math.tau),
        } for _ in range(n)]

    def _gen_dust(self, n):
        r = self._rng
        return [{
            "angle":  r.uniform(0, math.tau),
            "radius": r.uniform(0.06, 0.22),      # normalised to min(w,h)
            "speed":  r.uniform(0.008, 0.025) * (1 if r.random() > 0.5 else -1),
            "alpha":  r.uniform(0.04, 0.14),
            "width":  r.uniform(0.008, 0.022),
            "len":    r.uniform(0.3, 1.2),         # arc length in radians
        } for _ in range(n)]

    # ── Tick ──────────────────────────────────────────────────────────────────
    def _tick(self):
        self._t += 0.016

        # smooth cursor with inertia
        ease = 0.06 if self._hover else 0.02
        self._smx += (self._mx - self._smx) * ease
        self._smy += (self._my - self._smy) * ease

        # stars slowly spiral inward
        for s in self._stars:
            s["angle"]  += s["drift"] * 0.4
            # very slow pull — moves star 0.0001 normalised units/frame
            cx, cy = 0.62, 0.46          # black hole centre (normalised)
            dx = cx - s["x"]
            dy = cy - s["y"]
            dist = math.hypot(dx, dy) + 0.001
            s["x"] += dx / dist * s["drift"] * 0.05
            s["y"] += dy / dist * s["drift"] * 0.05
            # respawn far away when they get too close
            if dist < 0.04:
                s["x"] = self._rng.random()
                s["y"] = self._rng.random()
        # dust streamers rotate
        for d in self._dust:
            d["angle"] += d["speed"]
        self.queue_draw()
        return True

    def _on_unrealize(self, _widget):
        if self._tick_id:
            GLib.source_remove(self._tick_id)
            self._tick_id = None

    # ── Draw ──────────────────────────────────────────────────────────────────
    def _draw(self, area, cr, w, h):
        t   = self._t

        # cursor parallax — smx/smy are 0–1, centre at 0.5
        px  = (self._smx - 0.5) * 2   # -1 to +1
        py  = (self._smy - 0.5) * 2

        # black hole barely moves (heavy — resists the cursor)
        BX  = w * 0.62 + px * w * 0.012
        BY  = h * 0.46 + py * h * 0.012
        BHR = min(w, h) * 0.075
        # moon reacts more to cursor (lighter, tidal pull)
        MX  = w * 0.27 + 8 * math.sin(t * 0.38) - px * w * 0.028
        MY  = h * 0.40 + 12 * math.sin(t * 0.52) - py * h * 0.020
        MR  = min(w, h) * 0.115
        # cursor proximity to BH — boosts corona when mouse is near
        dist_cursor_bh = math.hypot(self._smx - 0.62, self._smy - 0.46)
        bh_hover_boost = max(0.0, 1.0 - dist_cursor_bh / 0.3) * self._hover

        # ── void background ───────────────────────────────────────────────
        grad = cairo.LinearGradient(0, 0, w, h)
        grad.add_color_stop_rgb(0.0, 0.027, 0.027, 0.050)
        grad.add_color_stop_rgb(0.5, 0.035, 0.030, 0.065)
        grad.add_color_stop_rgb(1.0, 0.020, 0.020, 0.040)
        cr.set_source(grad)
        cr.rectangle(0, 0, w, h)
        cr.fill()

        # ── nebula colour wash — faint clouds of purple / teal / pink ────
        nebulas = [
            (w*0.20, h*0.30, w*0.55, 0.486, 0.416, 0.969, 0.045 + 0.02*math.sin(t*0.18)),
            (w*0.70, h*0.65, w*0.45, 0.310, 0.851, 0.769, 0.030 + 0.015*math.sin(t*0.24+1)),
            (w*0.50, h*0.10, w*0.50, 0.753, 0.259, 0.984, 0.025 + 0.012*math.sin(t*0.31+2)),
            (w*0.85, h*0.25, w*0.35, 0.486, 0.416, 0.969, 0.020 + 0.010*math.sin(t*0.22+3)),
        ]
        for nx, ny, nr, r2, g2, b2, a2 in nebulas:
            ng = cairo.RadialGradient(nx, ny, 0, nx, ny, nr)
            ng.add_color_stop_rgba(0.0, r2, g2, b2, a2)
            ng.add_color_stop_rgba(1.0, r2, g2, b2, 0.0)
            cr.set_source(ng)
            cr.arc(nx, ny, nr, 0, math.tau)
            cr.fill()

        # ── stars ─────────────────────────────────────────────────────────
        for s in self._stars:
            depth_factor = s["drift"] / 0.0004
            sx = s["x"] * w - px * w * 0.018 * depth_factor
            sy = s["y"] * h - py * h * 0.014 * depth_factor
            # dim stars near BH (lensing darkens field)
            dist_bh = math.hypot(sx - BX, sy - BY)
            dim = min(1.0, dist_bh / (BHR * 6))
            alpha = dim * (0.35 + s["twink"] * 0.5 * (0.5 + 0.5 * math.sin(t * 2.2 + s["phase"])))
            # slight purple tint for stars near the corona
            rr = 0.88 + 0.12 * (1 - dim)
            gg = 0.87 + 0.05 * dim
            bb = 0.97
            cr.set_source_rgba(rr, gg, bb, alpha)
            cr.arc(sx, sy, s["rad"], 0, math.tau)
            cr.fill()
            # cross sparkle on bright ones
            if s["rad"] > 1.4 and alpha > 0.6:
                cr.set_source_rgba(rr, gg, bb, alpha * 0.28)
                cr.set_line_width(0.7)
                sp = s["rad"] * 3.8
                cr.move_to(sx-sp, sy); cr.line_to(sx+sp, sy); cr.stroke()
                cr.move_to(sx, sy-sp); cr.line_to(sx, sy+sp); cr.stroke()

        # ── gravitational dust streamers ──────────────────────────────────
        for d in self._dust:
            r_px = d["radius"] * min(w, h)
            a0   = d["angle"]
            a1   = a0 + d["len"] * math.copysign(1, d["speed"])
            # fade at inner/outer edges
            fade = 1.0 - abs(d["radius"] - 0.14) / 0.10
            fade = max(0.0, min(1.0, fade))
            # color alternates purple / teal
            if d["speed"] > 0:
                cr.set_source_rgba(0.486, 0.416, 0.969, d["alpha"] * fade)
            else:
                cr.set_source_rgba(0.310, 0.851, 0.769, d["alpha"] * fade * 0.7)
            cr.set_line_width(d["width"] * min(w, h))
            cr.set_line_cap(cairo.LINE_CAP_ROUND)
            cr.new_path()
            cr.arc(BX, BY, r_px, min(a0,a1), max(a0,a1))
            cr.stroke()

        # ── moon — crescent, floating left ────────────────────────────────
        # soft tidal glow
        tidal_pulse = 0.08 + 0.03 * math.sin(t * 0.6)
        for i in range(4):
            tr2   = MR * (1.5 + i * 0.35)
            ta    = tidal_pulse * (0.65 ** i)
            tg    = cairo.RadialGradient(MX, MY, MR*0.8, MX, MY, tr2)
            tg.add_color_stop_rgba(0.0, 0.310, 0.851, 0.769, ta)
            tg.add_color_stop_rgba(1.0, 0.310, 0.851, 0.769, 0.0)
            cr.set_source(tg)
            cr.arc(MX, MY, tr2, 0, math.tau)
            cr.fill()

        # moon body
        mg = cairo.RadialGradient(
            MX - MR*0.22, MY - MR*0.22, MR*0.08,
            MX, MY, MR)
        mg.add_color_stop_rgb(0.0, 0.96, 0.94, 0.98)
        mg.add_color_stop_rgb(0.55, 0.82, 0.79, 0.90)
        mg.add_color_stop_rgb(1.0,  0.62, 0.58, 0.78)
        cr.set_source(mg)
        cr.arc(MX, MY, MR, 0, math.tau)
        cr.fill()

        # crescent shadow — carved from right side toward BH
        cr.set_operator(cairo.OPERATOR_DEST_OUT)
        cr.set_source_rgba(0, 0, 0, 1)
        cr.arc(MX + MR*0.42, MY + MR*0.05, MR*0.86, 0, math.tau)
        cr.fill()
        cr.set_operator(cairo.OPERATOR_OVER)

        # rim glow on crescent edge
        rim = cairo.LinearGradient(MX - MR, MY, MX + MR*0.3, MY)
        rim.add_color_stop_rgba(0.0, 1.0, 1.0, 1.0, 0.50)
        rim.add_color_stop_rgba(0.5, 1.0, 1.0, 1.0, 0.08)
        rim.add_color_stop_rgba(1.0, 1.0, 1.0, 1.0, 0.0)
        cr.set_source(rim)
        cr.arc(MX, MY, MR, 0, math.tau)
        cr.fill()

        # craters
        for cx2, cy2, cr2 in [(-0.28,-0.25,0.08),(-0.08,-0.08,0.055),(-0.38,+0.18,0.05),(-0.16,+0.32,0.065)]:
            cxp = MX + cx2*MR; cyp = MY + cy2*MR
            cg2 = cairo.RadialGradient(cxp, cyp, 0, cxp, cyp, cr2*MR)
            cg2.add_color_stop_rgba(0.0, 0.4, 0.38, 0.55, 0.16)
            cg2.add_color_stop_rgba(1.0, 0.4, 0.38, 0.55, 0.0)
            cr.set_source(cg2)
            cr.arc(cxp, cyp, cr2*MR, 0, math.tau)
            cr.fill()

        # gravitational bridge — faint streamer from moon toward BH
        bridge_alpha = 0.04 + 0.02 * math.sin(t * 0.44)
        bg2 = cairo.LinearGradient(MX, MY, BX, BY)
        bg2.add_color_stop_rgba(0.0, 0.310, 0.851, 0.769, bridge_alpha)
        bg2.add_color_stop_rgba(0.5, 0.486, 0.416, 0.969, bridge_alpha * 0.6)
        bg2.add_color_stop_rgba(1.0, 0.486, 0.416, 0.969, 0.0)
        cr.set_source(bg2)
        cr.set_line_width(MR * 0.18)
        cr.set_line_cap(cairo.LINE_CAP_ROUND)
        cr.move_to(MX, MY)
        # bezier curves toward BH for a graceful arc
        ctrl1x = MX + (BX-MX)*0.3 + 20*math.sin(t*0.28)
        ctrl1y = MY + (BY-MY)*0.2 - 30
        ctrl2x = MX + (BX-MX)*0.7 - 20*math.sin(t*0.22)
        ctrl2y = MY + (BY-MY)*0.8 + 20
        cr.curve_to(ctrl1x, ctrl1y, ctrl2x, ctrl2y, BX, BY)
        cr.stroke()

        # ── black hole ────────────────────────────────────────────────────
        # outer glow / corona — pulsing
        corona_pulse = 0.18 + 0.07 * math.sin(t * 0.85)
        corona_rings = [
            (BHR * 4.5, 0.486, 0.416, 0.969, corona_pulse * 0.40),
            (BHR * 3.2, 0.753, 0.259, 0.984, corona_pulse * 0.55),
            (BHR * 2.2, 0.969, 0.471, 0.980, corona_pulse * 0.70),
            (BHR * 1.6, 0.980, 0.635, 0.255, corona_pulse * 0.50),  # amber accretion
        ]
        for ring_r, rr, gg, bb, aa in corona_rings:
            rg = cairo.RadialGradient(BX, BY, BHR*0.9, BX, BY, ring_r)
            rg.add_color_stop_rgba(0.0, rr, gg, bb, aa)
            rg.add_color_stop_rgba(1.0, rr, gg, bb, 0.0)
            cr.set_source(rg)
            cr.arc(BX, BY, ring_r, 0, math.tau)
            cr.fill()

        # accretion disk — bright horizontal ellipse
        disk_tilt = 0.28    # vertical scale
        disk_w    = BHR * 3.2
        disk_h    = BHR * disk_tilt
        disk_rot  = t * 0.12   # slow rotation
        for side, base_alpha in [(1, 0.75), (-1, 0.45)]:  # front/back
            cr.save()
            cr.translate(BX, BY)
            cr.rotate(disk_rot)
            cr.scale(1.0, disk_tilt)
            ag = cairo.RadialGradient(0, 0, BHR*1.05, 0, 0, disk_w)
            if side == 1:
                ag.add_color_stop_rgba(0.0,  0.980, 0.745, 0.255, base_alpha)
                ag.add_color_stop_rgba(0.35, 0.969, 0.471, 0.980, base_alpha * 0.7)
                ag.add_color_stop_rgba(0.65, 0.486, 0.416, 0.969, base_alpha * 0.4)
                ag.add_color_stop_rgba(1.0,  0.486, 0.416, 0.969, 0.0)
            else:
                ag.add_color_stop_rgba(0.0,  0.486, 0.416, 0.969, base_alpha * 0.5)
                ag.add_color_stop_rgba(1.0,  0.486, 0.416, 0.969, 0.0)
            cr.set_source(ag)
            # only draw semicircle for front/back split
            if side == 1:
                cr.arc(0, 0, disk_w, 0, math.pi)
            else:
                cr.arc(0, 0, disk_w, math.pi, math.tau)
            cr.line_to(0, 0); cr.close_path(); cr.fill()
            cr.restore()

        # photon ring — bright thin ring just outside event horizon
        ph_alpha = 0.5 + 0.2 * math.sin(t * 1.4) + bh_hover_boost * 0.35
        ph_r     = BHR * 1.22
        ph_width = BHR * 0.12
        pg = cairo.RadialGradient(BX, BY, ph_r - ph_width, BX, BY, ph_r + ph_width)
        pg.add_color_stop_rgba(0.0,  0.969, 0.471, 0.980, 0.0)
        pg.add_color_stop_rgba(0.5,  0.969, 0.471, 0.980, ph_alpha)
        pg.add_color_stop_rgba(1.0,  0.969, 0.471, 0.980, 0.0)
        cr.set_source(pg)
        cr.arc(BX, BY, ph_r + ph_width, 0, math.tau)
        cr.fill()
        # punch the inner hole
        cr.set_operator(cairo.OPERATOR_DEST_OUT)
        cr.set_source_rgba(0, 0, 0, 1)
        cr.arc(BX, BY, ph_r - ph_width, 0, math.tau)
        cr.fill()
        cr.set_operator(cairo.OPERATOR_OVER)

        # event horizon — absolute black circle
        cr.set_source_rgb(0.018, 0.014, 0.030)
        cr.arc(BX, BY, BHR, 0, math.tau)
        cr.fill()

        # innermost glow ring on event horizon edge
        eg = cairo.RadialGradient(BX, BY, BHR*0.7, BX, BY, BHR*1.05)
        eg.add_color_stop_rgba(0.0, 0.0, 0.0, 0.0, 0.0)
        eg.add_color_stop_rgba(0.8, 0.753, 0.259, 0.984, 0.35 + 0.15*math.sin(t*1.1))
        eg.add_color_stop_rgba(1.0, 0.753, 0.259, 0.984, 0.0)
        cr.set_source(eg)
        cr.arc(BX, BY, BHR*1.05, 0, math.tau)
        cr.fill()

        # gravitational lensing — distorted star arcs curving around BH
        for angle_off in [0.4, 1.1, 2.0, 3.3, 4.6, 5.5]:
            base_a = t * 0.05 + angle_off
            lens_r = BHR * (2.2 + 0.4 * math.sin(base_a * 3))
            arc_len = 0.4 + 0.2 * math.sin(base_a * 2.3)
            la = 0.07 + 0.04 * math.sin(base_a * 1.7)
            cr.set_source_rgba(0.88, 0.88, 0.97, la)
            cr.set_line_width(0.8)
            cr.new_path()
            cr.arc(BX, BY, lens_r, base_a, base_a + arc_len)
            cr.stroke()

        # ── bottom fade — blend into app background ───────────────────────
        fade = cairo.LinearGradient(0, h*0.72, 0, h)
        fade.add_color_stop_rgba(0.0, 0.027, 0.027, 0.050, 0.0)
        fade.add_color_stop_rgba(1.0, 0.027, 0.027, 0.050, 1.0)
        cr.set_source(fade)
        cr.rectangle(0, h*0.72, w, h*0.28)
        cr.fill()


# ── Application ───────────────────────────────────────────────────────────────
class SetupApp(Adw.Application):
    def __init__(self):
        super().__init__(application_id="org.fadeddream.Setup",
                         flags=Gio.ApplicationFlags.FLAGS_NONE)
        self.connect("activate", self._on_activate)

    def _on_activate(self, app):
        Adw.StyleManager.get_default().set_color_scheme(Adw.ColorScheme.FORCE_DARK)
        self.win = SetupWindow(application=app)
        _inject_css(self.win.get_display())
        self.win.present()


# ── Main Window ───────────────────────────────────────────────────────────────
class SetupWindow(Adw.ApplicationWindow):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.set_title("Faded Dream Setup — First Run")
        self.set_default_size(1080, 780)
        self.set_size_request(800, 600)

        self.selected    = set()
        self.browser     = None
        self.lo_langs    = set()
        self.tb_langs    = set()
        self._br_rows    = []   # list of (AnimatedRow, CheckMarkWidget, br_dict)
        self._count_lbl  = None
        self._installing = False
        self._secret     = ""

        key_ctrl = Gtk.EventControllerKey()
        key_ctrl.connect("key-pressed", self._on_key_pressed)
        self.add_controller(key_ctrl)

        self._build_ui()

    # ── Easter egg ────────────────────────────────────────────────────────────
    def _on_key_pressed(self, ctrl, keyval, keycode, state):
        ch = chr(keyval).upper() if keyval < 128 else ""
        self._secret += ch
        if "KOCMOC" in self._secret:
            self._secret = ""
            subprocess.Popen(["mpv", "https://www.youtube.com/watch?v=eMDu1byE45A"])
        elif not "KOCMOC".startswith(self._secret):
            self._secret = ch

    # ── UI ────────────────────────────────────────────────────────────────────
    def _build_ui(self):
        self._stack = Gtk.Stack()
        self._stack.set_transition_type(Gtk.StackTransitionType.SLIDE_LEFT_RIGHT)
        self._stack.set_transition_duration(250)
        self._stack.set_hexpand(True)
        self._stack.set_vexpand(True)

        # sidebar
        sidebar = Gtk.Box(orientation=Gtk.Orientation.VERTICAL)
        s_header = Adw.HeaderBar()
        s_header.set_show_end_title_buttons(False)
        s_title = Gtk.Label(label="Faded Dream")
        s_title.add_css_class("heading")
        s_header.set_title_widget(s_title)
        sidebar.append(s_header)

        self._nav_list = Gtk.ListBox()
        self._nav_list.add_css_class("navigation-sidebar")
        self._nav_list.set_selection_mode(Gtk.SelectionMode.SINGLE)
        self._nav_list.connect("row-selected", self._on_nav_select)

        nav_sw = Gtk.ScrolledWindow()
        nav_sw.set_policy(Gtk.PolicyType.NEVER, Gtk.PolicyType.AUTOMATIC)
        nav_sw.set_vexpand(True)
        nav_sw.set_child(self._nav_list)
        sidebar.append(nav_sw)

        pages = [
            ("🌙", "Welcome",     self._page_welcome()),
            ("🌐", "Browser",     self._page_browser()),
            ("🎮", "Gaming",      self._page_sections(GAMING)),
            ("💡", "Peripherals", self._page_sections(PERIPHERALS)),
            ("📁", "File Transfer", self._page_sections(FILE_TRANSFER)),
            ("📄", "Office",      self._page_office()),
            ("🎬", "Media",       self._page_flat(MEDIA)),
            ("💬", "Comms",       self._page_sections(COMMS, comms=True)),
            ("📋", "Log",         self._page_log()),
        ]
        self._log_page_name = "Log"

        _no_badge = {"Welcome", "Log"}
        self._nav_badges = {}   # page_name -> badge Gtk.Label

        for icon, label, page in pages:
            self._stack.add_named(page, label)
            row = Gtk.ListBoxRow()
            box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=10)
            box.set_margin_start(8); box.set_margin_end(8)
            box.set_margin_top(8);   box.set_margin_bottom(8)
            il = Gtk.Label(label=icon)
            il.set_valign(Gtk.Align.CENTER)
            # Pango font size — the only reliable way to scale emoji in GTK
            attrs = Pango.AttrList()
            attrs.insert(Pango.attr_size_new_absolute(Pango.units_from_double(20)))
            il.set_attributes(attrs)
            il.set_size_request(28, -1)
            tl = Gtk.Label(label=label)
            tl.set_halign(Gtk.Align.START)
            tl.set_valign(Gtk.Align.CENTER)
            tl.set_hexpand(True)
            box.append(il); box.append(tl)
            if label not in _no_badge:
                badge = Gtk.Label(label="")
                badge.set_css_classes(["nav-count-badge"])
                badge.set_valign(Gtk.Align.CENTER)
                badge.set_visible(False)   # hidden until count > 0
                box.append(badge)
                self._nav_badges[label] = badge
            row.set_child(box)
            row._page_name = label
            self._nav_list.append(row)

        # content side
        content = Gtk.Box(orientation=Gtk.Orientation.VERTICAL)
        c_header = Adw.HeaderBar()
        c_header.set_show_start_title_buttons(False)
        self._content_title = Adw.WindowTitle(title="Welcome", subtitle="")
        c_header.set_title_widget(self._content_title)
        content.append(c_header)
        content.append(self._stack)
        content.append(self._build_footer())

        split = Gtk.Paned(orientation=Gtk.Orientation.HORIZONTAL)
        split.set_position(200)
        split.set_shrink_start_child(False)
        split.set_shrink_end_child(False)
        split.set_start_child(sidebar)
        split.set_end_child(content)

        self.set_content(split)
        self._nav_list.select_row(self._nav_list.get_row_at_index(0))

    def _on_nav_select(self, lb, row):
        if row is None: return
        self._stack.set_visible_child_name(row._page_name)
        self._content_title.set_title(row._page_name)

    def _switch_to_log(self):
        self._navigate_to(self._log_page_name)

    def _navigate_to(self, page_name):
        for i in range(9):
            r = self._nav_list.get_row_at_index(i)
            if r and r._page_name == page_name:
                self._nav_list.select_row(r)
                break

    # ── Footer ────────────────────────────────────────────────────────────────
    def _build_footer(self):
        bar = Gtk.ActionBar()

        left = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=2)
        self._count_lbl = Gtk.Label()
        self._count_lbl.add_css_class("caption")
        self._count_lbl.set_halign(Gtk.Align.START)
        self._update_count()
        fsub = Gtk.Label(label="toggle startup off after install to stop autolaunch")
        fsub.add_css_class("caption"); fsub.add_css_class("dim-label")
        fsub.set_halign(Gtk.Align.START)
        left.append(self._count_lbl); left.append(fsub)
        bar.pack_start(left)

        tog_box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=6)
        tog_lbl = Gtk.Label(label="Run at startup")
        tog_lbl.add_css_class("caption")
        self._startup_sw = Gtk.Switch()
        self._startup_sw.set_active(self._startup_enabled())
        self._startup_sw.set_valign(Gtk.Align.CENTER)
        self._startup_sw.connect("notify::active", self._on_startup_toggle)
        tog_box.append(tog_lbl); tog_box.append(self._startup_sw)
        bar.pack_start(tog_box)

        skip_btn = Gtk.Button(label="Skip All")
        skip_btn.add_css_class("flat")
        skip_btn.connect("clicked", lambda _: self.close())
        bar.pack_end(skip_btn)

        self._install_btn = Gtk.Button(label="Install Selected")
        self._install_btn.add_css_class("suggested-action")
        self._install_btn.connect("clicked", self._on_install)
        bar.pack_end(self._install_btn)

        return bar

    # ── Count ─────────────────────────────────────────────────────────────────
    def _update_count(self):
        total = len(self.selected) + (1 if self.browser else 0)
        self._count_lbl.set_markup(
            f'<span foreground="#4fd9c4" weight="bold">{total}</span>'
            f'<span foreground="#666677"> packages selected</span>')
        self._count_lbl.remove_css_class("count-bump")
        def _bump():
            self._count_lbl.add_css_class("count-bump")
            return False
        GLib.idle_add(_bump)
        self._update_nav_badges()

    def _update_nav_badges(self):
        """Recount per-page selections and update sidebar badges."""
        # Build a page->count map from the data structures
        counts = {}

        # Browser (1 pkg)
        counts["Browser"] = 1 if self.browser else 0

        # Sections: Gaming, Peripherals, File Transfer, Comms
        for page_name, data in [
            ("Gaming",        GAMING),
            ("Peripherals",   PERIPHERALS),
            ("File Transfer", FILE_TRANSFER),
            ("Comms",         COMMS),
        ]:
            n = 0
            for sec in data:
                for pkg in sec["packages"]:
                    if pkg["pkg"] in self.selected:
                        n += 1
                    for sub in pkg.get("sub", []):
                        if sub["pkg"] in self.selected:
                            n += 1
            counts[page_name] = n

        # Office: lo_langs + office base pkg
        n = 0
        for p in OFFICE_BASE:
            if p["pkg"] in self.selected: n += 1
        n += len(getattr(self, 'lo_langs', set()))
        n += len(getattr(self, 'tb_langs', set()))
        counts["Office"] = n

        # Media: flat list
        counts["Media"] = sum(1 for p in MEDIA if p["pkg"] in self.selected)

        # Update badge labels
        for page_name, badge in self._nav_badges.items():
            n = counts.get(page_name, 0)
            if n > 0:
                badge.set_label(str(n))
                badge.set_visible(True)
                # re-trigger pop animation
                badge.remove_css_class("nav-count-badge")
                def _repop(b=badge):
                    b.add_css_class("nav-count-badge")
                    return False
                GLib.idle_add(_repop)
            else:
                badge.set_visible(False)

    # ── Startup toggle ────────────────────────────────────────────────────────
    def _startup_enabled(self):
        try:    return EXEC_LINE in open(HYPRLAND_CONF).read()
        except: return False

    def _on_startup_toggle(self, sw, _param):
        enabled = sw.get_active()
        try:
            conf = open(HYPRLAND_CONF).read()
            if enabled and EXEC_LINE not in conf:
                open(HYPRLAND_CONF, "w").write(conf + f"\n{EXEC_LINE}\n")
            elif not enabled and EXEC_LINE in conf:
                lines = [l for l in conf.splitlines() if EXEC_LINE not in l]
                open(HYPRLAND_CONF, "w").write("\n".join(lines) + "\n")
        except Exception as e:
            print(f"[startup toggle] {e}")

    # ── Welcome page ──────────────────────────────────────────────────────────
    def _page_welcome(self):
        outer = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=0)
        outer.add_css_class("welcome-page")

        # ── animated moon hero ──────────────────────────────────────────────
        hero = MoonHero()
        hero.set_size_request(-1, 220)
        outer.append(hero)

        # ── title row ───────────────────────────────────────────────────────
        title_box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=8)
        title_box.set_halign(Gtk.Align.CENTER)
        title_box.set_margin_bottom(6)

        title = Gtk.Label(label="Faded Dream")
        title.add_css_class("welcome-title")
        title_box.append(title)

        sub = Gtk.Label()
        sub.set_markup("Your dotfiles are installed.\n"
                       "Select optional packages across the tabs, then hit <b>Install</b>.\n"
                       "Toggle <i>Run at startup</i> off after install.")
        sub.add_css_class("welcome-sub")
        sub.set_justify(Gtk.Justification.CENTER)
        sub.set_wrap(True)
        title_box.append(sub)
        outer.append(title_box)

        # ── cards ────────────────────────────────────────────────────────────
        cards_data = [
            ("🌐","Browser",      "Pick your default browser"),
            ("🎮","Gaming",       "Steam, Heroic, Wine, MangoHud"),
            ("💡","Peripherals",  "OpenRazer, Polychromatic, Piper"),
            ("📁","File Transfer","Android, cameras, LAN sharing"),
            ("📄","Office",       "LibreOffice + language packs"),
            ("🎬","Media",        "GIMP, Kdenlive, OBS Liberty"),
            ("💬","Comms",        "Vesktop, Telegram, Thunderbird"),
        ]

        flow = Gtk.FlowBox()
        flow.set_max_children_per_line(4)
        flow.set_min_children_per_line(2)
        flow.set_selection_mode(Gtk.SelectionMode.NONE)
        flow.set_column_spacing(8)
        flow.set_row_spacing(8)
        flow.set_homogeneous(True)
        flow.set_margin_start(32); flow.set_margin_end(32)
        flow.set_margin_bottom(32)

        for _ci, (icon, t, d) in enumerate(cards_data):
            card = Adw.ActionRow()
            card.set_title(t); card.set_subtitle(d)
            card.set_size_request(144, 80)
            card.set_activatable(True)
            pfx = Gtk.Label(label=icon)
            pfx.add_css_class("title-2"); pfx.add_css_class("row-icon")
            pfx.set_valign(Gtk.Align.CENTER)
            card.add_prefix(pfx)

            # arrow hint
            arrow = Gtk.Image.new_from_icon_name("go-next-symbolic")
            arrow.set_pixel_size(14)
            arrow.set_valign(Gtk.Align.CENTER)
            arrow.set_opacity(0.35)
            arrow.add_css_class("welcome-card-arrow")
            card.add_suffix(arrow)

            def _nav(gesture, n, x, y, page=t):
                self._navigate_to(page)
            gc = Gtk.GestureClick()
            gc.connect("released", _nav)
            card.add_controller(gc)

            flow.append(card)
            # tag the FlowBoxChild wrapper (not the card itself) for stagger
            child = flow.get_child_at_index(_ci)
            if child:
                child.set_css_classes(["wcard", f"wcard-{_ci}"])

        outer.append(flow)
        return _scrolled(outer)

    # ── Browser page ──────────────────────────────────────────────────────────
    def _page_browser(self):
        box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=0)
        box.set_margin_top(12); box.set_margin_bottom(12)
        box.set_margin_start(12); box.set_margin_end(12)

        box.append(_section_label("Select Your Default Browser"))
        box.append(_sep())

        group = _boxed_list()
        self._br_rows = []

        for br in BROWSERS:
            arow = AnimatedRow(accent=ACCENT2_COLOR, is_pill=True)
            arow.row.set_title(br["name"])
            arow.row.set_subtitle(br["desc"])

            pfx = Gtk.Label(label=br["icon"])
            pfx.add_css_class("title-2"); pfx.add_css_class("row-icon")
            pfx.set_valign(Gtk.Align.CENTER)
            arow.row.add_prefix(pfx)

            if br.get("recommended"):
                rec = Gtk.Label(label="⭐ Recommended")
                rec.add_css_class("caption"); rec.add_css_class("success")
                rec.set_valign(Gtk.Align.CENTER)
                arow.row.add_suffix(rec)

            arow.row.add_suffix(_repo_badge(br["repo"]))

            cm = CheckMarkWidget(accent=ACCENT2_COLOR)
            cm.set_valign(Gtk.Align.CENTER)
            cm.set_margin_end(8)
            arow.row.add_suffix(cm)

            # click via gesture on the overlay
            gc = Gtk.GestureClick()
            gc.connect("released", self._on_browser_click, arow, cm, br)
            arow.add_controller(gc)

            self._br_rows.append((arow, cm, br))
            group.append(arow)

        box.append(group)
        return _scrolled(box)

    def _on_browser_click(self, gesture, n, x, y, arow, cm, br):
        if self.browser and self.browser["pkg"] == br["pkg"]:
            self.browser = None
            arow.set_selected(False); cm.set_checked(False)
        else:
            for other_arow, other_cm, other_br in self._br_rows:
                if other_br["pkg"] != br["pkg"]:
                    other_arow.set_selected(False); other_cm.set_checked(False)
            self.browser = br
            arow.set_selected(True); cm.set_checked(True)
        self._update_count()

    # ── Sections page ─────────────────────────────────────────────────────────
    def _page_sections(self, sections, comms=False):
        box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=0)
        box.set_margin_top(12); box.set_margin_bottom(12)
        box.set_margin_start(12); box.set_margin_end(12)

        for sec in sections:
            box.append(_section_label(sec["section"]))
            box.append(_sep())
            group = _boxed_list()

            for pkg in sec["packages"]:
                arow, cm = self._make_pkg_row(pkg)
                sub_rows = []
                group.append(arow)

                for sub in pkg.get("sub", []):
                    sarow, scm = self._make_sub_row(sub)
                    sub_rows.append((sarow, scm, sub["pkg"]))
                    group.append(sarow)

                # wire up parent→children selection
                def _bind(a, c, p, subs):
                    def _clicked(gesture, n, x, y):
                        sel = p not in self.selected
                        if sel:
                            self.selected.add(p)
                            a.set_selected(True); c.set_checked(True)
                            for sa, sc, sp in subs:
                                self.selected.add(sp)
                                sa.set_selected(True); sc.set_checked(True)
                        else:
                            self.selected.discard(p)
                            a.set_selected(False); c.set_checked(False)
                            for sa, sc, sp in subs:
                                self.selected.discard(sp)
                                sa.set_selected(False); sc.set_checked(False)
                        self._update_count()
                    gc = Gtk.GestureClick()
                    gc.connect("released", _clicked)
                    a.add_controller(gc)
                _bind(arow, cm, pkg["pkg"], sub_rows)

                for sarow, scm, sp in sub_rows:
                    def _sub_bind(a, c, p):
                        def _clicked(gesture, n, x, y):
                            sel = p not in self.selected
                            if sel: self.selected.add(p);    a.set_selected(True);  c.set_checked(True)
                            else:   self.selected.discard(p); a.set_selected(False); c.set_checked(False)
                            self._update_count()
                        gc = Gtk.GestureClick()
                        gc.connect("released", _clicked)
                        a.add_controller(gc)
                    _sub_bind(sarow, scm, sp)

                if comms and pkg["pkg"] == "thunderbird":
                    group.append(self._lang_grid_group("tb"))

            box.append(group)

        return _scrolled(box)

    # ── Flat page (media) ──────────────────────────────────────────────────────
    def _page_flat(self, packages):
        box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=0)
        box.set_margin_top(12); box.set_margin_bottom(12)
        box.set_margin_start(12); box.set_margin_end(12)
        box.append(_section_label("Creative Tools"))
        box.append(_sep())
        group = _boxed_list()
        for pkg in packages:
            arow, cm = self._make_pkg_row(pkg)
            def _bind(a, c, p):
                def _clicked(gesture, n, x, y):
                    sel = p not in self.selected
                    if sel: self.selected.add(p);    a.set_selected(True);  c.set_checked(True)
                    else:   self.selected.discard(p); a.set_selected(False); c.set_checked(False)
                    self._update_count()
                gc = Gtk.GestureClick()
                gc.connect("released", _clicked)
                a.add_controller(gc)
            _bind(arow, cm, pkg["pkg"])
            group.append(arow)
        box.append(group)
        return _scrolled(box)

    # ── Office page ───────────────────────────────────────────────────────────
    def _page_office(self):
        box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=0)
        box.set_margin_top(12); box.set_margin_bottom(12)
        box.set_margin_start(12); box.set_margin_end(12)

        box.append(_section_label("Base"))
        box.append(_sep())
        group = _boxed_list()
        for pkg in OFFICE_BASE:
            arow, cm = self._make_pkg_row(pkg)
            def _bind(a, c, p):
                def _clicked(gesture, n, x, y):
                    sel = p not in self.selected
                    if sel: self.selected.add(p);    a.set_selected(True);  c.set_checked(True)
                    else:   self.selected.discard(p); a.set_selected(False); c.set_checked(False)
                    self._update_count()
                gc = Gtk.GestureClick()
                gc.connect("released", _clicked)
                a.add_controller(gc)
            _bind(arow, cm, pkg["pkg"])
            group.append(arow)
        box.append(group)

        box.append(_section_label("LibreOffice Language Packs"))
        box.append(_sep())
        box.append(self._lang_grid("lo"))
        return _scrolled(box)

    # ── Language grid ──────────────────────────────────────────────────────────
    def _lang_grid(self, kind):
        flow = Gtk.FlowBox()
        flow.set_max_children_per_line(4)
        flow.set_min_children_per_line(2)
        flow.set_selection_mode(Gtk.SelectionMode.NONE)
        flow.set_column_spacing(6); flow.set_row_spacing(6)
        flow.set_margin_top(4); flow.set_margin_bottom(8)
        if kind == "tb": flow.set_margin_start(24)

        for i, (flag, name) in enumerate(LANG_LIST):
            pkg   = (f"libreoffice-fresh-{LO_CODES[i]}" if kind == "lo"
                     else f"thunderbird-i18n-{TB_CODES[i]}")
            store = self.lo_langs if kind == "lo" else self.tb_langs

            tile = Gtk.Overlay()
            inner_box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=8)
            inner_box.set_margin_start(10); inner_box.set_margin_end(10)
            inner_box.set_margin_top(4); inner_box.set_margin_bottom(4)

            cm = CheckMarkWidget()
            cm.set_valign(Gtk.Align.CENTER)
            lbl = Gtk.Label(label=f"{flag}  {name}")
            lbl.add_css_class("caption")
            lbl.set_halign(Gtk.Align.CENTER)
            inner_box.append(cm); inner_box.append(lbl)

            glow = GlowOverlay()
            shimmer = ShimmerWidget()
            tile.set_child(inner_box)
            tile.add_overlay(glow)
            tile.add_overlay(shimmer)

            def _bind(t, g, s, c, l, p, st):
                def _clicked(gesture, n, x, y):
                    if p in st:
                        st.discard(p); self.selected.discard(p)
                        g.set_selected(False); c.set_checked(False)
                        l.remove_css_class("accent")
                    else:
                        st.add(p); self.selected.add(p)
                        g.set_selected(True); c.set_checked(True)
                        s.play()
                        l.add_css_class("accent")
                    self._update_count()
                gc = Gtk.GestureClick()
                gc.connect("released", _clicked)
                t.add_controller(gc)
            _bind(tile, glow, shimmer, cm, lbl, pkg, store)

            flow.append(tile)

        return flow

    def _lang_grid_group(self, kind):
        """Wrap lang grid in a ListBoxRow for insertion into a boxed-list."""
        lbr = Gtk.ListBoxRow()
        lbr.set_activatable(False)
        lbr.set_child(self._lang_grid(kind))
        return lbr

    # ── Package row builder ───────────────────────────────────────────────────
    def _make_pkg_row(self, pkg):
        arow = AnimatedRow()
        arow.row.set_title(pkg["name"])
        arow.row.set_subtitle(pkg.get("desc", ""))
        arow.row.set_title_lines(1)
        arow.row.set_subtitle_lines(2)

        icon = Gtk.Label(label=pkg.get("icon", "📦"))
        icon.add_css_class("title-2"); icon.add_css_class("row-icon")
        icon.set_valign(Gtk.Align.CENTER)
        arow.row.add_prefix(icon)

        cm = CheckMarkWidget()
        cm.set_valign(Gtk.Align.CENTER)
        cm.set_margin_end(8)
        arow.row.add_suffix(_repo_badge(pkg["repo"]))
        arow.row.add_suffix(cm)

        return arow, cm

    def _make_sub_row(self, sub):
        arow = AnimatedRow()
        arow.row.set_title(sub["name"])
        arow.row.set_margin_start(24)

        # accent bar prefix
        bar_box = Gtk.Box()
        bar_box.set_size_request(2, 20)
        bar_box.set_css_classes(["sub-bar"])
        bar_box.set_valign(Gtk.Align.CENTER)
        arow.row.add_prefix(bar_box)

        cm = CheckMarkWidget()
        cm.set_valign(Gtk.Align.CENTER)
        cm.set_margin_end(8)
        arow.row.add_suffix(_repo_badge(sub["repo"]))
        arow.row.add_suffix(cm)

        return arow, cm

    # ── Log page ───────────────────────────────────────────────────────────────
    def _page_log(self):
        self._log_outer = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=0)

        # description panel
        self._log_desc = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=0)
        self._log_desc.set_margin_top(12); self._log_desc.set_margin_bottom(12)
        self._log_desc.set_margin_start(12); self._log_desc.set_margin_end(12)
        self._log_desc.append(_section_label("What This Installer Does"))
        self._log_desc.append(_sep())

        desc_lines = [
            ("🌐","Browser",
             "Pick one browser — LibreWolf, Zen, Firefox, Vivaldi, Chrome or Edge. "
             "Your choice is installed and $Browser in hyprland.conf is patched "
             "automatically so Super+B opens it."),
            ("🎮","Gaming",
             "Steam (lib32), Heroic Games Launcher, Wine + Winetricks/Mono/Gecko, "
             "ProtonPlus, GameMode + 32-bit, MangoHud + 32-bit, MangoJuice. "
             "Selecting Wine auto-selects its three sub-packages."),
            ("💡","Peripherals",
             "OpenRazer daemon + kernel driver (DKMS) + Python library for Razer hardware. "
             "Polychromatic for per-key RGB and effects. "
             "Piper for multi-brand mouse/keyboard config (Logitech, SteelSeries, Roccat…). "
             "Solaar for Logitech Unifying/Bolt receivers. "
             "jmtpfs and gphotofs for mounting Android phones and cameras — all AUR."),
            ("📄","Office",
             "LibreOffice Fresh plus any of 12 language packs you select "
             "(English UK, Romanian, French, German, Spanish, Italian, Portuguese, "
             "Russian, Japanese, Chinese, Korean, Arabic)."),
            ("🎬","Media",
             "Mirage image viewer, GIMP, Inkscape, Kdenlive video editor, "
             "HandBrake converter, OBS Studio Liberty (libre build)."),
            ("📁","File Transfer",
             "Android MTP with jmtpfs and go-mtpfs. Camera PTP via gphotofs and gphoto2. "
             "Wireless: Warpinator, LocalSend (cross-platform AirDrop), Croc (encrypted P2P). "
             "USB: Android Tools (ADB/fastboot) and Scrcpy for screen mirroring."),
            ("💬","Comms",
             "Vesktop (Discord + Vencord), Telegram, Element (Matrix), "
             "Thunderbird + optional language packs, Obsidian notes."),
            ("🔧","How It Works",
             "Repo packages are installed in one pacman batch. "
             "Each AUR package (paru) is built and installed individually — "
             "you will see full compile output here in real time. "
             "After install the startup toggle is disabled automatically so it won't launch again. "
             "You can re-enable it anytime from the footer."),
        ]

        group = _boxed_list()
        for icon, title, body in desc_lines:
            row = Adw.ActionRow()
            row.set_title(title); row.set_subtitle(body)
            row.set_subtitle_lines(4)
            pfx = Gtk.Label(label=icon)
            pfx.add_css_class("title-2"); pfx.set_valign(Gtk.Align.CENTER)
            row.add_prefix(pfx)
            group.append(row)
        self._log_desc.append(group)
        self._log_outer.append(_scrolled(self._log_desc))

        # terminal
        self._log_tv = Gtk.TextView()
        self._log_tv.set_editable(False)
        self._log_tv.set_cursor_visible(False)
        self._log_tv.set_monospace(True)
        self._log_tv.set_wrap_mode(Gtk.WrapMode.WORD_CHAR)
        self._log_tv.set_margin_start(14); self._log_tv.set_margin_end(14)
        self._log_tv.set_margin_top(10);   self._log_tv.set_margin_bottom(10)

        self._log_buf = self._log_tv.get_buffer()
        self._log_buf.create_tag("header", weight=Pango.Weight.BOLD, foreground="#7c6af7")
        self._log_buf.create_tag("repo",   foreground="#6aaff7")
        self._log_buf.create_tag("aur",    foreground="#4fd9c4")
        self._log_buf.create_tag("patch",  foreground="#b46af7")
        self._log_buf.create_tag("done",   weight=Pango.Weight.BOLD, foreground="#4fd9c4")
        self._log_buf.create_tag("raw",    foreground="#888899")

        self._log_sw = Gtk.ScrolledWindow()
        self._log_sw.set_policy(Gtk.PolicyType.NEVER, Gtk.PolicyType.AUTOMATIC)
        self._log_sw.set_vexpand(True)
        self._log_sw.set_child(self._log_tv)
        self._log_sw.set_visible(False)
        self._log_outer.append(self._log_sw)

        self._prog_bar = Gtk.ProgressBar()
        self._prog_bar.set_margin_start(16); self._prog_bar.set_margin_end(16)
        self._prog_bar.set_margin_bottom(8)
        self._prog_bar.set_show_text(True)
        self._prog_bar.set_visible(False)
        self._log_outer.append(self._prog_bar)

        return self._log_outer

    def _log_append(self, text, kind):
        def _do():
            end = self._log_buf.get_end_iter()
            self._log_buf.insert_with_tags_by_name(end, text + "\n", kind)
            adj = self._log_sw.get_vadjustment()
            adj.set_value(adj.get_upper())
            return False
        GLib.idle_add(_do)

    # ── Install ───────────────────────────────────────────────────────────────
    def _on_install(self, _btn):
        if not self.selected and not self.browser:
            self.close(); return
        if self._installing: return
        self._installing = True
        self._install_btn.set_sensitive(False)

        self._switch_to_log()
        self._log_desc.get_parent().set_visible(False)
        self._log_sw.set_visible(True)
        self._prog_bar.set_visible(True)

        all_pkgs  = ([self.browser["pkg"]] if self.browser else []) + list(self.selected)
        repo_pkgs = [p for p in all_pkgs if not AUR_MAP.get(p, False)]
        aur_pkgs  = [p for p in all_pkgs if     AUR_MAP.get(p, False)]

        self._log_append("╔══════════════════════════════════════════════╗", "header")
        self._log_append("  Faded Dream — Installing selected packages",   "header")
        self._log_append("╚══════════════════════════════════════════════╝", "header")
        self._log_append("", "raw")
        if repo_pkgs:
            self._log_append(f"  repo packages  ({len(repo_pkgs)}): {', '.join(repo_pkgs)}", "repo")
        if aur_pkgs:
            self._log_append(f"  AUR packages   ({len(aur_pkgs)}): {', '.join(aur_pkgs)}", "aur")
        if self.browser:
            self._log_append(f"  browser patch: $Browser = {self.browser['exec']}", "patch")
        self._log_append("", "raw")

        threading.Thread(target=self._install_thread, args=(repo_pkgs, aur_pkgs), daemon=True).start()

    def _install_thread(self, repo_pkgs, aur_pkgs):
        total = max(len(repo_pkgs) + len(aur_pkgs) + (1 if self.browser else 0), 1)
        done  = [0]

        def ui(msg, frac=None):
            f = frac if frac is not None else done[0] / total
            GLib.idle_add(self._prog_bar.set_fraction, f)
            GLib.idle_add(self._prog_bar.set_text, msg)

        def stream(cmd, kind="raw"):
            try:
                proc = subprocess.Popen(cmd, stdout=subprocess.PIPE,
                                        stderr=subprocess.STDOUT, text=True, bufsize=1)
                for line in proc.stdout:
                    s = line.rstrip("\n")
                    if s: self._log_append(s, kind)
                proc.wait()
            except Exception as exc:
                self._log_append(f"[error] {exc}", "raw")

        if repo_pkgs:
            self._log_append(f"── pacman  ({len(repo_pkgs)} packages) " + "─"*30, "header")
            ui(f"Installing {len(repo_pkgs)} repo packages...")
            stream(["sudo","pacman","-S","--noconfirm","--needed","--color=never"] + repo_pkgs, "repo")
            done[0] += len(repo_pkgs)

        for pkg in aur_pkgs:
            self._log_append(f"── paru  {pkg} " + "─"*40, "header")
            ui(f"Installing {pkg}...")
            stream(["paru","-S","--noconfirm","--needed","--color=never", pkg], "aur")
            done[0] += 1

        if self.browser:
            self._log_append("── hyprland.conf " + "─"*35, "header")
            ui(f"Patching hyprland.conf → {self.browser['exec']}...")
            if os.path.exists(HYPRLAND_CONF):
                subprocess.run(["sed","-i",
                    f"s|^\\$Browser = .*|\\$Browser = {self.browser['exec']}|",
                    HYPRLAND_CONF])
            self._log_append(f"  $Browser = {self.browser['exec']}", "patch")
            done[0] += 1

        self._log_append("", "raw")
        self._log_append("✓  All done!", "done")
        ui("✓ All done!", 1.0)
        GLib.idle_add(self._on_install_done)

    def _on_install_done(self):
        self._startup_sw.handler_block_by_func(self._on_startup_toggle)
        self._startup_sw.set_active(False)
        self._startup_sw.handler_unblock_by_func(self._on_startup_toggle)
        self._on_startup_toggle(self._startup_sw, None)
        GLib.timeout_add(2000, self.close)
        return False


# ── Entry ─────────────────────────────────────────────────────────────────────
if __name__ == "__main__":
    app = SetupApp()
    sys.exit(app.run(sys.argv))
