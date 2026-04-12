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

        # Colors
        self.bg_color       = "#f5f4f0"
        self.sidebar_color  = "#1e3a0e"
        self.sidebar_hover  = "#254614"
        self.accent_color   = "#254614"
        self.accent_fg      = "#a3d97a"
        self.text_color     = "#1a1a1a"
        self.muted_color    = "#6b7280"
        self.border_color   = "#e5e5e3"
        self.card_bg        = "#ffffff"
        self.row_hover      = "#f0f0ec"

        self.root.configure(bg=self.bg_color)
        self.pages = {}
        self._active_nav = None

        self.setup_layout()
        self.show_page("dashboard")

    # ================= LAYOUT =================
    def setup_layout(self):
        # ── Sidebar ──────────────────────────────────────────────────────────
        self.sidebar = tk.Frame(self.root, bg=self.sidebar_color, width=220)
        self.sidebar.pack(side=tk.LEFT, fill=tk.Y)
        self.sidebar.pack_propagate(False)

        # Brand
        brand_frame = tk.Frame(self.sidebar, bg=self.sidebar_color)
        brand_frame.pack(fill=tk.X, padx=18, pady=(22, 14))

        icon_frame = tk.Frame(brand_frame, bg="#2d4d1a", width=34, height=34)
        icon_frame.pack(anchor="w")
        icon_frame.pack_propagate(False)
        tk.Label(icon_frame, text="⬡", font=("Segoe UI", 14),
                 bg="#2d4d1a", fg=self.accent_fg).place(relx=0.5, rely=0.5, anchor="center")

        tk.Label(brand_frame, text="BlockChain",
                 font=("Segoe UI", 12, "bold"),
                 bg=self.sidebar_color, fg="#ffffff").pack(anchor="w", pady=(8, 0))
        tk.Label(brand_frame, text="Document Security",
                 font=("Segoe UI", 9),
                 bg=self.sidebar_color, fg="#6b8f4e").pack(anchor="w")

        # Separator
        tk.Frame(self.sidebar, bg="#2a4a18", height=1).pack(fill=tk.X)

        # Nav section label
        tk.Label(self.sidebar, text="MAIN",
                 font=("Segoe UI", 8), bg=self.sidebar_color,
                 fg="#5a7a40").pack(anchor="w", padx=20, pady=(14, 4))

        # Nav buttons
        self.btn_dashboard = self._nav_button(
            "  Dashboard", "📊",
            lambda: self.show_page("dashboard")
        )
        self.btn_verification = self._nav_button(
            "  Verification", "🔍",
            lambda: self.show_page("verification")
        )

        tk.Label(self.sidebar, text="SYSTEM",
                 font=("Segoe UI", 8), bg=self.sidebar_color,
                 fg="#5a7a40").pack(anchor="w", padx=20, pady=(14, 4))

        self._nav_button("  Settings", "⚙", lambda: None)

        # Spacer
        tk.Label(self.sidebar, bg=self.sidebar_color).pack(expand=True)

        # Separator
        tk.Frame(self.sidebar, bg="#2a4a18", height=1).pack(fill=tk.X)

        # User row
        user_frame = tk.Frame(self.sidebar, bg=self.sidebar_color)
        user_frame.pack(fill=tk.X, padx=10, pady=(8, 4))

        avatar = tk.Label(user_frame, text=self.username[:2].upper(),
                          font=("Segoe UI", 9, "bold"),
                          bg="#2d4d1a", fg=self.accent_fg,
                          width=3, height=1)
        avatar.pack(side=tk.LEFT, padx=(6, 8), pady=6)

        tk.Label(user_frame, text=self.username,
                 font=("Segoe UI", 10),
                 bg=self.sidebar_color, fg="#c0d8a8").pack(side=tk.LEFT)

        # Logout
        logout_btn = tk.Button(
            self.sidebar, text="  🚪  Logout",
            font=("Segoe UI", 10), bg=self.sidebar_color,
            fg="#f87171", bd=0, activebackground="#3a1a1a",
            activeforeground="#fca5a5", cursor="hand2",
            command=self.root.quit
        )
        logout_btn.pack(fill=tk.X, padx=10, pady=(0, 12))
        logout_btn.bind("<Enter>", lambda e: logout_btn.config(bg="#3a1a1a"))
        logout_btn.bind("<Leave>", lambda e: logout_btn.config(bg=self.sidebar_color))

        # ── Main container ────────────────────────────────────────────────────
        self.container = tk.Frame(self.root, bg=self.bg_color)
        self.container.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        self.create_dashboard_page()
        self.create_verification_page()

    # ── Nav button helper ──────────────────────────────────────────────────
    def _nav_button(self, text, icon, command):
        frame = tk.Frame(self.sidebar, bg=self.sidebar_color, cursor="hand2")
        frame.pack(fill=tk.X, padx=10, pady=1)

        lbl = tk.Label(frame, text=f"{icon}{text}",
                       font=("Segoe UI", 11),
                       bg=self.sidebar_color, fg="#a8c890",
                       anchor="w", padx=10, pady=8)
        lbl.pack(fill=tk.X)

        def on_click(e=None):
            command()

        def on_enter(e):
            if frame != self._active_nav:
                frame.config(bg=self.sidebar_hover)
                lbl.config(bg=self.sidebar_hover)

        def on_leave(e):
            if frame != self._active_nav:
                frame.config(bg=self.sidebar_color)
                lbl.config(bg=self.sidebar_color)

        frame.bind("<Button-1>", on_click)
        lbl.bind("<Button-1>", on_click)
        frame.bind("<Enter>", on_enter)
        frame.bind("<Leave>", on_leave)
        lbl.bind("<Enter>", on_enter)
        lbl.bind("<Leave>", on_leave)

        return (frame, lbl)

    def _set_active_nav(self, btn_tuple):
        # Reset previous
        if self._active_nav:
            f, l = self._active_nav
            f.config(bg=self.sidebar_color)
            l.config(bg=self.sidebar_color, fg="#a8c890")
        # Set new
        self._active_nav = btn_tuple
        f, l = btn_tuple
        f.config(bg="#2e5018")
        l.config(bg="#2e5018", fg=self.accent_fg)

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

        # ── Top bar ──────────────────────────────────────────────────────────
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
            activebackground="#1a2e0c", activeforeground=self.accent_fg,
            cursor="hand2", command=self.upload_action
        )
        upload_btn.pack(side=tk.RIGHT, padx=(0, 2))

        # ── Stat cards ───────────────────────────────────────────────────────
        stats_row = tk.Frame(page, bg=self.bg_color)
        stats_row.pack(fill=tk.X, pady=(0, 16))

        self._stat_card(stats_row, "Total Files", "–", "#1d4ed8", "#eff6ff")

        # ── Table card ───────────────────────────────────────────────────────
        table_card = tk.Frame(page, bg=self.card_bg,
                              highlightbackground=self.border_color,
                              highlightthickness=1)
        table_card.pack(fill=tk.BOTH, expand=True)

        # Table header row
        header_row = tk.Frame(table_card, bg="#f9f9f7")
        header_row.pack(fill=tk.X)
        tk.Frame(table_card, bg=self.border_color, height=1).pack(fill=tk.X)

        for col, width in [("File Name", 22), ("Upload Date", 14),
                           ("Blockchain Status", 16), ("SHA-256 Fingerprint", 35)]:
            tk.Label(header_row, text=col.upper(),
                     font=("Segoe UI", 8, "bold"),
                     bg="#f9f9f7", fg=self.muted_color,
                     width=width, anchor="w",
                     padx=10, pady=8).pack(side=tk.LEFT)

        # Treeview
        style = ttk.Style()
        style.theme_use("default")
        style.configure("Custom.Treeview",
                        background=self.card_bg,
                        foreground=self.text_color,
                        fieldbackground=self.card_bg,
                        rowheight=36,
                        borderwidth=0,
                        font=("Segoe UI", 10))
        style.configure("Custom.Treeview.Heading",
                        background="#f9f9f7",
                        foreground=self.muted_color,
                        font=("Segoe UI", 8, "bold"),
                        borderwidth=0)
        style.map("Custom.Treeview",
                  background=[("selected", "#e8f4d4")],
                  foreground=[("selected", self.text_color)])
        style.layout("Custom.Treeview", [
            ("Custom.Treeview.treearea", {"sticky": "nswe"})
        ])

        tree_frame = tk.Frame(table_card, bg=self.card_bg)
        tree_frame.pack(fill=tk.BOTH, expand=True)

        scrollbar = ttk.Scrollbar(tree_frame, orient="vertical")
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        self.tree = ttk.Treeview(
            tree_frame,
            columns=("name", "date", "status", "hash", "path"),
            show="headings",
            style="Custom.Treeview",
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

        self.tree.tag_configure("active",   background="#f0fdf4", foreground="#166534")
        self.tree.tag_configure("revoked",  background="#fef2f2", foreground="#991b1b")
        self.tree.tag_configure("archived", background="#f9fafb", foreground="#6b7280")
        self.tree.tag_configure("odd",      background=self.card_bg)
        self.tree.tag_configure("even",     background="#fafaf8")

        self.tree.bind("<Button-3>",  self.show_context_menu)
        self.tree.bind("<Double-1>",  self.open_selected_file)

    def _stat_card(self, parent, label, value, fg, bg):
        card = tk.Frame(parent, bg=bg,
                        highlightbackground="#e0e7ff",
                        highlightthickness=1)
        card.pack(side=tk.LEFT, padx=(0, 12), ipadx=16, ipady=10)

        tk.Label(card, text=label,
                 font=("Segoe UI", 9), bg=bg,
                 fg=self.muted_color).pack(anchor="w", padx=14, pady=(10, 2))

        val_lbl = tk.Label(card, text=value,
                           font=("Segoe UI", 22, "bold"),
                           bg=bg, fg=fg)
        val_lbl.pack(anchor="w", padx=14, pady=(0, 10))

        if label == "Total Files":
            self._total_files_label = val_lbl

        return card

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

        if hasattr(self, "_total_files_label"):
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
                           bg=self.card_bg, fg=self.text_color,
                           activebackground="#e8f4d4",
                           activeforeground=self.text_color,
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
        topbar = tk.Frame(page, bg=self.bg_color)
        topbar.pack(fill=tk.X, pady=(0, 24))

        tk.Label(topbar, text="Document Verification",
                 font=("Segoe UI", 18, "bold"),
                 bg=self.bg_color, fg=self.text_color).pack(anchor="w")
        tk.Label(topbar, text="Check if a file exists and is valid on the blockchain",
                 font=("Segoe UI", 10),
                 bg=self.bg_color, fg=self.muted_color).pack(anchor="w", pady=(2, 0))

        # Center card
        outer = tk.Frame(page, bg=self.bg_color)
        outer.pack(fill=tk.BOTH, expand=True)

        card = tk.Frame(outer, bg=self.card_bg,
                        highlightbackground=self.border_color,
                        highlightthickness=1)
        card.place(relx=0.5, rely=0.35, anchor="center", width=440)

        inner = tk.Frame(card, bg=self.card_bg)
        inner.pack(padx=36, pady=32)

        # Icon box
        icon_box = tk.Frame(inner, bg="#f3f4f6",
                            highlightbackground=self.border_color,
                            highlightthickness=1,
                            width=56, height=56)
        icon_box.pack(pady=(0, 16))
        icon_box.pack_propagate(False)
        tk.Label(icon_box, text="📄",
                 font=("Segoe UI", 22),
                 bg="#f3f4f6").place(relx=0.5, rely=0.5, anchor="center")

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
            activebackground="#1a2e0c",
            cursor="hand2",
            command=self.verify_action
        )
        choose_btn.pack()

        # Result label (hidden by default)
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
            self.result_label.config(
                text="✅  Match found on blockchain",
                bg="#f0fdf4", fg="#166534"
            )
            self.result_sub.config(
                text="File is authentic and unmodified",
                bg="#f0fdf4", fg="#4ade80"
            )
            self.result_frame.config(bg="#f0fdf4",
                                     highlightbackground="#bbf7d0",
                                     highlightthickness=1)
        else:
            self.result_label.config(
                text="❌  Not found in blockchain",
                bg="#fef2f2", fg="#991b1b"
            )
            self.result_sub.config(
                text="File may be altered or unsigned",
                bg="#fef2f2", fg="#f87171"
            )
            self.result_frame.config(bg="#fef2f2",
                                     highlightbackground="#fecaca",
                                     highlightthickness=1)

        self.result_label.pack(fill=tk.X)
        self.result_sub.pack(fill=tk.X, pady=(0, 6))


# ================= RUN =================
if __name__ == "__main__":
    root = tk.Tk()
    app = MainDashboard(root)
    root.mainloop()