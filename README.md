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

---
*Created by YoursTrulyInarius*
