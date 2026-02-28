import sqlite3
import os

# Get the directory where database.py is located
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(BASE_DIR, "employees.db")


def get_connection():
    return sqlite3.connect(DB_PATH, timeout=10)


def init_db():
    conn = None
    try:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS employees (
                employee_id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                gender TEXT,
                dob TEXT,
                department TEXT,
                position TEXT,
                status TEXT,
                contact TEXT,
                email TEXT,
                address TEXT
            )
        ''')
        conn.commit()
    finally:
        if conn:
            conn.close()


def add_employee(data):
    conn = None
    try:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute('''
            INSERT INTO employees (name, gender, dob, department, position, status, contact, email, address)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', (
            data['name'], data['gender'], data['dob'], data['department'],
            data['position'], data['status'], data['contact'], data['email'], data['address']
        ))
        conn.commit()
    finally:
        if conn:
            conn.close()


def get_all_employees():
    conn = None
    try:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM employees ORDER BY name ASC')
        return cursor.fetchall()
    finally:
        if conn:
            conn.close()


def get_employee_by_id(emp_id):
    conn = None
    try:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM employees WHERE employee_id = ?', (emp_id,))
        return cursor.fetchone()
    finally:
        if conn:
            conn.close()


def update_employee(emp_id, data):
    conn = None
    try:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute('''
            UPDATE employees SET
                name = ?, gender = ?, dob = ?, department = ?,
                position = ?, status = ?, contact = ?, email = ?, address = ?
            WHERE employee_id = ?
        ''', (
            data['name'], data['gender'], data['dob'], data['department'],
            data['position'], data['status'], data['contact'], data['email'], data['address'],
            emp_id
        ))
        conn.commit()
    finally:
        if conn:
            conn.close()


def delete_employee(emp_id):
    conn = None
    try:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute('DELETE FROM employees WHERE employee_id = ?', (emp_id,))
        conn.commit()
    finally:
        if conn:
            conn.close()


def search_employees(query):
    conn = None
    try:
        conn = get_connection()
        cursor = conn.cursor()
        search_term = "%{}%".format(query)
        cursor.execute('''
            SELECT * FROM employees
            WHERE name LIKE ? OR department LIKE ? OR position LIKE ?
            ORDER BY name ASC
        ''', (search_term, search_term, search_term))
        return cursor.fetchall()
    finally:
        if conn:
            conn.close()


def check_name_exists(name, exclude_id=None):
    import re

    def normalize(n):
        words = re.findall(r'\w+', n.lower())
        descriptive = [w for w in words if len(w) > 1]
        if descriptive:
            return "".join(descriptive)
        return "".join(words)

    conn = None
    try:
        conn = get_connection()
        cursor = conn.cursor()
        if exclude_id:
            cursor.execute('SELECT name FROM employees WHERE employee_id != ?', (exclude_id,))
        else:
            cursor.execute('SELECT name FROM employees')
        all_names = [row[0] for row in cursor.fetchall()]
    finally:
        if conn:
            conn.close()

    target_norm = normalize(name)
    if not target_norm:
        return False

    for existing_name in all_names:
        if normalize(existing_name) == target_norm:
            return True

    return False


def check_email_exists(email, exclude_id=None):
    """Return True if the given email already exists for another employee."""
    conn = None
    try:
        conn = get_connection()
        cursor = conn.cursor()
        if exclude_id:
            cursor.execute(
                'SELECT COUNT(*) FROM employees WHERE LOWER(email) = LOWER(?) AND employee_id != ?',
                (email, exclude_id)
            )
        else:
            cursor.execute(
                'SELECT COUNT(*) FROM employees WHERE LOWER(email) = LOWER(?)',
                (email,)
            )
        count = cursor.fetchone()[0]
        return count > 0
    finally:
        if conn:
            conn.close()


def check_contact_exists(contact, exclude_id=None):
    """Return True if the given contact number already exists for another employee."""
    conn = None
    try:
        conn = get_connection()
        cursor = conn.cursor()
        if exclude_id:
            cursor.execute(
                'SELECT COUNT(*) FROM employees WHERE contact = ? AND employee_id != ?',
                (contact, exclude_id)
            )
        else:
            cursor.execute(
                'SELECT COUNT(*) FROM employees WHERE contact = ?',
                (contact,)
            )
        count = cursor.fetchone()[0]
        return count > 0
    finally:
        if conn:
            conn.close()


if __name__ == "__main__":
    init_db()
    print("Database initialized.")
