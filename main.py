import tkinter as tk
from tkinter import ttk, messagebox
import datetime
import database


class ESMSApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("ESMS")
        
        # Adaptive View - use full screen on mobile, cap on desktop
        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()
        
        # On mobile (Pydroid), use full screen; on desktop, simulate mobile
        if screen_width <= 600:
            # Mobile device - use full screen
            width = screen_width
            height = screen_height
            self.geometry(f"{width}x{height}+0+0")
            self.attributes('-fullscreen', False)
        else:
            # Desktop - simulate mobile view
            width = 400
            height = 750
            x = (screen_width - width) // 2
            y = (screen_height - height) // 2
            self.geometry(f"{width}x{height}+{x}+{y}")
        
        self.app_width = width
        self.app_height = height
        self.resizable(False, False)
        
        # Colors & Constants
        self.BG_COLOR = "#f4f7f6"
        self.PRIMARY_COLOR = "#2c3e50"
        self.ACCENT_COLOR = "#3498db"
        self.TEXT_COLOR = "#2c3e50"
        self.HEADER_COLOR = "#ffffff"
        self.CARD_BG = "#ffffff"
        
        self.configure(bg=self.BG_COLOR)
        
        # Style configuration
        self.style = ttk.Style()
        self.style.theme_use('clam')
        
        # Button Styles
        self.style.configure("TButton", 
                            padding=10, 
                            font=("Helvetica", 10, "bold"),
                            background=self.ACCENT_COLOR,
                            foreground="white")
        self.style.map("TButton",
                    background=[('active', '#2980b9')])
        
        # Entry Style
        self.style.configure("TEntry", padding=8)
        
        # Label Styles
        self.style.configure("Header.TLabel", 
                            font=("Helvetica", 18, "bold"), 
                            background=self.BG_COLOR,
                            foreground=self.TEXT_COLOR)
        self.style.configure("SubHeader.TLabel", 
                            font=("Helvetica", 10), 
                            background=self.BG_COLOR, 
                            foreground="#7f8c8d")
        
        # Treeview Styling
        self.style.configure("Treeview", 
                            rowheight=45, 
                            font=("Helvetica", 10),
                            background=self.CARD_BG,
                            fieldbackground=self.CARD_BG,
                            borderwidth=0)
        self.style.configure("Treeview.Heading", 
                            font=("Helvetica", 9, "bold"),
                            background="#f4f7f6",
                            foreground="#2c3e50")
        self.style.map("Treeview", background=[('selected', self.ACCENT_COLOR)])
        
        # Container for screens
        self.container = tk.Frame(self, bg=self.BG_COLOR)
        self.container.pack(fill="both", expand=True)
        
        # Initialize Database with Error Handling
        try:
            database.init_db()
        except Exception as e:
            messagebox.showerror("Error", "Database init failed.\nCheck file permissions.")
            self.destroy()
            return

        self.show_frame("LoginFrame")

    def show_frame(self, page_name, **kwargs):
        for frame in self.container.winfo_children():
            frame.destroy()
            
        if page_name == "LoginFrame":
            frame = LoginFrame(parent=self.container, controller=self)
        elif page_name == "DashboardFrame":
            frame = DashboardFrame(parent=self.container, controller=self)
        elif page_name == "EmployeeFormFrame":
            frame = EmployeeFormFrame(parent=self.container, controller=self, emp_id=kwargs.get("emp_id"))
            
        frame.pack(fill="both", expand=True)

class LoginFrame(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent, bg=controller.BG_COLOR)
        self.controller = controller
        
        # Proportional padding based on screen height
        top_pad = max(30, controller.app_height // 12)
        side_pad = max(16, controller.app_width // 16)
        
        main_box = tk.Frame(self, bg=controller.BG_COLOR)
        main_box.pack(expand=True, fill="both")
        
        header_box = tk.Frame(main_box, bg=controller.BG_COLOR)
        header_box.pack(pady=(top_pad, top_pad // 2))
        
        tk.Label(header_box, text="ESMS", font=("Helvetica", 30, "bold"), 
                 bg=controller.BG_COLOR, fg=controller.ACCENT_COLOR).pack()
        ttk.Label(header_box, text="ESMS Login", style="Header.TLabel").pack(pady=(8, 0))
        ttk.Label(header_box, text="Employee Staff Management System", 
                  style="SubHeader.TLabel").pack()
        
        form_card = tk.Frame(main_box, bg=controller.CARD_BG, padx=side_pad, pady=side_pad, 
                             highlightbackground="#ddd", highlightthickness=1)
        form_card.pack(padx=side_pad, fill="x")
        
        tk.Label(form_card, text="Account Access", font=("Helvetica", 12, "bold"), 
                 bg=controller.CARD_BG, fg=controller.TEXT_COLOR).pack(anchor="w", pady=(0, 15))
        
        tk.Label(form_card, text="Username", bg=controller.CARD_BG, 
                 font=("Helvetica", 9, "bold")).pack(anchor="w")
        self.username_entry = ttk.Entry(form_card)
        self.username_entry.pack(fill="x", pady=(5, 12))
        self.username_entry.insert(0, "admin")
        
        # Focus fix for Pydroid keyboard
        self.username_entry.bind("<Button-1>", 
            lambda e: self.username_entry.after(50, self.username_entry.focus_force))
        
        # Next button -> move to password
        self.username_entry.bind("<Return>", lambda e: self.password_entry.focus_force())
        
        tk.Label(form_card, text="Password", bg=controller.CARD_BG, 
                 font=("Helvetica", 9, "bold")).pack(anchor="w")
        self.password_entry = ttk.Entry(form_card, show="*")
        self.password_entry.pack(fill="x", pady=(5, 0))
        self.password_entry.insert(0, "admin")
        
        # Focus fix for Pydroid keyboard
        self.password_entry.bind("<Button-1>", 
            lambda e: self.password_entry.after(50, self.password_entry.focus_force))
        
        # Next button on password -> trigger login
        self.password_entry.bind("<Return>", lambda e: self.login())
        
        self.show_password = tk.BooleanVar(value=False)
        def toggle_password():
            self.password_entry.config(show="" if self.show_password.get() else "*")
                
        tk.Checkbutton(form_card, text="Show Password", variable=self.show_password, 
                       command=toggle_password, bg=controller.CARD_BG, 
                       activebackground=controller.CARD_BG, font=("Helvetica", 8)
                       ).pack(anchor="w", pady=(5, 15))
        
        ttk.Button(form_card, text="LOGIN", command=self.login).pack(fill="x")
        
        tk.Label(main_box, text="\u00a9 2026 ESMS Solution", font=("Helvetica", 8), 
                 bg=controller.BG_COLOR, fg="#7f8c8d").pack(side="bottom", pady=15)

    def login(self):
        if self.username_entry.get() == "admin" and self.password_entry.get() == "admin":
            self.controller.show_frame("DashboardFrame")
        else:
            messagebox.showerror("Login Failed", "Invalid credentials.")

class DashboardFrame(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent, bg=controller.BG_COLOR)
        self.controller = controller
        
        # Proportional sizing
        side_pad = max(12, controller.app_width // 20)
        
        # Header
        header_bar = tk.Frame(self, bg=controller.HEADER_COLOR, height=56, 
                              highlightbackground="#ddd", highlightthickness=1)
        header_bar.pack(fill="x")
        header_bar.pack_propagate(False)
        
        tk.Label(header_bar, text="ESMS", font=("Helvetica", 18, "bold"), 
                 bg=controller.HEADER_COLOR, fg=controller.ACCENT_COLOR
                 ).pack(side="left", padx=side_pad)
        
        logout_btn = tk.Button(header_bar, text="Logout", font=("Helvetica", 9),
                               bg="#e74c3c", fg="white", borderwidth=0, padx=12,
                               command=lambda: controller.show_frame("LoginFrame"))
        logout_btn.pack(side="right", padx=side_pad)
        
        # Action Bar (Sticky Bottom)
        action_bar = tk.Frame(self, bg=controller.HEADER_COLOR,
                              highlightbackground="#ddd", highlightthickness=1)
        action_bar.pack(side="bottom", fill="x")
        
        btn_pad = max(6, side_pad // 2)
        ttk.Button(action_bar, text="+ ADD NEW", 
                   command=lambda: controller.show_frame("EmployeeFormFrame")
                   ).pack(side="left", fill="both", expand=True, padx=(btn_pad, 4), pady=btn_pad)
        
        tk.Button(action_bar, text="EDIT", font=("Helvetica", 9, "bold"), 
                  bg="#ecf0f1", fg=controller.TEXT_COLOR, borderwidth=0, 
                  command=self.edit_selected
                  ).pack(side="left", fill="both", expand=True, padx=4, pady=btn_pad)

        tk.Button(action_bar, text="DELETE", font=("Helvetica", 9, "bold"), 
                  bg="#fdeaea", fg="#e74c3c", borderwidth=0, 
                  command=self.delete_selected
                  ).pack(side="left", fill="both", expand=True, padx=(4, btn_pad), pady=btn_pad)
        
        # Main Content Area
        content_box = tk.Frame(self, bg=controller.BG_COLOR, padx=side_pad, pady=side_pad)
        content_box.pack(fill="both", expand=True)
        
        # Stats Display
        stats_frame = tk.Frame(content_box, bg=controller.BG_COLOR)
        stats_frame.pack(fill="x", pady=(0, 10))
        
        self.count_var = tk.StringVar(value="0")
        tk.Label(stats_frame, text="Active Employees", font=("Helvetica", 10, "bold"), 
                 bg=controller.BG_COLOR, fg="#7f8c8d").pack(side="left")
        tk.Label(stats_frame, textvariable=self.count_var, font=("Helvetica", 20, "bold"), 
                 bg=controller.BG_COLOR, fg=controller.TEXT_COLOR).pack(side="right")
        
        # Search Box
        search_card = tk.Frame(content_box, bg=controller.CARD_BG, padx=10, pady=8, 
                               highlightbackground="#e0e0e0", highlightthickness=1)
        search_card.pack(fill="x", pady=(0, 10))
        
        tk.Label(search_card, text="Search:", font=("Helvetica", 9), 
                 bg=controller.CARD_BG, fg="#95a5a6").pack(side="left", padx=(0, 5))
        self.search_entry = ttk.Entry(search_card)
        self.search_entry.pack(side="left", fill="x", expand=True)
        self.search_entry.bind("<KeyRelease>", lambda e: self.refresh_list())
        
        # Focus fix for Pydroid keyboard
        self.search_entry.bind("<Button-1>", 
            lambda e: self.search_entry.after(50, self.search_entry.focus_force))

        # Employee List
        tree_wrapper = tk.Frame(content_box, bg=controller.CARD_BG, 
                                highlightbackground="#e0e0e0", highlightthickness=1)
        tree_wrapper.pack(fill="both", expand=True)
        
        # Proportional column widths based on available width
        avail_width = controller.app_width - (side_pad * 2) - 4
        cols = ("name", "dob", "position")
        self.tree = ttk.Treeview(tree_wrapper, columns=cols, show="headings")
        self.tree.heading("name", text="NAME")
        self.tree.heading("dob", text="DOB")
        self.tree.heading("position", text="POSITION")
        
        # 40% name, 35% dob, 25% position
        self.tree.column("name", width=int(avail_width * 0.40), minwidth=60)
        self.tree.column("dob", width=int(avail_width * 0.35), minwidth=50)
        self.tree.column("position", width=int(avail_width * 0.25), minwidth=40)
        self.tree.pack(fill="both", expand=True)
        
        # Hidden data storage for ID
        self.row_ids = {}  # Mapping tree item iid -> database employee_id

        self.refresh_list()

    def format_dob(self, date_str):
        if not date_str: return "-"
        # Clean up common separators
        normalized = date_str.replace("/", "-").strip()
        try:
            # Expected format: YYYY-MM-DD
            dt = datetime.datetime.strptime(normalized, "%Y-%m-%d")
            return dt.strftime("%B %d %Y")
        except:
            return date_str # Return as is if format is unknown

    def refresh_list(self):
        for item in self.tree.get_children():
            self.tree.delete(item)
        self.row_ids = {}
        
        query = self.search_entry.get()
        employees = database.search_employees(query) if query else database.get_all_employees()
        
        for emp in employees:
            formatted_dob = self.format_dob(emp[3])
            iid = self.tree.insert("", "end", values=(emp[1], formatted_dob, emp[5]))
            self.row_ids[iid] = emp[0]
            
        self.count_var.set(str(len(employees)))

    def get_selected_id(self):
        sel = self.tree.selection()
        if not sel:
            messagebox.showwarning("Selection", "Please select a staff record.")
            return None
        return self.row_ids.get(sel[0])

    def edit_selected(self):
        emp_id = self.get_selected_id()
        if emp_id: self.controller.show_frame("EmployeeFormFrame", emp_id=emp_id)

    def delete_selected(self):
        emp_id = self.get_selected_id()
        if emp_id and messagebox.askyesno("Confirm", "Delete this record?"):
            database.delete_employee(emp_id)
            self.refresh_list()

class EmployeeFormFrame(tk.Frame):
    def __init__(self, parent, controller, emp_id=None):
        super().__init__(parent, bg=controller.BG_COLOR)
        self.controller = controller
        self.emp_id = emp_id
        
        # Header Bar
        header_bar = tk.Frame(self, bg=controller.HEADER_COLOR, height=56, 
                              highlightbackground="#ddd", highlightthickness=1)
        header_bar.pack(fill="x")
        header_bar.pack_propagate(False)
        
        tk.Label(header_bar, text="Edit Details" if emp_id else "New Staff", 
                 font=("Helvetica", 15, "bold"), bg=controller.HEADER_COLOR, 
                 fg=controller.TEXT_COLOR).pack(side="left", padx=15, pady=10)
        
        tk.Button(header_bar, text="Cancel", font=("Helvetica", 9), 
                  bg="#ecf0f1", fg=controller.TEXT_COLOR, borderwidth=0, padx=12,
                  command=lambda: controller.show_frame("DashboardFrame")).pack(side="right", padx=10)

        # Scrollable Canvas
        canvas = tk.Canvas(self, bg=controller.BG_COLOR, highlightthickness=0)
        form_box = tk.Frame(canvas, bg=controller.BG_COLOR)
        
        form_box.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))
        
        self._canvas_window = canvas.create_window((0, 0), window=form_box, anchor="nw")
        canvas.configure(yscrollcommand=lambda *a: None)  # Hide scrollbar for cleaner look
        
        # Auto-resize form_box to fill canvas width
        def _on_canvas_resize(event):
            canvas.itemconfig(self._canvas_window, width=event.width)
        canvas.bind("<Configure>", _on_canvas_resize)
        
        canvas.pack(fill="both", expand=True)

        # Form Content inside a padded container
        inner_pad = tk.Frame(form_box, bg=controller.BG_COLOR, padx=16, pady=12)
        inner_pad.pack(fill="x", expand=True)
        
        labels = [
            ("name", "Full Name"), ("gender", "Gender"), ("dob", "DOB (YYYY-MM-DD)"),
            ("department", "Department"), ("position", "Role / Position"), ("status", "Employment Status"),
            ("contact", "Phone Number"), ("email", "Work Email"), ("address", "Permanent Address")
        ]
        
        self.fields = {}
        for key, label in labels:
            # Card-style section for each field
            card = tk.Frame(inner_pad, bg=controller.CARD_BG, padx=12, pady=10,
                            highlightbackground="#e0e0e0", highlightthickness=1)
            card.pack(fill="x", pady=(0, 8))
            
            tk.Label(card, text=label.upper(), font=("Helvetica", 8, "bold"), 
                     bg=controller.CARD_BG, fg="#95a5a6").pack(anchor="w")
            
            if key == "gender":
                entry = ttk.Combobox(card, values=["MALE", "FEMALE", "OTHERS"], state="readonly")
            elif key == "department":
                entry = ttk.Combobox(card, values=["HR", "IT", "SALES", "FINANCE", "MARKETING", "OPERATIONS", "OTHERS"], state="readonly")
            elif key == "position":
                entry = ttk.Combobox(card, values=["ADMIN", "MANAGER", "SUPERVISOR", "STAFF", "INTERN", "OTHERS"], state="readonly")
            elif key == "status":
                entry = ttk.Combobox(card, values=["ACTIVE", "INACTIVE", "TERMINATED", "ON LEAVE"], state="readonly")
            elif key == "contact":
                vcmd = (self.register(self.validate_phone), '%P')
                entry = ttk.Entry(card, validate="key", validatecommand=vcmd)
            else:
                entry = ttk.Entry(card)
                
            entry.pack(fill="x", pady=(4, 0))
            self.fields[key] = entry
            
            # Fix: force focus on tap so keyboard reappears on Pydroid
            if isinstance(entry, ttk.Entry):
                entry.bind("<Button-1>", lambda e, w=entry: w.after(50, w.focus_force))
        
        # Bind Return (Android "Next" button) to move to next field
        field_keys = list(self.fields.keys())
        for i, key in enumerate(field_keys):
            widget = self.fields[key]
            if i < len(field_keys) - 1:
                next_widget = self.fields[field_keys[i + 1]]
                widget.bind("<Return>", lambda e, nw=next_widget: nw.focus_force())
            else:
                # Last field -> trigger save
                widget.bind("<Return>", lambda e: self.save())

        if emp_id:
            emp = database.get_employee_by_id(emp_id)
            if emp:
                map_idx = {"name": 1, "gender": 2, "dob": 3, "department": 4, "position": 5, 
                           "status": 6, "contact": 7, "email": 8, "address": 9}
                for k, i in map_idx.items():
                    val = str(emp[i])
                    if isinstance(self.fields[k], ttk.Combobox):
                        self.fields[k].set(val)
                    else:
                        self.fields[k].insert(0, val)
        
        ttk.Button(inner_pad, text="SAVE CHANGES" if emp_id else "REGISTER STAFF", 
                   command=self.save).pack(pady=(12, 20), fill="x")

    def validate_phone(self, P):
        if len(P) > 11:
            return False
        if P == "" or P.isdigit():
            return True
        return False

    def save(self):
        # Extract and clean data
        data = {k: v.get().strip() for k, v in self.fields.items()}
        
        # 1. Check for blank spaces / empty fields
        for key, value in data.items():
            if not value:
                field_label = key.replace('_', ' ').title()
                return messagebox.showerror("Error", f"{field_label} is required.")
        
        # 2. Check for duplicate names
        if database.check_name_exists(data['name'], exclude_id=self.emp_id):
            return messagebox.showerror("Error", "This name already exists.")
            
        # 3. Validate email format (requires @)
        if "@" not in data['email']:
            return messagebox.showerror("Error", "Email must contain '@'.")
            
        try:
            if self.emp_id: database.update_employee(self.emp_id, data)
            else: database.add_employee(data)
            messagebox.showinfo("Success", "Record saved successfully.")
            self.controller.show_frame("DashboardFrame")
        except Exception as e:
            messagebox.showerror("Error", "Failed to save record.")

if __name__ == "__main__":
    app = ESMSApp()
    app.mainloop()
