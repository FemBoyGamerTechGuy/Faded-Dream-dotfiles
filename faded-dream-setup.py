#!/usr/bin/env python3
# =============================================================================
# Faded Dream — First Run Setup
# PyQt6 · Fusion · animated checkmarks · shimmer · glow · pill browser rows
# Runs once on first login via exec-once in hyprland.conf, self-destructs after.
# dep: sudo pacman -S python-pyqt6
#
# hyprland.conf:
#   exec-once = [ -f ~/faded-dream-setup.py ] && python3 ~/faded-dream-setup.py
# =============================================================================

import sys, os, subprocess, math, random
from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QLabel, QScrollArea, QTabWidget, QFrame,
    QProgressBar, QPushButton, QGridLayout
)
from PyQt6.QtCore import (
    Qt, QThread, pyqtSignal, QObject, QPropertyAnimation,
    QEasingCurve, QTimer, QPointF, QRectF, pyqtProperty
)
from PyQt6.QtGui import (
    QCursor, QPainter, QColor, QPen, QBrush, QLinearGradient,
    QPainterPath
)

# ── Package data ──────────────────────────────────────────────────────────────
BROWSERS = [
    {"pkg":"librewolf",                "exec":"librewolf",            "name":"LibreWolf",      "desc":"Privacy-focused Firefox fork — no telemetry, hardened", "icon":"🦊","repo":"galaxy","aur":False,"recommended":True},
    {"pkg":"zen-browser-bin",          "exec":"zen-browser",          "name":"Zen Browser",    "desc":"Beautiful Firefox-based browser with a modern UI",       "icon":"🧘","repo":"AUR",   "aur":True, "recommended":False},
    {"pkg":"firefox",                  "exec":"firefox",              "name":"Firefox",        "desc":"Mozilla's open source browser",                          "icon":"🔥","repo":"galaxy","aur":False,"recommended":False},
    {"pkg":"vivaldi",                  "exec":"vivaldi",              "name":"Vivaldi",        "desc":"Feature-rich Chromium browser",                          "icon":"🎻","repo":"extra", "aur":False,"recommended":False},
    {"pkg":"google-chrome",            "exec":"google-chrome-stable", "name":"Google Chrome",  "desc":"Google's browser",                                       "icon":"🌐","repo":"AUR",   "aur":True, "recommended":False},
    {"pkg":"microsoft-edge-stable-bin","exec":"microsoft-edge-stable","name":"Microsoft Edge", "desc":"Microsoft's Chromium browser",                           "icon":"🔷","repo":"AUR",   "aur":True, "recommended":False},
]

GAMING = [
    {"section":"Launchers","packages":[
        {"pkg":"steam",                    "name":"Steam",      "desc":"Valve game platform",        "icon":"🎮","repo":"lib32","aur":False,"sub":[]},
        {"pkg":"heroic-games-launcher-bin","name":"Heroic",     "desc":"Epic & GOG launcher",        "icon":"🦸","repo":"AUR",  "aur":True, "sub":[]},
    ]},
    {"section":"Compatibility","packages":[
        {"pkg":"wine","name":"Wine","desc":"Windows compatibility layer","icon":"🍷","repo":"world","aur":False,"sub":[
            {"pkg":"winetricks","name":"Winetricks","repo":"world","aur":False},
            {"pkg":"wine-mono", "name":"Wine Mono", "repo":"extra","aur":False},
            {"pkg":"wine-gecko","name":"Wine Gecko","repo":"extra","aur":False},
        ]},
        {"pkg":"protonplus","name":"ProtonPlus","desc":"Proton version manager GUI","icon":"⚗️","repo":"AUR","aur":True,"sub":[]},
    ]},
    {"section":"Performance","packages":[
        {"pkg":"gamemode","name":"GameMode","desc":"CPU/GPU performance optimizer","icon":"⚡","repo":"world","aur":False,"sub":[
            {"pkg":"lib32-gamemode","name":"GameMode (32-bit)","repo":"lib32","aur":False},
        ]},
        {"pkg":"mangohud","name":"MangoHud","desc":"In-game FPS/stats overlay","icon":"📊","repo":"world","aur":False,"sub":[
            {"pkg":"lib32-mangohud","name":"MangoHud (32-bit)","repo":"multilib","aur":False},
        ]},
        {"pkg":"mangojuice","name":"MangoJuice","desc":"GUI configurator for MangoHud","icon":"🥭","repo":"AUR","aur":True,"sub":[]},
    ]},
]

LANG_LIST = [
    ("🇬🇧","English UK"),  ("🇷🇴","Romanian"),          ("🇫🇷","French"),   ("🇩🇪","German"),
    ("🇪🇸","Spanish"),     ("🇮🇹","Italian"),            ("🇵🇹","Portuguese"),("🇷🇺","Russian"),
    ("🇯🇵","Japanese"),    ("🇨🇳","Chinese (Simplified)"),("🇰🇷","Korean"),   ("🇸🇦","Arabic"),
]
LO_CODES = ["en-gb","ro","fr","de","es","it","pt","ru","ja","zh-cn","ko","ar"]
TB_CODES = ["en-gb","ro","fr","de","es-es","it","pt-pt","ru","ja","zh-cn","ko","ar"]

OFFICE_BASE = [
    {"pkg":"libreoffice-fresh","name":"LibreOffice Fresh",
     "desc":"Latest stable — Writer, Calc, Impress, Draw","icon":"📄","repo":"galaxy","aur":False},
]

MEDIA = [
    {"pkg":"mirage",            "name":"Mirage",      "desc":"Feature-rich image viewer",  "icon":"🖼️","repo":"AUR",  "aur":True, "sub":[]},
    {"pkg":"gimp",              "name":"GIMP",        "desc":"Image editor",               "icon":"🎨","repo":"world","aur":False,"sub":[]},
    {"pkg":"inkscape",          "name":"Inkscape",    "desc":"Vector graphics editor",     "icon":"✏️","repo":"world","aur":False,"sub":[]},
    {"pkg":"kdenlive",          "name":"Kdenlive",    "desc":"Video editor",               "icon":"🎬","repo":"world","aur":False,"sub":[]},
    {"pkg":"handbrake",         "name":"HandBrake",   "desc":"Video converter/compressor", "icon":"🔧","repo":"world","aur":False,"sub":[]},
    {"pkg":"obs-studio-liberty","name":"OBS Liberty", "desc":"Streaming & recording",      "icon":"🎙️","repo":"AUR",  "aur":True, "sub":[]},
]

COMMS = [
    {"section":"Messaging","packages":[
        {"pkg":"vesktop",         "name":"Vesktop",    "desc":"Discord client (Vencord)",  "icon":"💬","repo":"AUR",   "aur":True, "sub":[]},
        {"pkg":"telegram-desktop","name":"Telegram",   "desc":"Messaging platform",         "icon":"📡","repo":"galaxy","aur":False,"sub":[]},
        {"pkg":"element-desktop", "name":"Element",    "desc":"Matrix decentralized chat",  "icon":"🔒","repo":"extra", "aur":False,"sub":[]},
    ]},
    {"section":"Email","packages":[
        {"pkg":"thunderbird","name":"Thunderbird","desc":"Email client with language packs","icon":"⚡","repo":"galaxy","aur":False,"sub":[]},
    ]},
    {"section":"Notes","packages":[
        {"pkg":"obsidian","name":"Obsidian","desc":"Markdown note taking","icon":"💎","repo":"extra","aur":False,"sub":[]},
    ]},
]

PERIPHERALS = [
    {"section":"RGB / Razer","packages":[
        {"pkg":"openrazer-daemon","name":"OpenRazer Daemon","desc":"Background service that\ncommunicates with Razer hardware","icon":"🐍","repo":"extra","aur":False,"sub":[
            {"pkg":"openrazer-driver-dkms","name":"OpenRazer Driver","repo":"extra","aur":False},
            {"pkg":"python-openrazer",     "name":"Python OpenRazer","repo":"extra","aur":False},
        ]},
        {"pkg":"polychromatic","name":"Polychromatic","desc":"OpenRazer GUI — per-key RGB,\neffects and DPI profiles","icon":"🌈","repo":"AUR","aur":True,"sub":[]},
    ]},
    {"section":"Peripherals","packages":[
        {"pkg":"piper","name":"Piper","desc":"Mouse & keyboard configurator — DPI,\nbutttons, polling rate. Multi-brand support","icon":"🖱️","repo":"extra","aur":False,"sub":[]},
        {"pkg":"solaar","name":"Solaar","desc":"Logitech device manager — Unifying/Bolt\nreceiver pairing and battery levels","icon":"⌨️","repo":"galaxy","aur":False,"sub":[]},
    ]},
]

REPO_STYLE = {
    "AUR":     ("color:#4fd9c4","#0e2e2e","#1a4040"),
    "extra":   ("color:#a89ff7","#18183a","#28285a"),
    "galaxy":  ("color:#f7b96a","#2e2200","#4a3800"),
    "world":   ("color:#6aaff7","#001a2e","#002a48"),
    "lib32":   ("color:#f76a6a","#2e0e0e","#4a1818"),
    "multilib":("color:#b46af7","#1e0e2e","#381848"),
}

ACCENT  = QColor("#7c6af7")
ACCENT2 = QColor("#4fd9c4")

# ── QSS ───────────────────────────────────────────────────────────────────────
QSS = """
QMainWindow,QWidget{
    background:#0d0d12;
    color:#e8e8f0;
    font-family:"JetBrainsMono Nerd Font","Noto Mono",monospace;
    font-size:13px;
}
QLabel{ background:transparent; color:#e8e8f0; }
QScrollArea{ border:none; background:#0d0d12; }
QScrollBar:vertical{ background:#0d0d12; width:5px; border:none; }
QScrollBar::handle:vertical{ background:#2a2a3a; border-radius:2px; min-height:20px; }
QScrollBar::handle:vertical:hover{ background:#7c6af7; }
QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical{ height:0; }
QTabWidget::pane{ border:none; background:#0d0d12; }
QTabBar{ background:#13131a; }
QTabBar::tab{
    background:transparent; color:#444455;
    padding:10px 14px; border:none;
    border-bottom:2px solid transparent;
    font-size:12px; font-weight:bold;
}
QTabBar::tab:hover{ color:#aaaacc; }
QTabBar::tab:selected{ color:#e8e8f0; border-bottom:2px solid #7c6af7; background:#16152a; }
QWidget#titlebar{ background:#13131a; border-bottom:1px solid #1e1e2c; }
QLabel#title{ color:#555566; font-size:12px; font-weight:bold; background:transparent; }
QPushButton#close{
    background:#f76a6a; border-radius:6px; border:none;
    min-width:13px; max-width:13px; min-height:13px; max-height:13px; padding:0;
}
QPushButton#close:hover{ background:#ff3333; }
QWidget#footer{ background:#13131a; border-top:1px solid #1e1e2c; }
QLabel#count{ font-size:11px; background:transparent; }
QLabel#fsub{ font-size:10px; color:#444455; background:transparent; }
QPushButton#skip{
    background:#1a1a24; border:1px solid #2a2a3a; border-radius:8px;
    color:#888899; padding:5px 14px; font-size:12px; font-weight:bold;
}
QPushButton#skip:hover{ border-color:#555566; color:#e8e8f0; background:#222233; }
QPushButton#install{
    background:#7c6af7; border:none; border-radius:8px;
    color:#fff; padding:5px 18px; font-size:12px; font-weight:bold;
}
QPushButton#install:hover{ background:#9080ff; }
QPushButton#install:disabled{ background:#2a2a3a; color:#444455; }
QProgressBar{
    background:#1a1a24; border:none; border-radius:3px;
    max-height:4px; text-align:center;
}
QProgressBar::chunk{ background:#7c6af7; border-radius:3px; }
QLabel#plbl{ font-size:10px; color:#555566; background:transparent; }
QLabel#sec{ font-size:10px; font-weight:bold; color:#444455; letter-spacing:2px; }
QLabel#pkg-name{ font-size:13px; font-weight:bold; color:#e8e8f0; background:transparent; }
QLabel#pkg-desc{ font-size:11px; color:#555566; background:transparent; }
QLabel#sub-name{ font-size:11px; font-weight:bold; color:#9999bb; background:transparent; }
QLabel#icon{ font-size:18px; background:transparent; }
QLabel#wsub{ font-size:12px; color:#555566; }
QLabel#ctitle{ font-size:12px; font-weight:bold; }
QLabel#cdesc{ font-size:10px; color:#555566; }
"""

# ── Particle ──────────────────────────────────────────────────────────────────
class Particle:
    def __init__(self, x, y, color):
        angle      = random.uniform(0, math.tau)
        speed      = random.uniform(1.5, 4.5)
        self.x     = x
        self.y     = y
        self.vx    = math.cos(angle) * speed
        self.vy    = math.sin(angle) * speed
        self.life  = 1.0
        self.decay = random.uniform(0.04, 0.09)
        self.r     = random.uniform(2, 5)
        self.color = color

    def update(self):
        self.x    += self.vx
        self.y    += self.vy
        self.vy   += 0.12       # gravity
        self.vx   *= 0.96
        self.life -= self.decay
        return self.life > 0

# ── Animated checkmark ────────────────────────────────────────────────────────
class CheckMark(QWidget):
    def __init__(self, parent=None, color=None):
        super().__init__(parent)
        self.setFixedSize(24, 24)
        self._progress  = 0.0
        self._color     = color or ACCENT
        self._particles = []
        self._checked   = False

        self._anim = QPropertyAnimation(self, b"check_progress")
        self._anim.setDuration(280)
        self._anim.setEasingCurve(QEasingCurve.Type.OutBack)

        self._ptimer = QTimer(self)
        self._ptimer.timeout.connect(self._tick)

    @pyqtProperty(float)
    def check_progress(self):
        return self._progress

    @check_progress.setter
    def check_progress(self, v):
        self._progress = max(0.0, min(1.0, v))
        self.update()

    def set_checked(self, checked, burst_pos=None):
        if checked == self._checked:
            return
        self._checked = checked
        self._anim.stop()
        self._anim.setStartValue(self._progress)
        self._anim.setEndValue(1.0 if checked else 0.0)
        self._anim.start()
        if checked:
            cx = burst_pos.x() if burst_pos else self.width() // 2
            cy = burst_pos.y() if burst_pos else self.height() // 2
            for _ in range(18):
                self._particles.append(Particle(cx, cy, self._color))
            if not self._ptimer.isActive():
                self._ptimer.start(16)

    def _tick(self):
        self._particles = [p for p in self._particles if p.update()]
        self.update()
        if not self._particles:
            self._ptimer.stop()

    def paintEvent(self, _e):
        p = QPainter(self)
        p.setRenderHint(QPainter.RenderHint.Antialiasing)

        def cl(v): return max(0.0, min(1.0, v))

        # particles
        for pt in self._particles:
            c = QColor(self._color)
            c.setAlphaF(cl(pt.life * 0.85))
            p.setBrush(QBrush(c))
            p.setPen(Qt.PenStyle.NoPen)
            p.drawEllipse(QPointF(pt.x, pt.y), pt.r * pt.life, pt.r * pt.life)

        prog = cl(self._progress)

        if prog <= 0.01:
            p.setBrush(Qt.BrushStyle.NoBrush)
            p.setPen(QPen(QColor("#333348"), 1.5))
            p.drawEllipse(QRectF(3, 3, 18, 18))
            return

        # filled bg circle
        c = QColor(self._color); c.setAlphaF(cl(prog * 0.15))
        p.setBrush(QBrush(c)); p.setPen(Qt.PenStyle.NoPen)
        p.drawEllipse(QRectF(3, 3, 18, 18))

        # border circle
        bc = QColor(self._color); bc.setAlphaF(cl(prog))
        p.setPen(QPen(bc, 1.5)); p.setBrush(Qt.BrushStyle.NoBrush)
        p.drawEllipse(QRectF(3, 3, 18, 18))

        # checkmark stroke drawn progressively
        if prog > 0.05:
            p1 = QPointF(7,    12)
            p2 = QPointF(10.5, 16)
            p3 = QPointF(17.5,  8)
            path = QPainterPath()
            if prog < 0.4:
                t   = prog / 0.4
                mid = QPointF(p1.x()+(p2.x()-p1.x())*t, p1.y()+(p2.y()-p1.y())*t)
                path.moveTo(p1); path.lineTo(mid)
            else:
                t   = (prog - 0.4) / 0.6
                mid = QPointF(p2.x()+(p3.x()-p2.x())*t, p2.y()+(p3.y()-p2.y())*t)
                path.moveTo(p1); path.lineTo(p2); path.lineTo(mid)
            pen = QPen(QColor(self._color), 2.0,
                       Qt.PenStyle.SolidLine,
                       Qt.PenCapStyle.RoundCap,
                       Qt.PenJoinStyle.RoundJoin)
            p.setPen(pen); p.drawPath(path)

# ── Shimmer overlay ───────────────────────────────────────────────────────────
class ShimmerOverlay(QWidget):
    def __init__(self, parent):
        super().__init__(parent)
        self.setAttribute(Qt.WidgetAttribute.WA_TransparentForMouseEvents)
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)
        self._pos  = -1.0
        self._anim = QPropertyAnimation(self, b"shimmer_pos")
        self._anim.setDuration(500)
        self._anim.setStartValue(-0.3)
        self._anim.setEndValue(1.3)
        self._anim.setEasingCurve(QEasingCurve.Type.InOutQuad)
        self._anim.finished.connect(self.hide)
        self.hide()

    @pyqtProperty(float)
    def shimmer_pos(self): return self._pos

    @shimmer_pos.setter
    def shimmer_pos(self, v): self._pos = v; self.update()

    def play(self):
        self.setGeometry(self.parent().rect())
        self.raise_(); self.show()
        self._anim.stop(); self._anim.start()

    def paintEvent(self, _e):
        if self._pos < 0: return
        p  = QPainter(self)
        p.setRenderHint(QPainter.RenderHint.Antialiasing)
        w  = self.width()
        cx = w * self._pos
        g  = QLinearGradient(cx - 60, 0, cx + 60, 0)
        g.setColorAt(0.0, QColor(0, 0, 0, 0))
        g.setColorAt(0.5, QColor(255, 255, 255, 28))
        g.setColorAt(1.0, QColor(0, 0, 0, 0))
        p.fillRect(0, 0, w, self.height(), g)

# ── Glow frame ────────────────────────────────────────────────────────────────
class GlowFrame(QFrame):
    def __init__(self, parent=None, accent=None, radius=10, is_pill=False):
        super().__init__(parent)
        self._selected  = False
        self._glow_op   = 0.0
        self._accent    = accent or ACCENT
        self._radius    = radius
        self._is_pill   = is_pill
        self._shimmer   = ShimmerOverlay(self)
        self._subs      = []
        self._pkg       = ""

        self._glow_anim = QPropertyAnimation(self, b"glow_opacity")
        self._glow_anim.setDuration(220)
        self._glow_anim.setEasingCurve(QEasingCurve.Type.OutCubic)

    @pyqtProperty(float)
    def glow_opacity(self): return self._glow_op

    @glow_opacity.setter
    def glow_opacity(self, v): self._glow_op = v; self.update()

    def set_selected(self, sel):
        self._selected = sel
        self._glow_anim.stop()
        self._glow_anim.setStartValue(self._glow_op)
        self._glow_anim.setEndValue(1.0 if sel else 0.0)
        self._glow_anim.start()
        if sel: self._shimmer.play()

    def resizeEvent(self, e):
        super().resizeEvent(e)
        self._shimmer.setGeometry(self.rect())

    def paintEvent(self, e):
        p = QPainter(self)
        p.setRenderHint(QPainter.RenderHint.Antialiasing)
        r = self._radius if not self._is_pill else self.height() // 2

        # background
        if self._is_pill and self._selected:
            bg = QColor("#1a2e2e") if self._accent == ACCENT2 else QColor("#1e1c38")
        elif self._selected:
            bg = QColor("#1e1c38")
        else:
            bg = QColor("#1a1a24")
        p.setBrush(QBrush(bg)); p.setPen(Qt.PenStyle.NoPen)
        p.drawRoundedRect(self.rect(), r, r)

        # glow / border
        gop = max(0.0, min(1.0, self._glow_op))
        if gop > 0.01:
            ac = QColor(self._accent); ac.setAlphaF(gop)
            p.setPen(QPen(ac, 1.5)); p.setBrush(Qt.BrushStyle.NoBrush)
            p.drawRoundedRect(QRectF(0.75, 0.75, self.width()-1.5, self.height()-1.5), r, r)
            for i in range(3):
                gc = QColor(self._accent)
                gc.setAlphaF(max(0.0, min(1.0, gop * (0.15 - i * 0.04))))
                p.setPen(QPen(gc, 3 + i * 2))
                p.drawRoundedRect(QRectF(1+i, 1+i, self.width()-2-i*2, self.height()-2-i*2), r, r)
        else:
            p.setPen(QPen(QColor("#222233"), 1))
            p.setBrush(Qt.BrushStyle.NoBrush)
            p.drawRoundedRect(QRectF(0.5, 0.5, self.width()-1, self.height()-1), r, r)

        p.end()
        super().paintEvent(e)

# ── Helpers ───────────────────────────────────────────────────────────────────
def repo_badge(repo):
    color, bg, border = REPO_STYLE.get(repo, ("color:#e8e8f0","#1a1a24","#333344"))
    lbl = QLabel(repo)
    lbl.setStyleSheet(f"""QLabel{{
        {color}; background:{bg}; border:1px solid {border};
        border-radius:4px; padding:1px 6px; font-size:9px; font-weight:bold;
    }}""")
    lbl.setFixedHeight(18)
    return lbl

def scroll_wrap(inner):
    sc = QScrollArea()
    sc.setWidget(inner); sc.setWidgetResizable(True)
    sc.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
    return sc

def add_sep(layout, text):
    lbl = QLabel(text.upper()); lbl.setObjectName("sec")
    lbl.setContentsMargins(0, 10, 0, 4); layout.addWidget(lbl)
    line = QFrame(); line.setFrameShape(QFrame.Shape.HLine)
    line.setStyleSheet("background:#1e1e2c; max-height:1px; margin-bottom:6px;")
    layout.addWidget(line)

# ── Install worker ────────────────────────────────────────────────────────────
class Worker(QObject):
    progress = pyqtSignal(str, float)
    log_line = pyqtSignal(str, str)   # (text, kind)  kind: header|repo|aur|patch|done|raw
    done     = pyqtSignal()

    def __init__(self, repo_pkgs, aur_pkgs, browser):
        super().__init__()
        self.repo_pkgs = repo_pkgs
        self.aur_pkgs  = aur_pkgs
        self.browser   = browser

    def _stream(self, cmd, kind="raw"):
        """Run cmd, emit every stdout+stderr line as it arrives."""
        try:
            proc = subprocess.Popen(
                cmd,
                stdout=subprocess.PIPE,
                stderr=subprocess.STDOUT,
                text=True,
                bufsize=1,
            )
            for line in proc.stdout:
                stripped = line.rstrip("\n")
                if stripped:
                    self.log_line.emit(stripped, kind)
            proc.wait()
        except Exception as exc:
            self.log_line.emit(f"[error] {exc}", "raw")

    def run(self):
        total = max(len(self.repo_pkgs) + len(self.aur_pkgs) + (1 if self.browser else 0), 1)
        done  = 0

        def ui(msg, f=None):
            self.progress.emit(msg, f if f is not None else done / total)

        if self.repo_pkgs:
            header = f"── pacman  ({len(self.repo_pkgs)} packages) " + "─" * 30
            self.log_line.emit(header, "header")
            ui(f"Installing {len(self.repo_pkgs)} repo packages...")
            self._stream(
                ["sudo","pacman","-S","--noconfirm","--needed","--color=never"] + self.repo_pkgs,
                kind="repo"
            )
            done += len(self.repo_pkgs)

        for pkg in self.aur_pkgs:
            header = f"── paru  {pkg} " + "─" * 40
            self.log_line.emit(header, "header")
            ui(f"Installing {pkg}...")
            self._stream(
                ["paru","-S","--noconfirm","--needed","--color=never", pkg],
                kind="aur"
            )
            done += 1

        if self.browser:
            self.log_line.emit("── hyprland.conf " + "─" * 35, "header")
            ui(f"Patching hyprland.conf → {self.browser['exec']}...")
            conf = os.path.expanduser("~/.config/hypr/hyprland.conf")
            if os.path.exists(conf):
                subprocess.run(["sed","-i",
                    f"s|^\\$Browser = .*|\\$Browser = {self.browser['exec']}|", conf])
            self.log_line.emit(f"  $Browser = {self.browser['exec']}", "patch")
            done += 1

        self.log_line.emit("", "raw")
        self.log_line.emit("✓  All done!", "done")
        ui("✓ All done!", 1.0)
        self.done.emit()

# ── Main window ───────────────────────────────────────────────────────────────
class SetupWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.selected  = set()
        self.browser   = None
        self.lo_langs  = set()
        self.tb_langs  = set()
        self._drag     = None
        self._thread   = None
        self._worker   = None
        self._br_frames = []
        self._tabs_widget = None   # set after build
        self._log_tab_idx = 7      # Log is the 8th tab (0-indexed)

        self.setWindowTitle("Faded Dream Setup")
        self.setFixedSize(840, 700)
        self.setWindowFlags(Qt.WindowType.FramelessWindowHint)

        root = QWidget(); root.setObjectName("root")
        self.setCentralWidget(root)
        vl = QVBoxLayout(root); vl.setContentsMargins(0,0,0,0); vl.setSpacing(0)

        vl.addWidget(self._build_titlebar())
        vl.addWidget(self._build_tabs(), 1)

        # progress bar (hidden until install starts)
        self._prog_w = QWidget()
        pl = QVBoxLayout(self._prog_w); pl.setContentsMargins(20,6,20,2); pl.setSpacing(2)
        self._prog_lbl = QLabel("Installing..."); self._prog_lbl.setObjectName("plbl")
        pl.addWidget(self._prog_lbl)
        self._prog_bar = QProgressBar(); self._prog_bar.setRange(0, 1000)
        pl.addWidget(self._prog_bar)
        self._prog_w.setVisible(False)
        vl.addWidget(self._prog_w)

        vl.addWidget(self._build_footer())

    # ── Drag to move (frameless) ──────────────────────────────────────────────
    def mousePressEvent(self, e):
        if e.button() == Qt.MouseButton.LeftButton:
            self._drag = e.globalPosition().toPoint() - self.frameGeometry().topLeft()

    def mouseMoveEvent(self, e):
        if self._drag and e.buttons() == Qt.MouseButton.LeftButton:
            self.move(e.globalPosition().toPoint() - self._drag)

    def mouseReleaseEvent(self, _e):
        self._drag = None

    # ── Titlebar ──────────────────────────────────────────────────────────────
    def _build_titlebar(self):
        bar = QWidget(); bar.setObjectName("titlebar"); bar.setFixedHeight(40)
        h = QHBoxLayout(bar); h.setContentsMargins(16,0,16,0); h.setSpacing(10)

        close = QPushButton(); close.setObjectName("close"); close.setFixedSize(13,13)
        close.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        close.clicked.connect(self._on_skip)
        h.addWidget(close)

        title = QLabel("Faded Dream Setup — First Run"); title.setObjectName("title")
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        h.addWidget(title, 1)

        h.addSpacing(13)
        return bar

    # ── Tabs ──────────────────────────────────────────────────────────────────
    def _build_tabs(self):
        tabs = QTabWidget(); tabs.setDocumentMode(True)
        tabs.addTab(self._page_welcome(),                  "🌙  Welcome")
        tabs.addTab(self._page_browser(),                  "🌐  Browser")
        tabs.addTab(self._page_sections(GAMING),           "🎮  Gaming")
        tabs.addTab(self._page_sections(PERIPHERALS),      "💡  Peripherals")
        tabs.addTab(self._page_office(),                   "📄  Office")
        tabs.addTab(self._page_flat(MEDIA),                "🎬  Media")
        tabs.addTab(self._page_sections(COMMS,True),       "💬  Comms")
        tabs.addTab(self._page_log(),                      "📋  Log")
        self._tabs_widget = tabs
        self._log_tab_idx = 7
        return tabs

    # ── Footer ────────────────────────────────────────────────────────────────
    def _build_footer(self):
        foot = QWidget(); foot.setObjectName("footer"); foot.setFixedHeight(56)
        h = QHBoxLayout(foot); h.setContentsMargins(20,0,20,0); h.setSpacing(10)

        left = QVBoxLayout(); left.setSpacing(2)
        self._count_lbl = QLabel(); self._count_lbl.setObjectName("count")
        self._update_count()
        left.addWidget(self._count_lbl)
        fsub = QLabel("runs once · self-destructs after install")
        fsub.setObjectName("fsub"); left.addWidget(fsub)
        h.addLayout(left, 1)

        skip = QPushButton("Skip All"); skip.setObjectName("skip")
        skip.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        skip.clicked.connect(self._on_skip)
        h.addWidget(skip)

        self._install_btn = QPushButton("Install Selected")
        self._install_btn.setObjectName("install")
        self._install_btn.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        self._install_btn.clicked.connect(self._on_install)
        h.addWidget(self._install_btn)

        return foot

    # ── Log page ──────────────────────────────────────────────────────────────
    def _page_log(self):
        outer = QWidget()
        v = QVBoxLayout(outer); v.setContentsMargins(16,16,16,16); v.setSpacing(8)

        # description panel — shown before install, hidden during
        self._log_desc = QWidget()
        dv = QVBoxLayout(self._log_desc); dv.setContentsMargins(0,0,0,0); dv.setSpacing(6)

        add_sep(dv, "What This Installer Does")

        desc_lines = [
            ("🌐", "Browser",
             "Pick one browser — LibreWolf, Zen, Firefox, Vivaldi, Chrome or Edge. "
             "Your choice is installed and $Browser in hyprland.conf is patched "
             "automatically so Super+B opens it."),
            ("🎮", "Gaming",
             "Steam (lib32), Heroic Games Launcher, Wine + Winetricks/Mono/Gecko, "
             "ProtonPlus, GameMode + 32-bit, MangoHud + 32-bit, MangoJuice. "
             "Selecting Wine auto-selects its three sub-packages."),
            ("💡", "Peripherals",
             "OpenRazer daemon + kernel driver (DKMS) + Python library for Razer hardware. "
             "Polychromatic for per-key RGB and effects. "
             "Piper for multi-brand mouse/keyboard config (Logitech, SteelSeries, Roccat…). "
             "Solaar for Logitech Unifying/Bolt receivers."),
            ("📄", "Office",
             "LibreOffice Fresh plus any of 12 language packs you select "
             "(English UK, Romanian, French, German, Spanish, Italian, Portuguese, "
             "Russian, Japanese, Chinese, Korean, Arabic)."),
            ("🎬", "Media",
             "Mirage image viewer, GIMP, Inkscape, Kdenlive video editor, "
             "HandBrake converter, OBS Studio Liberty (libre build)."),
            ("💬", "Comms",
             "Vesktop (Discord + Vencord), Telegram, Element (Matrix), "
             "Thunderbird + optional language packs, Obsidian notes."),
            ("🔧", "How It Works",
             "Repo packages are installed in one pacman batch. "
             "Each AUR package (paru) is built and installed individually — "
             "you will see full compile output here in real time. "
             "After install the script deletes itself so it never runs again."),
        ]

        for icon, title, body in desc_lines:
            row = QHBoxLayout(); row.setSpacing(10); row.setContentsMargins(0,2,0,2)
            il = QLabel(icon); il.setFixedWidth(22)
            il.setStyleSheet("font-size:16px; background:transparent;")
            il.setAlignment(Qt.AlignmentFlag.AlignTop); row.addWidget(il)
            col = QVBoxLayout(); col.setSpacing(2)
            tl = QLabel(title); tl.setObjectName("pkg-name"); col.addWidget(tl)
            bl = QLabel(body);  bl.setObjectName("pkg-desc")
            bl.setWordWrap(True); col.addWidget(bl)
            row.addLayout(col)
            dv.addLayout(row)

        v.addWidget(self._log_desc)

        # terminal output area
        self._log_term = QScrollArea()
        self._log_term.setWidgetResizable(True)
        self._log_term.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self._log_term.setStyleSheet(
            "QScrollArea { background:#080810; border:1px solid #1e1e2c; border-radius:8px; }"
            "QScrollBar:vertical { background:#080810; width:5px; }"
            "QScrollBar::handle:vertical { background:#2a2a3a; border-radius:2px; }"
        )

        self._log_inner = QWidget()
        self._log_inner.setStyleSheet("background:#080810;")
        self._log_vbox = QVBoxLayout(self._log_inner)
        self._log_vbox.setContentsMargins(14, 10, 14, 10)
        self._log_vbox.setSpacing(1)
        self._log_vbox.addStretch()

        self._log_term.setWidget(self._log_inner)
        self._log_term.setVisible(False)   # hidden until install starts
        v.addWidget(self._log_term, 1)

        return outer

    def _log_append(self, text, kind):
        colors = {
            "header": "#7c6af7",
            "repo":   "#6aaff7",
            "aur":    "#4fd9c4",
            "patch":  "#b46af7",
            "done":   "#4fd9c4",
            "raw":    "#888899",
        }
        color = colors.get(kind, "#888899")
        bold  = kind in ("header", "done")

        lbl = QLabel(text)
        lbl.setWordWrap(True)
        lbl.setTextInteractionFlags(Qt.TextInteractionFlag.TextSelectableByMouse)
        weight = "bold" if bold else "normal"
        lbl.setStyleSheet(
            f"color:{color}; font-family:'JetBrainsMono Nerd Font','Noto Mono',monospace;"
            f"font-size:11px; font-weight:{weight}; background:transparent;"
        )
        # insert before the trailing stretch
        count = self._log_vbox.count()
        self._log_vbox.insertWidget(count - 1, lbl)
        # auto-scroll to bottom
        QTimer.singleShot(0, lambda: self._log_term.verticalScrollBar().setValue(
            self._log_term.verticalScrollBar().maximum()))

    # ── Welcome page ──────────────────────────────────────────────────────────
    def _page_welcome(self):
        inner = QWidget()
        v = QVBoxLayout(inner); v.setContentsMargins(40,40,40,40); v.setSpacing(20)
        v.setAlignment(Qt.AlignmentFlag.AlignHCenter | Qt.AlignmentFlag.AlignTop)

        t = QLabel("🌙  Faded Dream")
        t.setStyleSheet("font-size:32px; font-weight:bold; color:#e8e8f0;")
        t.setAlignment(Qt.AlignmentFlag.AlignCenter); v.addWidget(t)

        s = QLabel("Your dotfiles are installed.\n"
                   "Select optional packages across the tabs, then hit Install.\n"
                   "This app runs once and deletes itself.")
        s.setObjectName("wsub"); s.setAlignment(Qt.AlignmentFlag.AlignCenter); v.addWidget(s)

        cards_data = [
            ("🌐","Browser",     "Pick your default browser"),
            ("🎮","Gaming",      "Steam, Heroic, Wine, MangoHud"),
            ("💡","Peripherals", "OpenRazer, Polychromatic, Piper, Solaar"),
            ("📄","Office",      "LibreOffice + language packs"),
            ("🎬","Media",       "GIMP, Kdenlive, OBS Liberty"),
            ("💬","Comms",       "Vesktop, Telegram, Thunderbird"),
        ]

        grid_w = QWidget(); grid_w.setFixedWidth(452)
        grid = QGridLayout(grid_w); grid.setSpacing(8); grid.setContentsMargins(0,0,0,0)
        for i, (icon, title, desc) in enumerate(cards_data):
            card = GlowFrame(radius=10); card.setFixedWidth(140)
            cv = QVBoxLayout(card); cv.setContentsMargins(14,14,14,14); cv.setSpacing(4)
            for txt, obj in [(icon, None),(title,"ctitle"),(desc,"cdesc")]:
                l = QLabel(txt)
                if obj: l.setObjectName(obj)
                l.setWordWrap(True); cv.addWidget(l)
            grid.addWidget(card, i // 3, i % 3)

        v.addWidget(grid_w, 0, Qt.AlignmentFlag.AlignHCenter)
        v.addStretch()
        return scroll_wrap(inner)

    # ── Browser page ──────────────────────────────────────────────────────────
    def _page_browser(self):
        inner = QWidget()
        v = QVBoxLayout(inner); v.setContentsMargins(16,16,16,16); v.setSpacing(6)
        add_sep(v, "Select Your Default Browser")

        note = QLabel("hyprland.conf will be patched automatically with your choice.")
        note.setObjectName("pkg-desc"); note.setContentsMargins(0,0,0,8); v.addWidget(note)

        for br in BROWSERS:
            f = self._make_browser_pill(br)
            self._br_frames.append((f, br))
            v.addWidget(f)

        v.addStretch()
        return scroll_wrap(inner)

    def _make_browser_pill(self, br):
        frame = GlowFrame(radius=999, accent=ACCENT2, is_pill=True)
        frame.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        frame.setFixedHeight(62)

        h = QHBoxLayout(frame); h.setContentsMargins(16,0,16,0); h.setSpacing(12)

        cm = CheckMark(color=ACCENT2); frame._cm = cm; h.addWidget(cm)

        icon = QLabel(br["icon"]); icon.setObjectName("icon"); h.addWidget(icon)

        info = QVBoxLayout(); info.setSpacing(2)
        nr = QHBoxLayout(); nr.setSpacing(8)
        nl = QLabel(br["name"]); nl.setObjectName("pkg-name"); nr.addWidget(nl)
        if br.get("recommended"):
            rec = QLabel("⭐ Recommended")
            rec.setStyleSheet("color:#4fd9c4; background:#0a2e2a; border:1px solid #1a4840;"
                              "border-radius:4px; padding:1px 6px; font-size:9px; font-weight:bold;")
            nr.addWidget(rec)
        nr.addStretch(); info.addLayout(nr)
        dl = QLabel(br["desc"]); dl.setObjectName("pkg-desc"); info.addWidget(dl)
        h.addLayout(info, 1)
        h.addWidget(repo_badge(br["repo"]))

        def on_click(_e=None, f=frame, b=br):
            for other_f, _ in self._br_frames:
                if other_f is not f:
                    other_f.set_selected(False)
                    other_f._cm.set_checked(False)
            self.browser = b
            f.set_selected(True)
            f._cm.set_checked(True)
            self._update_count()

        frame.mousePressEvent = on_click
        return frame

    # ── Sections page (gaming / comms) ────────────────────────────────────────
    def _page_sections(self, sections, comms=False):
        inner = QWidget()
        v = QVBoxLayout(inner); v.setContentsMargins(16,16,16,16); v.setSpacing(2)
        for sec in sections:
            add_sep(v, sec["section"])
            for pkg in sec["packages"]:
                row = self._make_pkg_row(pkg); v.addWidget(row)
                for sub in pkg.get("sub", []):
                    sr = self._make_sub_row(sub); v.addWidget(sr)
                    row._subs.append(sr)
                if comms and pkg["pkg"] == "thunderbird":
                    v.addWidget(self._lang_grid("tb"))
        v.addStretch()
        return scroll_wrap(inner)

    # ── Flat page (media) ─────────────────────────────────────────────────────
    def _page_flat(self, packages):
        inner = QWidget()
        v = QVBoxLayout(inner); v.setContentsMargins(16,16,16,16); v.setSpacing(2)
        add_sep(v, "Creative Tools")
        for pkg in packages: v.addWidget(self._make_pkg_row(pkg))
        v.addStretch()
        return scroll_wrap(inner)

    # ── Office page ───────────────────────────────────────────────────────────
    def _page_office(self):
        inner = QWidget()
        v = QVBoxLayout(inner); v.setContentsMargins(16,16,16,16); v.setSpacing(2)
        add_sep(v, "Base")
        for p in OFFICE_BASE: v.addWidget(self._make_pkg_row(p))
        add_sep(v, "LibreOffice Language Packs")
        v.addWidget(self._lang_grid("lo"))
        v.addStretch()
        return scroll_wrap(inner)

    # ── Language grid ─────────────────────────────────────────────────────────
    def _lang_grid(self, kind):
        wrap = QWidget()
        if kind == "tb":
            wrap.setContentsMargins(28, 0, 0, 0)
        grid = QGridLayout(wrap); grid.setContentsMargins(0,4,0,8); grid.setSpacing(6)

        for i, (flag, name) in enumerate(LANG_LIST):
            pkg   = (f"libreoffice-fresh-{LO_CODES[i]}" if kind == "lo"
                     else f"thunderbird-i18n-{TB_CODES[i]}")
            store = self.lo_langs if kind == "lo" else self.tb_langs

            tile = GlowFrame(radius=8)
            tile.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
            tile.setFixedHeight(38)

            tl = QHBoxLayout(tile); tl.setContentsMargins(10,4,10,4); tl.setSpacing(8)
            cm = CheckMark(); tile._cm = cm; tl.addWidget(cm)
            lbl = QLabel(f"{flag}  {name}")
            lbl.setStyleSheet("font-size:12px; font-weight:bold; color:#e8e8f0; background:transparent;")
            lbl.setAlignment(Qt.AlignmentFlag.AlignCenter); tl.addWidget(lbl, 1)

            def on_click(_e=None, t=tile, p=pkg, s=store, l=lbl):
                if p in s:
                    s.discard(p); self.selected.discard(p)
                    t.set_selected(False); t._cm.set_checked(False)
                    l.setStyleSheet("font-size:12px; font-weight:bold; color:#e8e8f0; background:transparent;")
                else:
                    s.add(p); self.selected.add(p)
                    t.set_selected(True); t._cm.set_checked(True)
                    l.setStyleSheet("font-size:12px; font-weight:bold; color:#c4b8ff; background:transparent;")
                self._update_count()

            tile.mousePressEvent = on_click
            grid.addWidget(tile, i // 4, i % 4)

        return wrap

    # ── Package row ───────────────────────────────────────────────────────────
    def _make_pkg_row(self, pkg):
        frame = GlowFrame(radius=10)
        frame.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        frame._subs = []; frame._pkg = pkg["pkg"]

        h = QHBoxLayout(frame); h.setContentsMargins(12,10,12,10); h.setSpacing(10)
        cm = CheckMark(); frame._cm = cm; h.addWidget(cm)
        icon = QLabel(pkg.get("icon","📦")); icon.setObjectName("icon"); h.addWidget(icon)

        info = QVBoxLayout(); info.setSpacing(1)
        nl = QLabel(pkg["name"]); nl.setObjectName("pkg-name"); info.addWidget(nl)
        dl = QLabel(pkg["desc"]); dl.setObjectName("pkg-desc"); dl.setWordWrap(True); info.addWidget(dl)
        h.addLayout(info, 1)
        h.addWidget(repo_badge(pkg["repo"]))

        def on_click(_e=None, f=frame, p=pkg["pkg"]):
            sel = p not in self.selected
            if sel:
                self.selected.add(p); f.set_selected(True); f._cm.set_checked(True)
                for sr in f._subs:
                    self.selected.add(sr._pkg); sr.set_selected(True); sr._cm.set_checked(True)
            else:
                self.selected.discard(p); f.set_selected(False); f._cm.set_checked(False)
                for sr in f._subs:
                    self.selected.discard(sr._pkg); sr.set_selected(False); sr._cm.set_checked(False)
            self._update_count()

        frame.mousePressEvent = on_click
        return frame

    # ── Sub-package row ───────────────────────────────────────────────────────
    def _make_sub_row(self, sub):
        frame = GlowFrame(radius=8)
        frame.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        frame.setContentsMargins(28, 0, 0, 0); frame._pkg = sub["pkg"]

        h = QHBoxLayout(frame); h.setContentsMargins(12,7,12,7); h.setSpacing(10)
        bar = QFrame(); bar.setFixedSize(2, 20)
        bar.setStyleSheet("background:#7c6af7; border-radius:1px;"); h.addWidget(bar)
        cm = CheckMark(); frame._cm = cm; h.addWidget(cm)
        nl = QLabel(sub["name"]); nl.setObjectName("sub-name"); h.addWidget(nl, 1)
        h.addWidget(repo_badge(sub["repo"]))

        def on_click(_e=None, f=frame, p=sub["pkg"]):
            sel = p not in self.selected
            if sel:
                self.selected.add(p); f.set_selected(True); f._cm.set_checked(True)
            else:
                self.selected.discard(p); f.set_selected(False); f._cm.set_checked(False)
            self._update_count()

        frame.mousePressEvent = on_click
        return frame

    # ── Count label ───────────────────────────────────────────────────────────
    def _update_count(self):
        total = len(self.selected) + (1 if self.browser else 0)
        self._count_lbl.setText(
            f'<span style="color:#4fd9c4; font-weight:bold">{total}</span>'
            f'<span style="color:#444455"> packages selected</span>')

    # ── Skip (write flag, close — no install) ─────────────────────────────────
    def _on_skip(self):
        self.close()

    # ── Install ───────────────────────────────────────────────────────────────
    def _on_install(self):
        if not self.selected and not self.browser:
            self._on_skip(); return

        self._install_btn.setEnabled(False)
        self._prog_w.setVisible(True)

        # switch to log tab and show terminal
        self._log_desc.setVisible(False)
        self._log_term.setVisible(True)
        self._tabs_widget.setCurrentIndex(self._log_tab_idx)

        # seed the log with what we're about to do
        self._log_append("╔══════════════════════════════════════════════╗", "header")
        self._log_append("  Faded Dream — Installing selected packages", "header")
        self._log_append("╚══════════════════════════════════════════════╝", "header")
        self._log_append("", "raw")

        # build AUR lookup map
        aur_map = {}
        def idx(items):
            for it in items:
                aur_map[it["pkg"]] = it.get("aur", False)
                for s in it.get("sub", []): aur_map[s["pkg"]] = s.get("aur", False)
        for sec in GAMING:       idx(sec["packages"])
        for sec in PERIPHERALS:  idx(sec["packages"])
        for sec in COMMS:        idx(sec["packages"])
        idx(MEDIA); idx(OFFICE_BASE)
        for br in BROWSERS: aur_map[br["pkg"]] = br.get("aur", False)

        all_pkgs  = ([self.browser["pkg"]] if self.browser else []) + list(self.selected)
        repo_pkgs = [p for p in all_pkgs if not aur_map.get(p, False)]
        aur_pkgs  = [p for p in all_pkgs if     aur_map.get(p, False)]

        if repo_pkgs:
            self._log_append(f"  repo packages  ({len(repo_pkgs)}): {', '.join(repo_pkgs)}", "repo")
        if aur_pkgs:
            self._log_append(f"  AUR packages   ({len(aur_pkgs)}): {', '.join(aur_pkgs)}", "aur")
        if self.browser:
            self._log_append(f"  browser patch: $Browser = {self.browser['exec']}", "patch")
        self._log_append("", "raw")

        self._worker = Worker(repo_pkgs, aur_pkgs, self.browser)
        self._thread = QThread()
        self._worker.moveToThread(self._thread)
        self._thread.started.connect(self._worker.run)
        self._worker.progress.connect(self._on_progress)
        self._worker.log_line.connect(self._log_append)
        self._worker.done.connect(self._on_done)
        self._thread.start()

    def _on_progress(self, msg, frac):
        self._prog_lbl.setText(msg)
        self._prog_bar.setValue(int(frac * 1000))

    def _on_done(self):
        self._thread.quit()
        try: os.remove(os.path.abspath(sys.argv[0]))
        except: pass
        # give user a moment to read the log before closing
        QTimer.singleShot(2000, self.close)

# ── Entry ─────────────────────────────────────────────────────────────────────
if __name__ == "__main__":
    app = QApplication(sys.argv)
    app.setStyle("Fusion")
    app.setStyleSheet(QSS)
    win = SetupWindow()
    win.show()
    sys.exit(app.exec())
