import tkinter as tk
from tkinter import ttk, messagebox
import datetime
import re
import database


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def validate_email_chars(email):
    """
    Returns (True, '') if email is acceptable, or (False, reason) if not.
    Rules:
      - Must contain exactly one '@'
      - No quotation marks (' or ")
      - Only letters, digits, dots, underscores, dashes, @, and domain dots allowed
    """
    forbidden = ['"', "'"]
    for ch in forbidden:
        if ch in email:
            return False, "Email must not contain quotation marks."
    if "@" not in email:
        return False, "Email must contain '@'."
    if email.count("@") > 1:
        return False, "Email must contain only one '@'."
    # Basic structure: something@something.something
    pattern = r"^[A-Za-z0-9._\-]+@[A-Za-z0-9.\-]+\.[A-Za-z]{2,}$"
    if not re.match(pattern, email):
        return False, "Invalid email format.\nExample: juan@company.com"
    return True, ""


def validate_dob(dob):
    """Returns (True, '') or (False, reason). Expects YYYY-MM-DD."""
    try:
        parsed = datetime.datetime.strptime(dob.strip(), "%Y-%m-%d")
        # Sanity: not in the future, not before 1900
        today = datetime.date.today()
        if parsed.date() > today:
            return False, "Date of Birth cannot be in the future."
        if parsed.year < 1900:
            return False, "Date of Birth year must be 1900 or later."
        return True, ""
    except ValueError:
        return False, "DOB format must be YYYY-MM-DD.\nExample: 1995-06-15"


# ---------------------------------------------------------------------------
# App
# ---------------------------------------------------------------------------

class ESMSApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("ESMS")

        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()

        if screen_width <= 600:
            width = screen_width
            height = screen_height
            self.geometry("{}x{}+0+0".format(width, height))
        else:
            width = 400
            height = 750
            x = (screen_width - width) // 2
            y = (screen_height - height) // 2
            self.geometry("{}x{}+{}+{}".format(width, height, x, y))

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

        # Style
        self.style = ttk.Style()
        # 'clam' may not be available on all Pydroid/Android builds — fall back gracefully
        try:
            self.style.theme_use('clam')
        except Exception:
            pass  # use system default theme
        self.style.configure("TButton",
                             padding=10,
                             font=("Helvetica", 10, "bold"),
                             background=self.ACCENT_COLOR,
                             foreground="white")
        self.style.map("TButton", background=[('active', '#2980b9')])
        self.style.configure("TEntry", padding=8)
        self.style.configure("Header.TLabel",
                             font=("Helvetica", 18, "bold"),
                             background=self.BG_COLOR,
                             foreground=self.TEXT_COLOR)
        self.style.configure("SubHeader.TLabel",
                             font=("Helvetica", 10),
                             background=self.BG_COLOR,
                             foreground="#7f8c8d")
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

        self.container = tk.Frame(self, bg=self.BG_COLOR)
        self.container.pack(fill="both", expand=True)

        try:
            database.init_db()
        except Exception as e:
            messagebox.showerror("Database Error",
                                 "Failed to initialize database.\n"
                                 "Check file permissions and storage.\n\n"
                                 "Detail: {}".format(str(e)))
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
            frame = EmployeeFormFrame(parent=self.container, controller=self,
                                      emp_id=kwargs.get("emp_id"))

        frame.pack(fill="both", expand=True)


# ---------------------------------------------------------------------------
# Login
# ---------------------------------------------------------------------------

class LoginFrame(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent, bg=controller.BG_COLOR)
        self.controller = controller

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

        form_card = tk.Frame(main_box, bg=controller.CARD_BG,
                             padx=side_pad, pady=side_pad,
                             highlightbackground="#ddd", highlightthickness=1)
        form_card.pack(padx=side_pad, fill="x")

        tk.Label(form_card, text="Account Access", font=("Helvetica", 12, "bold"),
                 bg=controller.CARD_BG, fg=controller.TEXT_COLOR).pack(anchor="w", pady=(0, 15))

        tk.Label(form_card, text="Username", bg=controller.CARD_BG,
                 font=("Helvetica", 9, "bold")).pack(anchor="w")
        self.username_entry = ttk.Entry(form_card)
        self.username_entry.pack(fill="x", pady=(5, 12))
        self.username_entry.insert(0, "admin")
        self.username_entry.bind("<Button-1>",
            lambda e: self.username_entry.after(50, self.username_entry.focus_force))
        self.username_entry.bind("<Return>", lambda e: self.password_entry.focus_force())

        tk.Label(form_card, text="Password", bg=controller.CARD_BG,
                 font=("Helvetica", 9, "bold")).pack(anchor="w")
        self.password_entry = ttk.Entry(form_card, show="*")
        self.password_entry.pack(fill="x", pady=(5, 0))
        self.password_entry.insert(0, "admin")
        self.password_entry.bind("<Button-1>",
            lambda e: self.password_entry.after(50, self.password_entry.focus_force))
        self.password_entry.bind("<Return>", lambda e: self.login())

        self.show_password = tk.BooleanVar(value=False)

        def toggle_password():
            self.password_entry.config(show="" if self.show_password.get() else "*")

        tk.Checkbutton(form_card, text="Show Password", variable=self.show_password,
                       command=toggle_password, bg=controller.CARD_BG,
                       activebackground=controller.CARD_BG,
                       font=("Helvetica", 8)).pack(anchor="w", pady=(5, 15))

        ttk.Button(form_card, text="LOGIN", command=self.login).pack(fill="x")

        tk.Label(main_box, text="\u00a9 2026 ESMS Solution", font=("Helvetica", 8),
                 bg=controller.BG_COLOR, fg="#7f8c8d").pack(side="bottom", pady=15)

    def login(self):
        username = self.username_entry.get().strip()
        password = self.password_entry.get().strip()
        if username == "admin" and password == "admin":
            self.controller.show_frame("DashboardFrame")
        else:
            messagebox.showerror("Login Failed", "Invalid username or password.")


# ---------------------------------------------------------------------------
# Dashboard
# ---------------------------------------------------------------------------

class DashboardFrame(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent, bg=controller.BG_COLOR)
        self.controller = controller

        side_pad = max(12, controller.app_width // 20)

        # Header
        header_bar = tk.Frame(self, bg=controller.HEADER_COLOR, height=56,
                              highlightbackground="#ddd", highlightthickness=1)
        header_bar.pack(fill="x")
        header_bar.pack_propagate(False)

        tk.Label(header_bar, text="ESMS", font=("Helvetica", 18, "bold"),
                 bg=controller.HEADER_COLOR, fg=controller.ACCENT_COLOR
                 ).pack(side="left", padx=side_pad)

        tk.Button(header_bar, text="Logout", font=("Helvetica", 9),
                  bg="#e74c3c", fg="white", borderwidth=0, padx=12,
                  command=lambda: controller.show_frame("LoginFrame")
                  ).pack(side="right", padx=side_pad)

        # Action Bar (bottom)
        action_bar = tk.Frame(self, bg=controller.HEADER_COLOR,
                              highlightbackground="#ddd", highlightthickness=1)
        action_bar.pack(side="bottom", fill="x")

        btn_pad = max(6, side_pad // 2)
        ttk.Button(action_bar, text="+ ADD NEW",
                   command=lambda: controller.show_frame("EmployeeFormFrame")
                   ).pack(side="left", fill="both", expand=True,
                          padx=(btn_pad, 4), pady=btn_pad)

        tk.Button(action_bar, text="EDIT", font=("Helvetica", 9, "bold"),
                  bg="#ecf0f1", fg=controller.TEXT_COLOR, borderwidth=0,
                  command=self.edit_selected
                  ).pack(side="left", fill="both", expand=True, padx=4, pady=btn_pad)

        tk.Button(action_bar, text="DELETE", font=("Helvetica", 9, "bold"),
                  bg="#fdeaea", fg="#e74c3c", borderwidth=0,
                  command=self.delete_selected
                  ).pack(side="left", fill="both", expand=True,
                         padx=(4, btn_pad), pady=btn_pad)

        # Content
        content_box = tk.Frame(self, bg=controller.BG_COLOR, padx=side_pad, pady=side_pad)
        content_box.pack(fill="both", expand=True)

        stats_frame = tk.Frame(content_box, bg=controller.BG_COLOR)
        stats_frame.pack(fill="x", pady=(0, 10))

        self.count_var = tk.StringVar(value="0")
        tk.Label(stats_frame, text="Active Employees", font=("Helvetica", 10, "bold"),
                 bg=controller.BG_COLOR, fg="#7f8c8d").pack(side="left")
        tk.Label(stats_frame, textvariable=self.count_var, font=("Helvetica", 20, "bold"),
                 bg=controller.BG_COLOR, fg=controller.TEXT_COLOR).pack(side="right")

        # Search
        search_card = tk.Frame(content_box, bg=controller.CARD_BG, padx=10, pady=8,
                               highlightbackground="#e0e0e0", highlightthickness=1)
        search_card.pack(fill="x", pady=(0, 10))

        tk.Label(search_card, text="Search:", font=("Helvetica", 9),
                 bg=controller.CARD_BG, fg="#95a5a6").pack(side="left", padx=(0, 5))
        self.search_entry = ttk.Entry(search_card)
        self.search_entry.pack(side="left", fill="x", expand=True)
        self.search_entry.bind("<KeyRelease>", lambda e: self.refresh_list())
        self.search_entry.bind("<Button-1>",
            lambda e: self.search_entry.after(50, self.search_entry.focus_force))

        # Employee list (Treeview handles its own scrolling)
        tree_wrapper = tk.Frame(content_box, bg=controller.CARD_BG,
                                highlightbackground="#e0e0e0", highlightthickness=1)
        tree_wrapper.pack(fill="both", expand=True)

        avail_width = controller.app_width - (side_pad * 2) - 4
        cols = ("name", "dob", "position")
        self.tree = ttk.Treeview(tree_wrapper, columns=cols, show="headings")
        self.tree.heading("name", text="NAME")
        self.tree.heading("dob", text="DOB")
        self.tree.heading("position", text="POSITION")
        self.tree.column("name", width=int(avail_width * 0.40), minwidth=60)
        self.tree.column("dob",  width=int(avail_width * 0.35), minwidth=50)
        self.tree.column("position", width=int(avail_width * 0.25), minwidth=40)
        self.tree.pack(fill="both", expand=True)

        self.row_ids = {}
        self.refresh_list()

    def format_dob(self, date_str):
        if not date_str:
            return "-"
        try:
            dt = datetime.datetime.strptime(date_str.strip(), "%Y-%m-%d")
            return dt.strftime("%b %d %Y")
        except Exception:
            return date_str

    def refresh_list(self):
        for item in self.tree.get_children():
            self.tree.delete(item)
        self.row_ids = {}
        try:
            query = self.search_entry.get().strip()
            employees = database.search_employees(query) if query else database.get_all_employees()
            for emp in employees:
                formatted_dob = self.format_dob(emp[3])
                iid = self.tree.insert("", "end", values=(emp[1], formatted_dob, emp[5]))
                self.row_ids[iid] = emp[0]
            self.count_var.set(str(len(employees)))
        except Exception as e:
            messagebox.showerror("Error", "Could not load employee list.\n\n{}".format(str(e)))

    def get_selected_id(self):
        sel = self.tree.selection()
        if not sel:
            messagebox.showwarning("No Selection", "Please select a staff record first.")
            return None
        return self.row_ids.get(sel[0])

    def edit_selected(self):
        emp_id = self.get_selected_id()
        if emp_id:
            self.controller.show_frame("EmployeeFormFrame", emp_id=emp_id)

    def delete_selected(self):
        emp_id = self.get_selected_id()
        if emp_id and messagebox.askyesno("Confirm Delete",
                                          "Are you sure you want to delete this record?\nThis cannot be undone."):
            try:
                database.delete_employee(emp_id)
                self.refresh_list()
            except Exception as e:
                messagebox.showerror("Error", "Failed to delete record.\n\n{}".format(str(e)))


# ---------------------------------------------------------------------------
# Employee Form
# ---------------------------------------------------------------------------

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

        tk.Label(header_bar,
                 text="Edit Details" if emp_id else "New Staff",
                 font=("Helvetica", 15, "bold"),
                 bg=controller.HEADER_COLOR,
                 fg=controller.TEXT_COLOR).pack(side="left", padx=15, pady=10)

        tk.Button(header_bar, text="Cancel", font=("Helvetica", 9),
                  bg="#ecf0f1", fg=controller.TEXT_COLOR, borderwidth=0, padx=12,
                  command=lambda: controller.show_frame("DashboardFrame")
                  ).pack(side="right", padx=10)

        # ── Scrollable Canvas ──────────────────────────────────────────────
        scroll_outer = tk.Frame(self, bg=controller.BG_COLOR)
        scroll_outer.pack(fill="both", expand=True)

        canvas = tk.Canvas(scroll_outer, bg=controller.BG_COLOR, highlightthickness=0)
        scrollbar = ttk.Scrollbar(scroll_outer, orient="vertical", command=canvas.yview)
        canvas.configure(yscrollcommand=scrollbar.set)

        scrollbar.pack(side="right", fill="y")
        canvas.pack(side="left", fill="both", expand=True)

        form_box = tk.Frame(canvas, bg=controller.BG_COLOR)
        self._canvas_window = canvas.create_window((0, 0), window=form_box, anchor="nw")

        def _on_frame_configure(event):
            canvas.configure(scrollregion=canvas.bbox("all"))
        form_box.bind("<Configure>", _on_frame_configure)

        def _on_canvas_resize(event):
            canvas.itemconfig(self._canvas_window, width=event.width)
        canvas.bind("<Configure>", _on_canvas_resize)

        # Desktop: mouse-wheel scroll
        def _on_mousewheel(event):
            canvas.yview_scroll(int(-1 * (event.delta / 120)), "units")
        canvas.bind_all("<MouseWheel>", _on_mousewheel)

        # Linux / some platforms
        canvas.bind_all("<Button-4>", lambda e: canvas.yview_scroll(-1, "units"))
        canvas.bind_all("<Button-5>", lambda e: canvas.yview_scroll(1, "units"))

        # Mobile / Pydroid touch drag-to-scroll.
        # Bound ONLY to the canvas background, NOT form_box, so taps on child
        # widgets (Entry, Combobox, Button) are NOT intercepted.
        self._touch_y = None

        def _touch_start(event):
            self._touch_y = event.y

        def _touch_move(event):
            if self._touch_y is not None:
                delta = self._touch_y - event.y
                canvas.yview_scroll(int(delta / 5), "units")
                self._touch_y = event.y

        def _touch_end(event):
            self._touch_y = None

        canvas.bind("<ButtonPress-1>", _touch_start)
        canvas.bind("<B1-Motion>", _touch_move)
        canvas.bind("<ButtonRelease-1>", _touch_end)

        # Cleanup global bindings when leaving this screen
        def _on_destroy(event):
            try:
                canvas.unbind_all("<MouseWheel>")
                canvas.unbind_all("<Button-4>")
                canvas.unbind_all("<Button-5>")
            except Exception:
                pass
        self.bind("<Destroy>", _on_destroy)

        # ── Form Fields ────────────────────────────────────────────────────
        inner_pad = tk.Frame(form_box, bg=controller.BG_COLOR, padx=16, pady=12)
        inner_pad.pack(fill="x", expand=True)

        labels = [
            ("name",       "Full Name"),
            ("gender",     "Gender"),
            ("dob",        "Date of Birth (YYYY-MM-DD)"),
            ("department", "Department"),
            ("position",   "Role / Position"),
            ("status",     "Employment Status"),
            ("contact",    "Phone Number (digits only, max 11)"),
            ("email",      "Work Email"),
            ("address",    "Permanent Address"),
        ]

        self.fields = {}

        for key, label in labels:
            card = tk.Frame(inner_pad, bg=controller.CARD_BG, padx=12, pady=10,
                            highlightbackground="#e0e0e0", highlightthickness=1)
            card.pack(fill="x", pady=(0, 8))

            tk.Label(card, text=label.upper(), font=("Helvetica", 8, "bold"),
                     bg=controller.CARD_BG, fg="#95a5a6").pack(anchor="w")

            if key == "gender":
                entry = ttk.Combobox(card, values=["MALE", "FEMALE", "OTHERS"],
                                     state="readonly")
            elif key == "department":
                entry = ttk.Combobox(card,
                                     values=["HR", "IT", "SALES", "FINANCE",
                                             "MARKETING", "OPERATIONS", "OTHERS"],
                                     state="readonly")
            elif key == "position":
                entry = ttk.Combobox(card,
                                     values=["ADMIN", "MANAGER", "SUPERVISOR",
                                             "STAFF", "INTERN", "OTHERS"],
                                     state="readonly")
            elif key == "status":
                entry = ttk.Combobox(card,
                                     values=["ACTIVE", "INACTIVE", "TERMINATED", "ON LEAVE"],
                                     state="readonly")
            elif key == "contact":
                # Digits only, max 11 — validated on keypress
                vcmd = (self.register(self._validate_phone), '%P')
                entry = ttk.Entry(card, validate="key", validatecommand=vcmd)
                # Note: Control-v paste bindings are desktop-only and skipped.
                # Digit-only enforcement is handled in _validate_phone and on save.
            elif key == "email":
                entry = ttk.Entry(card)
                # Block quotation marks live on keypress
                entry.bind("<KeyPress>", self._block_email_quotes)
            else:
                entry = ttk.Entry(card)

            entry.pack(fill="x", pady=(4, 0))
            self.fields[key] = entry

            # Pydroid: force focus on tap so keyboard appears.
            # Only bind to plain Entry (not Combobox, which opens a dropdown on tap).
            if type(entry) is ttk.Entry:
                entry.bind("<Button-1>", lambda e, w=entry: w.after(50, w.focus_force))

        # Return/Next navigation between fields
        field_keys = list(self.fields.keys())
        for i, key in enumerate(field_keys):
            widget = self.fields[key]
            if i < len(field_keys) - 1:
                nxt = self.fields[field_keys[i + 1]]
                widget.bind("<Return>", lambda e, nw=nxt: nw.focus_force())
            else:
                widget.bind("<Return>", lambda e: self.save())

        # Pre-fill when editing
        if emp_id:
            try:
                emp = database.get_employee_by_id(emp_id)
                if emp:
                    map_idx = {
                        "name": 1, "gender": 2, "dob": 3, "department": 4,
                        "position": 5, "status": 6, "contact": 7, "email": 8, "address": 9
                    }
                    for k, idx in map_idx.items():
                        val = str(emp[idx]) if emp[idx] is not None else ""
                        if isinstance(self.fields[k], ttk.Combobox):
                            self.fields[k].set(val)
                        else:
                            self.fields[k].insert(0, val)
            except Exception as e:
                messagebox.showerror("Error",
                                     "Could not load employee data.\n\n{}".format(str(e)))

        ttk.Button(inner_pad,
                   text="SAVE CHANGES" if emp_id else "REGISTER STAFF",
                   command=self.save).pack(pady=(12, 20), fill="x")

    # ── Input Validators ───────────────────────────────────────────────────

    def _validate_phone(self, P):
        """Allow only digits, max 11 characters."""
        if len(P) > 11:
            return False
        if P == "" or P.isdigit():
            return True
        return False

    def _handle_paste_contact(self, event):
        """Strip non-digits from clipboard before pasting into contact field."""
        try:
            clipboard = self.clipboard_get()
            digits_only = "".join(ch for ch in clipboard if ch.isdigit())
            entry = self.fields["contact"]
            # Get current value and cursor position
            current = entry.get()
            # Clear and insert cleaned value capped at 11 digits
            combined = current + digits_only
            combined = combined[:11]
            entry.delete(0, tk.END)
            entry.insert(0, combined)
        except Exception:
            pass
        return "break"  # prevent default paste

    def _block_email_quotes(self, event):
        """Block single and double quotation marks in email field."""
        if event.char in ('"', "'"):
            return "break"

    # ── Save / Validation ──────────────────────────────────────────────────

    def save(self):
        data = {k: v.get().strip() for k, v in self.fields.items()}

        # 1. Required fields
        field_labels = {
            "name": "Full Name", "gender": "Gender", "dob": "Date of Birth",
            "department": "Department", "position": "Role / Position",
            "status": "Employment Status", "contact": "Phone Number",
            "email": "Work Email", "address": "Permanent Address",
        }
        for key, value in data.items():
            if not value:
                return messagebox.showerror(
                    "Required Field",
                    "{} is required.".format(field_labels.get(key, key)))

        # 2. Contact: digits only, 10–11 digits
        if not data["contact"].isdigit():
            return messagebox.showerror("Invalid Contact",
                                        "Phone number must contain digits only.")
        if len(data["contact"]) < 10 or len(data["contact"]) > 11:
            return messagebox.showerror("Invalid Contact",
                                        "Phone number must be 10 or 11 digits.")

        # 3. Email validation (format + forbidden chars)
        ok, reason = validate_email_chars(data["email"])
        if not ok:
            return messagebox.showerror("Invalid Email", reason)

        # 4. DOB format
        ok, reason = validate_dob(data["dob"])
        if not ok:
            return messagebox.showerror("Invalid Date of Birth", reason)

        # 5. Duplicate name check
        try:
            if database.check_name_exists(data["name"], exclude_id=self.emp_id):
                return messagebox.showerror("Duplicate Name",
                                            "An employee with this name already exists.")
        except Exception as e:
            return messagebox.showerror("Error", "Name check failed.\n\n{}".format(str(e)))

        # 6. Duplicate email check
        try:
            if database.check_email_exists(data["email"], exclude_id=self.emp_id):
                return messagebox.showerror("Duplicate Email",
                                            "This email address is already registered\n"
                                            "to another employee.")
        except Exception as e:
            return messagebox.showerror("Error", "Email check failed.\n\n{}".format(str(e)))

        # 7. Duplicate contact check
        try:
            if database.check_contact_exists(data["contact"], exclude_id=self.emp_id):
                return messagebox.showerror("Duplicate Contact",
                                            "This phone number is already registered\n"
                                            "to another employee.")
        except Exception as e:
            return messagebox.showerror("Error", "Contact check failed.\n\n{}".format(str(e)))

        # 8. Save
        try:
            if self.emp_id:
                database.update_employee(self.emp_id, data)
                messagebox.showinfo("Success", "Employee record updated successfully.")
            else:
                database.add_employee(data)
                messagebox.showinfo("Success", "Employee registered successfully.")
            self.controller.show_frame("DashboardFrame")
        except Exception as e:
            messagebox.showerror("Save Error",
                                 "Failed to save record.\n\n{}".format(str(e)))


# ---------------------------------------------------------------------------
# Entry point
# ---------------------------------------------------------------------------

if __name__ == "__main__":
    app = ESMSApp()
    app.mainloop()
