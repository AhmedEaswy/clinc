# UI Modules & Tabs: Clinic Management System

This document describes each UI module/tab, its purpose, and its main features for AI and developer reference.

## Main Window
- **main_window.py**: Hosts the main application window after login. Contains all tabs and manages user session and logout.

## Tabs

### Dashboard (dashboard_tab.py)
- Shows today's patient stats, waiting list, and checked patients.
- Quick actions: add patient, call next patient.
- Auto-refreshes waiting list and stats.

### Patients (patients_tab.py)
- Add, edit, delete, and search patient records.
- Soft-deletion (move to Trash) and restore.
- Table view of all patients with details.

### Appointments (appointments_tab.py)
- Schedule, update, cancel, and search appointments.
- Table view of all appointments with patient and doctor info.
- Soft-deletion and restore.

### Checkups (checkups_tab.py)
- Record, edit, delete, and search checkups.
- Add diagnosis, treatment, cost, and payment status.
- Mark checkups as paid.
- Table view of all checkups.

### Invoices (invoices_tab.py)
- Create, edit, delete, and search invoices.
- Mark invoices as paid.
- Table view of all invoices with payment status.

### Expenses (expenses_tab.py)
- Add, edit, delete, and search clinic expenses.
- Table view of all expenses.

### Cash Management (cash_tab.py)
- View, filter, and print cash transactions.
- See current balance and transaction history.
- Filter by date and type (income/expense).

### Trash (trash_tab.py)
- View, restore, or permanently delete soft-deleted records (patients, appointments, checkups, invoices, expenses).
- Only visible to users with the Doctor role.

## Custom Widgets (custom_widgets.py)
- Enhanced line edits, combo boxes, spin boxes, and buttons for better keyboard navigation and consistent styling.

---

For more details, see the corresponding Python files for each tab. 