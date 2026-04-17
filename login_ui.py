import tkinter as tk
from tkinter import messagebox
from manager_db import DatabaseManager
from File_Manager_ui import MainDashboard
try:
    from PIL import Image, ImageTk
    PIL_AVAILABLE = True
except ImportError:
    PIL_AVAILABLE = False
class LoginUI:
    def __init__(self, root: tk.Tk):
        self.db   = DatabaseManager()
        self.root = root

        self.root.title("Blockchain Document Security — Login")
        self.root.geometry("900x720")
        self.root.minsize(500, 680)
        self.root.resizable(True, True)

        # ── Dark Olive Palette ────────────────────────────────────────────────
        self.bg_color     = "#2b3a1e"   # dark olive background
        self.card_color   = "#f5f2ec"   # warm off-white card
        self.green_color  = "#4a6b30"   # olive green button
        self.green_hover  = "#3a5222"   # darker olive on hover
        self.text_color   = "#2b2a25"   # near-black text
        self.sub_color    = "#6b6455"   # muted subtitle
        self.input_bg     = "#fdfaf5"   # warm white inputs
        self.border_color = "#c8bfaf"   # soft tan border
        self.accent_fg    = "#a3d97a"   # light olive accent

        self.root.configure(bg=self.bg_color)
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)

        # Pre-load logo
        self._logo_img = self._load_logo()

        self._build_ui()

    # ── Logo loader ───────────────────────────────────────────────────────────
    def _load_logo(self):
        if not PIL_AVAILABLE:
            return None
        try:
            # افتح الصورة مباشرة من المجلد (تأكد أن الملف logo.png موجود بجانب الكود)
            img = Image.open("logo.png").convert("RGBA") 
            datas = img.getdata()
            newData = []
            for item in datas:
                # إذا كان اللون قريباً من الأبيض (255, 255, 255)
                if item[0] > 240 and item[1] > 240 and item[2] > 240:
                    # استبدله بلون البطاقة (245, 242, 236) الذي هو #f5f2ec
                    newData.append((245, 242, 236, 255))
                else:
                    newData.append(item)
            img.putdata(newData)
            img = img.resize((150,150), Image.LANCZOS)   
            return ImageTk.PhotoImage(img)
        except Exception as e:
            print(f"Error: {e}") # سيطبع الخطأ في التيرمينال إذا لم يجد الصورة
            return None
           

    # ── Build UI ──────────────────────────────────────────────────────────────
    def _build_ui(self):
        center = tk.Frame(self.root, bg=self.bg_color)
        center.grid(row=0, column=0, sticky="nsew")

        card_height = 620 if self._logo_img else 570
        card = tk.Frame(center, bg=self.card_color, width=460, height=card_height)
        card.place(relx=0.5, rely=0.5, anchor="center")
        card.pack_propagate(False)

        # Thin olive accent strip at top of card
        tk.Frame(card, bg=self.green_color, height=4).pack(side=tk.TOP, fill=tk.X)
        # Shadow strip at bottom
        tk.Frame(card, bg="#d8cfc0", height=1).pack(side=tk.BOTTOM, fill=tk.X)

        content = tk.Frame(card, bg=self.card_color)
        content.pack(fill=tk.BOTH, expand=True, padx=44, pady=(28, 36))

        # ── University Logo ───────────────────────────────────────────────────
        if self._logo_img:
            logo_lbl = tk.Label(content, image=self._logo_img,
                                bg=self.card_color)
            logo_lbl.pack(pady=(0, 10))
        else:
            # Fallback: hex icon box
            icon_frame = tk.Frame(content, bg="#2b3a1e", width=60, height=60)
            icon_frame.pack(pady=(0, 10))
            icon_frame.pack_propagate(False)
            tk.Label(icon_frame, text="⬡", font=("Segoe UI", 24),
                     bg="#2b3a1e", fg=self.accent_fg).place(relx=0.5, rely=0.5, anchor="center")

        # ── Titles ────────────────────────────────────────────────────────────
        tk.Label(content, text="University of Kufa",
                 font=("Segoe UI", 11, "bold"),
                 bg=self.card_color, fg=self.green_color).pack()

        tk.Label(content, text="Welcome To The System",
                 font=("Segoe UI", 22, "bold"),
                 bg=self.card_color, fg=self.text_color).pack(pady=(4, 0))

        tk.Label(content, text="Sign in to Blockchain Document Security",
                 font=("Segoe UI", 10),
                 bg=self.card_color, fg=self.sub_color).pack(pady=(2, 20))

        # ── Divider ───────────────────────────────────────────────────────────
        tk.Frame(content, bg=self.border_color, height=1).pack(fill=tk.X, pady=(0, 18))

        # ── Username field ────────────────────────────────────────────────────
        tk.Label(content, text="Username",
                 font=("Segoe UI", 10, "bold"),
                 bg=self.card_color, fg=self.text_color).pack(anchor=tk.W)

        self.username_entry = tk.Entry(
            content, font=("Segoe UI", 12),
            bg=self.input_bg, fg=self.text_color,
            relief=tk.FLAT, bd=0,
            highlightthickness=1,
            highlightbackground=self.border_color,
            highlightcolor=self.green_color
        )
        self.username_entry.pack(pady=(5, 14), ipady=9, fill=tk.X)

        # ── Password field ────────────────────────────────────────────────────
        tk.Label(content, text="Password",
                 font=("Segoe UI", 10, "bold"),
                 bg=self.card_color, fg=self.text_color).pack(anchor=tk.W)

        self.password_entry = tk.Entry(
            content, font=("Segoe UI", 12),
            bg=self.input_bg, fg=self.text_color,
            relief=tk.FLAT, bd=0, show="•",
            highlightthickness=1,
            highlightbackground=self.border_color,
            highlightcolor=self.green_color
        )
        self.password_entry.pack(pady=(5, 18), ipady=9, fill=tk.X)
        self.password_entry.bind("<Return>", lambda _e: self._handle_login())

        # ── Error label (hidden initially) ────────────────────────────────────
        self.error_label = tk.Label(
            content, text="",
            font=("Segoe UI", 9),
            bg=self.card_color, fg="#b03030"
        )
        self.error_label.pack()

        # ── Sign-in button ────────────────────────────────────────────────────
        btn = tk.Button(
            content, text="Sign In",
            font=("Segoe UI", 11, "bold"),
            bg=self.green_color, fg="white",
            relief=tk.FLAT, cursor="hand2",
            command=self._handle_login
        )
        btn.pack(pady=(8, 0), ipady=11, fill=tk.X)
        btn.bind("<Enter>", lambda _e: btn.config(bg=self.green_hover))
        btn.bind("<Leave>", lambda _e: btn.config(bg=self.green_color))

    # ── Login logic ───────────────────────────────────────────────────────────
    def _handle_login(self):
        user = self.username_entry.get().strip()
        pwd  = self.password_entry.get().strip()

        if not user or not pwd:
            self.error_label.config(text="⚠  Please fill in all fields.")
            return

        role = self.db.check_login(user, pwd)

        if role in ("admin", "employee"):
            self._clear_screen()
            MainDashboard(self.root, username=user)
        else:
            self.error_label.config(text="✗  Incorrect username or password.")
            self.password_entry.delete(0, tk.END)

    def _clear_screen(self):
        for widget in self.root.winfo_children():
            widget.destroy()


# ── Entry point ───────────────────────────────────────────────────────────────
if __name__ == "__main__":
    root = tk.Tk()
    LoginUI(root)
    root.mainloop()