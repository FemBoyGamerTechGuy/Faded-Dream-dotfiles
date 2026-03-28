#!/usr/bin/env python3
# faded-dream-setup.py — Faded Dream First Run Setup (GTK4 + libadwaita)
# Lives in ~/Faded-Dream-dotfiles/faded-dream-setup.py
# Launched via exec-once in hyprland.conf on first login.
# dep: sudo pacman -S python-gobject gtk4 libadwaita
# Easter egg: type KOCMOC
#
# Imports:
#   i18n.py      — translations, T(), TD(), TN(), TS()
#   packages.py  — package lists, AUR_MAP, HYPRLAND_CONF
#   widgets.py   — CSS, Cairo widgets, AnimatedRow, MoonHero

import sys, os, subprocess, threading, shutil

# ── Filter C-level Adwaita warnings ──────────────────────────────────
# GLib writes directly to fd 2 bypassing Python sys.stderr.
# Spawn a grep -v filter on fd 2 before gi/GTK loads.
def _filter_stderr():
    r, w = os.pipe()
    pid = os.fork()
    if pid == 0:  # child: filter process
        os.close(w)
        with os.fdopen(r, "rb", 0) as inp, \
             os.fdopen(os.dup(2), "wb", 0) as out:
            SUPPRESS = [
                b"gtk-application-prefer-dark-theme",
                b"GtkGizmo",
                b"reported min width",
                b"reported min height",
                b"pango_font_map_reload_font",
                b"g_object_ref: assertion",
                b"g_object_unref: assertion",
            ]
            for line in inp:
                if not any(s in line for s in SUPPRESS):
                    out.write(line)
        os._exit(0)
    else:  # parent: redirect stderr to write-end of pipe
        os.close(r)
        os.dup2(w, 2)
        os.close(w)
_filter_stderr()

import gi
gi.require_version("Gtk", "4.0")
gi.require_version("Adw", "1")
from gi.repository import Gtk, Adw, GLib, Gio, Pango, Gdk, GObject

from i18n    import T, TD, TN, TS, set_lang, _LANG

from packages import (BROWSERS, GAMING, FILE_MANAGERS, GITHUB_MAP, LANG_LIST, LO_CODES, TB_CODES,
                      OFFICE_BASE, MEDIA, COMMS, PERIPHERALS, FILE_TRANSFER,
                      PRINTING, BROTHER_DRIVERS, detect_init,
                      REPO_STYLE, AUR_MAP, HYPRLAND_CONF, EXEC_LINE,
                      ACCENT_COLOR, ACCENT2_COLOR)
from widgets  import (APP_CSS, _inject_css, _repo_badge, _faded_dream_badge, _section_label,
                      _sep, _scrolled, _boxed_list,
                      CheckMarkWidget, ShimmerWidget, GlowOverlay,
                      AnimatedRow, MoonHero)

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
            ("🗂️", T("nav_file_manager"), self._page_sections(FILE_MANAGERS),         "File Manager"),
            ("🖨️", T("nav_printing"),     self._page_sections(PRINTING),             "Printing"),
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
        for i in range(11):
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

        strings = Gtk.StringList()
        active_idx = 0
        for i, (code, label) in enumerate(_LANG_OPTIONS):
            strings.append(label)
            if code == _LANG:
                active_idx = i

        combo = Gtk.DropDown()
        combo.set_model(strings)
        combo.set_selected(active_idx)
        combo.set_hexpand(True)
        # Force app stylesheet so it doesn't inherit system GTK theme
        combo.add_css_class("flat")
        combo.add_css_class("lang-combo")

        def _on_lang_change(dd, _param):
            idx = dd.get_selected()
            code = _LANG_OPTIONS[idx][0]
            if code == _LANG:
                return
            try:
                cfg = os.path.expanduser("~/.config/faded-dream-lang")
                with open(cfg, "w") as _f:
                    _f.write(code)
                    _f.flush()
                    os.fsync(_f.fileno())
            except Exception:
                pass
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
            ("Printing", PRINTING),
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

        # File Manager
        n = 0
        for sec in FILE_MANAGERS:
            for pkg in sec["packages"]:
                if pkg["pkg"] in self.selected:
                    n += 1
                for sub in pkg.get("sub", []):
                    if sub["pkg"] in self.selected:
                        n += 1
        counts["File Manager"] = n

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
            ("🗂️", T("nav_file_manager"),  T("card_filemanager_sub"),   "File Manager"),
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
                # Brother dialog sentinel — clicking opens dedicated driver window
                if pkg.get("brother_dialog"):
                    arow, cm = self._make_pkg_row(pkg)
                    sfx = Gtk.Image.new_from_icon_name("go-next-symbolic")
                    sfx.set_valign(Gtk.Align.CENTER)
                    arow.row.add_suffix(sfx)
                    gc = Gtk.GestureClick()
                    gc.connect("released", self._open_brother_dialog)
                    arow.add_controller(gc)
                    group.append(arow)
                    continue
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
    def _open_brother_dialog(self, *_):
        """Open the Brother printer driver picker dialog with search."""
        dialog = Adw.Dialog()
        dialog.set_title("Brother Printer Drivers")
        dialog.set_content_width(520)
        dialog.set_content_height(520)

        tb = Adw.ToolbarView()
        header = Adw.HeaderBar()
        search_entry = Gtk.SearchEntry()
        search_entry.set_placeholder_text("Search model…")
        search_entry.set_hexpand(True)
        header.set_title_widget(search_entry)
        tb.add_top_bar(header)

        outer = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=0)
        outer.set_margin_top(12); outer.set_margin_bottom(12)
        outer.set_margin_start(12); outer.set_margin_end(12)

        def _build_list(query=""):
            while True:
                child = outer.get_first_child()
                if child is None: break
                outer.remove(child)
            q = query.lower().strip()
            filtered = [d for d in BROTHER_DRIVERS
                        if q in d["pkg"].lower() or q in d["name"].lower()]
            if not filtered:
                lbl = Gtk.Label(label="No models match your search")
                lbl.add_css_class("dim-label")
                lbl.set_margin_top(24)
                outer.append(lbl)
                return
            group = _boxed_list()
            for drv in filtered:
                arow, cm = self._make_pkg_row(drv)
                group.append(arow)
                if drv["pkg"] in self.selected:
                    arow.set_selected(True); cm.set_checked(True)
                def _bind(a, c_, p):
                    def _clicked(gesture, n, x, y):
                        sel = p not in self.selected
                        if sel: self.selected.add(p);    a.set_selected(True);  c_.set_checked(True)
                        else:   self.selected.discard(p); a.set_selected(False); c_.set_checked(False)
                        self._update_count()
                    gc = Gtk.GestureClick()
                    gc.connect("released", _clicked)
                    a.add_controller(gc)
                _bind(arow, cm, drv["pkg"])
            outer.append(group)

        _build_list()
        search_entry.connect("search-changed", lambda e: _build_list(e.get_text()))
        tb.set_content(_scrolled(outer))
        dialog.set_child(tb)
        dialog.present(self)

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
        if pkg.get("repo") == "github":
            arow.row.add_suffix(_faded_dream_badge())
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
            ("🗂️", T("log_row_fm_t"),      T("log_row_fm_b")),
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

        all_pkgs    = ([self.browser["pkg"]] if self.browser else []) + [p for p in self.selected if not p.startswith("__")]
        repo_pkgs   = [p for p in all_pkgs if not AUR_MAP.get(p, False) and p not in GITHUB_MAP]
        aur_pkgs    = [p for p in all_pkgs if     AUR_MAP.get(p, False)]
        github_pkgs = [p for p in all_pkgs if p in GITHUB_MAP]

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

        threading.Thread(target=self._install_thread, args=(repo_pkgs, aur_pkgs, github_pkgs), daemon=True).start()

    def _install_thread(self, repo_pkgs, aur_pkgs, github_pkgs=None):
        github_pkgs = github_pkgs or []
        total = max(len(repo_pkgs) + len(aur_pkgs) + len(github_pkgs) + (1 if self.browser else 0), 1)
        done  = [0]

        def ui(msg, frac=None):
            f = frac if frac is not None else done[0] / total
            GLib.idle_add(self._prog_bar.set_fraction, f)
            GLib.idle_add(self._prog_bar.set_text, msg)

        def stream(cmd, kind="raw", cwd=None):
            try:
                proc = subprocess.Popen(cmd, stdout=subprocess.PIPE,
                                        stderr=subprocess.STDOUT, text=True, bufsize=1,
                                        cwd=cwd)
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

        for pkg in github_pkgs:
            info = GITHUB_MAP[pkg]
            self._log_append(f"── GitHub: {pkg} ──", "header")
            ui(f"Cloning {pkg}...")
            clone_dst = info.get("post_cwd", f"/tmp/{pkg}-install").rsplit("/", 1)[0]
            if os.path.exists(clone_dst):
                shutil.rmtree(clone_dst)
            stream(info["install_cmd"], "repo")
            self._log_append(f"Running makepkg for {pkg}...", "header")
            ui(f"Building {pkg}...")
            stream(info["post_cmd"] + ["--noconfirm"], "aur",
                   cwd=info.get("post_cwd"))
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

        # Patch $fileManager in hyprland.conf if a file manager was selected
        _FM_EXEC = {
            "nautilus":      "nautilus",
            "nemo":          "nemo",
            "thunar":        "thunar",
            "dolphin":       "dolphin",
            "pcmanfm":       "pcmanfm",
            "caja":          "caja",
            "krusader":      "krusader",
            "doublecmd-qt6": "doublecmd",
            "sunflower":     "sunflower",
            "voiddream":     "kitty --hold VoidDream",
            "yazi":          "kitty --hold yazi",
            "lf":            "kitty --hold lf",
            "ranger":        "kitty --hold ranger",
            "nnn":           "kitty --hold nnn",
            "mc":            "kitty --hold mc",
            "broot":         "kitty --hold broot",
            "vifm":          "kitty --hold vifm",
            "superfile":     "kitty --hold superfile",
        }
        selected_fm = next(
            (pkg for pkg in all_pkgs if pkg in _FM_EXEC),
            None
        )
        if selected_fm and os.path.exists(HYPRLAND_CONF):
            fm_exec = _FM_EXEC[selected_fm]
            subprocess.run(["sed", "-i",
                f"s|^[$]fileManager = .*|[$]fileManager = {fm_exec}|",
                HYPRLAND_CONF])
            self._log_append(f"── Patched $fileManager = {fm_exec}", "patch")

        # ── Start CUPS service if installed ──────────────────────────────────
        cups_installed = any(p.startswith("cups") for p in (repo_pkgs + aur_pkgs))
        if cups_installed:
            init = detect_init()
            self._log_append("── Starting CUPS service ──", "header")
            if init == "runit":
                subprocess.run(["sudo", "ln", "-sf", "/etc/runit/sv/cupsd", "/run/runit/service/"], check=False)
                subprocess.run(["sudo", "sv", "up", "cupsd"], check=False)
                self._log_append("CUPS enabled via runit (sv up cupsd)", "patch")
            elif init == "openrc":
                subprocess.run(["sudo", "rc-update", "add", "cupsd", "default"], check=False)
                subprocess.run(["sudo", "rc-service", "cupsd", "start"], check=False)
                self._log_append("CUPS enabled via OpenRC", "patch")
            elif init == "systemd":
                subprocess.run(["sudo", "systemctl", "enable", "--now", "cups"], check=False)
                self._log_append("CUPS enabled via systemd", "patch")
            else:
                self._log_append("Unknown init — start CUPS manually", "patch")

        self._log_append("", "raw")
        self._log_append(T("log_done"), "done")
        ui(T("log_done_bar"), 1.0)
        GLib.idle_add(self._on_install_done)

    def _on_install_done(self):
        return False


# ── Entry ─────────────────────────────────────────────────────────────────────
if __name__ == "__main__":
    app = SetupApp()
    sys.exit(app.run(sys.argv))
