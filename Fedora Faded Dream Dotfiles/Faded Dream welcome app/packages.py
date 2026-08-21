#!/usr/bin/env python3
# packages.py — Package lists, repo metadata, Fedora map, Hyprland paths
import os
from i18n import _LANG, TS

# ── Browsers ──────────────────────────────────────────────────────────────────
BROWSERS = [
    {"pkg":"librewolf",               "exec":"librewolf",            "name":"LibreWolf",
     "desc":"Privacy-focused Firefox fork — no telemetry, hardened",
     "icon":"🦊", "repo":"librewolf", "aur":False, "recommended":True},
    {"pkg":"zen-browser",             "exec":"zen-browser",          "name":"Zen Browser",
     "desc":"Beautiful Firefox-based browser with a modern UI",
     "icon":"🧘", "repo":"copr-sneexy", "aur":False, "recommended":False},
    {"pkg":"firefox",                 "exec":"firefox",              "name":"Firefox",
     "desc":"Mozilla's open source browser",
     "icon":"🔥", "repo":"fedora", "aur":False, "recommended":False},
    {"pkg":"vivaldi",                 "exec":"vivaldi",              "name":"Vivaldi",
     "desc":"Feature-rich Chromium browser",
     "icon":"🎻", "repo":"vivaldi", "aur":False, "recommended":False},
    {"pkg":"google-chrome-stable",    "exec":"google-chrome-stable", "name":"Google Chrome",
     "desc":"Google's browser",
     "icon":"🌐", "repo":"google-chrome", "aur":False, "recommended":False},
    {"pkg":"microsoft-edge-stable",   "exec":"microsoft-edge-stable", "name":"Microsoft Edge",
     "desc":"Microsoft's Chromium browser",
     "icon":"🔷", "repo":"microsoft-edge", "aur":False, "recommended":False},
]

# ── Gaming ────────────────────────────────────────────────────────────────────
GAMING = [
    {"section":"Launchers", "packages":[
        {"pkg":"steam",                     "name":"Steam",
         "desc":"Valve game platform",
         "icon":"🎮", "repo":"rpmfusion-nonfree", "aur":False, "sub":[]},
        {"pkg":"heroic-games-launcher",     "name":"Heroic",
         "desc":"Epic & GOG launcher",
         "icon":"🦸", "repo":"copr", "aur":False, "sub":[]},
        {"pkg":"sober",                     "name":"Sober",
         "desc":"", "icon":"🎲", "repo":"flatpak", "aur":False, "sub":[], "risk_warning":"sober"},
    ]},
    {"section":"Compatibility", "packages":[
        {"pkg":"wine", "name":"Wine", "desc":"Windows compatibility layer",
         "icon":"🍷", "repo":"fedora", "aur":False, "sub":[
            {"pkg":"winetricks", "name":"Winetricks", "repo":"fedora", "aur":False},
            {"pkg":"wine-mono",  "name":"Wine Mono",  "repo":"fedora", "aur":False},
            {"pkg":"wine-gecko", "name":"Wine Gecko", "repo":"fedora", "aur":False},
        ]},
        {"pkg":"protonplus", "name":"ProtonPlus", "desc":"Proton version manager GUI",
         "icon":"⚗️", "repo":"copr", "aur":False, "sub":[]},
    ]},
    {"section":"Performance", "packages":[
        {"pkg":"gamemode", "name":"GameMode", "desc":"CPU/GPU performance optimizer",
         "icon":"⚡", "repo":"fedora", "aur":False, "sub":[]},
        {"pkg":"mangohud", "name":"MangoHud", "desc":"In-game FPS/stats overlay",
         "icon":"📊", "repo":"fedora", "aur":False, "sub":[]},
        {"pkg":"mangojuice", "name":"MangoJuice", "desc":"GUI configurator for MangoHud",
         "icon":"🥭", "repo":"copr", "aur":False, "sub":[]},
    ]},
]

OTHER = [
    {"section":"Other", "packages":[
        {"pkg":"ytdn", "name":"YT Downloader",
         "desc":"", "icon":"⬇️", "repo":"flatpak", "aur":False, "sub":[], "risk_warning":"ytdn"},
    ]},
]


# ── Language codes ────────────────────────────────────────────────────────────
LANG_LIST = [
    ("🇬🇧","English UK"),  ("🇷🇴","Romanian"),           ("🇫🇷","French"),    ("🇩🇪","German"),
    ("🇪🇸","Spanish"),     ("🇮🇹","Italian"),             ("🇵🇹","Portuguese"), ("🇷🇺","Russian"),
    ("🇯🇵","Japanese"),    ("🇨🇳","Chinese (Simplified)"), ("🇰🇷","Korean"),    ("🇸🇦","Arabic"),
]
LO_CODES = ["en-gb","ro","fr","de","es","it","pt","ru","ja","zh-cn","ko","ar"]
TB_CODES = ["en-gb","ro","fr","de","es-es","it","pt-pt","ru","ja","zh-cn","ko","ar"]

# ── Office ────────────────────────────────────────────────────────────────────
OFFICE_BASE = [
    {"pkg":"libreoffice", "name":"LibreOffice",
     "desc":"Latest stable — Writer, Calc, Impress, Draw",
     "icon":"📄", "repo":"fedora", "aur":False},
]

# ── Media ─────────────────────────────────────────────────────────────────────
MEDIA = [
    {"pkg":"mirage",             "name":"Mirage",
     "desc":"Feature-rich image viewer",
     "icon":"🖼️", "repo":"copr", "aur":False, "sub":[]},
    {"pkg":"gimp",               "name":"GIMP",
     "desc":"Image editor",
     "icon":"🎨", "repo":"fedora", "aur":False, "sub":[]},
    {"pkg":"inkscape",           "name":"Inkscape",
     "desc":"Vector graphics editor",
     "icon":"✏️", "repo":"fedora", "aur":False, "sub":[]},
    {"pkg":"kdenlive",           "name":"Kdenlive",
     "desc":"Video editor",
     "icon":"🎬", "repo":"fedora", "aur":False, "sub":[]},
    {"pkg":"handbrake",          "name":"HandBrake",
     "desc":"Video converter/compressor",
     "icon":"🔧", "repo":"rpmfusion-free", "aur":False, "sub":[]},
    {"pkg":"obs-studio",         "name":"OBS Studio",
     "desc":"Streaming & recording",
     "icon":"🎙️", "repo":"rpmfusion-free", "aur":False, "sub":[]},
]

# ── Comms ─────────────────────────────────────────────────────────────────────
COMMS = [
    {"section":"Messaging", "packages":[
        {"pkg":"vesktop",          "name":"Vesktop",
         "desc":"Discord client (Vencord)",
         "icon":"💬", "repo":"copr", "aur":False, "sub":[]},
        {"pkg":"telegram-desktop", "name":"Telegram",
         "desc":"Messaging platform",
         "icon":"📡", "repo":"fedora", "aur":False, "sub":[]},
        {"pkg":"element-desktop",  "name":"Element",
         "desc":"Matrix decentralized chat",
         "icon":"🔒", "repo":"fedora", "aur":False, "sub":[]},
    ]},
    {"section":"Email", "packages":[
        {"pkg":"thunderbird", "name":"Thunderbird",
         "desc":"Email client with language packs",
         "icon":"⚡", "repo":"fedora", "aur":False, "sub":[]},
    ]},
    {"section":"Notes", "packages":[
        {"pkg":"obsidian", "name":"Obsidian",
         "desc":"Markdown note taking",
         "icon":"💎", "repo":"copr", "aur":False, "sub":[]},
    ]},
]

# ── Peripherals ───────────────────────────────────────────────────────────────
PERIPHERALS = [
    {"section":"RGB / Razer", "packages":[
        {"pkg":"openrazer-daemon", "name":"OpenRazer Daemon",
         "desc":"Background service that communicates with Razer hardware",
         "icon":"🐍", "repo":"copr", "aur":False, "sub":[
            {"pkg":"openrazer-driver-dkms", "name":"OpenRazer Driver", "repo":"copr", "aur":False},
            {"pkg":"python3-openrazer",     "name":"Python OpenRazer", "repo":"copr", "aur":False},
        ]},
        {"pkg":"polychromatic", "name":"Polychromatic",
         "desc":"OpenRazer GUI — per-key RGB, effects and DPI profiles",
         "icon":"🌈", "repo":"copr", "aur":False, "sub":[]},
    ]},
    {"section":"Peripherals", "packages":[
        {"pkg":"piper", "name":"Piper",
         "desc":"Mouse & keyboard configurator — DPI, buttons, polling rate. Multi-brand support",
         "icon":"🖱️", "repo":"fedora", "aur":False, "sub":[]},
        {"pkg":"solaar", "name":"Solaar",
         "desc":"Logitech device manager — Unifying/Bolt receiver pairing and battery levels",
         "icon":"⌨️", "repo":"fedora", "aur":False, "sub":[]},
    ]},
]

# ── File Transfer ─────────────────────────────────────────────────────────────
FILE_TRANSFER = [
    {"section":"Android / MTP", "packages":[
        {"pkg":"jmtpfs", "name":"jmtpfs",
         "desc":"Mount Android phones via MTP — works with Android 4–14. Usage: jmtpfs ~/Phone",
         "icon":"📱", "repo":"copr", "aur":False, "sub":[]},
        {"pkg":"go-mtpfs", "name":"go-mtpfs",
         "desc":"Go implementation of MTP — faster for large file transfers",
         "icon":"🤖", "repo":"copr", "aur":False, "sub":[]},
    ]},
    {"section":"Camera / PTP", "packages":[
        {"pkg":"gphotofs", "name":"gphotofs",
         "desc":"PTP mount via FUSE — works better with older devices and cameras",
         "icon":"📷", "repo":"copr", "aur":False, "sub":[]},
        {"pkg":"gphoto2",  "name":"gphoto2",
         "desc":"Command-line tool for camera control and image download",
         "icon":"🎞️", "repo":"fedora", "aur":False, "sub":[]},
    ]},
    {"section":"Network / Wireless", "packages":[
        {"pkg":"warpinator", "name":"Warpinator",
         "desc":"LAN file sharing — send and receive files on the local network",
         "icon":"🌐", "repo":"fedora", "aur":False, "sub":[]},
        {"pkg":"localsend", "name":"LocalSend",
         "desc":"Cross-platform AirDrop alternative — works with iOS, Android, Windows",
         "icon":"📡", "repo":"copr", "aur":False, "sub":[]},
        {"pkg":"croc",      "name":"Croc",
         "desc":"Securely send files between any two computers — peer-to-peer, encrypted",
         "icon":"🐊", "repo":"fedora", "aur":False, "sub":[]},
    ]},
    {"section":"USB / Serial", "packages":[
        {"pkg":"android-tools", "name":"Android Tools",
         "desc":"ADB and fastboot — sideloading, debugging, file transfer over USB",
      "icon":"🔧", "repo":"fedora", "aur":False, "sub":[]},
        {"pkg":"scrcpy",        "name":"Scrcpy",
         "desc":"Display and control Android devices over USB or Wi-Fi — no root needed",
         "icon":"📲", "repo":"fedora", "aur":False, "sub":[]},
    ]},
]

# ── File Managers ─────────────────────────────────────────────────────────────
FILE_MANAGERS = [
    {"section":"Graphical File Managers", "packages":[
        {"pkg":"nautilus",      "name":"Nautilus",
         "desc":"GNOME Files — clean, modern, integrates well with GNOME/Hyprland",
         "icon":"🗂️", "repo":"fedora", "aur":False, "sub":[]},
        {"pkg":"nemo",          "name":"Nemo",
         "desc":"Cinnamon file manager — thumbnails, split pane, open-as-root",
         "icon":"📂", "repo":"fedora", "aur":False, "sub":[]},
        {"pkg":"thunar",        "name":"Thunar",
         "desc":"XFCE file manager — lightweight, fast, highly configurable",
         "icon":"📁", "repo":"fedora", "aur":False, "sub":[
            {"pkg":"thunar-volman",            "name":"Volume Manager",    "repo":"fedora", "aur":False},
            {"pkg":"thunar-archive-plugin",    "name":"Archive Plugin",    "repo":"fedora", "aur":False},
            {"pkg":"thunar-media-tags-plugin", "name":"Media Tags Plugin", "repo":"fedora", "aur":False},
        ]},
        {"pkg":"dolphin",       "name":"Dolphin",
         "desc":"KDE file manager — tabs, split view, Git integration, powerful",
         "icon":"🐬", "repo":"fedora", "aur":False, "sub":[]},
        {"pkg":"pcmanfm",       "name":"PCManFM",
         "desc":"LXDE file manager — extremely fast and lightweight",
         "icon":"📋", "repo":"fedora", "aur":False, "sub":[]},
        {"pkg":"caja",          "name":"Caja",
         "desc":"MATE file manager — Nautilus fork, stable and familiar",
         "icon":"🗃️", "repo":"fedora", "aur":False, "sub":[]},
        {"pkg":"krusader",      "name":"Krusader",
         "desc":"Twin-panel KDE file manager — like Total Commander for Linux",
         "icon":"⚔️", "repo":"fedora", "aur":False, "sub":[]},
        {"pkg":"doublecmd-qt6", "name":"Double Commander",
         "desc":"Cross-platform twin-panel file manager with built-in viewer/editor",
         "icon":"🗂️", "repo":"fedora", "aur":False, "sub":[]},
        {"pkg":"sunflower",     "name":"Sunflower",
         "desc":"Twin-panel Python file manager with plugin support",
         "icon":"🌻", "repo":"copr", "aur":False, "sub":[]},
    ]},
    {"section":"Terminal File Managers", "packages":[
        {"pkg":"voiddream",  "name":"VoidDream",
         "desc":"Part of the Faded Dream Ecosystem — TUI file manager built with Rust & Ratatui",
         "icon":"🌙", "repo":"github", "aur":False,
         "install_cmd": ["git", "clone",
                         "https://github.com/FemBoyGamerTechGuy/VoidDream.git",
                         "/tmp/VoidDream-install"],
         "post_cmd": ["dnf", "builddep", "-y", "packaging/voiddream.spec"],
         "post_cwd": "/tmp/VoidDream-install",
         "sub":[]},
        {"pkg":"yazi",       "name":"Yazi",
         "desc":"Blazing fast Rust file manager — image preview, async I/O, Lua plugins",
         "icon":"🦆", "repo":"fedora", "aur":False, "sub":[]},
        {"pkg":"lf",         "name":"lf",
         "desc":"Minimal Go file manager inspired by ranger — single binary, fast",
         "icon":"🔤", "repo":"fedora", "aur":False, "sub":[]},
        {"pkg":"ranger",     "name":"Ranger",
         "desc":"Classic Python terminal file manager with Vim keybindings",
         "icon":"🐾", "repo":"fedora", "aur":False, "sub":[]},
        {"pkg":"nnn",        "name":"nnn",
         "desc":"Tiny C file manager — fastest on the list, plugin ecosystem",
         "icon":"⚡", "repo":"fedora", "aur":False, "sub":[]},
        {"pkg":"mc",         "name":"Midnight Commander",
         "desc":"Classic ncurses twin-panel file manager, battle-tested since 1994",
         "icon":"🗄️", "repo":"fedora", "aur":False, "sub":[]},
        {"pkg":"broot",      "name":"broot",
         "desc":"Tree-based Rust file manager with fuzzy search and previews",
         "icon":"🌲", "repo":"fedora", "aur":False, "sub":[]},
        {"pkg":"vifm",       "name":"Vifm",
         "desc":"Vim-like dual-pane terminal file manager — familiar for Vim users",
         "icon":"✌️", "repo":"fedora", "aur":False, "sub":[]},
        {"pkg":"superfile",  "name":"Superfile",
         "desc":"Modern visual terminal file manager — fancy UI, mouse support",
         "icon":"✨", "repo":"copr", "aur":False, "sub":[]},
    ]},
    {"section":"Cloud & Network", "packages":[
        {"pkg":"rclone",    "name":"rclone",
         "desc":"Sync to/from 70+ cloud providers — S3, Google Drive, Dropbox...",
         "icon":"☁️", "repo":"fedora", "aur":False, "sub":[]},
        {"pkg":"filezilla", "name":"FileZilla",
         "desc":"FTP/SFTP/FTPS graphical client — industry standard for FTP",
         "icon":"📡", "repo":"fedora", "aur":False, "sub":[]},
        {"pkg":"gftp",      "name":"gFTP",
         "desc":"Lightweight multithreaded FTP client for GTK",
         "icon":"🔗", "repo":"copr", "aur":False, "sub":[]},
        {"pkg":"insync",    "name":"insync",
         "desc":"Google Drive & OneDrive sync client with tray icon",
         "icon":"🔄", "repo":"third-party", "aur":False, "sub":[]},
    ]},
]

# ── Section label translations ────────────────────────────────────────────────
_SEC_LABELS = {
    "Launchers":          {"en":"Launchers","ro":"Lansatoare","fr":"Lanceurs","de":"Starter","es":"Lanzadores","it":"Lanciatori","pt":"Lançadores","ru":"Лаунчеры","ja":"ランチャー","zh":"启动器","ko":"런처","ar":"المشغّلات"},
    "Compatibility":      {"en":"Compatibility","ro":"Compatibilitate","fr":"Compatibilité","de":"Kompatibilität","es":"Compatibilidad","it":"Compatibilità","pt":"Compatibilidade","ru":"Совместимость","ja":"互換性","zh":"兼容性","ko":"호환성","ar":"التوافق"},
    "Performance":        {"en":"Performance","ro":"Performanță","fr":"Performance","de":"Leistung","es":"Rendimiento","it":"Prestazioni","pt":"Desempenho","ru":"Производительность","ja":"パフォーマンス","zh":"性能","ko":"성능","ar":"الأداء"},
    "Messaging":          {"en":"Messaging","ro":"Mesagerie","fr":"Messagerie","de":"Messaging","es":"Mensajería","it":"Messaggistica","pt":"Mensagens","ru":"Мессенджеры","ja":"メッセージ","zh":"即时通讯","ko":"메시징","ar":"المراسلة"},
    "Email":              {"en":"Email","ro":"Email","fr":"Courriel","de":"E-Mail","es":"Correo","it":"Email","pt":"Email","ru":"Почта","ja":"メール","zh":"邮件","ko":"이메일","ar":"البريد"},
    "Notes":              {"en":"Notes","ro":"Notițe","fr":"Notes","de":"Notizen","es":"Notas","it":"Note","pt":"Notas","ru":"Заметки","ja":"メモ","zh":"笔记","ko":"노트","ar":"الملاحظات"},
    "RGB / Razer":        {"en":"RGB / Razer","ro":"RGB / Razer","fr":"RGB / Razer","de":"RGB / Razer","es":"RGB / Razer","it":"RGB / Razer","pt":"RGB / Razer","ru":"RGB / Razer","ja":"RGB / Razer","zh":"RGB / Razer","ko":"RGB / Razer","ar":"RGB / Razer"},
    "Peripherals":        {"en":"Peripherals","ro":"Periferice","fr":"Périphériques","de":"Peripherie","es":"Periféricos","it":"Periferiche","pt":"Periféricos","ru":"Периферия","ja":"周辺機器","zh":"外设","ko":"주변기기","ar":"الملحقات"},
    "Android / MTP":      {"en":"Android / MTP","ro":"Android / MTP","fr":"Android / MTP","de":"Android / MTP","es":"Android / MTP","it":"Android / MTP","pt":"Android / MTP","ru":"Android / MTP","ja":"Android / MTP","zh":"Android / MTP","ko":"Android / MTP","ar":"Android / MTP"},
    "Camera / PTP":       {"en":"Camera / PTP","ro":"Cameră / PTP","fr":"Appareil photo / PTP","de":"Kamera / PTP","es":"Cámara / PTP","it":"Fotocamera / PTP","pt":"Câmera / PTP","ru":"Камера / PTP","ja":"カメラ / PTP","zh":"相机 / PTP","ko":"카메라 / PTP","ar":"الكاميرا / PTP"},
    "Network / Wireless": {"en":"Network / Wireless","ro":"Rețea / Wireless","fr":"Réseau / Sans fil","de":"Netzwerk / WLAN","es":"Red / Inalámbrico","it":"Rete / Wireless","pt":"Rede / Sem fios","ru":"Сеть / Беспроводная","ja":"ネットワーク / ワイヤレス","zh":"网络 / 无线","ko":"네트워크 / 무선","ar":"الشبكة / اللاسلكي"},
    "USB / Serial":       {"en":"USB / Serial","ro":"USB / Serial","fr":"USB / Série","de":"USB / Seriell","es":"USB / Serie","it":"USB / Seriale","pt":"USB / Serial","ru":"USB / Последовательный","ja":"USB / シリアル","zh":"USB / 串口","ko":"USB / 시리얼","ar":"USB / تسلسلي"},
    "Base":               {"en":"Base","ro":"De bază","fr":"Base","de":"Basis","es":"Base","it":"Base","pt":"Base","ru":"Основное","ja":"基本","zh":"基础","ko":"기본","ar":"الأساسي"},
    "Creative Tools":     {"en":"Creative Tools","ro":"Instrumente Creative","fr":"Outils Créatifs","de":"Kreativwerkzeuge","es":"Herramientas Creativas","it":"Strumenti Creativi","pt":"Ferramentas Criativas","ru":"Творческие инструменты","ja":"クリエイティブツール","zh":"创意工具","ko":"크리에이티브 도구","ar":"الأدوات الإبداعية"},
    "Graphical File Managers": {"en":"Graphical File Managers","ro":"Managere Grafice","fr":"Gestionnaires Graphiques","de":"Grafische Dateimanager","es":"Gestores Gráficos","it":"Gestori Grafici","pt":"Gerenciadores Gráficos","ru":"Графические менеджеры","ja":"グラフィカルFM","zh":"图形文件管理器","ko":"그래픽 파일 관리자","ar":"مديرو الملفات الرسومية"},
    "Terminal File Managers":  {"en":"Terminal File Managers","ro":"Managere Terminal","fr":"Gestionnaires Terminal","de":"Terminal-Dateimanager","es":"Gestores de Terminal","it":"Gestori Terminale","pt":"Gerenciadores de Terminal","ru":"Терминальные менеджеры","ja":"ターミナルFM","zh":"终端文件管理器","ko":"터미널 파일 관리자","ar":"مديرو ملفات الطرفية"},
    "Cloud & Network":         {"en":"Cloud & Network","ro":"Cloud și Rețea","fr":"Cloud et Réseau","de":"Cloud & Netzwerk","es":"Nube y Red","it":"Cloud e Rete","pt":"Nuvem e Rede","ru":"Облако и Сеть","ja":"クラウド & ネットワーク","zh":"云与网络","ko":"클라우드 & 네트워크","ar":"السحابة والشبكة"},
}

def TS(section_name):
    """Return translated section label."""
    d = _SEC_LABELS.get(section_name, {})
    return d.get(_LANG) or d.get("en", section_name)

# ── Repo badge style map ──────────────────────────────────────────────────────
REPO_STYLE = {
    "fedora":            ("#2965f1", "#0a1a3a", "#143060"),
    "rpmfusion-free":    ("#4fd9c4", "#0e2e2e", "#1a4040"),
    "rpmfusion-nonfree": ("#e84c3d", "#2e0e0e", "#401818"),
    "copr":              ("#7c6af7", "#18183a", "#28285a"),
    "copr-sneexy":       ("#7c6af7", "#18183a", "#28285a"),
    "vivaldi":           ("#e84c3d", "#2e0e0e", "#401818"),
    "google-chrome":     ("#4285f4", "#0a1a3a", "#143060"),
    "microsoft-edge":    ("#0078d7", "#0a1a3a", "#143060"),
    "librewolf":         ("#e84c3d", "#2e0e0e", "#401818"),
    "flatpak":           ("#4a90d9", "#0a1929", "#0d2137"),
    "github":            ("#f0f6fc", "#0d1117", "#1a2233"),
    "third-party":       ("#f7177a", "#2e0e1a", "#401828"),
}

_BADGE_KEY = {
    "fedora":             "badge_fedora",
    "rpmfusion-free":     "badge_rpmfusion_free",
    "rpmfusion-nonfree":  "badge_rpmfusion_nonfree",
    "copr":               "badge_copr",
    "copr-sneexy":        "badge_copr",
    "vivaldi":            "badge_vivaldi",
    "google-chrome":      "badge_google_chrome",
    "microsoft-edge":     "badge_microsoft_edge",
    "librewolf":          "badge_librewolf",
    "flatpak":            "badge_flatpak",
    "github":             "badge_github",
    "third-party":        "badge_third_party",
}

ACCENT_COLOR  = (0.486, 0.416, 0.969)   # #7c6af7
ACCENT2_COLOR = (0.310, 0.851, 0.769)   # #4fd9c4

# ── Hyprland config ───────────────────────────────────────────────────────────
HYPRLAND_CONF = os.path.expanduser("~/.config/hypr/hyprland.lua")
SENTINEL_FILE = os.path.expanduser("~/.config/faded-dream-autostart")

# ── Init system detection ─────────────────────────────────────────────────────
_INIT_SYSTEM: str | None = None
def detect_init() -> str:
    """Cached: systemd/runit/openrc/dinit/s6/unknown."""
    global _INIT_SYSTEM
    if _INIT_SYSTEM is not None: return _INIT_SYSTEM
    import subprocess
    if os.path.isdir("/run/systemd/system"): _INIT_SYSTEM = "systemd"; return _INIT_SYSTEM
    if os.path.isdir("/run/runit"): _INIT_SYSTEM = "runit"; return _INIT_SYSTEM
    for cmd, name in [(["rc-service","--version"],"openrc"),(["dinitctl","--version"],"dinit"),(["s6-rc","--version"],"s6")]:
        try:
            subprocess.run(cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, timeout=2)
            _INIT_SYSTEM = name; return _INIT_SYSTEM
        except (FileNotFoundError, subprocess.TimeoutExpired): pass
    _INIT_SYSTEM = "unknown"; return _INIT_SYSTEM

def cups_pkg() -> str:
    init = detect_init()
    if init == "systemd": return "cups"
    if init == "runit":  return "cups"
    if init == "openrc": return "cups"
    if init == "dinit":  return "cups"
    if init == "s6":     return "cups"
    return "cups"

# ── Brother printer drivers (shown in dedicated dialog) ───────────────────────
BROTHER_DRIVERS = [
    {"pkg": "brother-mfc-1810",      "name": "Brother MFC-1810",
     "desc": "Multifunction laser printer — mono, scan, copy, fax",
     "icon": "🖨️", "repo": "copr", "aur": False},
    {"pkg": "brother-mfc6490cw-lpr", "name": "Brother MFC-6490CW",
     "desc": "Inkjet multifunction printer with wireless and fax support",
     "icon": "🖨️", "repo": "copr", "aur": False},
    {"pkg": "brother-mfc-l2710dw",   "name": "Brother MFC-L2710DW",
     "desc": "Compact mono laser multifunction printer with duplex and wireless",
     "icon": "🖨️", "repo": "copr", "aur": False},
    {"pkg": "brother-mfc-l8690cdw",  "name": "Brother MFC-L8690CDW",
     "desc": "Colour laser multifunction printer with duplex, wireless and NFC",
     "icon": "🖨️", "repo": "copr", "aur": False},
    {"pkg": "brother-mfc-j1010dw",   "name": "Brother MFC-J1010DW",
     "desc": "Compact inkjet multifunction printer with wireless support",
     "icon": "🖨️", "repo": "copr", "aur": False},
    {"pkg": "brother-mfc-9330cdw",   "name": "Brother MFC-9330CDW",
     "desc": "Colour laser multifunction printer with wireless and duplex",
     "icon": "🖨️", "repo": "copr", "aur": False},
    {"pkg": "brother-mfc-l3770cdw",  "name": "Brother MFC-L3770CDW",
     "desc": "Colour LED multifunction printer with duplex, wireless and NFC",
     "icon": "🖨️", "repo": "copr", "aur": False},
    # Add more Brother models here as needed
]

# ── Printing ──────────────────────────────────────────────────────────────────
PRINTING = [
    {"section": "Printing", "packages": [
        {"pkg": "__cups__", "name": "CUPS",
         "desc": "Common Unix Printing System — the core print server. Automatically selects the right package for your init system",
         "icon": "🖨️", "repo": "fedora", "aur": False, "sub": [
            {"pkg": "cups-pdf",              "name": "CUPS PDF",           "repo": "fedora", "aur": False},
            {"pkg": "ghostscript",           "name": "Ghostscript",        "repo": "fedora", "aur": False},
            {"pkg": "gsfonts",               "name": "GS Fonts",           "repo": "fedora", "aur": False},
            {"pkg": "system-config-printer", "name": "Printer Config GUI", "repo": "fedora", "aur": False},
        ]},
        {"pkg": "hplip", "name": "HP Printer Driver",
         "desc": "Full-featured driver for HP printers and all-in-ones — includes scanning support",
         "icon": "🖨️", "repo": "fedora", "aur": False, "sub": []},
        {"pkg": "epson-inkjet-printer-escpr", "name": "Epson Driver (ESC/P-R)",
         "desc": "Driver for Epson inkjet printers using the ESC/P-R protocol",
         "icon": "🖨️", "repo": "copr", "aur": False, "sub": [
            {"pkg": "epson-inkjet-printer-escpr2", "name": "Epson Driver 2 (ESC/P-R)", "repo": "copr", "aur": False},
        ]},
    ]},
    {"section": "Brother Printers", "packages": [
        {"pkg": "__brother_dialog__", "name": "Brother Printer Drivers",
         "desc": "Open the Brother driver selector to install drivers for your specific model",
         "icon": "🖨️", "repo": "copr", "aur": False, "sub": [],
         "brother_dialog": True},
    ]},
    {"section": "Scanning", "packages": [
        {"pkg": "sane",        "name": "SANE",
         "desc": "Scanner Access Now Easy — backend for most flatbed and document scanners",
         "icon": "🔍", "repo": "fedora", "aur": False, "sub": []},
        {"pkg": "simple-scan", "name": "Simple Scan",
         "desc": "Clean GTK scan app — works out of the box with SANE-supported devices",
         "icon": "📄", "repo": "fedora", "aur": False, "sub": []},
        {"pkg": "xsane",       "name": "XSane",
         "desc": "Full-featured scanner frontend with advanced controls",
         "icon": "🔬", "repo": "copr", "aur": False, "sub": []},
    ]},
]

# ── COPR map (Fedora equivalent of AUR map) ───────────────────────────────────
FLATPAK_MAP = {
    "sober": ["flatpak","install","--noninteractive","flathub","org.vinegarhq.Sober"],
    "ytdn":  ["flatpak","install","--noninteractive","flathub","io.github.aandrew_me.ytdn"],
}

def _build_copr_map():
    m = {}
    def idx(items):
        for it in items:
            m[it["pkg"]] = it.get("aur", False)  # using "aur" key for compat with widgets.py
            for s in it.get("sub", []): m[s["pkg"]] = s.get("aur", False)
    for sec in GAMING:        idx(sec["packages"])
    for sec in OTHER:         idx(sec["packages"])
    for sec in PERIPHERALS:   idx(sec["packages"])
    for sec in COMMS:         idx(sec["packages"])
    for sec in FILE_TRANSFER: idx(sec["packages"])
    for sec in FILE_MANAGERS: idx(sec["packages"])
    for sec in PRINTING:      idx(sec["packages"])
    for drv in BROTHER_DRIVERS: m[drv["pkg"]] = drv.get("aur", False)
    idx(MEDIA)
    idx(OFFICE_BASE)
    for br in BROWSERS: m[br["pkg"]] = br.get("aur", False)
    m["__cups__"] = False  # sentinel resolved at install time
    for fp in FLATPAK_MAP: m[fp] = False
    return m

COPR_MAP = _build_copr_map()

# For compatibility with widgets.py which expects AUR_MAP
AUR_MAP = COPR_MAP

# ── GitHub packages (cloned + dnf builddep / custom build) ────────────────────
GITHUB_MAP = {
    "voiddream": {
        "install_cmd": ["git", "clone",
                        "https://github.com/FemBoyGamerTechGuy/VoidDream.git",
                        "/tmp/VoidDream-install"],
        "post_cmd":    ["bash", "-c", "cd packaging && dnf builddep -y voiddream.spec && rpmbuild -bb voiddream.spec && dnf install -y ~/rpmbuild/RPMS/*/voiddream-*.rpm"],
        "post_cwd":    "/tmp/VoidDream-install",
    },
}