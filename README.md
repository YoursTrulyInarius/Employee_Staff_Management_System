# Employee Staff Management System (ESMS)

> [!IMPORTANT]
> **PROTOTYPE NOTICE**: This system is currently a **PROTOTYPE** and is still under active development (Under Production). Features and database schemas are subject to change.

## Overview
ESMS is a lightweight, mobile-first Employee Management System built with Python and Tkinter. It lets admins manage staff records — register, view, edit, delete, and search employees — all stored locally via SQLite. Designed to run on both Android (Pydroid 3) and desktop.

---

## Key Features

| Feature | Description |
|---------|-------------|
| **Mobile-First Design** | Full-screen on Android (Pydroid 3), simulated mobile view on desktop |
| **SQLite Database** | Local, fast, and reliable storage — no internet required |
| **CRUD Operations** | Register, View, Edit, and Delete staff records |
| **Deep Search** | Instantly filter employees by name, department, or position |
| **Scrollable Forms** | Add/Edit form scrolls via mouse wheel (desktop) and touch drag (mobile) |
| **Full Validation** | 8-step validation pipeline on every save (see below) |
| **Duplicate Prevention** | Blocks duplicate names, emails, and phone numbers across all employees |
| **Error Handling** | All database operations wrapped in try/finally — no connection leaks |

---

## Validation Rules (Save Pipeline)

Every time a record is saved (new or edited), these checks run in order:

1. **Required fields** — All 9 fields must be filled in
2. **Phone number** — Digits only, must be 10 or 11 digits
3. **Email format** — Must contain `@`, no quotation marks (`'` or `"`), must match `user@domain.tld` pattern
4. **Date of Birth** — Must be in `YYYY-MM-DD` format, not in the future, not before 1900
5. **Duplicate name** — Fuzzy match ignoring case, spacing, and initials (e.g. `John Doe` vs `john doe` vs `J. Doe`)
6. **Duplicate email** — Case-insensitive match across all existing records
7. **Duplicate contact** — Exact match across all existing records
8. **Database save** — Full error message shown if the database write fails

Live input guards (on keypress):
- **Phone field**: Letters blocked immediately; only digits accepted
- **Email field**: Quotation marks (`'`, `"`) blocked immediately on keypress

---

## Bug Fixes & Improvements

### Scrollable Form (Mobile & Desktop)
- The Add/Edit employee form now uses a `Canvas` + `Scrollbar` layout.
- **Desktop**: Mouse-wheel scroll (`<MouseWheel>`) and Linux scroll buttons (`<Button-4>/<Button-5>`).
- **Mobile**: Touch drag-to-scroll bound to the canvas background only — does **not** steal taps from input fields.

### Pydroid 3 (Android) Compatibility
- **Tkinter theme fallback**: `theme_use('clam')` is wrapped in `try/except` — falls back to the system default theme if `clam` is unavailable on the Android build.
- **Keyboard Focus Fix**: `<Button-1>` bindings on all plain Entry fields (`type(entry) is ttk.Entry`) so the on-screen keyboard reliably appears on tap.
- **Combobox fix**: Comboboxes are excluded from the focus hack (they use `type()` not `isinstance()`) so dropdowns open normally.
- **No Windows-only APIs**: All `f`-strings replaced with `.format()`, no platform-specific calls.
- **Remove Control-v bindings**: Paste key bindings removed (irrelevant on Android); phone validation is enforced at keypress and at save time.
- **\"Next\" Key Navigation**: Enter/Next on the Android keyboard moves focus to the next field, and triggers save on the last field.

### Responsive Layout
- All screens adapt to any screen size using proportional sizing based on `winfo_screenwidth()` / `winfo_screenheight()`.
- Column widths in the employee list are percentage-based: **40% Name / 35% DOB / 25% Position**.
- Padding and spacing scale dynamically on Login, Dashboard, and Form screens.

### Database Reliability
- Every DB function (`add`, `update`, `delete`, `get`, `search`, `check_*`) uses `try/finally` to guarantee connections are always closed — no leaks even on error.
- Added `check_email_exists(email, exclude_id)` and `check_contact_exists(contact, exclude_id)` helper functions.
- Employee lists are now sorted alphabetically by name.
- `get_connection()` includes `timeout=10` for slow storage devices.

### Database Path Resolution
- `employees.db` is created relative to `database.py` using `os.path.abspath(__file__)`, preventing "file not found" errors when running from a different working directory.

---

## Employee Record Fields

| Field | Type | Rules |
|-------|------|-------|
| Full Name | Text | Required, no duplicates (fuzzy match) |
| Gender | Dropdown | MALE / FEMALE / OTHERS |
| Date of Birth | Text | Required, YYYY-MM-DD, not future, ≥ 1900 |
| Department | Dropdown | HR / IT / SALES / FINANCE / MARKETING / OPERATIONS / OTHERS |
| Role / Position | Dropdown | ADMIN / MANAGER / SUPERVISOR / STAFF / INTERN / OTHERS |
| Employment Status | Dropdown | ACTIVE / INACTIVE / TERMINATED / ON LEAVE |
| Phone Number | Text | Digits only, 10–11 digits, no duplicates |
| Work Email | Text | Must contain `@`, no quotes, no duplicates |
| Permanent Address | Text | Required |

---

## Pydroid 3 (Android) Setup Instructions

1. **File Naming**: Ensure the database logic file is named exactly `database.py` (all lowercase).
2. **Same Directory**: Keep `main.py` and `database.py` in the same folder on your device.
3. **No pip installs needed**: Uses Python Standard Library only.
4. **Tkinter Support**: Install the **"Pydroid Repository Plugin"** from the Play Store — this enables the graphical interface.
5. **Run**: Open `main.py` in Pydroid 3 and press Run. The `employees.db` file will be created automatically.

---

## Project Structure

```
Employee_Staff_Management_System/
├── main.py          # GUI application (Tkinter) — all screens and validation
├── database.py      # SQLite database layer — CRUD + duplicate checks
└── employees.db     # Auto-generated local database (do not edit manually)
```

---

## Default Login

| Field | Value |
|-------|-------|
| Username | `admin` |
| Password | `admin` |
