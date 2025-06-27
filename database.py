import sqlite3
from datetime import datetime
import os

class Database:
    def __init__(self):
        self.db_file = 'clinic.db'
        self.conn = None
        self.cursor = None
        self.initialize_database()

    def connect(self):
        self.conn = sqlite3.connect(self.db_file)
        self.cursor = self.conn.cursor()

    def close(self):
        if self.conn:
            self.conn.close()

    def initialize_database(self):
        self.connect()
        
        # Users table
        self.cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL,
            role TEXT NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )''')

        # Insert default users if table is empty
        self.cursor.execute("SELECT COUNT(*) FROM users")
        if self.cursor.fetchone()[0] == 0:
            default_users = [
                ('Ahmed', '1234', 'Doctor'),
                ('Mohamed', '0000', 'Doctor'),
                ('Sarah', '1122', 'Secretary'),
                ('Nadine', '1112', 'Secretary')
            ]
            
            self.cursor.executemany(
                "INSERT INTO users (username, password, role) VALUES (?, ?, ?)",
                default_users
            )

        # Patients table
        self.cursor.execute('''
        CREATE TABLE IF NOT EXISTS patients (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            age INTEGER,
            phone TEXT,
            address TEXT,
            balance REAL DEFAULT 0,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            is_deleted INTEGER DEFAULT 0
        )''')

        # Appointments table
        self.cursor.execute('''
        CREATE TABLE IF NOT EXISTS appointments (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            patient_id INTEGER,
            doctor_id INTEGER,
            appointment_date TIMESTAMP,
            status TEXT DEFAULT 'scheduled',
            notes TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            is_deleted INTEGER DEFAULT 0,
            FOREIGN KEY (patient_id) REFERENCES patients (id),
            FOREIGN KEY (doctor_id) REFERENCES users (id)
        )''')

        # Checkups table
        self.cursor.execute('''
        CREATE TABLE IF NOT EXISTS checkups (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            patient_id INTEGER,
            doctor_id INTEGER,
            checkup_date TIMESTAMP,
            diagnosis TEXT,
            treatment TEXT,
            cost REAL,
            is_paid INTEGER DEFAULT 0,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            is_deleted INTEGER DEFAULT 0,
            FOREIGN KEY (patient_id) REFERENCES patients (id),
            FOREIGN KEY (doctor_id) REFERENCES users (id)
        )''')

        # Invoices table
        self.cursor.execute('''
        CREATE TABLE IF NOT EXISTS invoices (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            patient_id INTEGER,
            amount REAL,
            description TEXT,
            is_paid INTEGER DEFAULT 0,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            is_deleted INTEGER DEFAULT 0,
            FOREIGN KEY (patient_id) REFERENCES patients (id)
        )''')

        # Expenses table
        self.cursor.execute('''
        CREATE TABLE IF NOT EXISTS expenses (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            amount REAL,
            description TEXT,
            expense_date TIMESTAMP,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            is_deleted INTEGER DEFAULT 0
        )''')

        # Cash transactions table
        self.cursor.execute('''
        CREATE TABLE IF NOT EXISTS cash_transactions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            type TEXT,
            amount REAL,
            description TEXT,
            reference_id INTEGER,
            reference_type TEXT,
            transaction_date TIMESTAMP,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )''')

        # Insert default admin user if not exists
        self.cursor.execute('''
        INSERT OR IGNORE INTO users (username, password, role)
        VALUES (?, ?, ?)
        ''', ('admin', 'admin123', 'Doctor'))

        self.conn.commit()
        self.close()

    def execute_query(self, query, params=()):
        self.connect()
        try:
            self.cursor.execute(query, params)
            self.conn.commit()
            return self.cursor.fetchall()
        except Exception as e:
            print(f"Database error: {e}")
            return None
        finally:
            self.close()

    def get_user(self, username, password):
        # Trim whitespace and convert username to lowercase for comparison
        username = username.strip().lower()
        query = "SELECT * FROM users WHERE LOWER(username) = ? AND password = ?"
        return self.execute_query(query, (username, password))

    def add_patient(self, name, age, phone, address):
        query = '''
        INSERT INTO patients (name, age, phone, address)
        VALUES (?, ?, ?, ?)
        '''
        return self.execute_query(query, (name, age, phone, address))

    def get_all_patients(self):
        query = "SELECT * FROM patients WHERE is_deleted = 0"
        return self.execute_query(query)

    def update_patient(self, patient_id, name, age, phone, address):
        query = '''
        UPDATE patients 
        SET name = ?, age = ?, phone = ?, address = ?, updated_at = CURRENT_TIMESTAMP
        WHERE id = ?
        '''
        return self.execute_query(query, (name, age, phone, address, patient_id))

    def delete_patient(self, patient_id):
        query = '''
        UPDATE patients 
        SET is_deleted = 1, updated_at = CURRENT_TIMESTAMP
        WHERE id = ?
        '''
        return self.execute_query(query, (patient_id,))

    def add_appointment(self, patient_id, doctor_id, appointment_date, notes):
        query = '''
        INSERT INTO appointments (patient_id, doctor_id, appointment_date, notes)
        VALUES (?, ?, ?, ?)
        '''
        return self.execute_query(query, (patient_id, doctor_id, appointment_date, notes))

    def get_all_appointments(self):
        query = '''
        SELECT a.*, p.name as patient_name, u.username as doctor_name
        FROM appointments a
        JOIN patients p ON a.patient_id = p.id
        JOIN users u ON a.doctor_id = u.id
        WHERE a.is_deleted = 0
        ORDER BY a.appointment_date DESC
        '''
        return self.execute_query(query)

    def add_checkup(self, patient_id, doctor_id, checkup_date, diagnosis, treatment, cost):
        query = '''
        INSERT INTO checkups (patient_id, doctor_id, checkup_date, diagnosis, treatment, cost)
        VALUES (?, ?, ?, ?, ?, ?)
        '''
        return self.execute_query(query, (patient_id, doctor_id, checkup_date, diagnosis, treatment, cost))

    def add_expense(self, amount, description, expense_date):
        query = '''
        INSERT INTO expenses (amount, description, expense_date)
        VALUES (?, ?, ?)
        '''
        return self.execute_query(query, (amount, description, expense_date))

    def add_cash_transaction(self, type, amount, description, reference_id, reference_type):
        query = '''
        INSERT INTO cash_transactions (type, amount, description, reference_id, reference_type, transaction_date)
        VALUES (?, ?, ?, ?, ?, CURRENT_TIMESTAMP)
        '''
        return self.execute_query(query, (type, amount, description, reference_id, reference_type))

    def get_cash_balance(self):
        query = '''
        SELECT 
            SUM(CASE WHEN type = 'income' THEN amount ELSE -amount END) as balance
        FROM cash_transactions
        '''
        result = self.execute_query(query)
        return result[0][0] if result and result[0][0] is not None else 0

    def get_all_transactions(self):
        query = '''
        SELECT ct.*, 
               CASE 
                   WHEN ct.reference_type = 'checkup' THEN c.diagnosis
                   WHEN ct.reference_type = 'invoice' THEN i.description
                   WHEN ct.reference_type = 'expense' THEN e.description
                   ELSE ''
               END as reference_description
        FROM cash_transactions ct
        LEFT JOIN checkups c ON ct.reference_type = 'checkup' AND ct.reference_id = c.id
        LEFT JOIN invoices i ON ct.reference_type = 'invoice' AND ct.reference_id = i.id
        LEFT JOIN expenses e ON ct.reference_type = 'expense' AND ct.reference_id = e.id
        ORDER BY ct.transaction_date DESC
        '''
        return self.execute_query(query)

    def get_filtered_transactions(self, start_date, end_date, transaction_type):
        query = '''
        SELECT ct.*, 
               CASE 
                   WHEN ct.reference_type = 'checkup' THEN c.diagnosis
                   WHEN ct.reference_type = 'invoice' THEN i.description
                   WHEN ct.reference_type = 'expense' THEN e.description
                   ELSE ''
               END as reference_description
        FROM cash_transactions ct
        LEFT JOIN checkups c ON ct.reference_type = 'checkup' AND ct.reference_id = c.id
        LEFT JOIN invoices i ON ct.reference_type = 'invoice' AND ct.reference_id = i.id
        LEFT JOIN expenses e ON ct.reference_type = 'expense' AND ct.reference_id = e.id
        WHERE ct.transaction_date BETWEEN ? AND ?
        '''
        params = [start_date, end_date]

        if transaction_type != 'الكل':
            query += ' AND ct.type = ?'
            params.append('income' if transaction_type == 'دخل' else 'expense')

        query += ' ORDER BY ct.transaction_date DESC'
        return self.execute_query(query, tuple(params))

    def get_deleted_patients(self):
        query = "SELECT * FROM patients WHERE is_deleted = 1"
        return self.execute_query(query)

    def get_deleted_appointments(self):
        query = '''
        SELECT a.*, p.name as patient_name, u.username as doctor_name
        FROM appointments a
        JOIN patients p ON a.patient_id = p.id
        JOIN users u ON a.doctor_id = u.id
        WHERE a.is_deleted = 1
        '''
        return self.execute_query(query)

    def get_deleted_checkups(self):
        query = '''
        SELECT c.*, p.name as patient_name, u.username as doctor_name
        FROM checkups c
        JOIN patients p ON c.patient_id = p.id
        JOIN users u ON c.doctor_id = u.id
        WHERE c.is_deleted = 1
        '''
        return self.execute_query(query)

    def get_deleted_invoices(self):
        query = '''
        SELECT i.*, p.name as patient_name
        FROM invoices i
        JOIN patients p ON i.patient_id = p.id
        WHERE i.is_deleted = 1
        '''
        return self.execute_query(query)

    def get_deleted_expenses(self):
        query = "SELECT * FROM expenses WHERE is_deleted = 1"
        return self.execute_query(query)

    def restore_item(self, table_name, item_id):
        query = f"UPDATE {table_name} SET is_deleted = 0 WHERE id = ?"
        return self.execute_query(query, (item_id,))

    def delete_permanently(self, table_name, item_id):
        query = f"DELETE FROM {table_name} WHERE id = ?"
        return self.execute_query(query, (item_id,))

    def empty_trash(self):
        tables = ['patients', 'appointments', 'checkups', 'invoices', 'expenses']
        for table in tables:
            query = f"DELETE FROM {table} WHERE is_deleted = 1"
            self.execute_query(query)

    def get_checkup_patient_id(self, checkup_id):
        query = "SELECT patient_id FROM checkups WHERE id = ?"
        result = self.execute_query(query, (checkup_id,))
        return result[0][0] if result else None

    def get_invoice_patient_id(self, invoice_id):
        query = "SELECT patient_id FROM invoices WHERE id = ?"
        result = self.execute_query(query, (invoice_id,))
        return result[0][0] if result else None

    def mark_checkup_as_paid(self, patient_id, amount):
        self.add_cash_transaction('income', amount, 'دفعة كشف طبي', patient_id, 'checkup')

    def mark_invoice_as_paid(self, patient_id, amount):
        self.add_cash_transaction('income', amount, 'دفعة فاتورة', patient_id, 'invoice')

    def get_all_checkups(self):
        query = '''
        SELECT c.*, p.name as patient_name, u.username as doctor_name
        FROM checkups c
        JOIN patients p ON c.patient_id = p.id
        JOIN users u ON c.doctor_id = u.id
        WHERE c.is_deleted = 0
        ORDER BY c.checkup_date DESC
        '''
        return self.execute_query(query)

    def update_checkup(self, checkup_id, patient_id, doctor_id, checkup_date, diagnosis, treatment, cost):
        query = '''
        UPDATE checkups 
        SET patient_id = ?, doctor_id = ?, checkup_date = ?, diagnosis = ?, 
            treatment = ?, cost = ?, updated_at = CURRENT_TIMESTAMP
        WHERE id = ?
        '''
        return self.execute_query(query, (patient_id, doctor_id, checkup_date, diagnosis, treatment, cost, checkup_id))

    def delete_checkup(self, checkup_id):
        query = '''
        UPDATE checkups 
        SET is_deleted = 1, updated_at = CURRENT_TIMESTAMP
        WHERE id = ?
        '''
        return self.execute_query(query, (checkup_id,))

    def update_appointment(self, appointment_id, patient_id, doctor_id, appointment_date, notes):
        query = '''
        UPDATE appointments 
        SET patient_id = ?, doctor_id = ?, appointment_date = ?, notes = ?, 
            updated_at = CURRENT_TIMESTAMP
        WHERE id = ?
        '''
        return self.execute_query(query, (patient_id, doctor_id, appointment_date, notes, appointment_id))

    def cancel_appointment(self, appointment_id):
        query = '''
        UPDATE appointments 
        SET status = 'cancelled', updated_at = CURRENT_TIMESTAMP
        WHERE id = ?
        '''
        return self.execute_query(query, (appointment_id,))

    def get_all_invoices(self):
        query = '''
        SELECT i.*, p.name as patient_name
        FROM invoices i
        JOIN patients p ON i.patient_id = p.id
        WHERE i.is_deleted = 0
        ORDER BY i.created_at DESC
        '''
        return self.execute_query(query)

    def update_invoice(self, invoice_id, patient_id, amount, description):
        query = '''
        UPDATE invoices 
        SET patient_id = ?, amount = ?, description = ?, updated_at = CURRENT_TIMESTAMP
        WHERE id = ?
        '''
        return self.execute_query(query, (patient_id, amount, description, invoice_id))

    def delete_invoice(self, invoice_id):
        query = '''
        UPDATE invoices 
        SET is_deleted = 1, updated_at = CURRENT_TIMESTAMP
        WHERE id = ?
        '''
        return self.execute_query(query, (invoice_id,))

    def get_all_expenses(self):
        query = '''
        SELECT * FROM expenses 
        WHERE is_deleted = 0
        ORDER BY expense_date DESC
        '''
        return self.execute_query(query)

    def update_expense(self, expense_id, amount, description, expense_date):
        query = '''
        UPDATE expenses 
        SET amount = ?, description = ?, expense_date = ?, updated_at = CURRENT_TIMESTAMP
        WHERE id = ?
        '''
        return self.execute_query(query, (amount, description, expense_date, expense_id))

    def delete_expense(self, expense_id):
        query = '''
        UPDATE expenses 
        SET is_deleted = 1, updated_at = CURRENT_TIMESTAMP
        WHERE id = ?
        '''
        return self.execute_query(query, (expense_id,))

    def insert_default_users(self):
        # Check if users table is empty
        self.cursor.execute("SELECT COUNT(*) FROM users")
        if self.cursor.fetchone()[0] == 0:
            # Default users with unique passwords
            default_users = [
                ('Ahmed', 'Dr@hmed2024', 'Doctor'),
                ('Mohamed', 'Dr@mohamed2024', 'Doctor'),
                ('Sarah', 'Sec@sarah2024', 'Secretary'),
                ('Nadine', 'Sec@nadine2024', 'Secretary')
            ]
            
            # Insert default users
            self.cursor.executemany(
                "INSERT INTO users (username, password, role) VALUES (?, ?, ?)",
                default_users
            )
            self.conn.commit() 