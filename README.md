# Clinic Management System

A desktop application for managing clinic operations, built with Python and PySide6. The system supports patient management, appointments, checkups, invoices, expenses, cash transactions, and more, with a user-friendly interface and role-based access (Doctor/Secretary).

## Features

- **User Authentication**: Login system with roles (Doctor, Secretary).
- **Dashboard**: Overview of today's patients, waiting list, and checked patients.
- **Patient Management**: Add, edit, delete, and restore patient records.
- **Appointments**: Schedule, update, and cancel appointments.
- **Checkups**: Record checkups, diagnoses, treatments, and payment status.
- **Invoices**: Create and manage invoices for patients.
- **Expenses**: Track clinic expenses with descriptions and dates.
- **Cash Management**: View and filter cash transactions, see current balance.
- **Trash**: Soft-delete and restore records for patients, appointments, checkups, invoices, and expenses.
- **Modern UI**: Clean, right-to-left interface with custom widgets and styles.

## Installation

1. Clone the repository and navigate to the project directory.
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Run the application:
   ```bash
   python main.py
   ```

## Usage

- On launch, log in as a Doctor or Secretary (default users are pre-created).
- Navigate between tabs: Dashboard, Patients, Appointments, Checkups, Invoices, Expenses, Cash, and Trash (Doctors only).
- Add, edit, or delete records as needed. Deleted records go to Trash and can be restored or permanently deleted.

## Default Users

| Username | Password   | Role      |
|----------|------------|-----------|
| Ahmed    | 1234       | Doctor    |
| Mohamed  | 0000       | Doctor    |
| Sarah    | 1122       | Secretary |
| Nadine   | 1112       | Secretary |
| admin    | admin123   | Doctor    |

## Database Schema

The application uses SQLite (clinic.db) with the following main tables:

- **users**: id, username, password, role, created_at, updated_at
- **patients**: id, name, age, phone, address, balance, created_at, updated_at, is_deleted
- **appointments**: id, patient_id, doctor_id, appointment_date, status, notes, created_at, updated_at, is_deleted
- **checkups**: id, patient_id, doctor_id, checkup_date, diagnosis, treatment, cost, is_paid, created_at, updated_at, is_deleted
- **invoices**: id, patient_id, amount, description, is_paid, created_at, updated_at, is_deleted
- **expenses**: id, amount, description, expense_date, created_at, updated_at, is_deleted
- **cash_transactions**: id, type, amount, description, reference_id, reference_type, transaction_date, created_at, updated_at

## Customization

- **Styles**: Modify `styles.py` for color palette and UI styles.
- **Default Users**: Change or add users in `database.py` initialization.

## Requirements

- Python 3.8+
- PySide6==6.6.1
- python-dateutil==2.8.2

## License

This project is for educational and internal use. Please contact the author for other uses.
