import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import os
import sys
import subprocess
from datetime import datetime
from file import FileProcessor
class MainDashboard:
    def __init__(self, root, username="Mohamed Sattar"):
        self.root = root
        self.username = username

        self.root.title(f"Welcome {username} - Blockchain System")
        self.root.geometry("1200x700")
        self.root.minsize(1000, 600)

        # تهيئة المحرك الأساسي
        self.engine = FileProcessor()

        # ── الألوان (Dark Mode) ──────────────────────────────────────────
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

    def setup_layout(self):
        # ── القائمة الجانبية (Sidebar) ───────────────────────────────────────
        self.sidebar = tk.Frame(self.root, bg=self.sidebar_color, width=220)
        self.sidebar.pack(side=tk.LEFT, fill=tk.Y)
        self.sidebar.pack_propagate(False)

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

        tk.Label(self.sidebar, text="MAIN",
                 font=("Segoe UI", 8), bg=self.sidebar_color,
                 fg="#3a5a20").pack(anchor="w", padx=20, pady=(14, 4))

        self.btn_dashboard = self._nav_button("  Dashboard", "📊", lambda: self.show_page("dashboard"))
        self.btn_verification = self._nav_button("  Verification", "🔍", lambda: self.show_page("verification"))

        tk.Label(self.sidebar, bg=self.sidebar_color).pack(expand=True)

        # معلومات المستخدم في الأسفل
        user_row = tk.Frame(self.sidebar, bg=self.sidebar_color)
        user_row.pack(fill=tk.X, padx=10, pady=(8, 12))

        tk.Label(user_row, text=self.username[:2].upper(),
                 font=("Segoe UI", 9, "bold"), bg="#1e3a0e", fg=self.accent_fg,
                 width=3, height=1).pack(side=tk.LEFT, padx=(6, 8))

        tk.Label(user_row, text=self.username,
                 font=("Segoe UI", 10), bg=self.sidebar_color, fg=self.nav_text).pack(side=tk.LEFT)

        # ── الحاوية الرئيسية (Main Container) ───────────────────────────────
        self.container = tk.Frame(self.root, bg=self.bg_color)
        self.container.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        self.create_dashboard_page()
        self.create_verification_page()

    def _nav_button(self, text, icon, command):
        frame = tk.Frame(self.sidebar, bg=self.sidebar_color, cursor="hand2")
        frame.pack(fill=tk.X, padx=10, pady=1)
        lbl = tk.Label(frame, text=f"{icon}{text}", font=("Segoe UI", 11),
                       bg=self.sidebar_color, fg=self.nav_text, anchor="w", padx=10, pady=8)
        lbl.pack(fill=tk.X)
        for w in (frame, lbl):
            w.bind("<Button-1>", lambda e: command())
        return (frame, lbl)

    def _set_active_nav(self, btn_tuple):
        if self._active_nav:
            self._active_nav[0].config(bg=self.sidebar_color)
            self._active_nav[1].config(bg=self.sidebar_color, fg=self.nav_text)
        self._active_nav = btn_tuple
        btn_tuple[0].config(bg="#1e3a0e")
        btn_tuple[1].config(bg="#1e3a0e", fg=self.accent_fg)

    def show_page(self, name):
        for p in self.pages.values(): p.pack_forget()
        self.pages[name].pack(fill=tk.BOTH, expand=True, padx=32, pady=24)
        if name == "dashboard":
            self._set_active_nav(self.btn_dashboard)
            self.refresh_table()
        elif name == "verification":
            self._set_active_nav(self.btn_verification)

    # ================= صفحة الـ DASHBOARD =================
    def create_dashboard_page(self):
        page = tk.Frame(self.container, bg=self.bg_color)
        self.pages["dashboard"] = page

        topbar = tk.Frame(page, bg=self.bg_color)
        topbar.pack(fill=tk.X, pady=(0, 16))

        left = tk.Frame(topbar, bg=self.bg_color)
        left.pack(side=tk.LEFT)
        tk.Label(left, text="Secured Documents", font=("Segoe UI", 18, "bold"),
                 bg=self.bg_color, fg=self.text_color).pack(anchor="w")

        tk.Button(topbar, text="  ↑  Upload & Secure", font=("Segoe UI", 10, "bold"),
                  bg=self.accent_color, fg=self.accent_fg, bd=0, padx=16, pady=8,
                  command=self.upload_action, cursor="hand2").pack(side=tk.RIGHT)

        # جدول عرض الملفات
        table_card = tk.Frame(page, bg=self.card_bg, highlightbackground=self.border_color, highlightthickness=1)
        table_card.pack(fill=tk.BOTH, expand=True)

        style = ttk.Style()
        style.theme_use("clam") # ضروري لتغيير ألوان الرأس والخلفية بالكامل

        style.configure("Dark.Treeview", 
                        background=self.card_bg, 
                        foreground=self.body_color, 
                        fieldbackground=self.card_bg, # هذا يزيل المربع الأبيض
                        rowheight=36, 
                        borderwidth=0,
                        font=("Segoe UI", 10))
        
        style.configure("Dark.Treeview.Heading",
                        background=self.sidebar_color,
                        foreground=self.nav_text,
                        font=("Segoe UI", 9, "bold"),
                        relief="flat")

        # ترتيب الأعمدة: الاسم، التاريخ، CID، والمسار (مخفي)
        self.tree = ttk.Treeview(table_card, columns=("name", "date", "cid", "path"), 
                                 show="headings", style="Dark.Treeview")
        self.tree.heading("name", text="File Name")
        self.tree.heading("date", text="Upload Date")
        self.tree.heading("cid", text="IPFS CID (Blockchain Reference)")
        self.tree.heading("path", text="")
        
        self.tree.column("name", width=200)
        self.tree.column("date", width=150)
        self.tree.column("cid", width=400)
        self.tree.column("path", width=0, stretch=False)
        self.tree.pack(fill=tk.BOTH, expand=True)
        self.tree.bind("<Double-1>", self.open_selected_file)

    def refresh_table(self):
        for i in self.tree.get_children(): self.tree.delete(i)
        # قاعدة البيانات تعيد: (name, path, date, cid)
        rows = self.engine.db.get_all_files()
        for row in rows:
            # ترتيب البيانات للجدول: name(0), date(2), cid(3), path(1)
            self.tree.insert("", "end", values=(row[0], row[2], row[3], row[1]))

    def upload_action(self):
        file_path = filedialog.askopenfilename()
        if file_path:
            success, result = self.engine.process_upload(file_path)
            if success:
                self.refresh_table()
                messagebox.showinfo("Success", result)
            else:
                messagebox.showerror("Error", result)

    def open_selected_file(self, event=None):
        selected = self.tree.selection()
        if not selected: return
        # المسار مخزن في الفهرس رقم 3 في قيم الصف
        file_path = self.tree.item(selected[0])["values"][3]
        if os.path.exists(file_path):
            if sys.platform == "win32": os.startfile(file_path)
            else: subprocess.call(["xdg-open", file_path])

    # ================= صفحة الـ VERIFICATION =================
    def create_verification_page(self):
        page = tk.Frame(self.container, bg=self.bg_color)
        self.pages["verification"] = page

        tk.Label(page, text="Document Verification", font=("Segoe UI", 18, "bold"),
                 bg=self.bg_color, fg=self.text_color).pack(anchor="w")

        card = tk.Frame(page, bg=self.card_bg, highlightbackground=self.border_color, highlightthickness=1)
        card.place(relx=0.5, rely=0.4, anchor="center", width=500)

        inner = tk.Frame(card, bg=self.card_bg)
        inner.pack(padx=40, pady=40)

        tk.Label(inner, text="Verify File Integrity", font=("Segoe UI", 14, "bold"),
                 bg=self.card_bg, fg=self.text_color).pack()
        
        tk.Label(inner, text="System will upload file to IPFS to get CID\nand compare it with Blockchain records.",
                 font=("Segoe UI", 9), bg=self.card_bg, fg=self.muted_color).pack(pady=10)

        tk.Button(inner, text="🔍  Select File to Verify", font=("Segoe UI", 10, "bold"),
                  bg=self.accent_color, fg=self.accent_fg, bd=0, padx=20, pady=10,
                  command=self.verify_action, cursor="hand2").pack(pady=20)

        self.res_label = tk.Label(inner, text="", font=("Segoe UI", 10, "bold"), bg=self.card_bg)
        self.res_label.pack(fill=tk.X)
        self.res_info = tk.Label(inner, text="", font=("Segoe UI", 9), bg=self.card_bg, fg=self.muted_color)
        self.res_info.pack(fill=tk.X)

    def verify_action(self):
        file_path = filedialog.askopenfilename()
        if not file_path: return

        # الاعتماد على CID المستخرج من Pinata للتحقق
        result = self.engine.process_verification(file_path)

        if result.get("is_authentic"):
            ts = result.get('timestamp', 0)
            dt = datetime.fromtimestamp(ts).strftime('%Y-%m-%d %H:%M')
            self.res_label.config(text="✅ Document Verified!", fg="#34d399")
            self.res_info.config(text=f"File Name: {result.get('file_name')}\nUploaded on: {dt}")
        else:
            self.res_label.config(text="❌ Verification Failed", fg="#f87171")
            self.res_info.config(text=result.get("message", "File not found on chain."))

if __name__ == "__main__":
    root = tk.Tk()
    app = MainDashboard(root)
    root.mainloop()