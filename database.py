import sqlite3
import os

DB_NAME = "employees.db"

def get_connection():
    return sqlite3.connect(DB_NAME)

def init_db():
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
    conn.close()

def add_employee(data):
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
    conn.close()

def get_all_employees():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM employees')
    rows = cursor.fetchall()
    conn.close()
    return rows

def get_employee_by_id(emp_id):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM employees WHERE employee_id = ?', (emp_id,))
    row = cursor.fetchone()
    conn.close()
    return row

def update_employee(emp_id, data):
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
    conn.close()

def delete_employee(emp_id):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute('DELETE FROM employees WHERE employee_id = ?', (emp_id,))
    conn.commit()
    conn.close()

def search_employees(query):
    conn = get_connection()
    cursor = conn.cursor()
    search_term = f"%{query}%"
    cursor.execute('''
        SELECT * FROM employees 
        WHERE name LIKE ? OR department LIKE ? OR position LIKE ?
    ''', (search_term, search_term, search_term))
    rows = cursor.fetchall()
    conn.close()
    return rows

def check_name_exists(name, exclude_id=None):
    def normalize(n):
        import re
        words = re.findall(r'\w+', n.lower())
        # Filter initials (1-char) ONLY if there are other descriptive words (2+ chars)
        descriptive = [w for w in words if len(w) > 1]
        if descriptive:
            return "".join(descriptive)
        return "".join(words) # fallback if name is only initials/short words

    conn = get_connection()
    cursor = conn.cursor()
    if exclude_id:
        cursor.execute('SELECT name FROM employees WHERE employee_id != ?', (exclude_id,))
    else:
        cursor.execute('SELECT name FROM employees')
    
    all_names = [row[0] for row in cursor.fetchall()]
    conn.close()

    target_norm = normalize(name)
    if not target_norm: return False # Should be caught by blank check anyway
    
    for existing_name in all_names:
        if normalize(existing_name) == target_norm:
            return True
            
    return False

if __name__ == "__main__":
    init_db()
    print("Database initialized.")
