import tkinter as tk
from tkinter import ttk, filedialog, messagebox

class MainDashboard:
    def __init__(self, root, username="User"):
        self.root = root
        self.root.title("Employee Portal - Dashboard")
        self.root.geometry("1100x700")
        
        # الألوان الزيتونية المتناسقة مع تصميمك
        self.bg_color = "#f5f1eb"  # بيج فاتح (خلفية)
        self.sidebar_color = "#254614"  # زيتوني (شريط جانبي)
        self.accent_color = "#8b7355"  # بني محروق (للنصوص الهامة)
        self.card_color = "#fdfbf7"  # كريمي (للكروت)
        self.text_color = "#4a4238"  # رمادي بني (للنصوص)
        
        self.root.configure(bg=self.bg_color)
        
        self.setup_layout()

    def setup_layout(self):
        # 1. الشريط الجانبي (Sidebar)
        self.sidebar = tk.Frame(self.root, bg=self.sidebar_color, width=250)
        self.sidebar.pack(side=tk.LEFT, fill=tk.Y)
        self.sidebar.pack_propagate(False)

        # شعار أو عنوان فوق الأزرار
        tk.Label(self.sidebar, text="PORTAL", font=("Segoe UI", 20, "bold"), 
                 bg=self.sidebar_color, fg="white", pady=30).pack()

        # أزرار التنقل (Sidebar Buttons)
        buttons = [
            ("My Files", "📁"),
            ("Upload File", "📤"),
            ("Reports", "📊"),
            ("Settings", "⚙️"),
        ]

        for text, icon in buttons:
            btn = tk.Button(self.sidebar, text=f"  {icon}  {text}", font=("Segoe UI", 12),
                            bg=self.sidebar_color, fg="white", bd=0, cursor="hand2",
                            activebackground="#96a88d", activeforeground="white",
                            anchor="w", padx=30, pady=15)
            btn.pack(fill=tk.X)

        # زر تسجيل الخروج في الأسفل
        tk.Button(self.sidebar, text="  🚪  Logout", font=("Segoe UI", 11, "bold"),
                  bg="#96a88d", fg="white", bd=0, command=self.root.quit).pack(side=tk.BOTTOM, fill=tk.X, pady=20)

        # 2. منطقة المحتوى الرئيسية (Main Content)
        self.main_content = tk.Frame(self.root, bg=self.bg_color)
        self.main_content.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=40, pady=30)

        # رأس الصفحة (Header)
        header_frame = tk.Frame(self.main_content, bg=self.bg_color)
        header_frame.pack(fill=tk.X)

        tk.Label(header_frame, text="My Documents", font=("Segoe UI", 24, "bold"), 
                 bg=self.bg_color, fg=self.text_color).pack(side=tk.LEFT)

        # زر الرفع السريع
        upload_btn = tk.Button(header_frame, text="+ Upload New File", bg=self.accent_color,
                               fg="white", font=("Segoe UI", 10, "bold"), padx=15, pady=8,
                               relief=tk.FLAT, command=self.upload_action)
        upload_btn.pack(side=tk.RIGHT)

        # 3. جدول عرض الملفات (Files Table)
        style = ttk.Style()
        style.configure("Treeview", font=("Segoe UI", 10), rowheight=35, background=self.card_color)
        style.configure("Treeview.Heading", font=("Segoe UI", 11, "bold"))
        
        self.tree = ttk.Treeview(self.main_content, columns=("name", "date", "size"), show="headings")
        self.tree.heading("name", text="File Name")
        self.tree.heading("date", text="Upload Date")
        self.tree.heading("size", text="Size")
        
        self.tree.column("name", width=400)
        self.tree.column("date", width=150)
        self.tree.column("size", width=100)
        
        self.tree.pack(fill=tk.BOTH, expand=True, pady=20)

        

    def upload_action(self):
        file_path = filedialog.askopenfilename()
        if file_path:
            filename = file_path.split("/")[-1]
            messagebox.showinfo("Success", f"File '{filename}' uploaded successfully!")
            # هنا يمكنك إضافة كود حفظ المسار في قاعدة البيانات

if __name__ == "__main__":
    root = tk.Tk()
    app = MainDashboard(root)
    root.mainloop()