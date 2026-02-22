# Employee Staff Management System (ESMS)

> [!IMPORTANT]
> **PROTOTYPE NOTICE**: This system is currently a **PROTOTYPE** and is still under active development (Under Production). Features and database schemas are subject to change.

## Overview
ESMS is a lightweight, mobile-first Employee Management System designed for efficiency and simplicity. It allows users to manage staff records, including personal details, departments, and employment status.

## Key Features
- **Mobile-First Design**: Optimized for Android (Pydroid 3) and small screens.
- **SQLite Database**: Local, fast, and reliable storage.
- **CRUD Operations**: Register, View, Edit, and Delete staff records.
- **Deep Search**: Quickly find employees by name, department, or position.
- **Data Validation**: Automatic validation for phone numbers, email formats, and duplicate names.

## Bug Fixes & Improvements

### Responsive Layout Fix
- All screens (Login, Dashboard, Employee Form) now adapt properly to **any screen size**.
- Replaced hardcoded pixel values with **proportional sizing** based on screen dimensions.
- Column widths in the employee list are now **percentage-based** (40% / 35% / 25%) instead of fixed.
- Padding and spacing scale dynamically across Login, Dashboard, and Form screens.

### Pydroid 3 (Android) Compatibility
- **Tkinter Module Error**: Resolved `ModuleNotFoundError: No module named 'tkinter'` — requires the **Pydroid Repository Plugin** from the Play Store.
- **Keyboard Focus Fix**: Added `<Button-1>` focus bindings on all input fields so the on-screen keyboard reliably appears when tapping a field.
- **"Next" Key Navigation**: Pressing the Enter/Next button on the Android keyboard now moves focus to the next field, and triggers save on the last field.

### Database Path Resolution
- The database file (`employees.db`) is now created relative to `database.py`'s directory using `os.path.abspath(__file__)`, preventing "file not found" errors when running from different working directories.

### Duplicate Name Prevention
- Added **normalized name matching** that ignores spacing, casing, and initials to catch duplicate entries (e.g., "John Doe" vs "john doe" vs "J. Doe").

### Input Validation
- **Phone number**: Limited to 11 digits, numeric only.
- **Email**: Must contain `@`.
- **Required fields**: All fields are mandatory — blank submissions are blocked with a clear error message.

## Pydroid 3 (Android) Setup Instructions

To run this system on your mobile device using Pydroid 3:

1. **File Naming**: Ensure the database logic file is named exactly `database.py` (all lowercase).
2. **Directory**: Keep `main.py` and `database.py` in the same folder on your device.
3. **Dependencies**: This app uses the Python Standard Library. No `pip install` is required **except** for the Tkinter plugin.
4. **Tkinter Support**: Ensure you have the **"Pydroid Repository Plugin"** installed from the Play Store to enable the graphical interface.

## Project Structure
- `main.py`: The primary GUI application using Tkinter.
- `database.py`: Handles all SQLite database interactions.
- `employees.db`: The local database file (generated automatically).



