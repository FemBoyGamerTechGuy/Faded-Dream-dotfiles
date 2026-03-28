#!/usr/bin/env python3
# widgets.py — CSS, Cairo widgets, animated rows, moon hero
import math, random, cairo
import gi
gi.require_version("Gtk", "4.0")
gi.require_version("Adw", "1")
from gi.repository import Gtk, Adw, GLib, Pango

from i18n import T, _LANG
from packages import REPO_STYLE, _BADGE_KEY, ACCENT_COLOR, ACCENT2_COLOR

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

/* Search entry — used in Brother dialog header */
searchentry,
searchentry text,
entry,
entry text {
    background-color: #12111f;
    color: #d8d4f0;
    caret-color: #d8d4f0;
    border-color: #1e1c30;
}
searchentry:focus-within,
entry:focus-within {
    border-color: rgba(124,106,247,0.6);
    box-shadow: 0 0 0 2px rgba(124,106,247,0.15);
}
searchentry image { color: #9490b0; }
searchentry placeholder { color: #5a5875; }

/* Adw.Dialog — make sure the whole dialog follows app theme */
.adw-dialog,
dialog,
dialog > box,
dialog > box > contents {
    background-color: #0f0e1a;
    color: #d8d4f0;
}

/* GtkGizmo slider warning suppression — set a minimum size on scrollbar sliders */
scrollbar slider {
    min-width: 6px;
    min-height: 6px;
}

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
.nav-icon { font-size: 18px; }
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
.repo-github   { color: #f0f6fc; background-color: #0d1117; border: 1px solid #30363d; }
.faded-dream-badge { color: #bb9af7; font-size: 9px; font-weight: bold; letter-spacing: 0.4px;
    background-color: rgba(187,154,247,0.10); border: 1px solid rgba(187,154,247,0.30);
    border-radius: 5px; padding: 1px 7px; animation: fade-in 350ms ease both; }
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

/* DropDown popover — override system GTK theme on the language selector */
dropdown popover contents { background-color: #0f0e1a; }
dropdown popover listview { background-color: #0f0e1a; color: #d8d4f0; }
dropdown popover listview row { background-color: #0f0e1a; color: #d8d4f0; }
dropdown popover listview row:hover { background-color: #1a1830; }
dropdown popover listview row:selected { background-color: #2a2545; color: #d8d4f0; }
dropdown popover scrolledwindow { background-color: #0f0e1a; }
dropdown popover undershoot, dropdown popover overshoot { background-color: #0f0e1a; }

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
    # Special cases with fixed labels that don't need translation
    _FIXED = {"github": "GitHub"}
    label = _FIXED.get(repo) or T(_BADGE_KEY.get(repo, 'badge_extra'))
    lbl = Gtk.Label(label=label)
    lbl.set_css_classes(["repo-badge", f"repo-{repo.lower()}"])
    lbl.set_valign(Gtk.Align.CENTER)
    return lbl

def _faded_dream_badge():
    """Special ✦ Faded Dream suffix badge for ecosystem packages."""
    lbl = Gtk.Label(label="★ Faded Dream")
    lbl.set_css_classes(["faded-dream-badge"])
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
            if self.get_realized():
                self.queue_draw()
            if step_count[0] >= steps:
                self._progress = target
                if self.get_realized():
                    self.queue_draw()
                return False
            return self.get_realized()

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
        if self.get_realized():
            self.queue_draw()
        if self._pos > 1.3:
            self._active = False
            self._pos    = -1.0
            if self.get_realized():
                self.queue_draw()
            return False
        return self.get_realized()

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
            if self.get_realized():
                self.queue_draw()
            return sc[0] < steps and self.get_realized()

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
        self._tick_id = None
        self.connect("map",       self._on_map)
        self.connect("unmap",     self._on_unmap)
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
        w = self.get_width(); h = self.get_height()
        if w > 0 and h > 0:
            self._mx = x / w
            self._my = y / h

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
        if self.get_realized():
            self.queue_draw()
        return self.get_realized()

    def _on_map(self, _widget):
        if self._tick_id is None:
            self._tick_id = GLib.timeout_add(16, self._tick)

    def _on_unmap(self, _widget):
        if self._tick_id is not None:
            GLib.source_remove(self._tick_id)
            self._tick_id = None

    def _on_unrealize(self, _widget):
        if self._tick_id is not None:
            GLib.source_remove(self._tick_id)
            self._tick_id = None
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
