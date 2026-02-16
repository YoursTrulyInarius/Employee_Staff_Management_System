import tkinter as tk
from tkinter import ttk, messagebox
import database
import datetime

class ESMSApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("ESMS")
        
        # Simulated Mobile View
        self.geometry("400x750")
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
        
        # Initialize Database
        database.init_db()
        
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
        
        main_box = tk.Frame(self, bg=controller.BG_COLOR)
        main_box.pack(expand=True, fill="both")
        
        header_box = tk.Frame(main_box, bg=controller.BG_COLOR)
        header_box.pack(pady=(80, 40))
        
        tk.Label(header_box, text="👤", font=("Helvetica", 64), bg=controller.BG_COLOR, fg=controller.ACCENT_COLOR).pack()
        ttk.Label(header_box, text="ESMS Login", style="Header.TLabel").pack(pady=(10, 0))
        ttk.Label(header_box, text="Employee Staff Management System", style="SubHeader.TLabel").pack()
        
        form_card = tk.Frame(main_box, bg=controller.CARD_BG, padx=30, pady=30, 
                             highlightbackground="#ddd", highlightthickness=1)
        form_card.pack(padx=30, fill="x")
        
        tk.Label(form_card, text="Account Access", font=("Helvetica", 12, "bold"), 
                 bg=controller.CARD_BG, fg=controller.TEXT_COLOR).pack(anchor="w", pady=(0, 20))
        
        tk.Label(form_card, text="Username", bg=controller.CARD_BG, font=("Helvetica", 9, "bold")).pack(anchor="w")
        self.username_entry = ttk.Entry(form_card)
        self.username_entry.pack(fill="x", pady=(5, 15))
        self.username_entry.insert(0, "admin")
        
        tk.Label(form_card, text="Password", bg=controller.CARD_BG, font=("Helvetica", 9, "bold")).pack(anchor="w")
        password_container = tk.Frame(form_card, bg=controller.CARD_BG)
        password_container.pack(fill="x", pady=(5, 0))
        
        self.password_entry = ttk.Entry(password_container, show="*")
        self.password_entry.pack(side="left", fill="x", expand=True)
        self.password_entry.insert(0, "admin")
        
        self.show_password = tk.BooleanVar(value=False)
        def toggle_password():
            self.password_entry.config(show="" if self.show_password.get() else "*")
                
        tk.Checkbutton(form_card, text="Show Password", variable=self.show_password, 
                       command=toggle_password, bg=controller.CARD_BG, 
                       activebackground=controller.CARD_BG, font=("Helvetica", 8)).pack(anchor="w", pady=(0, 20))
        
        ttk.Button(form_card, text="LOGIN", command=self.login).pack(fill="x")
        
        tk.Label(main_box, text="© 2026 ESMS Solution", font=("Helvetica", 8), 
                 bg=controller.BG_COLOR, fg="#7f8c8d").pack(side="bottom", pady=20)

    def login(self):
        if self.username_entry.get() == "admin" and self.password_entry.get() == "admin":
            self.controller.show_frame("DashboardFrame")
        else:
            messagebox.showerror("Login Failed", "Invalid credentials.")

class DashboardFrame(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent, bg=controller.BG_COLOR)
        self.controller = controller
        
        # Header
        header_bar = tk.Frame(self, bg=controller.HEADER_COLOR, height=70, 
                              highlightbackground="#eee", highlightthickness=1)
        header_bar.pack(fill="x")
        header_bar.pack_propagate(False)
        
        tk.Label(header_bar, text="ESMS", font=("Helvetica", 20, "bold"), 
                 bg=controller.HEADER_COLOR, fg=controller.ACCENT_COLOR).pack(side="left", padx=20)
        
        logout_btn = tk.Button(header_bar, text="Logout", font=("Helvetica", 10),
                               bg="#e74c3c", fg="white", borderwidth=0, padx=15,
                               command=lambda: controller.show_frame("LoginFrame"))
        logout_btn.pack(side="right", padx=15)
        
        # Action Bar (Sticky Bottom)
        action_bar = tk.Frame(self, bg=controller.HEADER_COLOR, height=80,
                              highlightbackground="#eee", highlightthickness=1)
        action_bar.pack(side="bottom", fill="x")
        
        ttk.Button(action_bar, text="+ ADD NEW", command=lambda: controller.show_frame("EmployeeFormFrame")).pack(side="left", fill="both", expand=True, padx=15, pady=15)
        
        tk.Button(action_bar, text="EDIT", font=("Helvetica", 10, "bold"), bg="#ecf0f1", fg=controller.TEXT_COLOR, borderwidth=0, command=self.edit_selected).pack(side="left", fill="both", expand=True, padx=(0, 15), pady=15)

        tk.Button(action_bar, text="DELETE", font=("Helvetica", 10, "bold"), bg="#fdeaea", fg="#e74c3c", borderwidth=0, command=self.delete_selected).pack(side="left", fill="both", expand=True, padx=(0, 15), pady=15)
        
        # Main Scrollable Area
        content_box = tk.Frame(self, bg=controller.BG_COLOR, padx=20, pady=20)
        content_box.pack(fill="both", expand=True)
        
        # Cleaner Stats Display
        stats_frame = tk.Frame(content_box, bg=controller.BG_COLOR)
        stats_frame.pack(fill="x", pady=(0, 15))
        
        self.count_var = tk.StringVar(value="0")
        tk.Label(stats_frame, text="Active Employees", font=("Helvetica", 10, "bold"), bg=controller.BG_COLOR, fg="#7f8c8d").pack(side="left")
        tk.Label(stats_frame, textvariable=self.count_var, font=("Helvetica", 24, "bold"), bg=controller.BG_COLOR, fg=controller.TEXT_COLOR).pack(side="right")
        
        # Search Box (Integrated)
        search_card = tk.Frame(content_box, bg=controller.CARD_BG, padx=10, pady=5, highlightbackground="#eee", highlightthickness=1)
        search_card.pack(fill="x", pady=(0, 20))
        
        tk.Label(search_card, text="🔍", bg=controller.CARD_BG, fg="#bdc3c7").pack(side="left", padx=5)
        self.search_entry = ttk.Entry(search_card) # Entry style handled by controller
        self.search_entry.pack(side="left", fill="x", expand=True, padx=5)
        self.search_entry.bind("<KeyRelease>", lambda e: self.refresh_list())

        # Clean List Implementation
        tree_wrapper = tk.Frame(content_box, bg=controller.CARD_BG, highlightbackground="#eee", highlightthickness=1)
        tree_wrapper.pack(fill="both", expand=True)
        
        # Added DOB column, kept Name and Position
        cols = ("name", "dob", "position")
        self.tree = ttk.Treeview(tree_wrapper, columns=cols, show="headings")
        self.tree.heading("name", text="NAME")
        self.tree.heading("dob", text="DOB")
        self.tree.heading("position", text="POSITION")
        
        self.tree.column("name", width=140)
        self.tree.column("dob", width=110)
        self.tree.column("position", width=90)
        self.tree.pack(fill="both", expand=True)
        
        # Hidden data storage for ID
        self.row_ids = {} # Mapping tree item iid -> database employee_id

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
        if emp_id and messagebox.askyesno("Confirm", "Are you sure you want to delete this staff record?"):
            database.delete_employee(emp_id)
            self.refresh_list()

class EmployeeFormFrame(tk.Frame):
    def __init__(self, parent, controller, emp_id=None):
        super().__init__(parent, bg=controller.BG_COLOR)
        self.controller = controller
        self.emp_id = emp_id
        
        header_bar = tk.Frame(self, bg=controller.HEADER_COLOR, height=70, 
                              highlightbackground="#eee", highlightthickness=1)
        header_bar.pack(fill="x")
        header_bar.pack_propagate(False)
        
        tk.Label(header_bar, text="Edit Details" if emp_id else "New Staff", 
                 font=("Helvetica", 16, "bold"), bg=controller.HEADER_COLOR, fg=controller.TEXT_COLOR).pack(side="left", padx=20)
        
        tk.Button(header_bar, text="Cancel", font=("Helvetica", 10), bg="#ecf0f1", fg=controller.TEXT_COLOR, borderwidth=0, padx=15, command=lambda: controller.show_frame("DashboardFrame")).pack(side="right", padx=15)

        canvas = tk.Canvas(self, bg=controller.BG_COLOR, highlightthickness=0)
        scrollbar = ttk.Scrollbar(self, orient="vertical", command=canvas.yview)
        form_box = tk.Frame(canvas, bg=controller.BG_COLOR, padx=25, pady=25)
        
        form_box.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))
        canvas.create_window((0, 0), window=form_box, anchor="nw", width=380)
        canvas.configure(yscrollcommand=scrollbar.set)
        
        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
        
        labels = [
            ("name", "Full Name"), ("gender", "Gender"), ("dob", "Date of Birth (YYYY-MM-DD)"),
            ("department", "Department"), ("position", "Role / Position"), ("status", "Employment Status"),
            ("contact", "Phone Number"), ("email", "Work Email"), ("address", "Permanent Address")
        ]
        
        self.fields = {}
        for key, label in labels:
            section = tk.Frame(form_box, bg=controller.BG_COLOR, pady=10)
            section.pack(fill="x")
            tk.Label(section, text=label.upper(), font=("Helvetica", 8, "bold"), bg=controller.BG_COLOR, fg="#95a5a6").pack(anchor="w")
            
            if key == "gender":
                entry = ttk.Combobox(section, values=["MALE", "FEMALE", "OTHERS"], state="readonly")
            elif key == "department":
                entry = ttk.Combobox(section, values=["HR", "IT", "SALES", "FINANCE", "MARKETING", "OPERATIONS", "OTHERS"], state="readonly")
            elif key == "position":
                entry = ttk.Combobox(section, values=["ADMIN", "MANAGER", "SUPERVISOR", "STAFF", "INTERN", "OTHERS"], state="readonly")
            elif key == "status":
                entry = ttk.Combobox(section, values=["ACTIVE", "INACTIVE", "TERMINATED", "ON LEAVE"], state="readonly")
            elif key == "contact":
                vcmd = (self.register(self.validate_phone), '%P')
                entry = ttk.Entry(section, validate="key", validatecommand=vcmd)
            else:
                entry = ttk.Entry(section)
                
            entry.pack(fill="x", pady=(5, 0))
            self.fields[key] = entry

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
        
        ttk.Button(form_box, text="SAVE CHANGES" if emp_id else "REGISTER STAFF", command=self.save).pack(pady=30, fill="x")

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
                return messagebox.showerror("Validation Error", f"{field_label} cannot be empty or just spaces.")
        
        # 2. Check for duplicate names
        if database.check_name_exists(data['name'], exclude_id=self.emp_id):
            return messagebox.showerror("Duplicate Name", f"An employee named '{data['name']}' already exists.")
            
        # 3. Validate email format (requires @)
        if "@" not in data['email']:
            return messagebox.showerror("Invalid Email", "Email Address must contain '@'.")
            
        try:
            if self.emp_id: database.update_employee(self.emp_id, data)
            else: database.add_employee(data)
            messagebox.showinfo("Success", "Record saved successfully.")
            self.controller.show_frame("DashboardFrame")
        except Exception as e:
            messagebox.showerror("System Error", f"Failed to save record: {e}")

if __name__ == "__main__":
    app = ESMSApp()
    app.mainloop()
