import tkinter as tk
from tkinter import ttk, filedialog, messagebox
from file import FileProcessor

class MainDashboard:
    def __init__(self, root, username="User"):
        self.root = root
        self.username = username
        self.root.title(f"Welcome {self.username} - Blockchain System")
        self.root.geometry("1200x700")
        
        self.engine = FileProcessor()
        
        # إعدادات الألوان
        self.bg_color = "#f5f1eb"
        self.sidebar_color = "#254614"
        self.accent_color = "#8b7355"
        self.text_color = "#4a4238"
        
        self.root.configure(bg=self.bg_color)
        
        # قاموس لتخزين الصفحات
        self.pages = {}
        
        self.setup_layout()
        # إظهار شاشة الداشبورد كشاشة افتراضية عند الفتح
        self.show_page("dashboard")

    def setup_layout(self):
        # --- الشريط الجانبي (Sidebar) ---
        sidebar = tk.Frame(self.root, bg=self.sidebar_color, width=250)
        sidebar.pack(side=tk.LEFT, fill=tk.Y)
        sidebar.pack_propagate(False)

        tk.Label(sidebar, text="HOME", font=("Segoe UI", 20, "bold"), 
                 bg=self.sidebar_color, fg="white", pady=30).pack()

        # زر Dashboard
        tk.Button(sidebar, text="📊 Dashboard", font=("Segoe UI", 12),
                  bg=self.sidebar_color, fg="white", bd=0, cursor="hand2",
                  activebackground=self.accent_color, padx=20, pady=15, 
                  anchor="w", command=lambda: self.show_page("dashboard")).pack(fill=tk.X)

        # زر Verification (الشاشة الجديدة)
        tk.Button(sidebar, text="🔍 Verification", font=("Segoe UI", 12),
                  bg=self.sidebar_color, fg="white", bd=0, cursor="hand2",
                  activebackground=self.accent_color, padx=20, pady=15, 
                  anchor="w", command=lambda: self.show_page("verification")).pack(fill=tk.X)

        tk.Label(sidebar, bg=self.sidebar_color).pack(expand=True)
        
        tk.Button(sidebar, text="🚪 Logout", font=("Segoe UI", 11),
                  bg="#4e1a1a", fg="white", bd=0, cursor="hand2",
                  activebackground="#7a2828", pady=10, command=self.root.quit).pack(fill=tk.X)

        # --- منطقة المحتوى المتغيرة (Container) ---
        self.container = tk.Frame(self.root, bg=self.bg_color)
        self.container.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        # تعريف الصفحات
        self.create_dashboard_page()
        self.create_verification_page()

    def show_page(self, page_name):
        """إخفاء جميع الصفحات وإظهار الصفحة المطلوبة"""
        for page in self.pages.values():
            page.pack_forget()
        
        self.pages[page_name].pack(fill=tk.BOTH, expand=True, padx=40, pady=30)
        
        if page_name == "dashboard":
            self.refresh_table()

    def create_dashboard_page(self):
        """إنشاء واجهة الداشبورد (الرفع والجدول)"""
        page = tk.Frame(self.container, bg=self.bg_color)
        self.pages["dashboard"] = page

        header = tk.Frame(page, bg=self.bg_color)
        header.pack(fill=tk.X)

        tk.Label(header, text="Secured Documents", font=("Segoe UI", 24, "bold"), 
                 bg=self.bg_color, fg=self.text_color).pack(side=tk.LEFT)

        tk.Button(header, text="+ Upload & Secure", bg=self.accent_color, fg="white",
                  font=("Segoe UI", 10, "bold"), padx=15, pady=8, relief=tk.FLAT,
                  command=self.upload_action).pack(side=tk.RIGHT)

        style = ttk.Style()
        style.configure("Treeview", font=("Segoe UI", 10), rowheight=35)
        
        self.tree = ttk.Treeview(page, columns=("name", "date", "status", "hash"), show="headings")
        self.tree.heading("name", text="File Name")
        self.tree.heading("date", text="Upload Date")
        self.tree.heading("status", text="Blockchain Status")
        self.tree.heading("hash", text="SHA256 Fingerprint")
        
        self.tree.column("name", width=200)
        self.tree.column("date", width=150)
        self.tree.column("status", width=120)
        self.tree.column("hash", width=400)
        
        self.tree.pack(fill=tk.BOTH, expand=True, pady=20)
        self.tree.bind("<Button-3>", self.show_context_menu)

    def create_verification_page(self):
        """إنشاء واجهة التحقق (Verification)"""
        page = tk.Frame(self.container, bg=self.bg_color)
        self.pages["verification"] = page

        tk.Label(page, text="Document Verification", font=("Segoe UI", 24, "bold"), 
                 bg=self.bg_color, fg=self.text_color).pack(anchor="w")
        
        tk.Label(page, text="Select a file to verify its authenticity on the Blockchain:", 
                 font=("Segoe UI", 11), bg=self.bg_color, fg=self.text_color).pack(anchor="w", pady=(10, 20))

        # زر اختيار ملف للتحقق
        verify_btn = tk.Button(page, text="📁 Choose File to Verify", bg=self.sidebar_color, fg="white",
                              font=("Segoe UI", 12, "bold"), padx=30, pady=15, relief=tk.FLAT,
                              command=self.verify_action)
        verify_btn.pack(pady=20)

        # منطقة عرض النتائج
        self.result_frame = tk.LabelFrame(page, text="Verification Results", bg=self.bg_color, 
                                         font=("Segoe UI", 12, "bold"), fg=self.text_color, padx=20, pady=20)
        self.result_frame.pack(fill=tk.X, pady=20)
        
        self.res_label = tk.Label(self.result_frame, text="No file selected yet.", 
                                 font=("Segoe UI", 11), bg=self.bg_color, fg=self.text_color, justify=tk.LEFT)
        self.res_label.pack(fill=tk.X)

    def verify_action(self):
        """دالة التحقق من ملف خارجي"""
        file_path = filedialog.askopenfilename()
        if file_path:
            # حساب هاش الملف المختار
            f_hash = self.engine.calculate_sha256(file_path)
            
            # التحقق من البلوكتشين
            bc_data = self.engine.blockchain.verify_file(f_hash)
            
            if bc_data:
                res_text = (f"✅ MATCH FOUND!\n\n"
                            f"File Name: {file_path.split('/')[-1]}\n"
                            f"Uploader: {bc_data['uploader']}\n"
                            f"Timestamp: {bc_data['timestamp']}\n"
                            f"Current Status: {bc_data['status']}")
                self.res_label.config(text=res_text, fg="#1a472a") # أخضر غامق للنجاح
            else:
                self.res_label.config(text="❌ ALERT: Document NOT found on Blockchain!\nThis file might be tampered or unrecorded.", 
                                     fg="#8b0000") # أحمر للتحذير

    # --- الدوال المساعدة المتبقية كما هي ---
    def show_context_menu(self, event):
        item = self.tree.identify_row(event.y)
        if item:
            self.tree.selection_set(item)
            menu = tk.Menu(self.root, tearoff=0)
            menu.add_command(label="Set as Active", command=lambda: self.update_status(0))
            menu.add_command(label="Set as Revoked", command=lambda: self.update_status(1))
            menu.add_command(label="Set as Archived", command=lambda: self.update_status(2))
            menu.post(event.x_root, event.y_root)

    def update_status(self, status_code):
        selected_item = self.tree.selection()[0]
        file_hash = self.tree.item(selected_item)['values'][3]
        success, tx_id = self.engine.blockchain.update_file_status(file_hash, status_code)
        if success:
            messagebox.showinfo("Success", "Blockchain status updated!")
            self.refresh_table()
        else:
            messagebox.showerror("Error", tx_id)

    def refresh_table(self):
        for item in self.tree.get_children(): self.tree.delete(item)
        for row in self.engine.db.get_all_files():
            bc_data = self.engine.blockchain.verify_file(row[2])
            status = bc_data['status'] if bc_data else "Not Found"
            self.tree.insert("", "end", values=(row[0], row[1], status, row[2]))

    def upload_action(self):
        file_path = filedialog.askopenfilename()
        if file_path:
            success, result = self.engine.process_upload(file_path)
            if success:
                self.refresh_table()
                messagebox.showinfo("Success", "File secured on Blockchain!")
            else:
                messagebox.showerror("Error", result)

if __name__ == "__main__":
    root = tk.Tk()
    app = MainDashboard(root)
    root.mainloop()