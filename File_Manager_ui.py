import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import os
import sys
import subprocess

from file import FileProcessor


class MainDashboard:
    def __init__(self, root, username="User"):
        self.root = root
        self.username = username

        self.root.title(f"Welcome {username} - Blockchain System")
        self.root.geometry("1200x700")
        self.root.minsize(1000, 600)

        self.engine = FileProcessor()

        # ── Dark mode colors ──────────────────────────────────────────────────
        self.bg_color      = "#141412"
        self.sidebar_color = "#0f1f07"
        self.sidebar_hover = "#1a2e0e"
        self.sidebar_bdr   = "#1e2e10"
        self.accent_color  = "#1e3a0e"
        self.accent_fg     = "#a3d97a"
        self.text_color    = "#e8e8e4"
        self.body_color    = "#c8c8c4"
        self.muted_color   = "#5a5a56"
        self.border_color  = "#242420"
        self.card_bg       = "#1a1a18"
        self.row_hover     = "#1e1e1c"
        self.nav_text      = "#7a9a60"

        self.root.configure(bg=self.bg_color)
        self.pages = {}
        self._active_nav = None

        self.setup_layout()
        self.show_page("dashboard")

    # ================= LAYOUT =================
    def setup_layout(self):

        # ── Sidebar ───────────────────────────────────────────────────────────
        self.sidebar = tk.Frame(self.root, bg=self.sidebar_color, width=220)
        self.sidebar.pack(side=tk.LEFT, fill=tk.Y)
        self.sidebar.pack_propagate(False)

        # Brand
        brand_frame = tk.Frame(self.sidebar, bg=self.sidebar_color)
        brand_frame.pack(fill=tk.X, padx=18, pady=(22, 14))

        icon_box = tk.Frame(brand_frame, bg="#1e3a0e", width=34, height=34)
        icon_box.pack(anchor="w")
        icon_box.pack_propagate(False)
        tk.Label(icon_box, text="⬡", font=("Segoe UI", 14),
                 bg="#1e3a0e", fg=self.accent_fg).place(relx=0.5, rely=0.5, anchor="center")

        tk.Label(brand_frame, text="BlockChain",
                 font=("Segoe UI", 12, "bold"),
                 bg=self.sidebar_color, fg=self.text_color).pack(anchor="w", pady=(8, 0))
        tk.Label(brand_frame, text="Document Security",
                 font=("Segoe UI", 9),
                 bg=self.sidebar_color, fg="#4a6b30").pack(anchor="w")

        tk.Frame(self.sidebar, bg=self.sidebar_bdr, height=1).pack(fill=tk.X)

        # Nav
        tk.Label(self.sidebar, text="MAIN",
                 font=("Segoe UI", 8), bg=self.sidebar_color,
                 fg="#3a5a20").pack(anchor="w", padx=20, pady=(14, 4))

        self.btn_dashboard = self._nav_button(
            "  Dashboard", "📊", lambda: self.show_page("dashboard"))
        self.btn_verification = self._nav_button(
            "  Verification", "🔍", lambda: self.show_page("verification"))

        tk.Label(self.sidebar, text="SYSTEM",
                 font=("Segoe UI", 8), bg=self.sidebar_color,
                 fg="#3a5a20").pack(anchor="w", padx=20, pady=(14, 4))

        self._nav_button("  Settings", "⚙", lambda: None)

        tk.Label(self.sidebar, bg=self.sidebar_color).pack(expand=True)

        tk.Frame(self.sidebar, bg=self.sidebar_bdr, height=1).pack(fill=tk.X)

        # User row
        user_row = tk.Frame(self.sidebar, bg=self.sidebar_color)
        user_row.pack(fill=tk.X, padx=10, pady=(8, 4))

        tk.Label(user_row, text=self.username[:2].upper(),
                 font=("Segoe UI", 9, "bold"),
                 bg="#1e3a0e", fg=self.accent_fg,
                 width=3, height=1).pack(side=tk.LEFT, padx=(6, 8), pady=6)

        tk.Label(user_row, text=self.username,
                 font=("Segoe UI", 10),
                 bg=self.sidebar_color, fg=self.nav_text).pack(side=tk.LEFT)

        logout_btn = tk.Button(
            self.sidebar, text="  🚪  Logout",
            font=("Segoe UI", 10), bg=self.sidebar_color,
            fg="#7a4040", bd=0,
            activebackground="#2a1414", activeforeground="#f87171",
            cursor="hand2", command=self.root.quit
        )
        logout_btn.pack(fill=tk.X, padx=10, pady=(0, 12))
        logout_btn.bind("<Enter>", lambda e: logout_btn.config(bg="#2a1414", fg="#f87171"))
        logout_btn.bind("<Leave>", lambda e: logout_btn.config(bg=self.sidebar_color, fg="#7a4040"))

        # ── Main container ────────────────────────────────────────────────────
        self.container = tk.Frame(self.root, bg=self.bg_color)
        self.container.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        self.create_dashboard_page()
        self.create_verification_page()

    # ── Nav button helper ─────────────────────────────────────────────────────
    def _nav_button(self, text, icon, command):
        frame = tk.Frame(self.sidebar, bg=self.sidebar_color, cursor="hand2")
        frame.pack(fill=tk.X, padx=10, pady=1)

        lbl = tk.Label(frame, text=f"{icon}{text}",
                       font=("Segoe UI", 11),
                       bg=self.sidebar_color, fg=self.nav_text,
                       anchor="w", padx=10, pady=8)
        lbl.pack(fill=tk.X)

        def on_click(e=None): command()
        def on_enter(e):
            if (frame, lbl) != self._active_nav:
                frame.config(bg=self.sidebar_hover)
                lbl.config(bg=self.sidebar_hover)
        def on_leave(e):
            if (frame, lbl) != self._active_nav:
                frame.config(bg=self.sidebar_color)
                lbl.config(bg=self.sidebar_color)

        for w in (frame, lbl):
            w.bind("<Button-1>", on_click)
            w.bind("<Enter>",    on_enter)
            w.bind("<Leave>",    on_leave)

        return (frame, lbl)

    def _set_active_nav(self, btn_tuple):
        if self._active_nav:
            f, l = self._active_nav
            f.config(bg=self.sidebar_color)
            l.config(bg=self.sidebar_color, fg=self.nav_text)
        self._active_nav = btn_tuple
        f, l = btn_tuple
        f.config(bg="#1e3a0e")
        l.config(bg="#1e3a0e", fg=self.accent_fg)

    # ================= PAGE SWITCH =================
    def show_page(self, name):
        for p in self.pages.values():
            p.pack_forget()
        self.pages[name].pack(fill=tk.BOTH, expand=True, padx=32, pady=24)

        if name == "dashboard":
            self._set_active_nav(self.btn_dashboard)
            self.refresh_table()
        elif name == "verification":
            self._set_active_nav(self.btn_verification)

    # ================= DASHBOARD =================
    def create_dashboard_page(self):
        page = tk.Frame(self.container, bg=self.bg_color)
        self.pages["dashboard"] = page

        # Top bar
        topbar = tk.Frame(page, bg=self.bg_color)
        topbar.pack(fill=tk.X, pady=(0, 16))

        left = tk.Frame(topbar, bg=self.bg_color)
        left.pack(side=tk.LEFT)
        tk.Label(left, text="Secured Documents",
                 font=("Segoe UI", 18, "bold"),
                 bg=self.bg_color, fg=self.text_color).pack(anchor="w")
        tk.Label(left, text="All files are hashed and stored on-chain",
                 font=("Segoe UI", 10),
                 bg=self.bg_color, fg=self.muted_color).pack(anchor="w", pady=(2, 0))

        upload_btn = tk.Button(
            topbar, text="  ↑  Upload & Secure",
            font=("Segoe UI", 10, "bold"),
            bg=self.accent_color, fg=self.accent_fg,
            bd=0, padx=16, pady=8,
            activebackground="#152b0a", activeforeground=self.accent_fg,
            cursor="hand2", command=self.upload_action
        )
        upload_btn.pack(side=tk.RIGHT)

        # Stat card — Total Files only
        stats_row = tk.Frame(page, bg=self.bg_color)
        stats_row.pack(fill=tk.X, pady=(0, 16))

        stat = tk.Frame(stats_row, bg=self.card_bg,
                        highlightbackground=self.border_color,
                        highlightthickness=1)
        stat.pack(side=tk.LEFT, ipadx=16, ipady=6)

        tk.Label(stat, text="Total Files",
                 font=("Segoe UI", 9),
                 bg=self.card_bg, fg=self.muted_color).pack(anchor="w", padx=14, pady=(10, 2))

        self._total_files_label = tk.Label(
            stat, text="–",
            font=("Segoe UI", 22, "bold"),
            bg=self.card_bg, fg=self.text_color)
        self._total_files_label.pack(anchor="w", padx=14)
        # Table card
        table_card = tk.Frame(page, bg=self.card_bg,
                              highlightbackground=self.border_color,
                              highlightthickness=1)
        table_card.pack(fill=tk.BOTH, expand=True)

        # Treeview style
        style = ttk.Style()
        style.theme_use("default")
        style.configure("Dark.Treeview",
                        background=self.card_bg,
                        foreground=self.body_color,
                        fieldbackground=self.card_bg,
                        rowheight=36,
                        borderwidth=0,
                        font=("Segoe UI", 10))
        style.configure("Dark.Treeview.Heading",
                        background="#141412",
                        foreground=self.muted_color,
                        font=("Segoe UI", 8, "bold"),
                        relief="flat",
                        borderwidth=0)
        style.map("Dark.Treeview",
                  background=[("selected", "#1e3a0e")],
                  foreground=[("selected", self.accent_fg)])
        style.layout("Dark.Treeview", [
            ("Dark.Treeview.treearea", {"sticky": "nswe"})
        ])

        tree_frame = tk.Frame(table_card, bg=self.card_bg)
        tree_frame.pack(fill=tk.BOTH, expand=True)

        scrollbar = ttk.Scrollbar(tree_frame, orient="vertical")
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        self.tree = ttk.Treeview(
            tree_frame,
            columns=("name", "date", "status", "hash", "path"),
            show="headings",
            style="Dark.Treeview",
            yscrollcommand=scrollbar.set
        )
        scrollbar.config(command=self.tree.yview)

        self.tree.heading("name",   text="File Name")
        self.tree.heading("date",   text="Upload Date")
        self.tree.heading("status", text="Blockchain Status")
        self.tree.heading("hash",   text="SHA-256 Fingerprint")
        self.tree.heading("path",   text="")

        self.tree.column("name",   width=220, anchor="w")
        self.tree.column("date",   width=140, anchor="w")
        self.tree.column("status", width=160, anchor="w")
        self.tree.column("hash",   width=380, anchor="w")
        self.tree.column("path",   width=0, stretch=False)

        self.tree.pack(fill=tk.BOTH, expand=True)

        # Row tags
        self.tree.tag_configure("active",   background="#0e2218", foreground="#34d399")
        self.tree.tag_configure("revoked",  background="#2a1414", foreground="#f87171")
        self.tree.tag_configure("archived", background="#1e1e1c", foreground="#5a5a56")
        self.tree.tag_configure("odd",      background=self.card_bg)
        self.tree.tag_configure("even",     background="#161614")

        self.tree.bind("<Button-3>", self.show_context_menu)
        self.tree.bind("<Double-1>", self.open_selected_file)

    # ================= OPEN FILE =================
    def open_selected_file(self, event=None):
        selected = self.tree.selection()
        if not selected:
            return
        file_path = self.tree.item(selected[0])["values"][4]
        if not os.path.exists(file_path):
            messagebox.showerror("Error", "File not found!")
            return
        try:
            if sys.platform == "win32":
                os.startfile(file_path)
            elif sys.platform == "darwin":
                subprocess.call(["open", file_path])
            else:
                subprocess.call(["xdg-open", file_path])
        except Exception as e:
            messagebox.showerror("Error", str(e))

    # ================= TABLE =================
    def refresh_table(self):
        for i in self.tree.get_children():
            self.tree.delete(i)

        rows = self.engine.db.get_all_files()
        self._total_files_label.config(text=str(len(rows)))

        for idx, row in enumerate(rows):
            bc     = self.engine.blockchain.verify_file(row[3])
            status = bc["status"] if bc else "Not Found"

            tag = "even" if idx % 2 == 0 else "odd"
            s   = status.lower()
            if "active"   in s: tag = "active"
            elif "revoked" in s: tag = "revoked"
            elif "archive" in s: tag = "archived"

            self.tree.insert("", "end", tags=(tag,), values=(
                row[0],   # name
                row[2],   # date
                status,   # blockchain status
                row[3],   # hash
                row[1]    # path
            ))

    # ================= UPLOAD =================
    def upload_action(self):
        file_path = filedialog.askopenfilename()
        if file_path:
            success, result = self.engine.process_upload(file_path)
            if success:
                self.refresh_table()
                messagebox.showinfo("Success", "File secured on Blockchain!")
            else:
                messagebox.showerror("Error", result)

    # ================= CONTEXT MENU =================
    def show_context_menu(self, event):
        item = self.tree.identify_row(event.y)
        if item:
            self.tree.selection_set(item)
            menu = tk.Menu(self.root, tearoff=0,
                           bg="#1e1e1c", fg=self.body_color,
                           activebackground="#1e3a0e",
                           activeforeground=self.accent_fg,
                           font=("Segoe UI", 10))
            menu.add_command(label="✅  Set Active",
                             command=lambda: self.update_status(0))
            menu.add_command(label="🚫  Set Revoked",
                             command=lambda: self.update_status(1))
            menu.add_command(label="📦  Set Archived",
                             command=lambda: self.update_status(2))
            menu.post(event.x_root, event.y_root)

    def update_status(self, status):
        selected = self.tree.selection()[0]
        file_hash = self.tree.item(selected)["values"][3]
        success, tx = self.engine.blockchain.update_file_status(file_hash, status)
        if success:
            messagebox.showinfo("Success", "Blockchain updated!")
            self.refresh_table()
        else:
            messagebox.showerror("Error", tx)

    # ================= VERIFICATION =================
    def create_verification_page(self):
        page = tk.Frame(self.container, bg=self.bg_color)
        self.pages["verification"] = page

        # Top bar
        tk.Label(page, text="Document Verification",
                 font=("Segoe UI", 18, "bold"),
                 bg=self.bg_color, fg=self.text_color).pack(anchor="w")
        tk.Label(page, text="Check if a file exists and is valid on the blockchain",
                 font=("Segoe UI", 10),
                 bg=self.bg_color, fg=self.muted_color).pack(anchor="w", pady=(3, 24))

        # Center card
        outer = tk.Frame(page, bg=self.bg_color)
        outer.pack(fill=tk.BOTH, expand=True)

        card = tk.Frame(outer, bg=self.card_bg,
                        highlightbackground=self.border_color,
                        highlightthickness=1)
        card.place(relx=0.5, rely=0.35, anchor="center", width=440)

        inner = tk.Frame(card, bg=self.card_bg)
        inner.pack(padx=36, pady=32)

        # Icon
        icon_box = tk.Frame(inner, bg="#1e1e1c",
                            highlightbackground=self.border_color,
                            highlightthickness=1,
                            width=56, height=56)
        icon_box.pack(pady=(0, 16))
        icon_box.pack_propagate(False)
        tk.Label(icon_box, text="📄", font=("Segoe UI", 22),
                 bg="#1e1e1c").place(relx=0.5, rely=0.5, anchor="center")

        tk.Label(inner, text="Verify a document",
                 font=("Segoe UI", 14, "bold"),
                 bg=self.card_bg, fg=self.text_color).pack()

        tk.Label(inner,
                 text="Select a file to check its SHA-256 fingerprint\nagainst the blockchain ledger.",
                 font=("Segoe UI", 10), bg=self.card_bg,
                 fg=self.muted_color, justify="center").pack(pady=(6, 20))

        choose_btn = tk.Button(
            inner, text="  ↑  Choose File",
            font=("Segoe UI", 10, "bold"),
            bg=self.accent_color, fg=self.accent_fg,
            bd=0, padx=20, pady=9,
            activebackground="#152b0a",
            cursor="hand2",
            command=self.verify_action
        )
        choose_btn.pack()

        # Result area
        self.result_frame = tk.Frame(inner, bg=self.card_bg)
        self.result_frame.pack(fill=tk.X, pady=(16, 0))

        self.result_label = tk.Label(
            self.result_frame, text="",
            font=("Segoe UI", 11, "bold"),
            bg=self.card_bg, fg=self.text_color,
            pady=10, padx=14
        )
        self.result_sub = tk.Label(
            self.result_frame, text="",
            font=("Segoe UI", 9),
            bg=self.card_bg, fg=self.muted_color,
            pady=4
        )

    def verify_action(self):
        file_path = filedialog.askopenfilename()
        if not file_path:
            return

        file_hash = self.engine.calculate_sha256(file_path)
        result    = self.engine.blockchain.verify_file(file_hash)

        if result:
            self.result_frame.config(bg="#0e2218",
                                     highlightbackground="#1a4a2a",
                                     highlightthickness=1)
            self.result_label.config(text="✅  Match found on blockchain",
                                     bg="#0e2218", fg="#34d399")
            self.result_sub.config(text="File is authentic and unmodified",
                                   bg="#0e2218", fg="#1a8a50")
        else:
            self.result_frame.config(bg="#2a1414",
                                     highlightbackground="#4a1a1a",
                                     highlightthickness=1)
            self.result_label.config(text="❌  Not found in blockchain",
                                     bg="#2a1414", fg="#f87171")
            self.result_sub.config(text="File may be altered or unsigned",
                                   bg="#2a1414", fg="#a04040")

        self.result_label.pack(fill=tk.X)
        self.result_sub.pack(fill=tk.X, pady=(0, 6))


# ================= RUN =================
if __name__ == "__main__":
    root = tk.Tk()
    app = MainDashboard(root)
    root.mainloop()