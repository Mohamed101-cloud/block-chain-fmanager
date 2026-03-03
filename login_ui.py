import tkinter as tk
from tkinter import messagebox
from manager_db import DatabaseManager
from File_Manager_ui import MainDashboard

class Login_ui:
    def __init__(self, root):
        self.db = DatabaseManager()
        self.root = root
        self.root.title("Mohamed Sattar Saeed")
        self.root.geometry("900x700")
        self.root.minsize(500, 650)
        self.root.resizable(True, True)
        
        self.bg_color = "#31654e"
        self.card_color = "#fdfbf7"
        self.accent_color = "#8b7355"
        self.green_color = "#a8b8a0"
        self.text_color = "#4a4238"
        self.input_bg = "#fef9f3"
        
        self.root.configure(bg=self.bg_color)

        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)
        
        self.center_frame = tk.Frame(self.root, bg=self.bg_color)
        self.center_frame.grid(row=0, column=0, sticky="nsew")
        
        self.create_card()

    def create_card(self):
        self.card = tk.Frame(self.center_frame, bg=self.card_color, width=450, height=600)
        self.card.place(relx=0.5, rely=0.5, anchor="center")
        self.card.pack_propagate(False)

        self.setup_card_shadow()
        
        content = tk.Frame(self.card, bg=self.card_color)
        content.pack(fill=tk.BOTH, expand=True, padx=40, pady=40)

        welcome_label = tk.Label(
            content, text="Welcome", font=("Segoe UI", 28, "bold"),
            bg=self.card_color, fg=self.text_color
        )
        welcome_label.pack()

        tk.Label(
            content, text="Username", font=("Segoe UI", 11, "bold"),
            bg=self.card_color, fg=self.text_color
        ).pack(anchor=tk.W, pady=10)

        self.username_entry = tk.Entry(
            content, font=("Segoe UI", 12), bg=self.input_bg,
            fg=self.text_color, relief=tk.FLAT, bd=0
        )
        self.username_entry.pack(pady=10, ipady=10, fill=tk.X)
        self.add_border_to_entry(self.username_entry)

        tk.Label(
            content, text="Password", font=("Segoe UI", 11, "bold"),
            bg=self.card_color, fg=self.text_color
        ).pack(anchor=tk.W, pady=10)

        self.password_entry = tk.Entry(
            content, font=("Segoe UI", 12), bg=self.input_bg,
            fg=self.text_color, relief=tk.FLAT, bd=0, show="•"
        )
        self.password_entry.pack(pady=10, ipady=10, fill=tk.X)
        self.add_border_to_entry(self.password_entry)

        self.password_entry.bind("<Return>", lambda e: self.handle_login())

        self.login_btn = tk.Button(
            content, text="Sign In", font=("Segoe UI", 12, "bold"),
            bg=self.green_color, fg="white", relief=tk.FLAT,
            cursor="hand2", command=self.handle_login
        )
        self.login_btn.pack(pady=10, ipady=12, fill=tk.X)

    def add_border_to_entry(self, entry):
        entry.configure(highlightthickness=1, highlightbackground="#e8dfd5", highlightcolor=self.green_color)
    
    def setup_card_shadow(self):
        shadow = tk.Frame(self.card, bg="#e8dfd5", height=1)
        shadow.pack(side=tk.BOTTOM, fill=tk.X)

    # --- الدالة المفقودة التي كانت تسبب الخطأ ---
    def clear_screen(self):
        for widget in self.root.winfo_children():
            widget.destroy()

    def handle_login(self):
        user = self.username_entry.get().strip()
        pwd = self.password_entry.get().strip()
        
        if not user or not pwd:
            messagebox.showwarning("Incomplete", "Please fill in all fields")
            return

        role = self.db.check_login(user, pwd)
        
        if role == "admin":
            self.clear_screen() 
            MainDashboard(self.root, username=user)
        elif role == "employee":
            # إذا كنت تريد للموظف أيضاً فتح الـ Dashboard، طبق نفس كود الـ admin هنا
            self.clear_screen()
            MainDashboard(self.root, username=user)
        else:
            messagebox.showerror("Error", "بيانات الدخول خاطئة")

if __name__ == "__main__":
    root = tk.Tk()
    app = Login_ui(root)
    root.mainloop()