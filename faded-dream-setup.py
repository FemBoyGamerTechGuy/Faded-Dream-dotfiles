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

# ── Translations ──────────────────────────────────────────────────────────────
import locale as _locale

TRANSLATIONS = {
    "en": {
        # window / nav
        "app_title":            "Faded Dream Setup \u2014 First Run",
        "sidebar_title":        "Faded Dream",
        "nav_welcome":          "Welcome",
        "nav_browser":          "Browser",
        "nav_gaming":           "Gaming",
        "nav_peripherals":      "Peripherals",
        "nav_file_transfer":    "File Transfer",
        "nav_office":           "Office",
        "nav_media":            "Media",
        "nav_comms":            "Comms",
        "nav_log":              "Log",
        # bottom bar
        "packages_selected":    "{n} packages selected",
        "startup_hint":         "toggle startup off after install to stop autolaunch",
        "run_at_startup":       "Run at startup",
        "skip_all":             "Skip All",
        "install_selected":     "Install Selected",
        # welcome
        "welcome_sub":          "Your dotfiles are installed.\nSelect optional packages across the tabs, then hit <b>Install</b>.\nToggle <i>Run at startup</i> off after install.",
        "card_browser_sub":     "Pick your default browser",
        "card_gaming_sub":      "Steam, Heroic, Wine, MangoHud",
        "card_peripherals_sub": "OpenRazer, Polychromatic, Piper",
        "card_filetransfer_sub":"Android, cameras, LAN sharing",
        "card_office_sub":      "LibreOffice + language packs",
        "card_media_sub":       "GIMP, Kdenlive, OBS Liberty",
        "card_comms_sub":       "Vesktop, Telegram, Thunderbird",
        # browser page
        "browser_section":      "Select Your Default Browser",
        "recommended":          "\u2b50 Recommended",
        # office page
        "lo_lang_section":      "LibreOffice Language Packs",
        # log page — section titles
        "log_what_title":       "What This Installer Does",
        "log_row_browser_t":    "Browser",
        "log_row_browser_b":    "Pick one browser \u2014 LibreWolf, Zen, Firefox, Vivaldi, Chrome or Edge. Your choice is installed and $Browser in hyprland.conf is patched automatically so Super+B opens it.",
        "log_row_gaming_t":     "Gaming",
        "log_row_gaming_b":     "Steam (lib32), Heroic Games Launcher, Wine + Winetricks/Mono/Gecko, ProtonPlus, GameMode + 32-bit, MangoHud + 32-bit, MangoJuice. Selecting Wine auto-selects its three sub-packages.",
        "log_row_periph_t":     "Peripherals",
        "log_row_periph_b":     "OpenRazer daemon + kernel driver (DKMS) + Python library for Razer hardware. Polychromatic for per-key RGB and effects. Piper for multi-brand mouse/keyboard config (Logitech, SteelSeries, Roccat\u2026). Solaar for Logitech Unifying/Bolt receivers. jmtpfs and gphotofs for mounting Android phones and cameras \u2014 all AUR.",
        "log_row_office_t":     "Office",
        "log_row_office_b":     "LibreOffice Fresh plus any of 12 language packs you select (English UK, Romanian, French, German, Spanish, Italian, Portuguese, Russian, Japanese, Chinese, Korean, Arabic).",
        "log_row_media_t":      "Media",
        "log_row_media_b":      "Mirage image viewer, GIMP, Inkscape, Kdenlive video editor, HandBrake converter, OBS Studio Liberty (libre build).",
        "log_row_ft_t":         "File Transfer",
        "log_row_ft_b":         "Android MTP with jmtpfs and go-mtpfs. Camera PTP via gphotofs and gphoto2. Wireless: Warpinator, LocalSend (cross-platform AirDrop), Croc (encrypted P2P). USB: Android Tools (ADB/fastboot) and Scrcpy for screen mirroring.",
        "log_row_comms_t":      "Comms",
        "log_row_comms_b":      "Vesktop (Discord + Vencord), Telegram, Element (Matrix), Thunderbird + optional language packs, Obsidian notes.",
        "log_row_how_t":        "How It Works",
        "log_row_how_b":        "Repo packages are installed in one pacman batch. Each AUR package (paru) is built and installed individually \u2014 you will see full compile output here in real time. After install the startup toggle is disabled automatically so it won\u2019t launch again. You can re-enable it anytime from the footer.",
        # install log lines
        "log_header":           "Faded Dream \u2014 Installing selected packages",
        "log_repo_line":        "  repo packages  ({n}): {pkgs}",
        "log_aur_line":         "  AUR packages   ({n}): {pkgs}",
        "log_browser_patch":    "  browser patch: $Browser = {exec}",
        "log_done":             "\u2713  All done!",
        "log_done_bar":         "\u2713 All done!",
        "log_error":            "[error] {exc}",
        # install progress bar
        "prog_repo":            "Installing {n} repo packages...",
        "prog_pkg":             "Installing {pkg}...",
        "prog_patch":           "Patching hyprland.conf \u2192 {exec}...",
            "log_banner_pacman": "\u2500\u2500 pacman  ({n} pkg) \u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500",
        "log_banner_paru": "\u2500\u2500 paru  {pkg} \u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500",
        "log_banner_hypr": "\u2500\u2500 hyprland.conf \u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500",
        "log_browser_set": "  $Browser = {exec}",
        "badge_aur": "AUR",
        "badge_extra": "extra",
        "badge_galaxy": "galaxy",
        "badge_world": "world",
        "badge_lib32": "lib32",
        "badge_multilib": "multilib",
        "nothing_selected": "Nothing selected \u2014 closing.",
        "lang_label": "Language",
        "welcome_title": "Faded Dream",
},
    "ro": {
        "app_title":            "Configurare Faded Dream \u2014 Prima Rulare",
        "sidebar_title":        "Faded Dream",
        "nav_welcome":          "Bun venit",
        "nav_browser":          "Browser",
        "nav_gaming":           "Jocuri",
        "nav_peripherals":      "Periferice",
        "nav_file_transfer":    "Transfer Fi\u0219iere",
        "nav_office":           "Birou",
        "nav_media":            "Media",
        "nav_comms":            "Comunicare",
        "nav_log":              "Jurnal",
        "packages_selected":    "{n} pachete selectate",
        "startup_hint":         "dezactiveaz\u0103 pornirea automat\u0103 dup\u0103 instalare",
        "run_at_startup":       "Pornire automat\u0103",
        "skip_all":             "Sari tot",
        "install_selected":     "Instaleaz\u0103 Selectate",
        "welcome_sub":          "Dotfile-urile tale sunt instalate.\nSelecteaz\u0103 pachete op\u021bionale din file, apoi apas\u0103 <b>Instaleaz\u0103</b>.\nDezactiveaz\u0103 <i>Pornire automat\u0103</i> dup\u0103 instalare.",
        "card_browser_sub":     "Alege browserul implicit",
        "card_gaming_sub":      "Steam, Heroic, Wine, MangoHud",
        "card_peripherals_sub": "OpenRazer, Polychromatic, Piper",
        "card_filetransfer_sub":"Android, camere, partajare LAN",
        "card_office_sub":      "LibreOffice + pachete de limb\u0103",
        "card_media_sub":       "GIMP, Kdenlive, OBS Liberty",
        "card_comms_sub":       "Vesktop, Telegram, Thunderbird",
        "browser_section":      "Selecteaz\u0103 Browserul Implicit",
        "recommended":          "\u2b50 Recomandat",
        "lo_lang_section":      "Pachete de Limb\u0103 LibreOffice",
        "log_what_title":       "Ce Face Acest Instalator",
        "log_row_browser_t":    "Browser",
        "log_row_browser_b":    "Alege un browser \u2014 LibreWolf, Zen, Firefox, Vivaldi, Chrome sau Edge. Alegerea ta este instalat\u0103 \u0219i $Browser din hyprland.conf este actualizat automat astfel \u00eenc\u00e2t Super+B s\u0103 \u00eel deschid\u0103.",
        "log_row_gaming_t":     "Gaming",
        "log_row_gaming_b":     "Steam (lib32), Heroic Games Launcher, Wine + Winetricks/Mono/Gecko, ProtonPlus, GameMode + 32-bit, MangoHud + 32-bit, MangoJuice. Selectarea Wine selecteaz\u0103 automat cele trei sub-pachete.",
        "log_row_periph_t":     "Periferice",
        "log_row_periph_b":     "Daemon OpenRazer + driver kernel (DKMS) + bibliotec\u0103 Python pentru hardware Razer. Polychromatic pentru RGB per-tast\u0103 \u0219i efecte. Piper pentru configurare mouse/tastatur\u0103 multi-brand (Logitech, SteelSeries, Roccat\u2026). Solaar pentru receptoare Logitech Unifying/Bolt. jmtpfs \u0219i gphotofs pentru montarea telefoanelor Android \u0219i camerelor \u2014 toate AUR.",
        "log_row_office_t":     "Office",
        "log_row_office_b":     "LibreOffice Fresh plus oricare dintre cele 12 pachete de limb\u0103 (Englez\u0103 UK, Rom\u00e2n\u0103, Francez\u0103, German\u0103, Spaniol\u0103, Italian\u0103, Portughez\u0103, Rus\u0103, Japonez\u0103, Chineze\u0103, Coreean\u0103, Arab\u0103).",
        "log_row_media_t":      "Media",
        "log_row_media_b":      "Vizualizator imagini Mirage, GIMP, Inkscape, editor video Kdenlive, convertor HandBrake, OBS Studio Liberty (build liber).",
        "log_row_ft_t":         "Transfer Fi\u0219iere",
        "log_row_ft_b":         "Android MTP cu jmtpfs \u0219i go-mtpfs. Camer\u0103 PTP via gphotofs \u0219i gphoto2. Wireless: Warpinator, LocalSend (AirDrop cross-platform), Croc (P2P criptat). USB: Android Tools (ADB/fastboot) \u0219i Scrcpy pentru oglindire ecran.",
        "log_row_comms_t":      "Comunicare",
        "log_row_comms_b":      "Vesktop (Discord + Vencord), Telegram, Element (Matrix), Thunderbird + pachete de limb\u0103 op\u021bionale, noti\u021be Obsidian.",
        "log_row_how_t":        "Cum Func\u021bioneaz\u0103",
        "log_row_how_b":        "Pachetele din repo sunt instalate \u00edntr-un singur batch pacman. Fiecare pachet AUR (paru) este compilat \u0219i instalat individual \u2014 vei vedea output-ul complet de compilare \u00een timp real. Dup\u0103 instalare, pornirea automat\u0103 este dezactivat\u0103 automat. O po\u021bi reactiva oric\u00e2nd din footer.",
        "log_header":           "Faded Dream \u2014 Instalare pachete selectate",
        "log_repo_line":        "  pachete repo  ({n}): {pkgs}",
        "log_aur_line":         "  pachete AUR   ({n}): {pkgs}",
        "log_browser_patch":    "  patch browser: $Browser = {exec}",
        "log_done":             "\u2713  Gata!",
        "log_done_bar":         "\u2713 Gata!",
        "log_error":            "[eroare] {exc}",
        "prog_repo":            "Instalare {n} pachete repo...",
        "prog_pkg":             "Instalare {pkg}...",
        "prog_patch":           "Actualizare hyprland.conf \u2192 {exec}...",
            "log_banner_pacman": "\u2500\u2500 pacman  ({n} pachete) \u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500",
        "log_banner_paru": "\u2500\u2500 paru  {pkg} \u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500",
        "log_banner_hypr": "\u2500\u2500 hyprland.conf \u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500",
        "log_browser_set": "  $Browser = {exec}",
        "badge_aur": "AUR",
        "badge_extra": "extra",
        "badge_galaxy": "galaxy",
        "badge_world": "world",
        "badge_lib32": "lib32",
        "badge_multilib": "multilib",
        "nothing_selected": "Nimic selectat \u2014 se \u00eenchide.",
        "lang_label": "Limb\u0103",
        "welcome_title": "Faded Dream",
},
    "fr": {
        "app_title":            "Configuration Faded Dream \u2014 Premi\u00e8re Ex\u00e9cution",
        "sidebar_title":        "Faded Dream",
        "nav_welcome":          "Bienvenue",
        "nav_browser":          "Navigateur",
        "nav_gaming":           "Jeux",
        "nav_peripherals":      "P\u00e9riph\u00e9riques",
        "nav_file_transfer":    "Transfert Fichiers",
        "nav_office":           "Bureau",
        "nav_media":            "M\u00e9dias",
        "nav_comms":            "Communication",
        "nav_log":              "Journal",
        "packages_selected":    "{n} paquets s\u00e9lectionn\u00e9s",
        "startup_hint":         "d\u00e9sactiver le d\u00e9marrage apr\u00e8s l\u2019installation",
        "run_at_startup":       "D\u00e9marrage auto",
        "skip_all":             "Tout ignorer",
        "install_selected":     "Installer la s\u00e9lection",
        "welcome_sub":          "Vos dotfiles sont install\u00e9s.\nS\u00e9lectionnez des paquets optionnels dans les onglets, puis cliquez sur <b>Installer</b>.\nD\u00e9sactivez <i>D\u00e9marrage auto</i> apr\u00e8s l\u2019installation.",
        "card_browser_sub":     "Choisissez votre navigateur",
        "card_gaming_sub":      "Steam, Heroic, Wine, MangoHud",
        "card_peripherals_sub": "OpenRazer, Polychromatic, Piper",
        "card_filetransfer_sub":"Android, appareils photo, r\u00e9seau",
        "card_office_sub":      "LibreOffice + packs de langue",
        "card_media_sub":       "GIMP, Kdenlive, OBS Liberty",
        "card_comms_sub":       "Vesktop, Telegram, Thunderbird",
        "browser_section":      "S\u00e9lectionnez Votre Navigateur Par D\u00e9faut",
        "recommended":          "\u2b50 Recommand\u00e9",
        "lo_lang_section":      "Packs de Langue LibreOffice",
        "log_what_title":       "Ce Que Fait Cet Installateur",
        "log_row_browser_t":    "Navigateur",
        "log_row_browser_b":    "Choisissez un navigateur \u2014 LibreWolf, Zen, Firefox, Vivaldi, Chrome ou Edge. Votre choix est install\u00e9 et $Browser dans hyprland.conf est patch\u00e9 automatiquement pour que Super+B l\u2019ouvre.",
        "log_row_gaming_t":     "Jeux",
        "log_row_gaming_b":     "Steam (lib32), Heroic Games Launcher, Wine + Winetricks/Mono/Gecko, ProtonPlus, GameMode + 32 bits, MangoHud + 32 bits, MangoJuice. S\u00e9lectionner Wine s\u00e9lectionne automatiquement ses trois sous-paquets.",
        "log_row_periph_t":     "P\u00e9riph\u00e9riques",
        "log_row_periph_b":     "D\u00e9mon OpenRazer + pilote noyau (DKMS) + biblioth\u00e8que Python pour le mat\u00e9riel Razer. Polychromatic pour le RGB par touche et les effets. Piper pour la configuration souris/clavier multi-marque (Logitech, SteelSeries, Roccat\u2026). Solaar pour les r\u00e9cepteurs Logitech Unifying/Bolt. jmtpfs et gphotofs pour monter les t\u00e9l\u00e9phones Android et appareils photo \u2014 tous AUR.",
        "log_row_office_t":     "Bureau",
        "log_row_office_b":     "LibreOffice Fresh plus n\u2019importe lequel des 12 packs de langue (Anglais UK, Roumain, Fran\u00e7ais, Allemand, Espagnol, Italien, Portugais, Russe, Japonais, Chinois, Cor\u00e9en, Arabe).",
        "log_row_media_t":      "M\u00e9dias",
        "log_row_media_b":      "Visionneuse d\u2019images Mirage, GIMP, Inkscape, \u00e9diteur vid\u00e9o Kdenlive, convertisseur HandBrake, OBS Studio Liberty (build libre).",
        "log_row_ft_t":         "Transfert Fichiers",
        "log_row_ft_b":         "Android MTP avec jmtpfs et go-mtpfs. Camera PTP via gphotofs et gphoto2. Sans fil\u00a0: Warpinator, LocalSend (AirDrop multiplateforme), Croc (P2P chiffr\u00e9). USB\u00a0: Android Tools (ADB/fastboot) et Scrcpy pour la mise en miroir d\u2019\u00e9cran.",
        "log_row_comms_t":      "Communication",
        "log_row_comms_b":      "Vesktop (Discord + Vencord), Telegram, Element (Matrix), Thunderbird + packs de langue optionnels, notes Obsidian.",
        "log_row_how_t":        "Comment \u00c7a Fonctionne",
        "log_row_how_b":        "Les paquets du d\u00e9p\u00f4t sont install\u00e9s en un seul batch pacman. Chaque paquet AUR (paru) est compil\u00e9 et install\u00e9 individuellement \u2014 vous verrez la sortie compl\u00e8te de compilation en temps r\u00e9el. Apr\u00e8s l\u2019installation le d\u00e9marrage automatique est d\u00e9sactiv\u00e9 automatiquement. Vous pouvez le r\u00e9activer \u00e0 tout moment depuis le pied de page.",
        "log_header":           "Faded Dream \u2014 Installation des paquets s\u00e9lectionn\u00e9s",
        "log_repo_line":        "  paquets d\u00e9p\u00f4t  ({n}): {pkgs}",
        "log_aur_line":         "  paquets AUR    ({n}): {pkgs}",
        "log_browser_patch":    "  patch navigateur: $Browser = {exec}",
        "log_done":             "\u2713  Termin\u00e9\u00a0!",
        "log_done_bar":         "\u2713 Termin\u00e9\u00a0!",
        "log_error":            "[erreur] {exc}",
        "prog_repo":            "Installation de {n} paquets du d\u00e9p\u00f4t...",
        "prog_pkg":             "Installation de {pkg}...",
        "prog_patch":           "Mise \u00e0 jour de hyprland.conf \u2192 {exec}...",
            "log_banner_pacman": "\u2500\u2500 pacman  ({n} paquets) \u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500",
        "log_banner_paru": "\u2500\u2500 paru  {pkg} \u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500",
        "log_banner_hypr": "\u2500\u2500 hyprland.conf \u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500",
        "log_browser_set": "  $Browser = {exec}",
        "badge_aur": "AUR",
        "badge_extra": "extra",
        "badge_galaxy": "galaxy",
        "badge_world": "world",
        "badge_lib32": "lib32",
        "badge_multilib": "multilib",
        "nothing_selected": "Rien de s\u00e9lectionn\u00e9 \u2014 fermeture.",
        "lang_label": "Langue",
        "welcome_title": "Faded Dream",
},
    "de": {
        "app_title":            "Faded Dream Einrichtung \u2014 Erster Start",
        "sidebar_title":        "Faded Dream",
        "nav_welcome":          "Willkommen",
        "nav_browser":          "Browser",
        "nav_gaming":           "Gaming",
        "nav_peripherals":      "Peripherie",
        "nav_file_transfer":    "Datei\u00fcbertragung",
        "nav_office":           "B\u00fcro",
        "nav_media":            "Medien",
        "nav_comms":            "Kommunikation",
        "nav_log":              "Protokoll",
        "packages_selected":    "{n} Pakete ausgew\u00e4hlt",
        "startup_hint":         "Autostart nach Installation deaktivieren",
        "run_at_startup":       "Autostart",
        "skip_all":             "Alles \u00fcberspringen",
        "install_selected":     "Auswahl installieren",
        "welcome_sub":          "Deine Dotfiles sind installiert.\nW\u00e4hle optionale Pakete in den Tabs und klicke auf <b>Installieren</b>.\nDeaktiviere <i>Autostart</i> nach der Installation.",
        "card_browser_sub":     "Standardbrowser w\u00e4hlen",
        "card_gaming_sub":      "Steam, Heroic, Wine, MangoHud",
        "card_peripherals_sub": "OpenRazer, Polychromatic, Piper",
        "card_filetransfer_sub":"Android, Kameras, LAN-Freigabe",
        "card_office_sub":      "LibreOffice + Sprachpakete",
        "card_media_sub":       "GIMP, Kdenlive, OBS Liberty",
        "card_comms_sub":       "Vesktop, Telegram, Thunderbird",
        "browser_section":      "Standardbrowser Ausw\u00e4hlen",
        "recommended":          "\u2b50 Empfohlen",
        "lo_lang_section":      "LibreOffice-Sprachpakete",
        "log_what_title":       "Was Dieser Installer Macht",
        "log_row_browser_t":    "Browser",
        "log_row_browser_b":    "W\u00e4hle einen Browser \u2014 LibreWolf, Zen, Firefox, Vivaldi, Chrome oder Edge. Deine Wahl wird installiert und $Browser in hyprland.conf wird automatisch angepasst, damit Super+B ihn \u00f6ffnet.",
        "log_row_gaming_t":     "Gaming",
        "log_row_gaming_b":     "Steam (lib32), Heroic Games Launcher, Wine + Winetricks/Mono/Gecko, ProtonPlus, GameMode + 32-bit, MangoHud + 32-bit, MangoJuice. Die Auswahl von Wine w\u00e4hlt automatisch die drei Unterpakete.",
        "log_row_periph_t":     "Peripherie",
        "log_row_periph_b":     "OpenRazer-Daemon + Kernel-Treiber (DKMS) + Python-Bibliothek f\u00fcr Razer-Hardware. Polychromatic f\u00fcr Einzel-Tasten-RGB und Effekte. Piper f\u00fcr Multi-Marken Maus-/Tastaturkonfiguration (Logitech, SteelSeries, Roccat\u2026). Solaar f\u00fcr Logitech Unifying/Bolt-Empf\u00e4nger. jmtpfs und gphotofs zum Einbinden von Android-Telefonen und Kameras \u2014 alles AUR.",
        "log_row_office_t":     "B\u00fcro",
        "log_row_office_b":     "LibreOffice Fresh plus beliebige der 12 Sprachpakete (Englisch UK, Rum\u00e4nisch, Franz\u00f6sisch, Deutsch, Spanisch, Italienisch, Portugiesisch, Russisch, Japanisch, Chinesisch, Koreanisch, Arabisch).",
        "log_row_media_t":      "Medien",
        "log_row_media_b":      "Mirage-Bildbetrachter, GIMP, Inkscape, Kdenlive-Videoeditor, HandBrake-Konverter, OBS Studio Liberty (freier Build).",
        "log_row_ft_t":         "Datei\u00fcbertragung",
        "log_row_ft_b":         "Android MTP mit jmtpfs und go-mtpfs. Kamera PTP via gphotofs und gphoto2. Drahtlos: Warpinator, LocalSend (plattform\u00fcbergreifendes AirDrop), Croc (verschl\u00fcsseltes P2P). USB: Android Tools (ADB/fastboot) und Scrcpy f\u00fcr Screen-Mirroring.",
        "log_row_comms_t":      "Kommunikation",
        "log_row_comms_b":      "Vesktop (Discord + Vencord), Telegram, Element (Matrix), Thunderbird + optionale Sprachpakete, Obsidian-Notizen.",
        "log_row_how_t":        "So Funktioniert Es",
        "log_row_how_b":        "Repository-Pakete werden in einem einzigen pacman-Batch installiert. Jedes AUR-Paket (paru) wird einzeln kompiliert und installiert \u2014 du siehst die vollst\u00e4ndige Kompilierungsausgabe in Echtzeit. Nach der Installation wird der Autostart automatisch deaktiviert. Du kannst ihn jederzeit \u00fcber die Fu\u00dfzeile wieder aktivieren.",
        "log_header":           "Faded Dream \u2014 Ausgew\u00e4hlte Pakete werden installiert",
        "log_repo_line":        "  Repo-Pakete  ({n}): {pkgs}",
        "log_aur_line":         "  AUR-Pakete   ({n}): {pkgs}",
        "log_browser_patch":    "  Browser-Patch: $Browser = {exec}",
        "log_done":             "\u2713  Fertig!",
        "log_done_bar":         "\u2713 Fertig!",
        "log_error":            "[Fehler] {exc}",
        "prog_repo":            "{n} Repo-Pakete werden installiert...",
        "prog_pkg":             "{pkg} wird installiert...",
        "prog_patch":           "hyprland.conf wird aktualisiert \u2192 {exec}...",
            "log_banner_pacman": "\u2500\u2500 pacman  ({n} Pakete) \u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500",
        "log_banner_paru": "\u2500\u2500 paru  {pkg} \u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500",
        "log_banner_hypr": "\u2500\u2500 hyprland.conf \u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500",
        "log_browser_set": "  $Browser = {exec}",
        "badge_aur": "AUR",
        "badge_extra": "extra",
        "badge_galaxy": "galaxy",
        "badge_world": "world",
        "badge_lib32": "lib32",
        "badge_multilib": "multilib",
        "nothing_selected": "Nichts ausgew\u00e4hlt \u2014 wird geschlossen.",
        "lang_label": "Sprache",
        "welcome_title": "Faded Dream",
},
    "es": {
        "app_title":            "Configuraci\u00f3n Faded Dream \u2014 Primera Ejecuci\u00f3n",
        "sidebar_title":        "Faded Dream",
        "nav_welcome":          "Bienvenido",
        "nav_browser":          "Navegador",
        "nav_gaming":           "Juegos",
        "nav_peripherals":      "Perif\u00e9ricos",
        "nav_file_transfer":    "Transferencia",
        "nav_office":           "Oficina",
        "nav_media":            "Medios",
        "nav_comms":            "Comunicaci\u00f3n",
        "nav_log":              "Registro",
        "packages_selected":    "{n} paquetes seleccionados",
        "startup_hint":         "desactivar inicio autom\u00e1tico tras instalar",
        "run_at_startup":       "Inicio autom\u00e1tico",
        "skip_all":             "Omitir todo",
        "install_selected":     "Instalar selecci\u00f3n",
        "welcome_sub":          "Tus dotfiles est\u00e1n instalados.\nSelecciona paquetes opcionales en las pesta\u00f1as y pulsa <b>Instalar</b>.\nDesactiva <i>Inicio autom\u00e1tico</i> tras instalar.",
        "card_browser_sub":     "Elige tu navegador predeterminado",
        "card_gaming_sub":      "Steam, Heroic, Wine, MangoHud",
        "card_peripherals_sub": "OpenRazer, Polychromatic, Piper",
        "card_filetransfer_sub":"Android, c\u00e1maras, red local",
        "card_office_sub":      "LibreOffice + paquetes de idioma",
        "card_media_sub":       "GIMP, Kdenlive, OBS Liberty",
        "card_comms_sub":       "Vesktop, Telegram, Thunderbird",
        "browser_section":      "Selecciona Tu Navegador Predeterminado",
        "recommended":          "\u2b50 Recomendado",
        "lo_lang_section":      "Paquetes de Idioma de LibreOffice",
        "log_what_title":       "Qu\u00e9 Hace Este Instalador",
        "log_row_browser_t":    "Navegador",
        "log_row_browser_b":    "Elige un navegador \u2014 LibreWolf, Zen, Firefox, Vivaldi, Chrome o Edge. Tu elecci\u00f3n se instala y $Browser en hyprland.conf se parchea autom\u00e1ticamente para que Super+B lo abra.",
        "log_row_gaming_t":     "Juegos",
        "log_row_gaming_b":     "Steam (lib32), Heroic Games Launcher, Wine + Winetricks/Mono/Gecko, ProtonPlus, GameMode + 32 bits, MangoHud + 32 bits, MangoJuice. Seleccionar Wine selecciona autom\u00e1ticamente sus tres subpaquetes.",
        "log_row_periph_t":     "Perif\u00e9ricos",
        "log_row_periph_b":     "Daemon OpenRazer + controlador kernel (DKMS) + biblioteca Python para hardware Razer. Polychromatic para RGB por tecla y efectos. Piper para configuraci\u00f3n de rat\u00f3n/teclado multimarca (Logitech, SteelSeries, Roccat\u2026). Solaar para receptores Logitech Unifying/Bolt. jmtpfs y gphotofs para montar tel\u00e9fonos Android y c\u00e1maras \u2014 todo AUR.",
        "log_row_office_t":     "Oficina",
        "log_row_office_b":     "LibreOffice Fresh m\u00e1s cualquiera de los 12 paquetes de idioma (Ingl\u00e9s UK, Rumano, Franc\u00e9s, Alem\u00e1n, Espa\u00f1ol, Italiano, Portugu\u00e9s, Ruso, Japon\u00e9s, Chino, Coreano, \u00c1rabe).",
        "log_row_media_t":      "Medios",
        "log_row_media_b":      "Visor de im\u00e1genes Mirage, GIMP, Inkscape, editor de v\u00eddeo Kdenlive, conversor HandBrake, OBS Studio Liberty (build libre).",
        "log_row_ft_t":         "Transferencia",
        "log_row_ft_b":         "Android MTP con jmtpfs y go-mtpfs. C\u00e1mara PTP via gphotofs y gphoto2. Inal\u00e1mbrico: Warpinator, LocalSend (AirDrop multiplataforma), Croc (P2P cifrado). USB: Android Tools (ADB/fastboot) y Scrcpy para duplicaci\u00f3n de pantalla.",
        "log_row_comms_t":      "Comunicaci\u00f3n",
        "log_row_comms_b":      "Vesktop (Discord + Vencord), Telegram, Element (Matrix), Thunderbird + paquetes de idioma opcionales, notas Obsidian.",
        "log_row_how_t":        "C\u00f3mo Funciona",
        "log_row_how_b":        "Los paquetes del repositorio se instalan en un \u00fanico batch de pacman. Cada paquete AUR (paru) se compila e instala individualmente \u2014 ver\u00e1s la salida completa de compilaci\u00f3n en tiempo real. Tras la instalaci\u00f3n el inicio autom\u00e1tico se desactiva autom\u00e1ticamente. Puedes reactivarlo en cualquier momento desde el pie de p\u00e1gina.",
        "log_header":           "Faded Dream \u2014 Instalando paquetes seleccionados",
        "log_repo_line":        "  paquetes repo  ({n}): {pkgs}",
        "log_aur_line":         "  paquetes AUR   ({n}): {pkgs}",
        "log_browser_patch":    "  parche navegador: $Browser = {exec}",
        "log_done":             "\u2713  \u00a1Listo!",
        "log_done_bar":         "\u2713 \u00a1Listo!",
        "log_error":            "[error] {exc}",
        "prog_repo":            "Instalando {n} paquetes del repositorio...",
        "prog_pkg":             "Instalando {pkg}...",
        "prog_patch":           "Actualizando hyprland.conf \u2192 {exec}...",
            "log_banner_pacman": "\u2500\u2500 pacman  ({n} paquetes) \u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500",
        "log_banner_paru": "\u2500\u2500 paru  {pkg} \u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500",
        "log_banner_hypr": "\u2500\u2500 hyprland.conf \u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500",
        "log_browser_set": "  $Browser = {exec}",
        "badge_aur": "AUR",
        "badge_extra": "extra",
        "badge_galaxy": "galaxy",
        "badge_world": "world",
        "badge_lib32": "lib32",
        "badge_multilib": "multilib",
        "nothing_selected": "Nada seleccionado \u2014 cerrando.",
        "lang_label": "Idioma",
        "welcome_title": "Faded Dream",
},
    "it": {
        "app_title":                   "Configurazione Faded Dream \u2014 Primo Avvio",
        "sidebar_title":               "Faded Dream",
        "nav_welcome":                 "Benvenuto",
        "nav_browser":                 "Browser",
        "nav_gaming":                  "Gaming",
        "nav_peripherals":             "Periferiche",
        "nav_file_transfer":           "Trasferimento File",
        "nav_office":                  "Ufficio",
        "nav_media":                   "Media",
        "nav_comms":                   "Comunicazione",
        "nav_log":                     "Registro",
        "packages_selected":           "{n} pacchetti selezionati",
        "startup_hint":                "disattiva l\u2019avvio automatico dopo l\u2019installazione",
        "run_at_startup":              "Avvio automatico",
        "skip_all":                    "Salta tutto",
        "install_selected":            "Installa selezionati",
        "welcome_sub":                 "I tuoi dotfile sono installati.\nSeleziona i pacchetti opzionali nelle schede, poi clicca <b>Installa</b>.\nDisattiva <i>Avvio automatico</i> dopo l\u2019installazione.",
        "card_browser_sub":            "Scegli il browser predefinito",
        "card_gaming_sub":             "Steam, Heroic, Wine, MangoHud",
        "card_peripherals_sub":        "OpenRazer, Polychromatic, Piper",
        "card_filetransfer_sub":       "Android, fotocamere, condivisione LAN",
        "card_office_sub":             "LibreOffice + pacchetti lingua",
        "card_media_sub":              "GIMP, Kdenlive, OBS Liberty",
        "card_comms_sub":              "Vesktop, Telegram, Thunderbird",
        "browser_section":             "Seleziona il Browser Predefinito",
        "recommended":                 "\u2b50 Consigliato",
        "lo_lang_section":             "Pacchetti Lingua LibreOffice",
        "log_what_title":              "Cosa Fa Questo Installer",
        "log_row_browser_t":           "Browser",
        "log_row_browser_b":           "Scegli un browser \u2014 LibreWolf, Zen, Firefox, Vivaldi, Chrome o Edge. La tua scelta viene installata e $Browser in hyprland.conf viene aggiornato automaticamente in modo che Super+B lo apra.",
        "log_row_gaming_t":            "Gaming",
        "log_row_gaming_b":            "Steam (lib32), Heroic Games Launcher, Wine + Winetricks/Mono/Gecko, ProtonPlus, GameMode + 32-bit, MangoHud + 32-bit, MangoJuice. Selezionare Wine seleziona automaticamente i tre sotto-pacchetti.",
        "log_row_periph_t":            "Periferiche",
        "log_row_periph_b":            "Daemon OpenRazer + driver kernel (DKMS) + libreria Python per hardware Razer. Polychromatic per RGB per tasto ed effetti. Piper per configurazione mouse/tastiera multi-brand (Logitech, SteelSeries, Roccat\u2026). Solaar per ricevitori Logitech Unifying/Bolt. jmtpfs e gphotofs per montare telefoni Android e fotocamere \u2014 tutti AUR.",
        "log_row_office_t":            "Ufficio",
        "log_row_office_b":            "LibreOffice Fresh pi\u00f9 qualsiasi dei 12 pacchetti lingua (Inglese UK, Rumeno, Francese, Tedesco, Spagnolo, Italiano, Portoghese, Russo, Giapponese, Cinese, Coreano, Arabo).",
        "log_row_media_t":             "Media",
        "log_row_media_b":             "Visualizzatore immagini Mirage, GIMP, Inkscape, editor video Kdenlive, convertitore HandBrake, OBS Studio Liberty (build libera).",
        "log_row_ft_t":                "Trasferimento File",
        "log_row_ft_b":                "Android MTP con jmtpfs e go-mtpfs. Fotocamera PTP via gphotofs e gphoto2. Wireless: Warpinator, LocalSend (AirDrop multipiattaforma), Croc (P2P cifrato). USB: Android Tools (ADB/fastboot) e Scrcpy per il mirroring dello schermo.",
        "log_row_comms_t":             "Comunicazione",
        "log_row_comms_b":             "Vesktop (Discord + Vencord), Telegram, Element (Matrix), Thunderbird + pacchetti lingua opzionali, note Obsidian.",
        "log_row_how_t":               "Come Funziona",
        "log_row_how_b":               "I pacchetti del repository vengono installati in un unico batch pacman. Ogni pacchetto AUR (paru) viene compilato e installato singolarmente \u2014 vedrai l\u2019output completo di compilazione in tempo reale. Dopo l\u2019installazione l\u2019avvio automatico viene disabilitato automaticamente. Puoi riattivarlo in qualsiasi momento dal pi\u00e8 di pagina.",
        "log_header":                  "Faded Dream \u2014 Installazione pacchetti selezionati",
        "log_repo_line":               "  pacchetti repo  ({n}): {pkgs}",
        "log_aur_line":                "  pacchetti AUR   ({n}): {pkgs}",
        "log_browser_patch":           "  patch browser: $Browser = {exec}",
        "log_done":                    "\u2713  Fatto!",
        "log_done_bar":                "\u2713 Fatto!",
        "log_error":                   "[errore] {exc}",
        "prog_repo":                   "Installazione di {n} pacchetti repo...",
        "prog_pkg":                    "Installazione di {pkg}...",
        "prog_patch":                  "Aggiornamento hyprland.conf \u2192 {exec}...",
            "log_banner_pacman": "\u2500\u2500 pacman  ({n} pacchetti) \u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500",
        "log_banner_paru": "\u2500\u2500 paru  {pkg} \u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500",
        "log_banner_hypr": "\u2500\u2500 hyprland.conf \u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500",
        "log_browser_set": "  $Browser = {exec}",
        "badge_aur": "AUR",
        "badge_extra": "extra",
        "badge_galaxy": "galaxy",
        "badge_world": "world",
        "badge_lib32": "lib32",
        "badge_multilib": "multilib",
        "nothing_selected": "Nulla selezionato \u2014 chiusura.",
        "lang_label": "Lingua",
        "welcome_title": "Faded Dream",
},
    "pt": {
        "app_title":                   "Configura\u00e7\u00e3o Faded Dream \u2014 Primeira Execu\u00e7\u00e3o",
        "sidebar_title":               "Faded Dream",
        "nav_welcome":                 "Bem-vindo",
        "nav_browser":                 "Navegador",
        "nav_gaming":                  "Jogos",
        "nav_peripherals":             "Perif\u00e9ricos",
        "nav_file_transfer":           "Transfer\u00eancia",
        "nav_office":                  "Escrit\u00f3rio",
        "nav_media":                   "M\u00eddia",
        "nav_comms":                   "Comunica\u00e7\u00e3o",
        "nav_log":                     "Registo",
        "packages_selected":           "{n} pacotes selecionados",
        "startup_hint":                "desativar arranque autom\u00e1tico ap\u00f3s instala\u00e7\u00e3o",
        "run_at_startup":              "Arranque autom\u00e1tico",
        "skip_all":                    "Ignorar tudo",
        "install_selected":            "Instalar selecionados",
        "welcome_sub":                 "Os teus dotfiles est\u00e3o instalados.\nSeleciona pacotes opcionais nos separadores e clica em <b>Instalar</b>.\nDesativa <i>Arranque autom\u00e1tico</i> ap\u00f3s instalar.",
        "card_browser_sub":            "Escolhe o teu navegador padr\u00e3o",
        "card_gaming_sub":             "Steam, Heroic, Wine, MangoHud",
        "card_peripherals_sub":        "OpenRazer, Polychromatic, Piper",
        "card_filetransfer_sub":       "Android, c\u00e2meras, partilha LAN",
        "card_office_sub":             "LibreOffice + pacotes de idioma",
        "card_media_sub":              "GIMP, Kdenlive, OBS Liberty",
        "card_comms_sub":              "Vesktop, Telegram, Thunderbird",
        "browser_section":             "Seleciona o Teu Navegador Padr\u00e3o",
        "recommended":                 "\u2b50 Recomendado",
        "lo_lang_section":             "Pacotes de Idioma LibreOffice",
        "log_what_title":              "O Que Este Instalador Faz",
        "log_row_browser_t":           "Navegador",
        "log_row_browser_b":           "Escolhe um navegador \u2014 LibreWolf, Zen, Firefox, Vivaldi, Chrome ou Edge. A tua escolha \u00e9 instalada e $Browser em hyprland.conf \u00e9 atualizado automaticamente para que Super+B o abra.",
        "log_row_gaming_t":            "Jogos",
        "log_row_gaming_b":            "Steam (lib32), Heroic Games Launcher, Wine + Winetricks/Mono/Gecko, ProtonPlus, GameMode + 32-bit, MangoHud + 32-bit, MangoJuice. Selecionar Wine seleciona automaticamente os tr\u00eas subpacotes.",
        "log_row_periph_t":            "Perif\u00e9ricos",
        "log_row_periph_b":            "Daemon OpenRazer + driver kernel (DKMS) + biblioteca Python para hardware Razer. Polychromatic para RGB por tecla e efeitos. Piper para configura\u00e7\u00e3o de rato/teclado multi-marca (Logitech, SteelSeries, Roccat\u2026). Solaar para recetores Logitech Unifying/Bolt. jmtpfs e gphotofs para montar telef\u00f3nes Android e c\u00e2meras \u2014 todos AUR.",
        "log_row_office_t":            "Escrit\u00f3rio",
        "log_row_office_b":            "LibreOffice Fresh mais qualquer um dos 12 pacotes de idioma (Ingl\u00eas UK, Romeno, Franc\u00eas, Alem\u00e3o, Espanhol, Italiano, Portugu\u00eas, Russo, Japon\u00eas, Chin\u00eas, Coreano, \u00c1rabe).",
        "log_row_media_t":             "M\u00eddia",
        "log_row_media_b":             "Visualizador de imagens Mirage, GIMP, Inkscape, editor de v\u00eddeo Kdenlive, conversor HandBrake, OBS Studio Liberty (build livre).",
        "log_row_ft_t":                "Transfer\u00eancia",
        "log_row_ft_b":                "Android MTP com jmtpfs e go-mtpfs. C\u00e2mera PTP via gphotofs e gphoto2. Sem fios: Warpinator, LocalSend (AirDrop multiplataforma), Croc (P2P cifrado). USB: Android Tools (ADB/fastboot) e Scrcpy para espelhamento de ecr\u00e3.",
        "log_row_comms_t":             "Comunica\u00e7\u00e3o",
        "log_row_comms_b":             "Vesktop (Discord + Vencord), Telegram, Element (Matrix), Thunderbird + pacotes de idioma opcionais, notas Obsidian.",
        "log_row_how_t":               "Como Funciona",
        "log_row_how_b":               "Os pacotes do reposit\u00f3rio s\u00e3o instalados num \u00fanico batch pacman. Cada pacote AUR (paru) \u00e9 compilado e instalado individualmente \u2014 ver\u00e1s a sa\u00edda completa de compila\u00e7\u00e3o em tempo real. Ap\u00f3s a instala\u00e7\u00e3o o arranque autom\u00e1tico \u00e9 desativado automaticamente. Podes reativ\u00e1-lo a qualquer momento no rodap\u00e9.",
        "log_header":                  "Faded Dream \u2014 Instala\u00e7\u00e3o de pacotes selecionados",
        "log_repo_line":               "  pacotes repo  ({n}): {pkgs}",
        "log_aur_line":                "  pacotes AUR   ({n}): {pkgs}",
        "log_browser_patch":           "  patch navegador: $Browser = {exec}",
        "log_done":                    "\u2713  Conclu\u00eddo!",
        "log_done_bar":                "\u2713 Conclu\u00eddo!",
        "log_error":                   "[erro] {exc}",
        "prog_repo":                   "A instalar {n} pacotes repo...",
        "prog_pkg":                    "A instalar {pkg}...",
        "prog_patch":                  "A atualizar hyprland.conf \u2192 {exec}...",
            "log_banner_pacman": "\u2500\u2500 pacman  ({n} pacotes) \u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500",
        "log_banner_paru": "\u2500\u2500 paru  {pkg} \u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500",
        "log_banner_hypr": "\u2500\u2500 hyprland.conf \u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500",
        "log_browser_set": "  $Browser = {exec}",
        "badge_aur": "AUR",
        "badge_extra": "extra",
        "badge_galaxy": "galaxy",
        "badge_world": "world",
        "badge_lib32": "lib32",
        "badge_multilib": "multilib",
        "nothing_selected": "Nada selecionado \u2014 a fechar.",
        "lang_label": "Idioma",
        "welcome_title": "Faded Dream",
},
    "ru": {
        "app_title":                   "Faded Dream \u2014 \u041f\u0435\u0440\u0432\u044b\u0439 \u0437\u0430\u043f\u0443\u0441\u043a",
        "sidebar_title":               "Faded Dream",
        "nav_welcome":                 "\u0414\u043e\u0431\u0440\u043e \u043f\u043e\u0436\u0430\u043b\u043e\u0432\u0430\u0442\u044c",
        "nav_browser":                 "\u0411\u0440\u0430\u0443\u0437\u0435\u0440",
        "nav_gaming":                  "\u0418\u0433\u0440\u044b",
        "nav_peripherals":             "\u041f\u0435\u0440\u0438\u0444\u0435\u0440\u0438\u044f",
        "nav_file_transfer":           "\u041f\u0435\u0440\u0435\u0434\u0430\u0447\u0430 \u0444\u0430\u0439\u043b\u043e\u0432",
        "nav_office":                  "\u041e\u0444\u0438\u0441",
        "nav_media":                   "\u041c\u0435\u0434\u0438\u0430",
        "nav_comms":                   "\u041e\u0431\u0449\u0435\u043d\u0438\u0435",
        "nav_log":                     "\u0416\u0443\u0440\u043d\u0430\u043b",
        "packages_selected":           "\u0432\u044b\u0431\u0440\u0430\u043d\u043e {n} \u043f\u0430\u043a\u0435\u0442\u043e\u0432",
        "startup_hint":                "\u043e\u0442\u043a\u043b\u044e\u0447\u0438\u0442\u0435 \u0430\u0432\u0442\u043e\u0437\u0430\u043f\u0443\u0441\u043a \u043f\u043e\u0441\u043b\u0435 \u0443\u0441\u0442\u0430\u043d\u043e\u0432\u043a\u0438",
        "run_at_startup":              "\u0410\u0432\u0442\u043e\u0437\u0430\u043f\u0443\u0441\u043a",
        "skip_all":                    "\u041f\u0440\u043e\u043f\u0443\u0441\u0442\u0438\u0442\u044c \u0432\u0441\u0451",
        "install_selected":            "\u0423\u0441\u0442\u0430\u043d\u043e\u0432\u0438\u0442\u044c \u0432\u044b\u0431\u0440\u0430\u043d\u043d\u043e\u0435",
        "welcome_sub":                 "\u0412\u0430\u0448\u0438 dotfile\u0443 \u0443\u0441\u0442\u0430\u043d\u043e\u0432\u043b\u0435\u043d\u044b.\n\u0412\u044b\u0431\u0435\u0440\u0438\u0442\u0435 \u043e\u043f\u0446\u0438\u043e\u043d\u0430\u043b\u044c\u043d\u044b\u0435 \u043f\u0430\u043a\u0435\u0442\u044b \u043d\u0430 \u0432\u043a\u043b\u0430\u0434\u043a\u0430\u0445, \u0437\u0430\u0442\u0435\u043c \u043d\u0430\u0436\u043c\u0438\u0442\u0435 <b>\u0423\u0441\u0442\u0430\u043d\u043e\u0432\u0438\u0442\u044c</b>.\n\u041e\u0442\u043a\u043b\u044e\u0447\u0438\u0442\u0435 <i>\u0410\u0432\u0442\u043e\u0437\u0430\u043f\u0443\u0441\u043a</i> \u043f\u043e\u0441\u043b\u0435 \u0443\u0441\u0442\u0430\u043d\u043e\u0432\u043a\u0438.",
        "card_browser_sub":            "\u0412\u044b\u0431\u0435\u0440\u0438\u0442\u0435 \u0431\u0440\u0430\u0443\u0437\u0435\u0440 \u043f\u043e \u0443\u043c\u043e\u043b\u0447\u0430\u043d\u0438\u044e",
        "card_gaming_sub":             "Steam, Heroic, Wine, MangoHud",
        "card_peripherals_sub":        "OpenRazer, Polychromatic, Piper",
        "card_filetransfer_sub":       "Android, \u043a\u0430\u043c\u0435\u0440\u044b, \u043e\u0431\u043c\u0435\u043d LAN",
        "card_office_sub":             "LibreOffice + \u044f\u0437\u044b\u043a\u043e\u0432\u044b\u0435 \u043f\u0430\u043a\u0435\u0442\u044b",
        "card_media_sub":              "GIMP, Kdenlive, OBS Liberty",
        "card_comms_sub":              "Vesktop, Telegram, Thunderbird",
        "browser_section":             "\u0412\u044b\u0431\u0435\u0440\u0438\u0442\u0435 \u0431\u0440\u0430\u0443\u0437\u0435\u0440 \u043f\u043e \u0443\u043c\u043e\u043b\u0447\u0430\u043d\u0438\u044e",
        "recommended":                 "\u2b50 \u0420\u0435\u043a\u043e\u043c\u0435\u043d\u0434\u0443\u0435\u0442\u0441\u044f",
        "lo_lang_section":             "\u042f\u0437\u044b\u043a\u043e\u0432\u044b\u0435 \u043f\u0430\u043a\u0435\u0442\u044b LibreOffice",
        "log_what_title":              "\u0427\u0442\u043e \u0434\u0435\u043b\u0430\u0435\u0442 \u044d\u0442\u043e\u0442 \u0443\u0441\u0442\u0430\u043d\u043e\u0432\u0449\u0438\u043a",
        "log_row_browser_t":           "\u0411\u0440\u0430\u0443\u0437\u0435\u0440",
        "log_row_browser_b":           "\u0412\u044b\u0431\u0435\u0440\u0438\u0442\u0435 \u0431\u0440\u0430\u0443\u0437\u0435\u0440 \u2014 LibreWolf, Zen, Firefox, Vivaldi, Chrome \u0438\u043b\u0438 Edge. \u0412\u044b\u0431\u0440\u0430\u043d\u043d\u044b\u0439 \u0431\u0440\u0430\u0443\u0437\u0435\u0440 \u0443\u0441\u0442\u0430\u043d\u0430\u0432\u043b\u0438\u0432\u0430\u0435\u0442\u0441\u044f, \u0430 $Browser \u0432 hyprland.conf \u043e\u0431\u043d\u043e\u0432\u043b\u044f\u0435\u0442\u0441\u044f \u0430\u0432\u0442\u043e\u043c\u0430\u0442\u0438\u0447\u0435\u0441\u043a\u0438, \u0447\u0442\u043e\u0431\u044b Super+B \u0435\u0433\u043e \u043e\u0442\u043a\u0440\u044b\u0432\u0430\u043b.",
        "log_row_gaming_t":            "\u0418\u0433\u0440\u044b",
        "log_row_gaming_b":            "Steam (lib32), Heroic Games Launcher, Wine + Winetricks/Mono/Gecko, ProtonPlus, GameMode + 32-bit, MangoHud + 32-bit, MangoJuice. \u041f\u0440\u0438 \u0432\u044b\u0431\u043e\u0440\u0435 Wine \u0430\u0432\u0442\u043e\u043c\u0430\u0442\u0438\u0447\u0435\u0441\u043a\u0438 \u0432\u044b\u0431\u0438\u0440\u0430\u044e\u0442\u0441\u044f \u0442\u0440\u0438 \u0441\u0443\u0431\u043f\u0430\u043a\u0435\u0442\u0430.",
        "log_row_periph_t":            "\u041f\u0435\u0440\u0438\u0444\u0435\u0440\u0438\u044f",
        "log_row_periph_b":            "\u0414\u0435\u043c\u043e\u043d OpenRazer + \u0434\u0440\u0430\u0439\u0432\u0435\u0440 \u044f\u0434\u0440\u0430 (DKMS) + \u0431\u0438\u0431\u043b\u0438\u043e\u0442\u0435\u043a\u0430 Python \u0434\u043b\u044f Razer. Polychromatic \u0434\u043b\u044f RGB \u043f\u043e\u043a\u043b\u0430\u0432\u0438\u0448\u043d\u043e \u0438 \u044d\u0444\u0444\u0435\u043a\u0442\u043e\u0432. Piper \u0434\u043b\u044f \u043d\u0430\u0441\u0442\u0440\u043e\u0439\u043a\u0438 \u043c\u044b\u0448\u0435\u0439/\u043a\u043b\u0430\u0432\u0438\u0430\u0442\u0443\u0440 \u0440\u0430\u0437\u043d\u044b\u0445 \u0431\u0440\u0435\u043d\u0434\u043e\u0432. Solaar \u0434\u043b\u044f Logitech Unifying/Bolt. jmtpfs \u0438 gphotofs \u0434\u043b\u044f \u043f\u043e\u0434\u043a\u043b\u044e\u0447\u0435\u043d\u0438\u044f Android-\u0443\u0441\u0442\u0440\u043e\u0439\u0441\u0442\u0432 \u0438 \u043a\u0430\u043c\u0435\u0440 \u2014 \u0432\u0441\u0451 AUR.",
        "log_row_office_t":            "\u041e\u0444\u0438\u0441",
        "log_row_office_b":            "LibreOffice Fresh \u043f\u043b\u044e\u0441 \u043b\u044e\u0431\u043e\u0439 \u0438\u0437 12 \u044f\u0437\u044b\u043a\u043e\u0432\u044b\u0445 \u043f\u0430\u043a\u0435\u0442\u043e\u0432 (\u0410\u043d\u0433\u043b\u0438\u0439\u0441\u043a\u0438\u0439 UK, \u0420\u0443\u043c\u044b\u043d\u0441\u043a\u0438\u0439, \u0424\u0440\u0430\u043d\u0446\u0443\u0437\u0441\u043a\u0438\u0439, \u041d\u0435\u043c\u0435\u0446\u043a\u0438\u0439, \u0418\u0441\u043f\u0430\u043d\u0441\u043a\u0438\u0439, \u0418\u0442\u0430\u043b\u044c\u044f\u043d\u0441\u043a\u0438\u0439, \u041f\u043e\u0440\u0442\u0443\u0433\u0430\u043b\u044c\u0441\u043a\u0438\u0439, \u0420\u0443\u0441\u0441\u043a\u0438\u0439, \u042f\u043f\u043e\u043d\u0441\u043a\u0438\u0439, \u041a\u0438\u0442\u0430\u0439\u0441\u043a\u0438\u0439, \u041a\u043e\u0440\u0435\u0439\u0441\u043a\u0438\u0439, \u0410\u0440\u0430\u0431\u0441\u043a\u0438\u0439).",
        "log_row_media_t":             "\u041c\u0435\u0434\u0438\u0430",
        "log_row_media_b":             "\u041f\u0440\u043e\u0441\u043c\u043e\u0442\u0440\u0449\u0438\u043a Mirage, GIMP, Inkscape, \u0432\u0438\u0434\u0435\u043e\u0440\u0435\u0434\u0430\u043a\u0442\u043e\u0440 Kdenlive, \u043a\u043e\u043d\u0432\u0435\u0440\u0442\u0435\u0440 HandBrake, OBS Studio Liberty (\u0441\u0432\u043e\u0431\u043e\u0434\u043d\u0430\u044f \u0441\u0431\u043e\u0440\u043a\u0430).",
        "log_row_ft_t":                "\u041f\u0435\u0440\u0435\u0434\u0430\u0447\u0430 \u0444\u0430\u0439\u043b\u043e\u0432",
        "log_row_ft_b":                "Android MTP \u0447\u0435\u0440\u0435\u0437 jmtpfs \u0438 go-mtpfs. \u041a\u0430\u043c\u0435\u0440\u0430 PTP \u0447\u0435\u0440\u0435\u0437 gphotofs \u0438 gphoto2. \u0411\u0435\u0441\u043f\u0440\u043e\u0432\u043e\u0434\u043d\u043e: Warpinator, LocalSend (AirDrop \u043c\u0435\u0436\u043f\u043b\u0430\u0442\u0444\u043e\u0440\u043c\u0435\u043d\u043d\u044b\u0439), Croc (\u0437\u0430\u0448\u0438\u0444\u0440\u043e\u0432\u0430\u043d\u043d\u044b\u0439 P2P). USB: Android Tools (ADB/fastboot) \u0438 Scrcpy \u0434\u043b\u044f \u0437\u0435\u0440\u043a\u0430\u043b\u0438\u0440\u043e\u0432\u0430\u043d\u0438\u044f \u044d\u043a\u0440\u0430\u043d\u0430.",
        "log_row_comms_t":             "\u041e\u0431\u0449\u0435\u043d\u0438\u0435",
        "log_row_comms_b":             "Vesktop (Discord + Vencord), Telegram, Element (Matrix), Thunderbird + \u043e\u043f\u0446\u0438\u043e\u043d\u0430\u043b\u044c\u043d\u044b\u0435 \u044f\u0437\u044b\u043a\u043e\u0432\u044b\u0435 \u043f\u0430\u043a\u0435\u0442\u044b, \u0437\u0430\u043c\u0435\u0442\u043a\u0438 Obsidian.",
        "log_row_how_t":               "\u041a\u0430\u043a \u044d\u0442\u043e \u0440\u0430\u0431\u043e\u0442\u0430\u0435\u0442",
        "log_row_how_b":               "\u041f\u0430\u043a\u0435\u0442\u044b \u0440\u0435\u043f\u043e\u0437\u0438\u0442\u043e\u0440\u0438\u044f \u0443\u0441\u0442\u0430\u043d\u0430\u0432\u043b\u0438\u0432\u0430\u044e\u0442\u0441\u044f \u0432 \u043e\u0434\u0438\u043d\u043e\u043c batch pacman. \u041a\u0430\u0436\u0434\u044b\u0439 AUR-\u043f\u0430\u043a\u0435\u0442 (paru) \u0441\u043e\u0431\u0438\u0440\u0430\u0435\u0442\u0441\u044f \u0438 \u0443\u0441\u0442\u0430\u043d\u0430\u0432\u043b\u0438\u0432\u0430\u0435\u0442\u0441\u044f \u043e\u0442\u0434\u0435\u043b\u044c\u043d\u043e \u2014 \u0432\u0435\u0441\u044c \u0432\u044b\u0432\u043e\u0434 \u043a\u043e\u043c\u043f\u0438\u043b\u044f\u0446\u0438\u0438 \u043e\u0442\u043e\u0431\u0440\u0430\u0436\u0430\u0435\u0442\u0441\u044f \u0432 \u0440\u0435\u0430\u043b\u044c\u043d\u043e\u043c \u0432\u0440\u0435\u043c\u0435\u043d\u0438. \u041f\u043e\u0441\u043b\u0435 \u0443\u0441\u0442\u0430\u043d\u043e\u0432\u043a\u0438 \u0430\u0432\u0442\u043e\u0437\u0430\u043f\u0443\u0441\u043a \u043e\u0442\u043a\u043b\u044e\u0447\u0430\u0435\u0442\u0441\u044f \u0430\u0432\u0442\u043e\u043c\u0430\u0442\u0438\u0447\u0435\u0441\u043a\u0438. \u0412\u044b \u043c\u043e\u0436\u0435\u0442\u0435 \u0432\u043a\u043b\u044e\u0447\u0438\u0442\u044c \u0435\u0433\u043e \u0432 \u043b\u044e\u0431\u043e\u0435 \u0432\u0440\u0435\u043c\u044f.",
        "log_header":                  "Faded Dream \u2014 \u0423\u0441\u0442\u0430\u043d\u043e\u0432\u043a\u0430 \u0432\u044b\u0431\u0440\u0430\u043d\u043d\u044b\u0445 \u043f\u0430\u043a\u0435\u0442\u043e\u0432",
        "log_repo_line":               "  \u043f\u0430\u043a\u0435\u0442\u044b repo  ({n}): {pkgs}",
        "log_aur_line":                "  \u043f\u0430\u043a\u0435\u0442\u044b AUR   ({n}): {pkgs}",
        "log_browser_patch":           "  \u043f\u0430\u0442\u0447 \u0431\u0440\u0430\u0443\u0437\u0435\u0440\u0430: $Browser = {exec}",
        "log_done":                    "\u2713  \u0413\u043e\u0442\u043e\u0432\u043e!",
        "log_done_bar":                "\u2713 \u0413\u043e\u0442\u043e\u0432\u043e!",
        "log_error":                   "[\u043e\u0448\u0438\u0431\u043a\u0430] {exc}",
        "prog_repo":                   "\u0423\u0441\u0442\u0430\u043d\u043e\u0432\u043a\u0430 {n} \u043f\u0430\u043a\u0435\u0442\u043e\u0432 repo...",
        "prog_pkg":                    "\u0423\u0441\u0442\u0430\u043d\u043e\u0432\u043a\u0430 {pkg}...",
        "prog_patch":                  "\u041e\u0431\u043d\u043e\u0432\u043b\u0435\u043d\u0438\u0435 hyprland.conf \u2192 {exec}...",
            "log_banner_pacman": "\u2500\u2500 pacman  ({n} \u043f\u0430\u043a\u0435\u0442(\u043e\u0432)) \u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500",
        "log_banner_paru": "\u2500\u2500 paru  {pkg} \u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500",
        "log_banner_hypr": "\u2500\u2500 hyprland.conf \u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500",
        "log_browser_set": "  $Browser = {exec}",
        "badge_aur": "AUR",
        "badge_extra": "extra",
        "badge_galaxy": "galaxy",
        "badge_world": "world",
        "badge_lib32": "lib32",
        "badge_multilib": "multilib",
        "nothing_selected": "\u041d\u0438\u0447\u0435\u0433\u043e \u043d\u0435 \u0432\u044b\u0431\u0440\u0430\u043d\u043e \u2014 \u0437\u0430\u043a\u0440\u044b\u0432\u0430\u044e.",
        "lang_label": "\u042f\u0437\u044b\u043a",
        "welcome_title": "Faded Dream",
},
    "ja": {
        "app_title":                   "Faded Dream \u30bb\u30c3\u30c8\u30a2\u30c3\u30d7 \u2014 \u521d\u56de\u8d77\u52d5",
        "sidebar_title":               "Faded Dream",
        "nav_welcome":                 "\u30a6\u30a7\u30eb\u30ab\u30e0",
        "nav_browser":                 "\u30d6\u30e9\u30a6\u30b6",
        "nav_gaming":                  "\u30b2\u30fc\u30df\u30f3\u30b0",
        "nav_peripherals":             "\u5468\u8fba\u6a5f\u5668",
        "nav_file_transfer":           "\u30d5\u30a1\u30a4\u30eb\u8ee2\u9001",
        "nav_office":                  "\u30aa\u30d5\u30a3\u30b9",
        "nav_media":                   "\u30e1\u30c7\u30a3\u30a2",
        "nav_comms":                   "\u901a\u4fe1",
        "nav_log":                     "\u30ed\u30b0",
        "packages_selected":           "{n} \u500b\u306e\u30d1\u30c3\u30b1\u30fc\u30b8\u3092\u9078\u629e",
        "startup_hint":                "\u30a4\u30f3\u30b9\u30c8\u30fc\u30eb\u5f8c\u306b\u81ea\u52d5\u8d77\u52d5\u3092\u7121\u52b9\u306b\u3057\u3066\u304f\u3060\u3055\u3044",
        "run_at_startup":              "\u81ea\u52d5\u8d77\u52d5",
        "skip_all":                    "\u3059\u3079\u3066\u30b9\u30ad\u30c3\u30d7",
        "install_selected":            "\u9078\u629e\u3057\u305f\u3082\u306e\u3092\u30a4\u30f3\u30b9\u30c8\u30fc\u30eb",
        "welcome_sub":                 "dotfiles\u304c\u30a4\u30f3\u30b9\u30c8\u30fc\u30eb\u3055\u308c\u307e\u3057\u305f\u3002\n\u30bf\u30d6\u304b\u3089\u30aa\u30d7\u30b7\u30e7\u30ca\u30eb\u30d1\u30c3\u30b1\u30fc\u30b8\u3092\u9078\u629e\u3057\u3001<b>\u30a4\u30f3\u30b9\u30c8\u30fc\u30eb</b>\u3092\u30af\u30ea\u30c3\u30af\u3057\u3066\u304f\u3060\u3055\u3044\u3002\n\u30a4\u30f3\u30b9\u30c8\u30fc\u30eb\u5f8c\u306f<i>\u81ea\u52d5\u8d77\u52d5</i>\u3092\u30aa\u30d5\u306b\u3057\u3066\u304f\u3060\u3055\u3044\u3002",
        "card_browser_sub":            "\u30c7\u30d5\u30a9\u30eb\u30c8\u30d6\u30e9\u30a6\u30b6\u3092\u9078\u629e",
        "card_gaming_sub":             "Steam, Heroic, Wine, MangoHud",
        "card_peripherals_sub":        "OpenRazer, Polychromatic, Piper",
        "card_filetransfer_sub":       "Android\u3001\u30ab\u30e1\u30e9\u3001LAN\u5171\u6709",
        "card_office_sub":             "LibreOffice + \u8a00\u8a9e\u30d1\u30c3\u30af",
        "card_media_sub":              "GIMP, Kdenlive, OBS Liberty",
        "card_comms_sub":              "Vesktop, Telegram, Thunderbird",
        "browser_section":             "\u30c7\u30d5\u30a9\u30eb\u30c8\u30d6\u30e9\u30a6\u30b6\u306e\u9078\u629e",
        "recommended":                 "\u2b50 \u304a\u3059\u3059\u3081",
        "lo_lang_section":             "LibreOffice \u8a00\u8a9e\u30d1\u30c3\u30af",
        "log_what_title":              "\u30a4\u30f3\u30b9\u30c8\u30fc\u30e9\u30fc\u306e\u6a5f\u80fd",
        "log_row_browser_t":           "\u30d6\u30e9\u30a6\u30b6",
        "log_row_browser_b":           "\u30d6\u30e9\u30a6\u30b6\u3092\u9078\u629e\u3057\u3066\u304f\u3060\u3055\u3044 \u2014 LibreWolf\u3001Zen\u3001Firefox\u3001Vivaldi\u3001Chrome\u3001Edge\u3002\u9078\u629e\u3057\u305f\u30d6\u30e9\u30a6\u30b6\u304c\u30a4\u30f3\u30b9\u30c8\u30fc\u30eb\u3055\u308c\u3001hyprland.conf\u306e$Browser\u304c\u81ea\u52d5\u66f4\u65b0\u3055\u308c\u3066Super+B\u3067\u958b\u304f\u3088\u3046\u306b\u306a\u308a\u307e\u3059\u3002",
        "log_row_gaming_t":            "\u30b2\u30fc\u30df\u30f3\u30b0",
        "log_row_gaming_b":            "Steam (lib32)\u3001Heroic Games Launcher\u3001Wine + Winetricks/Mono/Gecko\u3001ProtonPlus\u3001GameMode + 32bit\u3001MangoHud + 32bit\u3001MangoJuice\u3002Wine\u3092\u9078\u629e\u3059\u308b\u3068\u30b5\u30d6\u30d1\u30c3\u30b1\u30fc\u30b8\u306e3\u3064\u304c\u81ea\u52d5\u9078\u629e\u3055\u308c\u307e\u3059\u3002",
        "log_row_periph_t":            "\u5468\u8fba\u6a5f\u5668",
        "log_row_periph_b":            "OpenRazer\u30c7\u30fc\u30e2\u30f3 + \u30ab\u30fc\u30cd\u30eb\u30c9\u30e9\u30a4\u30d0\u30fc (DKMS) + Razer\u30cf\u30fc\u30c9\u30a6\u30a7\u30a2\u7528Python\u30e9\u30a4\u30d6\u30e9\u30ea\u3002Polychromatic\u3067\u30ad\u30fc\u3054\u3068\u306eRGB\u3068\u30a8\u30d5\u30a7\u30af\u30c8\u8a2d\u5b9a\u3002Piper\u3067\u30de\u30eb\u30c1\u30d6\u30e9\u30f3\u30c9\u306e\u30de\u30a6\u30b9\uff0f\u30ad\u30fc\u30dc\u30fc\u30c9\u3092\u8a2d\u5b9a\u3002Solaar\u3067Logitech Unifying/Bolt\u30ec\u30b7\u30fc\u30d0\u30fc\u3002jmtpfs\u3068gphotofs\u3067Android\u3084\u30ab\u30e1\u30e9\u3092\u30de\u30a6\u30f3\u30c8 \u2014 \u3059\u3079\u3066AUR\u3002",
        "log_row_office_t":            "\u30aa\u30d5\u30a3\u30b9",
        "log_row_office_b":            "LibreOffice Fresh\u306b\u52a0\u3048\u300112\u7a2e\u306e\u8a00\u8a9e\u30d1\u30c3\u30af\u304b\u3089\u9078\u629e\u3067\u304d\u307e\u3059\uff08\u82f1\u8a9eUK\u3001\u30eb\u30fc\u30de\u30cb\u30a2\u8a9e\u3001\u30d5\u30e9\u30f3\u30b9\u8a9e\u3001\u30c9\u30a4\u30c4\u8a9e\u3001\u30b9\u30da\u30a4\u30f3\u8a9e\u3001\u30a4\u30bf\u30ea\u30a2\u8a9e\u3001\u30dd\u30eb\u30c8\u30ac\u30eb\u8a9e\u3001\u30ed\u30b7\u30a2\u8a9e\u3001\u65e5\u672c\u8a9e\u3001\u4e2d\u56fd\u8a9e\u3001\u97d3\u56fd\u8a9e\u3001\u30a2\u30e9\u30d3\u30a2\u8a9e\uff09\u3002",
        "log_row_media_t":             "\u30e1\u30c7\u30a3\u30a2",
        "log_row_media_b":             "\u753b\u50cf\u30d3\u30e5\u30fc\u30a2\u30fcMirage\u3001GIMP\u3001Inkscape\u3001\u52d5\u753b\u7de8\u96c6Kdenlive\u3001\u5909\u63db\u30bd\u30d5\u30c8HandBrake\u3001OBS Studio Liberty\uff08\u30d5\u30ea\u30fc\u30d3\u30eb\u30c9\uff09\u3002",
        "log_row_ft_t":                "\u30d5\u30a1\u30a4\u30eb\u8ee2\u9001",
        "log_row_ft_b":                "jmtpfs\u3068go-mtpfs\u3067Android MTP\u3002gphotofs\u3068gphoto2\u3067\u30ab\u30e1\u30e9PTP\u3002\u7121\u7dda: Warpinator\u3001LocalSend\uff08\u30af\u30ed\u30b9\u30d7\u30e9\u30c3\u30c8\u30d5\u30a9\u30fc\u30e0AirDrop\uff09\u3001Croc\uff08\u6697\u53f7\u5316P2P\uff09\u3002USB: Android Tools\uff08ADB/fastboot\uff09\u3068\u30b9\u30af\u30ea\u30fc\u30f3\u30df\u30e9\u30fc\u30ea\u30f3\u30b0Scrcpy\u3002",
        "log_row_comms_t":             "\u901a\u4fe1",
        "log_row_comms_b":             "Vesktop\uff08Discord + Vencord\uff09\u3001Telegram\u3001Element\uff08Matrix\uff09\u3001Thunderbird + \u30aa\u30d7\u30b7\u30e7\u30ca\u30eb\u8a00\u8a9e\u30d1\u30c3\u30af\u3001Obsidian\u30e1\u30e2\u3002",
        "log_row_how_t":               "\u52d5\u4f5c\u306e\u4ed5\u7d44\u307f",
        "log_row_how_b":               "\u30ea\u30dd\u30b8\u30c8\u30ea\u30d1\u30c3\u30b1\u30fc\u30b8\u306f\u4e00\u62ecpacman\u3067\u30a4\u30f3\u30b9\u30c8\u30fc\u30eb\u3055\u308c\u307e\u3059\u3002AUR\u30d1\u30c3\u30b1\u30fc\u30b8\uff08paru\uff09\u306f\u500b\u5225\u306b\u30d3\u30eb\u30c9\u30fb\u30a4\u30f3\u30b9\u30c8\u30fc\u30eb \u2014 \u30b3\u30f3\u30d1\u30a4\u30eb\u51fa\u529b\u3092\u30ea\u30a2\u30eb\u30bf\u30a4\u30e0\u3067\u78ba\u8a8d\u3067\u304d\u307e\u3059\u3002\u5b8c\u4e86\u5f8c\u306f\u81ea\u52d5\u8d77\u52d5\u304c\u81ea\u52d5\u7121\u52b9\u5316\u3055\u308c\u307e\u3059\u3002\u30d5\u30c3\u30bf\u30fc\u304b\u3089\u518d\u6709\u52b9\u5316\u3067\u304d\u307e\u3059\u3002",
        "log_header":                  "Faded Dream \u2014 \u9078\u629e\u3057\u305f\u30d1\u30c3\u30b1\u30fc\u30b8\u3092\u30a4\u30f3\u30b9\u30c8\u30fc\u30eb\u4e2d",
        "log_repo_line":               "  repo\u30d1\u30c3\u30b1\u30fc\u30b8  ({n}): {pkgs}",
        "log_aur_line":                "  AUR\u30d1\u30c3\u30b1\u30fc\u30b8   ({n}): {pkgs}",
        "log_browser_patch":           "  \u30d6\u30e9\u30a6\u30b6\u30d1\u30c3\u30c1: $Browser = {exec}",
        "log_done":                    "\u2713  \u5b8c\u4e86\uff01",
        "log_done_bar":                "\u2713 \u5b8c\u4e86\uff01",
        "log_error":                   "[\u30a8\u30e9\u30fc] {exc}",
        "prog_repo":                   "repo\u30d1\u30c3\u30b1\u30fc\u30b8 {n}\u500b\u3092\u30a4\u30f3\u30b9\u30c8\u30fc\u30eb\u4e2d...",
        "prog_pkg":                    "{pkg}\u3092\u30a4\u30f3\u30b9\u30c8\u30fc\u30eb\u4e2d...",
        "prog_patch":                  "hyprland.conf\u3092\u66f4\u65b0\u4e2d \u2192 {exec}...",
            "log_banner_pacman": "\u2500\u2500 pacman  ({n} \u30d1\u30c3\u30b1\u30fc\u30b8) \u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500",
        "log_banner_paru": "\u2500\u2500 paru  {pkg} \u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500",
        "log_banner_hypr": "\u2500\u2500 hyprland.conf \u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500",
        "log_browser_set": "  $Browser = {exec}",
        "badge_aur": "AUR",
        "badge_extra": "extra",
        "badge_galaxy": "galaxy",
        "badge_world": "world",
        "badge_lib32": "lib32",
        "badge_multilib": "multilib",
        "nothing_selected": "\u9078\u629e\u306a\u3057 \u2014 \u9589\u3058\u307e\u3059\u3002",
        "lang_label": "\u8a00\u8a9e",
        "welcome_title": "Faded Dream",
},
    "zh": {
        "app_title":                   "Faded Dream \u8bbe\u7f6e \u2014 \u9996\u6b21\u8fd0\u884c",
        "sidebar_title":               "Faded Dream",
        "nav_welcome":                 "\u6b22\u8fce",
        "nav_browser":                 "\u6d4f\u89c8\u5668",
        "nav_gaming":                  "\u6e38\u620f",
        "nav_peripherals":             "\u5916\u8bbe",
        "nav_file_transfer":           "\u6587\u4ef6\u4f20\u8f93",
        "nav_office":                  "\u529e\u516c",
        "nav_media":                   "\u5a92\u4f53",
        "nav_comms":                   "\u901a\u8baf",
        "nav_log":                     "\u65e5\u5fd7",
        "packages_selected":           "\u5df2\u9009\u62e9 {n} \u4e2a\u8f6f\u4ef6\u5305",
        "startup_hint":                "\u5b89\u88c5\u540e\u8bf7\u5173\u95ed\u81ea\u52a8\u542f\u52a8",
        "run_at_startup":              "\u5f00\u673a\u81ea\u542f",
        "skip_all":                    "\u8df3\u8fc7\u5168\u90e8",
        "install_selected":            "\u5b89\u88c5\u6240\u9009",
        "welcome_sub":                 "\u60a8\u7684 dotfiles \u5df2\u5b89\u88c5\u5b8c\u6210\u3002\n\u5728\u6807\u7b7e\u9875\u4e2d\u9009\u62e9\u53ef\u9009\u8f6f\u4ef6\u5305\uff0c\u7136\u540e\u70b9\u51fb<b>\u5b89\u88c5</b>\u3002\n\u5b89\u88c5\u5b8c\u6210\u540e\u8bf7\u5173\u95ed<i>\u5f00\u673a\u81ea\u542f</i>\u3002",
        "card_browser_sub":            "\u9009\u62e9\u9ed8\u8ba4\u6d4f\u89c8\u5668",
        "card_gaming_sub":             "Steam, Heroic, Wine, MangoHud",
        "card_peripherals_sub":        "OpenRazer, Polychromatic, Piper",
        "card_filetransfer_sub":       "Android\u3001\u76f8\u673a\u3001\u5c40\u57df\u7f51\u5171\u4eab",
        "card_office_sub":             "LibreOffice + \u8bed\u8a00\u5305",
        "card_media_sub":              "GIMP, Kdenlive, OBS Liberty",
        "card_comms_sub":              "Vesktop, Telegram, Thunderbird",
        "browser_section":             "\u9009\u62e9\u9ed8\u8ba4\u6d4f\u89c8\u5668",
        "recommended":                 "\u2b50 \u63a8\u8350",
        "lo_lang_section":             "LibreOffice \u8bed\u8a00\u5305",
        "log_what_title":              "\u6b64\u5b89\u88c5\u7a0b\u5e8f\u7684\u529f\u80fd",
        "log_row_browser_t":           "\u6d4f\u89c8\u5668",
        "log_row_browser_b":           "\u9009\u62e9\u4e00\u4e2a\u6d4f\u89c8\u5668 \u2014 LibreWolf\u3001Zen\u3001Firefox\u3001Vivaldi\u3001Chrome \u6216 Edge\u3002\u60a8\u7684\u9009\u62e9\u5c06\u88ab\u5b89\u88c5\uff0c\u5e76\u81ea\u52a8\u66f4\u65b0 hyprland.conf \u4e2d\u7684 $Browser\uff0c\u4f7f Super+B \u53ef\u4ee5\u6253\u5f00\u5b83\u3002",
        "log_row_gaming_t":            "\u6e38\u620f",
        "log_row_gaming_b":            "Steam (lib32)\u3001Heroic Games Launcher\u3001Wine + Winetricks/Mono/Gecko\u3001ProtonPlus\u3001GameMode + 32\u4f4d\u3001MangoHud + 32\u4f4d\u3001MangoJuice\u3002\u9009\u62e9 Wine \u4f1a\u81ea\u52a8\u9009\u4e2d\u4e09\u4e2a\u5b50\u5305\u3002",
        "log_row_periph_t":            "\u5916\u8bbe",
        "log_row_periph_b":            "OpenRazer \u5b88\u62a4\u8fdb\u7a0b + \u5185\u6838\u9a71\u52a8 (DKMS) + Razer \u786c\u4ef6 Python \u5e93\u3002Polychromatic \u7528\u4e8e\u6bcf\u952e RGB \u548c\u6548\u679c\u3002Piper \u7528\u4e8e\u591a\u54c1\u724c\u9f20\u6807/\u952e\u76d8\u914d\u7f6e\u3002Solaar \u7528\u4e8e Logitech Unifying/Bolt\u3002jmtpfs \u548c gphotofs \u7528\u4e8e\u6302\u8f7d Android \u624b\u673a\u548c\u76f8\u673a \u2014 \u5747\u4e3a AUR\u3002",
        "log_row_office_t":            "\u529e\u516c",
        "log_row_office_b":            "LibreOffice Fresh \u52a0\u4e0a 12 \u4e2a\u8bed\u8a00\u5305\u4e2d\u7684\u4efb\u610f\u9009\u62e9\uff08\u82f1\u8bed UK\u3001\u7f57\u9a6c\u5c3c\u4e9a\u8bed\u3001\u6cd5\u8bed\u3001\u5fb7\u8bed\u3001\u897f\u73ed\u7259\u8bed\u3001\u610f\u5927\u5229\u8bed\u3001\u8461\u8404\u7259\u8bed\u3001\u4fc4\u8bed\u3001\u65e5\u8bed\u3001\u4e2d\u6587\u3001\u97e9\u8bed\u3001\u963f\u62c9\u4f2f\u8bed\uff09\u3002",
        "log_row_media_t":             "\u5a92\u4f53",
        "log_row_media_b":             "Mirage \u56fe\u7247\u67e5\u770b\u5668\u3001GIMP\u3001Inkscape\u3001Kdenlive \u89c6\u9891\u7f16\u8f91\u5668\u3001HandBrake \u8f6c\u6362\u5668\u3001OBS Studio Liberty\uff08\u81ea\u7531\u7248\u672c\uff09\u3002",
        "log_row_ft_t":                "\u6587\u4ef6\u4f20\u8f93",
        "log_row_ft_b":                "\u901a\u8fc7 jmtpfs \u548c go-mtpfs \u5b9e\u73b0 Android MTP\u3002\u901a\u8fc7 gphotofs \u548c gphoto2 \u5b9e\u73b0\u76f8\u673a PTP\u3002\u65e0\u7ebf: Warpinator\u3001LocalSend\uff08\u8de8\u5e73\u53f0 AirDrop\uff09\u3001Croc\uff08\u52a0\u5bc6 P2P\uff09\u3002USB: Android Tools\uff08ADB/fastboot\uff09\u548c Scrcpy \u5c4f\u5e55\u955c\u50cf\u3002",
        "log_row_comms_t":             "\u901a\u8baf",
        "log_row_comms_b":             "Vesktop\uff08Discord + Vencord\uff09\u3001Telegram\u3001Element\uff08Matrix\uff09\u3001Thunderbird + \u53ef\u9009\u8bed\u8a00\u5305\u3001Obsidian \u7b14\u8bb0\u3002",
        "log_row_how_t":               "\u5de5\u4f5c\u539f\u7406",
        "log_row_how_b":               "\u4ed3\u5e93\u8f6f\u4ef6\u5305\u901a\u8fc7\u4e00\u4e2a pacman \u6279\u5904\u7406\u5b89\u88c5\u3002\u6bcf\u4e2a AUR \u8f6f\u4ef6\u5305\uff08paru\uff09\u5355\u72ec\u7f16\u8bd1\u5b89\u88c5 \u2014 \u53ef\u5b9e\u65f6\u67e5\u770b\u5b8c\u6574\u7f16\u8bd1\u8f93\u51fa\u3002\u5b89\u88c5\u5b8c\u6210\u540e\u5f00\u673a\u81ea\u542f\u5c06\u81ea\u52a8\u7981\u7528\u3002\u60a8\u53ef\u4ee5\u968f\u65f6\u5728\u5e95\u90e8\u91cd\u65b0\u5f00\u542f\u3002",
        "log_header":                  "Faded Dream \u2014 \u5b89\u88c5\u6240\u9009\u8f6f\u4ef6\u5305",
        "log_repo_line":               "  repo \u5305  ({n}): {pkgs}",
        "log_aur_line":                "  AUR \u5305   ({n}): {pkgs}",
        "log_browser_patch":           "  \u6d4f\u89c8\u5668\u8865\u4e01: $Browser = {exec}",
        "log_done":                    "\u2713  \u5b8c\u6210\uff01",
        "log_done_bar":                "\u2713 \u5b8c\u6210\uff01",
        "log_error":                   "[\u9519\u8bef] {exc}",
        "prog_repo":                   "\u6b63\u5728\u5b89\u88c5 {n} \u4e2a repo \u5305...",
        "prog_pkg":                    "\u6b63\u5728\u5b89\u88c5 {pkg}...",
        "prog_patch":                  "\u6b63\u5728\u66f4\u65b0 hyprland.conf \u2192 {exec}...",
            "log_banner_pacman": "\u2500\u2500 pacman  ({n} \u4e2a\u8f6f\u4ef6\u5305) \u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500",
        "log_banner_paru": "\u2500\u2500 paru  {pkg} \u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500",
        "log_banner_hypr": "\u2500\u2500 hyprland.conf \u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500",
        "log_browser_set": "  $Browser = {exec}",
        "badge_aur": "AUR",
        "badge_extra": "extra",
        "badge_galaxy": "galaxy",
        "badge_world": "world",
        "badge_lib32": "lib32",
        "badge_multilib": "multilib",
        "nothing_selected": "\u672a\u9009\u62e9\u4efb\u4f55\u5185\u5bb9 \u2014 \u6b63\u5728\u5173\u95ed\u3002",
        "lang_label": "\u8bed\u8a00",
        "welcome_title": "Faded Dream",
},
    "ko": {
        "app_title":                   "Faded Dream \uc124\uc815 \u2014 \uccab \uc2e4\ud589",
        "sidebar_title":               "Faded Dream",
        "nav_welcome":                 "\ud658\uc601\ud569\ub2c8\ub2e4",
        "nav_browser":                 "\ube0c\ub77c\uc6b0\uc800",
        "nav_gaming":                  "\uac8c\uc784",
        "nav_peripherals":             "\uc8fc\ubcc0\uae30\uae30",
        "nav_file_transfer":           "\ud30c\uc77c \uc804\uc1a1",
        "nav_office":                  "\uc624\ud53c\uc2a4",
        "nav_media":                   "\ubbf8\ub514\uc5b4",
        "nav_comms":                   "\ud1b5\uc2e0",
        "nav_log":                     "\ub85c\uadf8",
        "packages_selected":           "\ud328\ud0a4\uc9c0 {n}\uac1c \uc120\ud0dd\ub428",
        "startup_hint":                "\uc124\uce58 \ud6c4 \uc790\ub3d9 \uc2dc\uc791\uc744 \ube44\ud65c\uc131\ud654\ud558\uc138\uc694",
        "run_at_startup":              "\uc790\ub3d9 \uc2dc\uc791",
        "skip_all":                    "\ubaa8\ub450 \uac74\ub108\ub6f0\uae30",
        "install_selected":            "\uc120\ud0dd \ud56d\ubaa9 \uc124\uce58",
        "welcome_sub":                 "dotfiles\uac00 \uc124\uce58\ub418\uc5c8\uc2b5\ub2c8\ub2e4.\n\ud0ed\uc5d0\uc11c \uc120\ud0dd\uc801 \ud328\ud0a4\uc9c0\ub97c \uace0\ub974\uace0 <b>\uc124\uce58</b>\ub97c \ud074\ub9ad\ud558\uc138\uc694.\n\uc124\uce58 \ud6c4 <i>\uc790\ub3d9 \uc2dc\uc791</i>\uc744 \ubcf4\ub85c \ub044\uc138\uc694.",
        "card_browser_sub":            "\uae30\ubcf8 \ube0c\ub77c\uc6b0\uc800 \uc120\ud0dd",
        "card_gaming_sub":             "Steam, Heroic, Wine, MangoHud",
        "card_peripherals_sub":        "OpenRazer, Polychromatic, Piper",
        "card_filetransfer_sub":       "Android, \uce74\uba54\ub77c, LAN \uacf5\uc720",
        "card_office_sub":             "LibreOffice + \uc5b8\uc5b4 \ud329",
        "card_media_sub":              "GIMP, Kdenlive, OBS Liberty",
        "card_comms_sub":              "Vesktop, Telegram, Thunderbird",
        "browser_section":             "\uae30\ubcf8 \ube0c\ub77c\uc6b0\uc800 \uc120\ud0dd",
        "recommended":                 "\u2b50 \ucd94\ucc9c",
        "lo_lang_section":             "LibreOffice \uc5b8\uc5b4 \ud329",
        "log_what_title":              "\uc774 \uc124\uce58\uad00\ub9ac\uc790\uac00 \ud558\ub294 \uc77c",
        "log_row_browser_t":           "\ube0c\ub77c\uc6b0\uc800",
        "log_row_browser_b":           "\ube0c\ub77c\uc6b0\uc800\ub97c \uc120\ud0dd\ud558\uc138\uc694 \u2014 LibreWolf, Zen, Firefox, Vivaldi, Chrome \ub610\ub294 Edge. \uc120\ud0dd\ud55c \ube0c\ub77c\uc6b0\uc800\uac00 \uc124\uce58\ub418\uace0 hyprland.conf\uc758 $Browser\uac00 \uc790\ub3d9 \uc5c5\ub370\uc774\ud2b8\ub418\uc5b4 Super+B\ub85c \uc5f4 \uc218 \uc788\uc2b5\ub2c8\ub2e4.",
        "log_row_gaming_t":            "\uac8c\uc784",
        "log_row_gaming_b":            "Steam (lib32), Heroic Games Launcher, Wine + Winetricks/Mono/Gecko, ProtonPlus, GameMode + 32bit, MangoHud + 32bit, MangoJuice. Wine\uc744 \uc120\ud0dd\ud558\uba74 \uc138 \uac1c\uc758 \uc11c\ube0c\ud328\ud0a4\uc9c0\uac00 \uc790\ub3d9 \uc120\ud0dd\ub429\ub2c8\ub2e4.",
        "log_row_periph_t":            "\uc8fc\ubcc0\uae30\uae30",
        "log_row_periph_b":            "OpenRazer \ub370\ubaa8\ub144 + \ucee4\ub110 \ub4dc\ub77c\uc774\ubc84 (DKMS) + Razer \ud558\ub4dc\uc6e8\uc5b4\uc6a9 Python \ub77c\uc774\ube0c\ub7ec\ub9ac. Polychromatic\uc73c\ub85c \ud0a4\ubcc4 RGB \ubc0f \ud6a8\uacfc \uc124\uc815. Piper\ub85c \ub2e4\uc911 \ube0c\ub79c\ub4dc \ub9c8\uc6b0\uc2a4/\ud0a4\ubcf4\ub4dc \uc124\uc815. Solaar\ub85c Logitech Unifying/Bolt. jmtpfs\uc640 gphotofs\ub85c Android \ubc0f \uce74\uba54\ub77c \ub9c8\uc6b4\ud2b8 \u2014 \ubaa8\ub450 AUR.",
        "log_row_office_t":            "\uc624\ud53c\uc2a4",
        "log_row_office_b":            "LibreOffice Fresh\uc640 12\uac1c \uc5b8\uc5b4 \ud329 \uc911 \uc6d0\ud558\ub294 \uac83 (\uc601\uc5b4 UK, \ub8e8\ub9c8\ub2c8\uc544\uc5b4, \ud504\ub791\uc2a4\uc5b4, \ub3c5\uc77c\uc5b4, \uc2a4\ud398\uc778\uc5b4, \uc774\ud0c8\ub9ac\uc544\uc5b4, \ud3ec\ub974\ud22c\uac08\uc5b4, \ub7ec\uc2dc\uc544\uc5b4, \uc77c\ubcf8\uc5b4, \uc911\uad6d\uc5b4, \ud55c\uad6d\uc5b4, \uc544\ub78d\uc5b4).",
        "log_row_media_t":             "\ubbf8\ub514\uc5b4",
        "log_row_media_b":             "Mirage \uc774\ubbf8\uc9c0 \ubdf0\uc5b4, GIMP, Inkscape, Kdenlive \ube44\ub514\uc624 \ud3b8\uc9d1\uae30, HandBrake \ubcc0\ud658\uae30, OBS Studio Liberty (\uc790\uc720 \ube4c\ub4dc).",
        "log_row_ft_t":                "\ud30c\uc77c \uc804\uc1a1",
        "log_row_ft_b":                "jmtpfs\uc640 go-mtpfs\ub85c Android MTP. gphotofs\uc640 gphoto2\ub85c \uce74\uba54\ub77c PTP. \ubb34\uc120: Warpinator, LocalSend (\ud06c\ub85c\uc2a4 \ud50c\ub7ab\ud3fc AirDrop), Croc (\uc554\ud638\ud654 P2P). USB: Android Tools (ADB/fastboot)\uc640 Scrcpy \ud654\uba74 \ubbf8\ub7ec\ub9c1.",
        "log_row_comms_t":             "\ud1b5\uc2e0",
        "log_row_comms_b":             "Vesktop (Discord + Vencord), Telegram, Element (Matrix), Thunderbird + \uc120\ud0dd\uc801 \uc5b8\uc5b4 \ud329, Obsidian \ub178\ud2b8.",
        "log_row_how_t":               "\uc791\ub3d9 \ubc29\uc2dd",
        "log_row_how_b":               "\ub808\ud3ec\uc9c0\ud1a0\ub9ac \ud328\ud0a4\uc9c0\ub294 \ud558\ub098\uc758 pacman \ubc30\uce58\ub85c \uc124\uce58\ub429\ub2c8\ub2e4. \uac01 AUR \ud328\ud0a4\uc9c0(paru)\ub294 \uac1c\ubcc4\uc801\uc73c\ub85c \ube4c\ub4dc \ubc0f \uc124\uce58 \u2014 \uc2e4\uc2dc\uac04\uc73c\ub85c \uc804\uccb4 \ucef4\ud30c\uc77c \ucd9c\ub825\uc744 \ubcfc \uc218 \uc788\uc2b5\ub2c8\ub2e4. \uc124\uce58 \ud6c4 \uc790\ub3d9 \uc2dc\uc791\uc774 \uc790\ub3d9\uc73c\ub85c \ube44\ud65c\uc131\ud654\ub429\ub2c8\ub2e4. \ud478\ud130\uc5d0\uc11c \uc5b8\uc81c\ub4e0\uc9c0 \uc7ac\ud65c\uc131\ud654\ud560 \uc218 \uc788\uc2b5\ub2c8\ub2e4.",
        "log_header":                  "Faded Dream \u2014 \uc120\ud0dd\ud55c \ud328\ud0a4\uc9c0 \uc124\uce58 \uc911",
        "log_repo_line":               "  repo \ud328\ud0a4\uc9c0  ({n}): {pkgs}",
        "log_aur_line":                "  AUR \ud328\ud0a4\uc9c0   ({n}): {pkgs}",
        "log_browser_patch":           "  \ube0c\ub77c\uc6b0\uc800 \ud328\uce58: $Browser = {exec}",
        "log_done":                    "\u2713  \uc644\ub8cc!",
        "log_done_bar":                "\u2713 \uc644\ub8cc!",
        "log_error":                   "[\uc624\ub958] {exc}",
        "prog_repo":                   "repo \ud328\ud0a4\uc9c0 {n}\uac1c \uc124\uce58 \uc911...",
        "prog_pkg":                    "{pkg} \uc124\uce58 \uc911...",
        "prog_patch":                  "hyprland.conf \uc5c5\ub370\uc774\ud2b8 \uc911 \u2192 {exec}...",
            "log_banner_pacman": "\u2500\u2500 pacman  ({n} \ud328\ud0a4\uc9c0) \u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500",
        "log_banner_paru": "\u2500\u2500 paru  {pkg} \u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500",
        "log_banner_hypr": "\u2500\u2500 hyprland.conf \u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500",
        "log_browser_set": "  $Browser = {exec}",
        "badge_aur": "AUR",
        "badge_extra": "extra",
        "badge_galaxy": "galaxy",
        "badge_world": "world",
        "badge_lib32": "lib32",
        "badge_multilib": "multilib",
        "nothing_selected": "\uc120\ud0dd \uc5c6\uc74c \u2014 \uc885\ub8cc \uc911\u3002",
        "lang_label": "\uc5b8\uc5b4",
        "welcome_title": "Faded Dream",
},
    "ar": {
        "app_title":                   "Faded Dream \u2014 \u0627\u0644\u0625\u0639\u062f\u0627\u062f \u0627\u0644\u0623\u0648\u0644",
        "sidebar_title":               "Faded Dream",
        "nav_welcome":                 "\u0645\u0631\u062d\u0628\u0627\u064b",
        "nav_browser":                 "\u0627\u0644\u0645\u062a\u0635\u0641\u062d",
        "nav_gaming":                  "\u0627\u0644\u0623\u0644\u0639\u0627\u0628",
        "nav_peripherals":             "\u0627\u0644\u0645\u0644\u062d\u0642\u0627\u062a",
        "nav_file_transfer":           "\u0646\u0642\u0644 \u0627\u0644\u0645\u0644\u0641\u0627\u062a",
        "nav_office":                  "\u0627\u0644\u0645\u0643\u062a\u0628",
        "nav_media":                   "\u0627\u0644\u0648\u0633\u0627\u0626\u0637",
        "nav_comms":                   "\u0627\u0644\u062a\u0648\u0627\u0635\u0644",
        "nav_log":                     "\u0627\u0644\u0633\u062c\u0644",
        "packages_selected":           "\u062a\u0645 \u062a\u062d\u062f\u064a\u062f {n} \u062d\u0632\u0645\u0629",
        "startup_hint":                "\u0639\u0637\u0651\u0644 \u0627\u0644\u062a\u0634\u063a\u064a\u0644 \u0639\u0646\u062f \u0627\u0644\u0628\u062f\u0621 \u0628\u0639\u062f \u0627\u0644\u062a\u062b\u0628\u064a\u062a",
        "run_at_startup":              "\u0634\u063a\u0651\u0644 \u0639\u0646\u062f \u0627\u0644\u0628\u062f\u0621",
        "skip_all":                    "\u062a\u062e\u0637\u064a \u0627\u0644\u0643\u0644",
        "install_selected":            "\u062a\u062b\u0628\u064a\u062a \u0627\u0644\u0645\u062d\u062f\u062f",
        "welcome_sub":                 "\u062a\u0645 \u062a\u062b\u0628\u064a\u062a dotfiles \u0627\u0644\u062e\u0627\u0635\u0629 \u0628\u0643.\n\u0627\u062e\u062a\u0631 \u0627\u0644\u062d\u0632\u0645 \u0627\u0644\u0627\u062e\u062a\u064a\u0627\u0631\u064a\u0629 \u0645\u0646 \u0627\u0644\u062a\u0628\u0648\u064a\u0628\u0627\u062a \u062b\u0645 \u0627\u0636\u063a\u0637 <b>\u062a\u062b\u0628\u064a\u062a</b>.\n\u0639\u0637\u0651\u0644 <i>\u0627\u0644\u062a\u0634\u063a\u064a\u0644 \u0639\u0646\u062f \u0627\u0644\u0628\u062f\u0621</i> \u0628\u0639\u062f \u0627\u0644\u062a\u062b\u0628\u064a\u062a.",
        "card_browser_sub":            "\u0627\u062e\u062a\u0631 \u0645\u062a\u0635\u0641\u062d\u0643 \u0627\u0644\u0627\u0641\u062a\u0631\u0627\u0636\u064a",
        "card_gaming_sub":             "Steam, Heroic, Wine, MangoHud",
        "card_peripherals_sub":        "OpenRazer, Polychromatic, Piper",
        "card_filetransfer_sub":       "\u0623\u0646\u062f\u0631\u0648\u064a\u062f\u060c \u0643\u0627\u0645\u064a\u0631\u0627\u062a\u060c \u0645\u0634\u0627\u0631\u0643\u0629 \u0634\u0628\u0643\u064a\u0629",
        "card_office_sub":             "LibreOffice + \u062d\u0632\u0645 \u0627\u0644\u0644\u063a\u0629",
        "card_media_sub":              "GIMP, Kdenlive, OBS Liberty",
        "card_comms_sub":              "Vesktop, Telegram, Thunderbird",
        "browser_section":             "\u0627\u062e\u062a\u0631 \u0627\u0644\u0645\u062a\u0635\u0641\u062d \u0627\u0644\u0627\u0641\u062a\u0631\u0627\u0636\u064a",
        "recommended":                 "\u2b50 \u0645\u0648\u0635\u0649 \u0628\u0647",
        "lo_lang_section":             "\u062d\u0632\u0645 \u0627\u0644\u0644\u063a\u0629 LibreOffice",
        "log_what_title":              "\u0645\u0627 \u064a\u0641\u0639\u0644\u0647 \u0647\u0630\u0627 \u0627\u0644\u0645\u062b\u0628\u062a",
        "log_row_browser_t":           "\u0627\u0644\u0645\u062a\u0635\u0641\u062d",
        "log_row_browser_b":           "\u0627\u062e\u062a\u0631 \u0645\u062a\u0635\u0641\u062d\u0627\u064b \u2014 LibreWolf\u200f \u0623\u0648 Zen \u0623\u0648 Firefox \u0623\u0648 Vivaldi \u0623\u0648 Chrome \u0623\u0648 Edge. \u064a\u064f\u062b\u0628\u062a \u0627\u062e\u062a\u064a\u0627\u0631\u0643 \u062a\u0644\u0642\u0627\u0626\u064a\u0627\u064b \u0648\u064a\u064f\u062d\u062f\u0651\u062b \u0645\u062a\u063a\u064a\u0631 $Browser \u0641\u064a hyprland.conf \u0644\u064a\u0641\u062a\u062d \u0628\u0627\u0644\u0636\u063a\u0637 \u0639\u0644\u0649 Super+B.",
        "log_row_gaming_t":            "\u0627\u0644\u0623\u0644\u0639\u0627\u0628",
        "log_row_gaming_b":            "Steam (lib32)\u200f\u060c Heroic Games Launcher\u200f\u060c Wine + Winetricks/Mono/Gecko\u200f\u060c ProtonPlus\u200f\u060c GameMode + 32bit\u200f\u060c MangoHud + 32bit\u200f\u060c MangoJuice. \u0627\u062e\u062a\u064a\u0627\u0631 Wine \u064a\u062e\u062a\u0627\u0631 \u062a\u0644\u0642\u0627\u0626\u064a\u0627\u064b \u0627\u0644\u062d\u0632\u0645 \u0627\u0644\u0641\u0631\u0639\u064a\u0629 \u0627\u0644\u062b\u0644\u0627\u062b.",
        "log_row_periph_t":            "\u0627\u0644\u0645\u0644\u062d\u0642\u0627\u062a",
        "log_row_periph_b":            "\u062e\u062f\u0645\u0629 OpenRazer + \u062a\u0639\u0631\u064a\u0641 \u0627\u0644\u0646\u0648\u0627\u0629 (DKMS) + \u0645\u0643\u062a\u0628\u0629 Python \u0644\u0623\u062c\u0647\u0632\u0629 Razer. Polychromatic \u0644\u0625\u0636\u0627\u0621\u0629 RGB \u0644\u0643\u0644 \u0645\u0641\u062a\u0627\u062d. Piper \u0644\u0625\u0639\u062f\u0627\u062f \u0627\u0644\u0641\u0623\u0631\u0629/\u0644\u0648\u062d\u0629 \u0627\u0644\u0645\u0641\u0627\u062a\u064a\u062d. Solaar \u0644\u0645\u0633\u062a\u0642\u0628\u0644\u0627\u062a Logitech. jmtpfs \u0648 gphotofs \u0644\u062a\u062d\u0645\u064a\u0644 \u0627\u0644\u0623\u062c\u0647\u0632\u0629 \u0648\u0627\u0644\u0643\u0627\u0645\u064a\u0631\u0627\u062a \u2014 \u062c\u0645\u064a\u0639\u0647\u0627 AUR.",
        "log_row_office_t":            "\u0627\u0644\u0645\u0643\u062a\u0628",
        "log_row_office_b":            "LibreOffice Fresh \u0645\u0639 \u0623\u064a \u0645\u0646 \u062d\u0632\u0645 \u0627\u0644\u0644\u063a\u0629 \u0627\u0644\u0627\u062b\u0646\u062a\u064a \u0639\u0634\u0631\u0629 (\u0627\u0644\u0625\u0646\u062c\u0644\u064a\u0632\u064a\u0629 UK\u060c \u0627\u0644\u0631\u0648\u0645\u0627\u0646\u064a\u0629\u060c \u0627\u0644\u0641\u0631\u0646\u0633\u064a\u0629\u060c \u0627\u0644\u0623\u0644\u0645\u0627\u0646\u064a\u0629\u060c \u0627\u0644\u0625\u0633\u0628\u0627\u0646\u064a\u0629\u060c \u0627\u0644\u0625\u064a\u0637\u0627\u0644\u064a\u0629\u060c \u0627\u0644\u0628\u0631\u062a\u063a\u0627\u0644\u064a\u0629\u060c \u0627\u0644\u0631\u0648\u0633\u064a\u0629\u060c \u0627\u0644\u064a\u0627\u0628\u0627\u0646\u064a\u0629\u060c \u0627\u0644\u0635\u064a\u0646\u064a\u0629\u060c \u0627\u0644\u0643\u0648\u0631\u064a\u0629\u060c \u0627\u0644\u0639\u0631\u0628\u064a\u0629).",
        "log_row_media_t":             "\u0627\u0644\u0648\u0633\u0627\u0626\u0637",
        "log_row_media_b":             "\u0639\u0627\u0631\u0636 \u0627\u0644\u0635\u0648\u0631 Mirage\u060c GIMP\u060c Inkscape\u060c \u0645\u062d\u0631\u0631 \u0627\u0644\u0641\u064a\u062f\u064a\u0648 Kdenlive\u060c \u0645\u062d\u0648\u0644 HandBrake\u060c OBS Studio Liberty (\u0628\u0646\u0627\u0621 \u062d\u0631).",
        "log_row_ft_t":                "\u0646\u0642\u0644 \u0627\u0644\u0645\u0644\u0641\u0627\u062a",
        "log_row_ft_b":                "Android MTP \u0628\u0627\u0633\u062a\u062e\u062f\u0627\u0645 jmtpfs \u0648 go-mtpfs. \u0643\u0627\u0645\u064a\u0631\u0627 PTP \u0639\u0628\u0631 gphotofs \u0648 gphoto2. \u0644\u0627\u0633\u0644\u0643\u064a: Warpinator\u060c LocalSend (\u0645\u062a\u0639\u062f\u062f \u0627\u0644\u0645\u0646\u0635\u0627\u062a)\u060c Croc (P2P \u0645\u0634\u0641\u0631). USB: \u0623\u062f\u0648\u0627\u062a Android (ADB/fastboot) \u0648 Scrcpy \u0644\u0645\u0631\u0622\u0629 \u0627\u0644\u0634\u0627\u0634\u0629.",
        "log_row_comms_t":             "\u0627\u0644\u062a\u0648\u0627\u0635\u0644",
        "log_row_comms_b":             "Vesktop (Discord + Vencord)\u060c Telegram\u060c Element (Matrix)\u060c Thunderbird + \u062d\u0632\u0645 \u0644\u063a\u0629 \u0627\u062e\u062a\u064a\u0627\u0631\u064a\u0629\u060c \u0645\u0644\u0627\u062d\u0638\u0627\u062a Obsidian.",
        "log_row_how_t":               "\u0637\u0631\u064a\u0642\u0629 \u0627\u0644\u0639\u0645\u0644",
        "log_row_how_b":               "\u062a\u064f\u062b\u0628\u062a \u062d\u0632\u0645 \u0627\u0644\u0645\u0633\u062a\u0648\u062f\u0639 \u0641\u064a \u062f\u0641\u0639\u0629 pacman \u0648\u0627\u062d\u062f\u0629. \u062a\u064f\u0628\u0646\u0649 \u0648\u062a\u064f\u062b\u0628\u062a \u0643\u0644 \u062d\u0632\u0645\u0629 AUR (paru) \u0628\u0634\u0643\u0644 \u0645\u0646\u0641\u0635\u0644 \u2014 \u064a\u0645\u0643\u0646\u0643 \u0645\u0634\u0627\u0647\u062f\u0629 \u0645\u062e\u0631\u062c\u0627\u062a \u0627\u0644\u062a\u062c\u0645\u064a\u0639 \u0641\u064a \u0627\u0644\u0648\u0642\u062a \u0627\u0644\u0641\u0639\u0644\u064a. \u0628\u0639\u062f \u0627\u0644\u062a\u062b\u0628\u064a\u062a \u064a\u064f\u0639\u0637\u0651\u0644 \u0627\u0644\u062a\u0634\u063a\u064a\u0644 \u0639\u0646\u062f \u0627\u0644\u0628\u062f\u0621 \u062a\u0644\u0642\u0627\u0626\u064a\u0627\u064b. \u064a\u0645\u0643\u0646\u0643 \u0625\u0639\u0627\u062f\u0629 \u062a\u0641\u0639\u064a\u0644\u0647 \u0641\u064a \u0623\u064a \u0648\u0642\u062a.",
        "log_header":                  "Faded Dream \u2014 \u062a\u062b\u0628\u064a\u062a \u0627\u0644\u062d\u0632\u0645 \u0627\u0644\u0645\u062d\u062f\u062f\u0629",
        "log_repo_line":               "  \u062d\u0632\u0645 repo  ({n}): {pkgs}",
        "log_aur_line":                "  \u062d\u0632\u0645 AUR   ({n}): {pkgs}",
        "log_browser_patch":           "  \u062a\u0631\u0642\u064a\u0639 \u0627\u0644\u0645\u062a\u0635\u0641\u062d: $Browser = {exec}",
        "log_done":                    "\u2713  \u0627\u0643\u062a\u0645\u0644!",
        "log_done_bar":                "\u2713 \u0627\u0643\u062a\u0645\u0644!",
        "log_error":                   "[\u062e\u0637\u0623] {exc}",
        "prog_repo":                   "\u062c\u0627\u0631\u064a \u062a\u062b\u0628\u064a\u062a {n} \u062d\u0632\u0645\u0629 repo...",
        "prog_pkg":                    "\u062c\u0627\u0631\u064a \u062a\u062b\u0628\u064a\u062a {pkg}...",
        "prog_patch":                  "\u062c\u0627\u0631\u064a \u062a\u062d\u062f\u064a\u062b hyprland.conf \u2192 {exec}...",
            "log_banner_pacman": "\u2500\u2500 pacman  ({n} \u062d\u0632\u0645\u0629) \u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500",
        "log_banner_paru": "\u2500\u2500 paru  {pkg} \u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500",
        "log_banner_hypr": "\u2500\u2500 hyprland.conf \u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500",
        "log_browser_set": "  $Browser = {exec}",
        "badge_aur": "AUR",
        "badge_extra": "extra",
        "badge_galaxy": "galaxy",
        "badge_world": "world",
        "badge_lib32": "lib32",
        "badge_multilib": "multilib",
        "nothing_selected": "\u0644\u0645 \u064a\u062a\u0645 \u0627\u0644\u062a\u062d\u062f\u064a\u062f \u2014 \u062c\u0627\u0631\u064d \u0627\u0644\u0625\u063a\u0644\u0627\u0642\u3002",
        "lang_label": "\u0627\u0644\u0644\u063a\u0629",
        "welcome_title": "Faded Dream",
},
}

def _detect_lang():
    """Detect system language, fall back to English."""
    try:
        import locale as _lc
        lang = _lc.getlocale()[0] or ""
        code = lang.split("_")[0].lower()
        # handle zh_CN / zh_TW → zh
        if code.startswith("zh"):
            code = "zh"
        return code if code in TRANSLATIONS else "en"
    except Exception:
        return "en"

_LANG = _detect_lang()
# Load user's saved language preference if present
try:
    _saved = open(os.path.expanduser('~/.config/faded-dream-lang')).read().strip()
    if _saved in TRANSLATIONS:
        _LANG = _saved
except Exception:
    pass

def T(key, **kw):
    """Return translated string for key, with optional .format() kwargs."""
    s = (TRANSLATIONS.get(_LANG) or {}).get(key) or TRANSLATIONS["en"].get(key, key)
    return s.format(**kw) if kw else s

def set_lang(code):
    """Change the active UI language at runtime."""
    global _LANG
    if code in TRANSLATIONS:
        _LANG = code




SUB_PKG_NAMES = {
    "winetricks": {
        "en": "Winetricks",
        "ro": "Winetricks",
        "fr": "Winetricks",
        "de": "Winetricks",
        "es": "Winetricks",
        "it": "Winetricks",
        "pt": "Winetricks",
        "ru": "Winetricks",
        "ja": "Winetricks",
        "zh": "Winetricks",
        "ko": "Winetricks",
        "ar": "Winetricks"
    },
    "wine-mono": {
        "en": "Wine Mono",
        "ro": "Wine Mono",
        "fr": "Wine Mono",
        "de": "Wine Mono",
        "es": "Wine Mono",
        "it": "Wine Mono",
        "pt": "Wine Mono",
        "ru": "Wine Mono",
        "ja": "Wine Mono",
        "zh": "Wine Mono",
        "ko": "Wine Mono",
        "ar": "Wine Mono"
    },
    "wine-gecko": {
        "en": "Wine Gecko",
        "ro": "Wine Gecko",
        "fr": "Wine Gecko",
        "de": "Wine Gecko",
        "es": "Wine Gecko",
        "it": "Wine Gecko",
        "pt": "Wine Gecko",
        "ru": "Wine Gecko",
        "ja": "Wine Gecko",
        "zh": "Wine Gecko",
        "ko": "Wine Gecko",
        "ar": "Wine Gecko"
    },
    "lib32-gamemode": {
        "en": "GameMode (32-bit)",
        "ro": "GameMode (32-biți)",
        "fr": "GameMode (32 bits)",
        "de": "GameMode (32-Bit)",
        "es": "GameMode (32 bits)",
        "it": "GameMode (32 bit)",
        "pt": "GameMode (32 bits)",
        "ru": "GameMode (32-бит)",
        "ja": "GameMode (32ビット)",
        "zh": "GameMode (32位)",
        "ko": "GameMode (32비트)",
        "ar": "GameMode (32 بت)"
    },
    "lib32-mangohud": {
        "en": "MangoHud (32-bit)",
        "ro": "MangoHud (32-biți)",
        "fr": "MangoHud (32 bits)",
        "de": "MangoHud (32-Bit)",
        "es": "MangoHud (32 bits)",
        "it": "MangoHud (32 bit)",
        "pt": "MangoHud (32 bits)",
        "ru": "MangoHud (32-бит)",
        "ja": "MangoHud (32ビット)",
        "zh": "MangoHud (32位)",
        "ko": "MangoHud (32비트)",
        "ar": "MangoHud (32 بت)"
    },
    "openrazer-driver-dkms": {
        "en": "OpenRazer Driver",
        "ro": "Driver OpenRazer",
        "fr": "Pilote OpenRazer",
        "de": "OpenRazer-Treiber",
        "es": "Controlador OpenRazer",
        "it": "Driver OpenRazer",
        "pt": "Driver OpenRazer",
        "ru": "Драйвер OpenRazer",
        "ja": "OpenRazerドライバー",
        "zh": "OpenRazer驱动",
        "ko": "OpenRazer 드라이버",
        "ar": "تعريف OpenRazer"
    },
    "python-openrazer": {
        "en": "Python OpenRazer",
        "ro": "Python OpenRazer",
        "fr": "Python OpenRazer",
        "de": "Python OpenRazer",
        "es": "Python OpenRazer",
        "it": "Python OpenRazer",
        "pt": "Python OpenRazer",
        "ru": "Python OpenRazer",
        "ja": "Python OpenRazer",
        "zh": "Python OpenRazer",
        "ko": "Python OpenRazer",
        "ar": "Python OpenRazer"
    }
}

def TN(pkg_key):
    """Return translated sub-package name, falling back to key."""
    d = SUB_PKG_NAMES.get(pkg_key, {})
    return d.get(_LANG) or d.get("en", "")

# ── Per-package translated descriptions ───────────────────────────────────────
# Key = pkg identifier, value = dict of lang→translated desc
PKG_DESCS = {
    # Browsers
    "librewolf":                 {"en":"Privacy-focused Firefox fork — no telemetry, hardened","ro":"Fork Firefox axat pe confidențialitate — fără telemetrie, securizat","fr":"Fork Firefox axé sur la vie privée — sans télémétrie, renforcé","de":"Datenschutz-Firefox-Fork — keine Telemetrie, gehärtet","es":"Fork de Firefox enfocado en privacidad — sin telemetría, reforzado","it":"Fork Firefox orientato alla privacy — nessuna telemetria, hardened","pt":"Fork do Firefox focado em privacidade — sem telemetria, reforçado","ru":"Firefox-форк для приватности — без телеметрии, защищённый","ja":"プライバシー重視Firefoxフォーク — テレメトリなし","zh":"注重隐私的Firefox分支 — 无遥测，已加固","ko":"개인정보 중심 Firefox 포크 — 텔레메트리 없음","ar":"فرع Firefox مركّز على الخصوصية — بلا تتبع"},
    "zen-browser-bin":           {"en":"Beautiful Firefox-based browser with a modern UI","ro":"Browser bazat pe Firefox cu interfață modernă","fr":"Navigateur basé sur Firefox avec une interface moderne","de":"Schöner Firefox-basierter Browser mit moderner UI","es":"Navegador basado en Firefox con interfaz moderna","it":"Browser basato su Firefox con UI moderna","pt":"Navegador baseado no Firefox com UI moderna","ru":"Красивый браузер на Firefox с современным интерфейсом","ja":"モダンUIの美しいFirefoxベースブラウザ","zh":"基于Firefox的现代UI浏览器","ko":"현대적 UI의 Firefox 기반 브라우저","ar":"متصفح Firefox جميل بواجهة حديثة"},
    "firefox":                   {"en":"Mozilla's open source browser","ro":"Browserul open source de la Mozilla","fr":"Le navigateur open source de Mozilla","de":"Mozillas Open-Source-Browser","es":"El navegador open source de Mozilla","it":"Il browser open source di Mozilla","pt":"O navegador open source da Mozilla","ru":"Браузер с открытым кодом от Mozilla","ja":"Mozillaのオープンソースブラウザ","zh":"Mozilla的开源浏览器","ko":"Mozilla의 오픈소스 브라우저","ar":"متصفح Mozilla مفتوح المصدر"},
    "vivaldi":                   {"en":"Feature-rich Chromium browser","ro":"Browser Chromium bogat în funcții","fr":"Navigateur Chromium riche en fonctionnalités","de":"Funktionsreicher Chromium-Browser","es":"Navegador Chromium repleto de funciones","it":"Browser Chromium ricco di funzionalità","pt":"Navegador Chromium repleto de recursos","ru":"Функциональный браузер на Chromium","ja":"高機能Chromiumブラウザ","zh":"功能丰富的Chromium浏览器","ko":"기능이 풍부한 Chromium 브라우저","ar":"متصفح Chromium غني بالميزات"},
    "google-chrome":             {"en":"Google's browser","ro":"Browserul Google","fr":"Le navigateur de Google","de":"Googles Browser","es":"El navegador de Google","it":"Il browser di Google","pt":"O navegador do Google","ru":"Браузер Google","ja":"Googleのブラウザ","zh":"Google的浏览器","ko":"Google 브라우저","ar":"متصفح Google"},
    "microsoft-edge-stable-bin": {"en":"Microsoft's Chromium browser","ro":"Browserul Chromium de la Microsoft","fr":"Le navigateur Chromium de Microsoft","de":"Microsofts Chromium-Browser","es":"El navegador Chromium de Microsoft","it":"Il browser Chromium di Microsoft","pt":"O navegador Chromium da Microsoft","ru":"Chromium-браузер от Microsoft","ja":"MicrosoftのChromiumブラウザ","zh":"微软的Chromium浏览器","ko":"Microsoft의 Chromium 브라우저","ar":"متصفح Chromium من Microsoft"},
    # Gaming
    "steam":                     {"en":"Valve game platform","ro":"Platforma de jocuri Valve","fr":"Plateforme de jeux Valve","de":"Valve-Spieleplattform","es":"Plataforma de juegos Valve","it":"Piattaforma giochi Valve","pt":"Plataforma de jogos Valve","ru":"Игровая платформа Valve","ja":"Valveゲームプラットフォーム","zh":"Valve游戏平台","ko":"Valve 게임 플랫폼","ar":"منصة ألعاب Valve"},
    "heroic-games-launcher-bin": {"en":"Epic &amp; GOG launcher","ro":"Lansator Epic &amp; GOG","fr":"Lanceur Epic &amp; GOG","de":"Epic &amp; GOG-Starter","es":"Lanzador Epic &amp; GOG","it":"Lanciatore Epic &amp; GOG","pt":"Lançador Epic &amp; GOG","ru":"Лаунчер Epic &amp; GOG","ja":"Epic &amp; GOGランチャー","zh":"Epic &amp; GOG启动器","ko":"Epic &amp; GOG 런처","ar":"مشغّل Epic &amp; GOG"},
    "wine":                      {"en":"Windows compatibility layer","ro":"Strat de compatibilitate Windows","fr":"Couche de compatibilité Windows","de":"Windows-Kompatibilitätsschicht","es":"Capa de compatibilidad con Windows","it":"Livello di compatibilità Windows","pt":"Camada de compatibilidade com Windows","ru":"Слой совместимости с Windows","ja":"Windows互換レイヤー","zh":"Windows兼容层","ko":"Windows 호환성 레이어","ar":"طبقة توافق Windows"},
    "protonplus":                {"en":"Proton version manager GUI","ro":"Manager GUI pentru versiuni Proton","fr":"Interface de gestion des versions Proton","de":"Proton-Versionsmanager GUI","es":"Gestor de versiones Proton con GUI","it":"GUI per gestione versioni Proton","pt":"GUI de gestão de versões Proton","ru":"Графический менеджер версий Proton","ja":"ProtonバージョンマネージャGUI","zh":"Proton版本管理器图形界面","ko":"Proton 버전 관리자 GUI","ar":"واجهة رسومية لإدارة إصدارات Proton"},
    "gamemode":                  {"en":"CPU/GPU performance optimizer","ro":"Optimizator de performanță CPU/GPU","fr":"Optimiseur de performances CPU/GPU","de":"CPU/GPU-Leistungsoptimierer","es":"Optimizador de rendimiento CPU/GPU","it":"Ottimizzatore prestazioni CPU/GPU","pt":"Otimizador de desempenho CPU/GPU","ru":"Оптимизатор производительности CPU/GPU","ja":"CPU/GPUパフォーマンス最適化ツール","zh":"CPU/GPU性能优化器","ko":"CPU/GPU 성능 최적화기","ar":"محسّن أداء المعالج والرسومات"},
    "mangohud":                  {"en":"In-game FPS/stats overlay","ro":"Overlay în joc cu FPS/statistici","fr":"Overlay FPS/statistiques en jeu","de":"In-Game-Overlay für FPS/Statistiken","es":"Overlay de FPS/estadísticas en juego","it":"Overlay FPS/statistiche in gioco","pt":"Overlay de FPS/estatísticas em jogo","ru":"Игровой оверлей FPS/статистики","ja":"ゲーム内FPS/統計オーバーレイ","zh":"游戏内FPS/统计叠加层","ko":"게임 내 FPS/통계 오버레이","ar":"طبقة عرض FPS داخل اللعبة"},
    "mangojuice":                {"en":"GUI configurator for MangoHud","ro":"Configurator GUI pentru MangoHud","fr":"Configurateur graphique pour MangoHud","de":"GUI-Konfigurator für MangoHud","es":"Configurador gráfico para MangoHud","it":"Configuratore GUI per MangoHud","pt":"Configurador GUI para MangoHud","ru":"Графический конфигуратор MangoHud","ja":"MangoHudのGUI設定ツール","zh":"MangoHud图形配置器","ko":"MangoHud GUI 설정기","ar":"أداة ضبط رسومية لـ MangoHud"},
    # Peripherals
    "openrazer-daemon":          {"en":"Background service for Razer hardware","ro":"Serviciu de fundal pentru hardware Razer","fr":"Service en arrière-plan pour matériel Razer","de":"Hintergrunddienst für Razer-Hardware","es":"Servicio en segundo plano para hardware Razer","it":"Servizio in background per hardware Razer","pt":"Serviço em segundo plano para hardware Razer","ru":"Фоновая служба для оборудования Razer","ja":"Razerhardware用バックグラウンドサービス","zh":"Razer硬件后台服务","ko":"Razer 하드웨어 백그라운드 서비스","ar":"خدمة خلفية لأجهزة Razer"},
    "polychromatic":             {"en":"OpenRazer GUI — per-key RGB, effects and DPI profiles","ro":"GUI OpenRazer — RGB per-tastă, efecte și profiluri DPI","fr":"GUI OpenRazer — RGB par touche, effets et profils DPI","de":"OpenRazer GUI — Einzel-Tasten-RGB, Effekte und DPI-Profile","es":"GUI OpenRazer — RGB por tecla, efectos y perfiles DPI","it":"GUI OpenRazer — RGB per tasto, effetti e profili DPI","pt":"GUI OpenRazer — RGB por tecla, efeitos e perfis DPI","ru":"GUI OpenRazer — RGB на клавишу, эффекты и DPI-профили","ja":"OpenRazer GUI — キー別RGB・エフェクト・DPIプロファイル","zh":"OpenRazer图形界面 — 按键RGB、特效与DPI配置","ko":"OpenRazer GUI — 키별 RGB, 효과 및 DPI 프로필","ar":"واجهة OpenRazer — RGB لكل مفتاح وتأثيرات"},
    "piper":                     {"en":"Mouse &amp; keyboard configurator — DPI, buttons, polling rate. Multi-brand","ro":"Configurator mouse și tastatură — DPI, butoane, rată sondare. Multi-brand","fr":"Configurateur souris &amp; clavier — DPI, boutons, taux de sondage. Multi-marque","de":"Maus- &amp; Tastatur-Konfigurator — DPI, Tasten, Abtastrate. Multi-Marke","es":"Configurador de ratón y teclado — DPI, botones, tasa de sondeo. Multimarca","it":"Configuratore mouse e tastiera — DPI, pulsanti, polling. Multi-brand","pt":"Configurador de rato e teclado — DPI, botões, taxa de sondagem. Multimarca","ru":"Конфигуратор мыши и клавиатуры — DPI, кнопки, опрос. Мультибренд","ja":"マウス・キーボード設定 — DPI・ボタン・ポーリングレート。マルチブランド","zh":"鼠标键盘配置器 — DPI、按键、轮询率，多品牌","ko":"마우스 &amp; 키보드 설정기 — DPI, 버튼, 폴링레이트. 멀티브랜드","ar":"ضابط الفأرة والكيبورد — DPI وأزرار ومعدل الاستطلاع"},
    "solaar":                    {"en":"Logitech device manager — Unifying/Bolt receiver pairing","ro":"Manager dispozitive Logitech — asociere receptor Unifying/Bolt","fr":"Gestionnaire Logitech — association récepteur Unifying/Bolt","de":"Logitech-Geräteverwaltung — Unifying/Bolt-Empfänger-Kopplung","es":"Gestor de dispositivos Logitech — emparejamiento receptor Unifying/Bolt","it":"Gestore dispositivi Logitech — associazione ricevitore Unifying/Bolt","pt":"Gestor de dispositivos Logitech — emparelhamento receptor Unifying/Bolt","ru":"Менеджер устройств Logitech — сопряжение Unifying/Bolt","ja":"Logitechデバイスマネージャー — Unifying/Bolt受信機ペアリング","zh":"Logitech设备管理器 — Unifying/Bolt配对","ko":"Logitech 장치 관리자 — Unifying/Bolt 수신기 페어링","ar":"مدير أجهزة Logitech — إقران مستقبل Unifying/Bolt"},
    # File Transfer
    "jmtpfs":                    {"en":"Mount Android phones via MTP — Android 4–14","ro":"Montare telefoane Android via MTP — Android 4–14","fr":"Monter téléphones Android via MTP — Android 4–14","de":"Android-Geräte via MTP einbinden — Android 4–14","es":"Montar teléfonos Android vía MTP — Android 4–14","it":"Monta telefoni Android via MTP — Android 4–14","pt":"Montar telemóveis Android via MTP — Android 4–14","ru":"Монтировать Android по MTP — Android 4–14","ja":"MTP経由でAndroidを接続 — Android 4–14","zh":"通过MTP挂载Android手机 — Android 4–14","ko":"MTP로 Android 폰 마운트 — Android 4–14","ar":"تركيب هواتف Android عبر MTP — الإصدارات 4–14"},
    "go-mtpfs-git":              {"en":"Go-based MTP filesystem — faster for large transfers","ro":"Sistem MTP bazat pe Go — mai rapid pentru fișiere mari","fr":"Système MTP en Go — plus rapide pour les gros transferts","de":"Go-basierter MTP-Treiber — schneller für große Dateien","es":"Sistema MTP en Go — más rápido para transferencias grandes","it":"Filesystem MTP in Go — più veloce per grandi trasferimenti","pt":"Sistema MTP em Go — mais rápido para transferências grandes","ru":"MTP-файловая система на Go — быстрее для больших файлов","ja":"Go製MTPファイルシステム — 大容量転送が高速","zh":"基于Go的MTP文件系统 — 大文件传输更快","ko":"Go 기반 MTP 파일시스템 — 대용량 전송에 빠름","ar":"نظام ملفات MTP بـGo — أسرع للملفات الكبيرة"},
    "gphotofs":                  {"en":"PTP mount via FUSE — good for older cameras","ro":"Montare PTP via FUSE — bun pentru camere mai vechi","fr":"Montage PTP via FUSE — adapté aux appareils anciens","de":"PTP-Einbindung via FUSE — gut für ältere Kameras","es":"Montaje PTP via FUSE — bueno para cámaras antiguas","it":"Mount PTP via FUSE — adatto per fotocamere datate","pt":"Mount PTP via FUSE — bom para câmeras mais antigas","ru":"PTP-монтирование через FUSE — для старых камер","ja":"FUSE経由のPTPマウント — 古いカメラに対応","zh":"通过FUSE的PTP挂载 — 适合旧款相机","ko":"FUSE 통한 PTP 마운트 — 구형 카메라에 적합","ar":"تركيب PTP عبر FUSE — مناسب للكاميرات القديمة"},
    "gphoto2":                   {"en":"Command-line camera control and image download","ro":"Control cameră foto și descărcare imagini din linie de comandă","fr":"Contrôle appareil photo et téléchargement en ligne de commande","de":"Kamera-Steuerung und Bild-Download per Kommandozeile","es":"Control de cámara y descarga de imágenes por línea de comandos","it":"Controllo fotocamera e download immagini da terminale","pt":"Controlo de câmera e download de imagens por linha de comando","ru":"Командная строка для управления камерой и скачивания фото","ja":"コマンドラインでカメラ制御と画像ダウンロード","zh":"命令行相机控制与图片下载","ko":"커맨드라인 카메라 제어 및 이미지 다운로드","ar":"التحكم في الكاميرا وتنزيل الصور عبر سطر الأوامر"},
    "warpinator":                {"en":"LAN file sharing — send and receive on local network","ro":"Partajare fișiere LAN — trimite și primește pe rețeaua locală","fr":"Partage de fichiers LAN — envoyer et recevoir sur le réseau local","de":"LAN-Dateifreigabe — Dateien im lokalen Netz senden und empfangen","es":"Compartir archivos LAN — enviar y recibir en red local","it":"Condivisione file LAN — invia e ricevi sulla rete locale","pt":"Partilha de ficheiros LAN — enviar e receber na rede local","ru":"Общий доступ по LAN — отправка и получение в локальной сети","ja":"LANファイル共有 — ローカルネットワークで送受信","zh":"局域网文件共享 — 在本地网络收发文件","ko":"LAN 파일 공유 — 로컬 네트워크에서 송수신","ar":"مشاركة ملفات LAN — الإرسال والاستقبال على الشبكة المحلية"},
    "localsend-bin":             {"en":"Cross-platform AirDrop — works with iOS, Android, Windows","ro":"AirDrop cross-platform — funcționează cu iOS, Android, Windows","fr":"AirDrop multiplateforme — fonctionne avec iOS, Android, Windows","de":"Plattformübergreifendes AirDrop — iOS, Android, Windows","es":"AirDrop multiplataforma — funciona con iOS, Android, Windows","it":"AirDrop multipiattaforma — funziona con iOS, Android, Windows","pt":"AirDrop multiplataforma — funciona com iOS, Android, Windows","ru":"Кроссплатформенный AirDrop — iOS, Android, Windows","ja":"クロスプラットフォームAirDrop — iOS/Android/Windows対応","zh":"跨平台AirDrop — 支持iOS、Android、Windows","ko":"크로스 플랫폼 AirDrop — iOS, Android, Windows 지원","ar":"AirDrop متعدد المنصات — يدعم iOS وAndroid وWindows"},
    "croc":                      {"en":"Securely send files between any two computers — P2P encrypted","ro":"Trimite fișiere securizat între orice două calculatoare — P2P criptat","fr":"Envoyer des fichiers en toute sécurité entre deux ordinateurs — P2P chiffré","de":"Dateien sicher zwischen zwei Computern senden — P2P verschlüsselt","es":"Enviar archivos de forma segura entre dos ordenadores — P2P cifrado","it":"Invia file in modo sicuro tra due computer — P2P cifrato","pt":"Enviar ficheiros com segurança entre dois computadores — P2P cifrado","ru":"Безопасная отправка файлов между компьютерами — P2P с шифрованием","ja":"2台のPC間でファイルを安全に送受信 — P2P暗号化","zh":"在任意两台电脑间安全传输文件 — P2P加密","ko":"두 컴퓨터 간 안전한 파일 전송 — P2P 암호화","ar":"إرسال ملفات بأمان بين جهازين — P2P مشفّر"},
    "android-tools":             {"en":"ADB and fastboot — sideloading, debugging, USB file transfer","ro":"ADB și fastboot — sideloading, depanare, transfer fișiere USB","fr":"ADB et fastboot — chargement latéral, débogage, transfert USB","de":"ADB und fastboot — Sideloading, Debugging, USB-Dateiübertragung","es":"ADB y fastboot — carga lateral, depuración, transferencia USB","it":"ADB e fastboot — sideloading, debug, trasferimento USB","pt":"ADB e fastboot — sideloading, depuração, transferência USB","ru":"ADB и fastboot — сайдлоадинг, отладка, передача файлов по USB","ja":"ADB・fastboot — サイドロード・デバッグ・USB転送","zh":"ADB和fastboot — 旁加载、调试、USB传文件","ko":"ADB 및 fastboot — 사이드로딩, 디버깅, USB 파일 전송","ar":"ADB و fastboot — التثبيت الجانبي والتصحيح ونقل الملفات"},
    "scrcpy":                    {"en":"Display and control Android over USB or Wi-Fi — no root needed","ro":"Afișează și controlează Android via USB sau Wi-Fi — fără root","fr":"Afficher et contrôler Android via USB ou Wi-Fi — sans root","de":"Android-Anzeige und -Steuerung per USB oder WLAN — kein Root","es":"Muestra y controla Android vía USB o Wi-Fi — sin root","it":"Visualizza e controlla Android via USB o Wi-Fi — no root","pt":"Visualizar e controlar Android via USB ou Wi-Fi — sem root","ru":"Управление Android по USB или Wi-Fi — без root","ja":"USB/Wi-Fi経由でAndroidを表示・操作 — root不要","zh":"通过USB或Wi-Fi显示和控制Android — 无需root","ko":"USB 또는 Wi-Fi로 Android 표시 &amp; 제어 — 루트 불필요","ar":"عرض والتحكم في Android عبر USB أو واي فاي — بدون روت"},
    # Media
    "mirage":                    {"en":"Feature-rich image viewer","ro":"Vizualizator de imagini bogat în funcții","fr":"Visionneuse d'images riche en fonctionnalités","de":"Funktionsreicher Bildbetrachter","es":"Visor de imágenes repleto de funciones","it":"Visualizzatore immagini ricco di funzionalità","pt":"Visualizador de imagens repleto de recursos","ru":"Многофункциональный просмотрщик изображений","ja":"高機能画像ビューア","zh":"功能丰富的图像查看器","ko":"기능이 풍부한 이미지 뷰어","ar":"عارض صور غني بالميزات"},
    "gimp":                      {"en":"Image editor","ro":"Editor de imagini","fr":"Éditeur d'images","de":"Bildbearbeitungsprogramm","es":"Editor de imágenes","it":"Editor di immagini","pt":"Editor de imagens","ru":"Редактор изображений","ja":"画像エディタ","zh":"图像编辑器","ko":"이미지 편집기","ar":"محرر الصور"},
    "inkscape":                  {"en":"Vector graphics editor","ro":"Editor grafică vectorială","fr":"Éditeur de graphiques vectoriels","de":"Vektorgrafik-Editor","es":"Editor de gráficos vectoriales","it":"Editor di grafica vettoriale","pt":"Editor de gráficos vetoriais","ru":"Редактор векторной графики","ja":"ベクター画像エディタ","zh":"矢量图形编辑器","ko":"벡터 그래픽 편집기","ar":"محرر الرسومات المتجهية"},
    "kdenlive":                  {"en":"Video editor","ro":"Editor video","fr":"Éditeur vidéo","de":"Videobearbeitungsprogramm","es":"Editor de vídeo","it":"Editor video","pt":"Editor de vídeo","ru":"Видеоредактор","ja":"ビデオエディタ","zh":"视频编辑器","ko":"비디오 편집기","ar":"محرر الفيديو"},
    "handbrake":                 {"en":"Video converter/compressor","ro":"Convertor/compresor video","fr":"Convertisseur/compresseur vidéo","de":"Video-Konverter/-Kompressor","es":"Conversor/compresor de vídeo","it":"Convertitore/compressore video","pt":"Conversor/compressor de vídeo","ru":"Конвертер/компрессор видео","ja":"動画変換・圧縮ツール","zh":"视频转换/压缩器","ko":"비디오 변환기/압축기","ar":"محوّل ومضغوط الفيديو"},
    "obs-studio-liberty":        {"en":"Streaming &amp; recording","ro":"Streaming și înregistrare","fr":"Streaming et enregistrement","de":"Streaming &amp; Aufnahme","es":"Streaming y grabación","it":"Streaming e registrazione","pt":"Streaming e gravação","ru":"Стриминг и запись","ja":"配信・録画","zh":"直播与录制","ko":"스트리밍 &amp; 녹화","ar":"البث والتسجيل"},
    # Comms
    "vesktop":                   {"en":"Discord client with Vencord mods","ro":"Client Discord cu moduri Vencord","fr":"Client Discord avec mods Vencord","de":"Discord-Client mit Vencord-Mods","es":"Cliente Discord con mods Vencord","it":"Client Discord con mod Vencord","pt":"Cliente Discord com mods Vencord","ru":"Discord-клиент с модами Vencord","ja":"Vencordモッド入りDiscordクライアント","zh":"带Vencord插件的Discord客户端","ko":"Vencord 모드 Discord 클라이언트","ar":"عميل Discord مع إضافات Vencord"},
    "telegram-desktop":          {"en":"Messaging platform","ro":"Platformă de mesagerie","fr":"Plateforme de messagerie","de":"Messaging-Plattform","es":"Plataforma de mensajería","it":"Piattaforma di messaggistica","pt":"Plataforma de mensagens","ru":"Мессенджер","ja":"メッセージングプラットフォーム","zh":"即时通讯平台","ko":"메시징 플랫폼","ar":"منصة مراسلة"},
    "element-desktop":           {"en":"Matrix decentralized chat","ro":"Chat Matrix descentralizat","fr":"Chat décentralisé Matrix","de":"Matrix dezentraler Chat","es":"Chat descentralizado Matrix","it":"Chat decentralizzata Matrix","pt":"Chat descentralizado Matrix","ru":"Децентрализованный чат Matrix","ja":"Matrix分散チャット","zh":"Matrix去中心化聊天","ko":"Matrix 탈중앙화 채팅","ar":"دردشة Matrix لامركزية"},
    "thunderbird":               {"en":"Email client with language packs","ro":"Client de email cu pachete de limbă","fr":"Client email avec packs de langue","de":"E-Mail-Client mit Sprachpaketen","es":"Cliente de correo con paquetes de idioma","it":"Client email con pacchetti lingua","pt":"Cliente de email com pacotes de idioma","ru":"Почтовый клиент с языковыми пакетами","ja":"言語パック対応メールクライアント","zh":"含语言包的邮件客户端","ko":"언어 팩 지원 이메일 클라이언트","ar":"عميل بريد مع حزم اللغة"},
    "obsidian":                  {"en":"Markdown note taking","ro":"Notițe în format Markdown","fr":"Prise de notes Markdown","de":"Markdown-Notizen","es":"Toma de notas Markdown","it":"Note in Markdown","pt":"Notas em Markdown","ru":"Заметки на Markdown","ja":"Markdownノートアプリ","zh":"Markdown笔记应用","ko":"Markdown 노트 앱","ar":"تدوين ملاحظات بصيغة Markdown"},
    # Office
    "libreoffice-fresh":         {"en":"Latest stable — Writer, Calc, Impress, Draw","ro":"Ultima versiune stabilă — Writer, Calc, Impress, Draw","fr":"Dernière version stable — Writer, Calc, Impress, Draw","de":"Neueste stabile Version — Writer, Calc, Impress, Draw","es":"Última versión estable — Writer, Calc, Impress, Draw","it":"Ultima versione stabile — Writer, Calc, Impress, Draw","pt":"Última versão estável — Writer, Calc, Impress, Draw","ru":"Последняя стабильная — Writer, Calc, Impress, Draw","ja":"最新安定版 — Writer, Calc, Impress, Draw","zh":"最新稳定版 — Writer、Calc、Impress、Draw","ko":"최신 안정 버전 — Writer, Calc, Impress, Draw","ar":"أحدث إصدار مستقر — Writer و Calc و Impress و Draw"},
}

def TD(pkg_key):
    """Return translated description for a package, falling back to English."""
    d = PKG_DESCS.get(pkg_key, {})
    return d.get(_LANG) or d.get("en", "")

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


# ── Section label translations ────────────────────────────────────────────────
_SEC_LABELS = {
    "Launchers":         {"en":"Launchers","ro":"Lansatoare","fr":"Lanceurs","de":"Starter","es":"Lanzadores","it":"Lanciatori","pt":"Lançadores","ru":"Лаунчеры","ja":"ランチャー","zh":"启动器","ko":"런처","ar":"المشغّلات"},
    "Compatibility":     {"en":"Compatibility","ro":"Compatibilitate","fr":"Compatibilité","de":"Kompatibilität","es":"Compatibilidad","it":"Compatibilità","pt":"Compatibilidade","ru":"Совместимость","ja":"互換性","zh":"兼容性","ko":"호환성","ar":"التوافق"},
    "Performance":       {"en":"Performance","ro":"Performanță","fr":"Performance","de":"Leistung","es":"Rendimiento","it":"Prestazioni","pt":"Desempenho","ru":"Производительность","ja":"パフォーマンス","zh":"性能","ko":"성능","ar":"الأداء"},
    "Messaging":         {"en":"Messaging","ro":"Mesagerie","fr":"Messagerie","de":"Messaging","es":"Mensajería","it":"Messaggistica","pt":"Mensagens","ru":"Мессенджеры","ja":"メッセージ","zh":"即时通讯","ko":"메시징","ar":"المراسلة"},
    "Email":             {"en":"Email","ro":"Email","fr":"Courriel","de":"E-Mail","es":"Correo","it":"Email","pt":"Email","ru":"Почта","ja":"メール","zh":"邮件","ko":"이메일","ar":"البريد"},
    "Notes":             {"en":"Notes","ro":"Notițe","fr":"Notes","de":"Notizen","es":"Notas","it":"Note","pt":"Notas","ru":"Заметки","ja":"メモ","zh":"笔记","ko":"노트","ar":"الملاحظات"},
    "RGB / Razer":       {"en":"RGB / Razer","ro":"RGB / Razer","fr":"RGB / Razer","de":"RGB / Razer","es":"RGB / Razer","it":"RGB / Razer","pt":"RGB / Razer","ru":"RGB / Razer","ja":"RGB / Razer","zh":"RGB / Razer","ko":"RGB / Razer","ar":"RGB / Razer"},
    "Peripherals":       {"en":"Peripherals","ro":"Periferice","fr":"Périphériques","de":"Peripherie","es":"Periféricos","it":"Periferiche","pt":"Periféricos","ru":"Периферия","ja":"周辺機器","zh":"外设","ko":"주변기기","ar":"الملحقات"},
    "Android / MTP":     {"en":"Android / MTP","ro":"Android / MTP","fr":"Android / MTP","de":"Android / MTP","es":"Android / MTP","it":"Android / MTP","pt":"Android / MTP","ru":"Android / MTP","ja":"Android / MTP","zh":"Android / MTP","ko":"Android / MTP","ar":"Android / MTP"},
    "Camera / PTP":      {"en":"Camera / PTP","ro":"Cameră / PTP","fr":"Appareil photo / PTP","de":"Kamera / PTP","es":"Cámara / PTP","it":"Fotocamera / PTP","pt":"Câmera / PTP","ru":"Камера / PTP","ja":"カメラ / PTP","zh":"相机 / PTP","ko":"카메라 / PTP","ar":"الكاميرا / PTP"},
    "Network / Wireless":{"en":"Network / Wireless","ro":"Rețea / Wireless","fr":"Réseau / Sans fil","de":"Netzwerk / WLAN","es":"Red / Inalámbrico","it":"Rete / Wireless","pt":"Rede / Sem fios","ru":"Сеть / Беспроводная","ja":"ネットワーク / ワイヤレス","zh":"网络 / 无线","ko":"네트워크 / 무선","ar":"الشبكة / اللاسلكي"},
    "USB / Serial":      {"en":"USB / Serial","ro":"USB / Serial","fr":"USB / Série","de":"USB / Seriell","es":"USB / Serie","it":"USB / Seriale","pt":"USB / Serial","ru":"USB / Последовательный","ja":"USB / シリアル","zh":"USB / 串口","ko":"USB / 시리얼","ar":"USB / تسلسلي"},
    "Base":              {"en":"Base","ro":"De bază","fr":"Base","de":"Basis","es":"Base","it":"Base","pt":"Base","ru":"Основное","ja":"基本","zh":"基础","ko":"기본","ar":"الأساسي"},
    "Creative Tools":    {"en":"Creative Tools","ro":"Instrumente Creative","fr":"Outils Créatifs","de":"Kreativwerkzeuge","es":"Herramientas Creativas","it":"Strumenti Creativi","pt":"Ferramentas Criativas","ru":"Творческие инструменты","ja":"クリエイティブツール","zh":"创意工具","ko":"크리에이티브 도구","ar":"الأدوات الإبداعية"},
}

def TS(section_name):
    """Return translated section label."""
    d = _SEC_LABELS.get(section_name, {})
    return d.get(_LANG) or d.get("en", section_name)

# ── Repo badge style map ──────────────────────────────────────────────────────
REPO_STYLE = {
    "AUR":     ("#4fd9c4","#0e2e2e","#1a4040"),
    "extra":   ("#a89ff7","#18183a","#28285a"),
    "galaxy":  ("#f7b96a","#2e2200","#4a3800"),
    "world":   ("#6aaff7","#001a2e","#002a48"),
    "lib32":   ("#f76a6a","#2e0e0e","#4a1818"),
    "multilib":("#b46af7","#1e0e2e","#381848"),
}

_BADGE_KEY = {
    "AUR":      "badge_aur",
    "extra":    "badge_extra",
    "galaxy":   "badge_galaxy",
    "world":    "badge_world",
    "lib32":    "badge_lib32",
    "multilib": "badge_multilib",
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
    lbl = Gtk.Label(label=T(_BADGE_KEY.get(repo, 'badge_extra')))
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
        self.set_title(T("app_title"))
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
        s_title = Gtk.Label(label=T("sidebar_title"))
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
        sidebar.append(self._build_lang_selector())

        pages = [
            ("🌙", T("nav_welcome"),      self._page_welcome(),                      "Welcome"),
            ("🌐", T("nav_browser"),      self._page_browser(),                      "Browser"),
            ("🎮", T("nav_gaming"),       self._page_sections(GAMING),               "Gaming"),
            ("💡", T("nav_peripherals"),  self._page_sections(PERIPHERALS),          "Peripherals"),
            ("📁", T("nav_file_transfer"),self._page_sections(FILE_TRANSFER),        "File Transfer"),
            ("📄", T("nav_office"),       self._page_office(),                       "Office"),
            ("🎬", T("nav_media"),        self._page_flat(MEDIA),                    "Media"),
            ("💬", T("nav_comms"),        self._page_sections(COMMS, comms=True),    "Comms"),
            ("📋", T("nav_log"),          self._page_log(),                          "Log"),
        ]
        self._log_page_name = "Log"

        _no_badge = {"Welcome", "Log"}
        self._nav_badges = {}   # page_name -> badge Gtk.Label

        for _pt in pages:
            icon, label, page = _pt[0], _pt[1], _pt[2]
            eng = _pt[3] if len(_pt) > 3 else label
            self._stack.add_named(page, eng)
            row = Gtk.ListBoxRow()
            box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=10)
            box.set_margin_start(8); box.set_margin_end(8)
            box.set_margin_top(8);   box.set_margin_bottom(8)
            il = Gtk.Label(label=icon)
            il.set_valign(Gtk.Align.CENTER)
            il.add_css_class("nav-icon")
            il.set_size_request(28, -1)
            tl = Gtk.Label(label=label)
            tl.set_halign(Gtk.Align.START)
            tl.set_valign(Gtk.Align.CENTER)
            tl.set_hexpand(True)
            box.append(il); box.append(tl)
            if eng not in _no_badge:
                badge = Gtk.Label(label="")
                badge.set_css_classes(["nav-count-badge"])
                badge.set_valign(Gtk.Align.CENTER)
                badge.set_visible(False)   # hidden until count > 0
                box.append(badge)
                self._nav_badges[eng] = badge
            row.set_child(box)
            row._page_name = eng
            row._display_label = label  # translated
            self._nav_list.append(row)

        # content side
        content = Gtk.Box(orientation=Gtk.Orientation.VERTICAL)
        c_header = Adw.HeaderBar()
        c_header.set_show_start_title_buttons(False)
        self._content_title = Adw.WindowTitle(title=T("nav_welcome"), subtitle="")
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
        self._content_title.set_title(getattr(row, "_display_label", row._page_name))

    def _switch_to_log(self):
        self._navigate_to(self._log_page_name)

    def _navigate_to(self, page_name):
        for i in range(9):
            r = self._nav_list.get_row_at_index(i)
            if r and r._page_name == page_name:
                self._nav_list.select_row(r)
                break


    def _build_lang_selector(self):
        """Compact language selector row for the sidebar footer."""
        # Map of locale code → display label
        _LANG_OPTIONS = [
            ("en", "🇬🇧  English"),
            ("ro", "🇷🇴  Română"),
            ("fr", "🇫🇷  Français"),
            ("de", "🇩🇪  Deutsch"),
            ("es", "🇪🇸  Español"),
            ("it", "🇮🇹  Italiano"),
            ("pt", "🇵🇹  Português"),
            ("ru", "🇷🇺  Русский"),
            ("ja", "🇯🇵  日本語"),
            ("zh", "🇨🇳  中文"),
            ("ko", "🇰🇷  한국어"),
            ("ar", "🇸🇦  العربية"),
        ]
        box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=6)
        box.set_margin_start(10); box.set_margin_end(10)
        box.set_margin_top(6);    box.set_margin_bottom(6)

        lbl = Gtk.Label(label="🌐")
        lbl.set_valign(Gtk.Align.CENTER)
        box.append(lbl)

        combo = Gtk.DropDown()
        strings = Gtk.StringList()
        active_idx = 0
        for i, (code, label) in enumerate(_LANG_OPTIONS):
            strings.append(label)
            if code == _LANG:
                active_idx = i
        combo.set_model(strings)
        combo.set_selected(active_idx)
        combo.set_hexpand(True)
        combo.add_css_class("flat")

        def _on_lang_change(dd, _param):
            idx = dd.get_selected()
            code = _LANG_OPTIONS[idx][0]
            if code == _LANG:
                return
            # Save preference
            try:
                cfg = os.path.expanduser("~/.config/faded-dream-lang")
                open(cfg, "w").write(code)
            except Exception:
                pass
            # Restart to apply
            os.execv(sys.executable, [sys.executable] + sys.argv)

        combo.connect("notify::selected", _on_lang_change)
        box.append(combo)
        return box

    # ── Footer ────────────────────────────────────────────────────────────────
    def _build_footer(self):
        bar = Gtk.ActionBar()

        left = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=2)
        self._count_lbl = Gtk.Label()
        self._count_lbl.add_css_class("caption")
        self._count_lbl.set_halign(Gtk.Align.START)
        self._update_count()
        fsub = Gtk.Label(label=T("startup_hint"))
        fsub.add_css_class("caption"); fsub.add_css_class("dim-label")
        fsub.set_halign(Gtk.Align.START)
        left.append(self._count_lbl); left.append(fsub)
        bar.pack_start(left)

        tog_box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=6)
        tog_lbl = Gtk.Label(label=T("run_at_startup"))
        tog_lbl.add_css_class("caption")
        self._startup_sw = Gtk.Switch()
        self._startup_sw.set_active(self._startup_enabled())
        self._startup_sw.set_valign(Gtk.Align.CENTER)
        self._startup_sw.connect("notify::active", self._on_startup_toggle)
        tog_box.append(tog_lbl); tog_box.append(self._startup_sw)
        bar.pack_start(tog_box)

        skip_btn = Gtk.Button(label=T("skip_all"))
        skip_btn.add_css_class("flat")
        skip_btn.connect("clicked", lambda _: self.close())
        bar.pack_end(skip_btn)

        self._install_btn = Gtk.Button(label=T("install_selected"))
        self._install_btn.add_css_class("suggested-action")
        self._install_btn.connect("clicked", self._on_install)
        bar.pack_end(self._install_btn)

        return bar

    # ── Count ─────────────────────────────────────────────────────────────────
    def _update_count(self):
        total = len(self.selected) + (1 if self.browser else 0)
        self._count_lbl.set_markup(
            f'<span foreground="#4fd9c4" weight="bold">{total}</span>'
            f'<span foreground="#666677"> {T("packages_selected", n=total).split(str(total), 1)[-1].strip()}</span>')
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

        # Office: lo_langs + office base pkg only
        n = 0
        for p in OFFICE_BASE:
            if p["pkg"] in self.selected: n += 1
        n += len(getattr(self, 'lo_langs', set()))
        counts["Office"] = n
        # Thunderbird language packs → Comms badge
        counts["Comms"] = counts.get("Comms", 0) + len(getattr(self, 'tb_langs', set()))

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

        title = Gtk.Label(label=T("welcome_title"))
        title.add_css_class("welcome-title")
        title_box.append(title)

        sub = Gtk.Label()
        sub.set_markup(T("welcome_sub"))
        sub.add_css_class("welcome-sub")
        sub.set_justify(Gtk.Justification.CENTER)
        sub.set_wrap(True)
        title_box.append(sub)
        outer.append(title_box)

        # ── cards ────────────────────────────────────────────────────────────
        cards_data = [
            ("🌐", T("nav_browser"),       T("card_browser_sub"),      "Browser"),
            ("🎮", T("nav_gaming"),        T("card_gaming_sub"),        "Gaming"),
            ("💡", T("nav_peripherals"),   T("card_peripherals_sub"),   "Peripherals"),
            ("📁", T("nav_file_transfer"), T("card_filetransfer_sub"),  "File Transfer"),
            ("📄", T("nav_office"),        T("card_office_sub"),        "Office"),
            ("🎬", T("nav_media"),         T("card_media_sub"),         "Media"),
            ("💬", T("nav_comms"),         T("card_comms_sub"),         "Comms"),
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

        for _ci, _cd in enumerate(cards_data):
            icon, t, d = _cd[0], _cd[1], _cd[2]
            _ceng = _cd[3] if len(_cd) > 3 else t
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

            def _nav(gesture, n, x, y, page=_ceng):
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

        box.append(_section_label(T("browser_section")))
        box.append(_sep())

        group = _boxed_list()
        self._br_rows = []

        for br in BROWSERS:
            arow = AnimatedRow(accent=ACCENT2_COLOR, is_pill=True)
            arow.row.set_title(br["name"])
            arow.row.set_subtitle(TD(br["pkg"]) or br["desc"])

            pfx = Gtk.Label(label=br["icon"])
            pfx.add_css_class("title-2"); pfx.add_css_class("row-icon")
            pfx.set_valign(Gtk.Align.CENTER)
            arow.row.add_prefix(pfx)

            if br.get("recommended"):
                rec = Gtk.Label(label=T("recommended"))
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
            box.append(_section_label(TS(sec["section"])))
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
        box.append(_section_label(TS("Creative Tools")))
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

        box.append(_section_label(TS("Base")))
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

        box.append(_section_label(T("lo_lang_section")))
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
        arow.row.set_subtitle(TD(pkg["pkg"]) or pkg.get("desc", ""))
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
        arow.row.set_title(TN(sub["pkg"]) or sub["name"])
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
        self._log_desc.append(_section_label(T("log_what_title")))
        self._log_desc.append(_sep())

        desc_lines = [
            ("🌐", T("log_row_browser_t"), T("log_row_browser_b")),
            ("🎮", T("log_row_gaming_t"),  T("log_row_gaming_b")),
            ("💡", T("log_row_periph_t"),  T("log_row_periph_b")),
            ("📄", T("log_row_office_t"),  T("log_row_office_b")),
            ("🎬", T("log_row_media_t"),   T("log_row_media_b")),
            ("📁", T("log_row_ft_t"),      T("log_row_ft_b")),
            ("💬", T("log_row_comms_t"),   T("log_row_comms_b")),
            ("🔧", T("log_row_how_t"),      T("log_row_how_b")),
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
        self._log_append("  " + T("log_header"), "header")
        self._log_append("╚══════════════════════════════════════════════╝", "header")
        self._log_append("", "raw")
        if repo_pkgs:
            self._log_append(T('log_repo_line', n=len(repo_pkgs), pkgs=', '.join(repo_pkgs)), 'repo')
        if aur_pkgs:
            self._log_append(T('log_aur_line', n=len(aur_pkgs), pkgs=', '.join(aur_pkgs)), 'aur')
        if self.browser:
            self._log_append(T('log_browser_patch', exec=self.browser['exec']), 'patch')
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
                self._log_append(T("log_error", exc=exc), "raw")

        if repo_pkgs:
            self._log_append(T('log_banner_pacman', n=len(repo_pkgs)), 'header')
            ui(T('prog_repo', n=len(repo_pkgs)))
            stream(["sudo","pacman","-S","--noconfirm","--needed","--color=never"] + repo_pkgs, "repo")
            done[0] += len(repo_pkgs)

        for pkg in aur_pkgs:
            self._log_append(T('log_banner_paru', pkg=pkg), 'header')
            ui(T('prog_pkg', pkg=pkg))
            stream(["paru","-S","--noconfirm","--needed","--color=never", pkg], "aur")
            done[0] += 1

        if self.browser:
            self._log_append(T('log_banner_hypr'), 'header')
            ui(T('prog_patch', exec=self.browser['exec']))
            if os.path.exists(HYPRLAND_CONF):
                subprocess.run(["sed","-i",
                    f"s|^\\$Browser = .*|\\$Browser = {self.browser['exec']}|",
                    HYPRLAND_CONF])
            self._log_append(T('log_browser_set', exec=self.browser['exec']), 'patch')
            done[0] += 1

        self._log_append("", "raw")
        self._log_append(T("log_done"), "done")
        ui(T("log_done_bar"), 1.0)
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
