# Project Structure: Clinic Management System

This document provides an overview of the project structure, main modules, and their purposes to help AI systems and developers understand the codebase.

## Main Files and Their Roles

- **main.py**: Application entry point. Initializes the Qt application, sets the style, and launches the login window.
- **login.py**: Implements the login window, user authentication, and role selection (Doctor/Secretary).
- **main_window.py**: The main application window after login. Organizes the app into tabs (Dashboard, Patients, Appointments, Checkups, Invoices, Expenses, Cash, Trash) and manages user session and logout.
- **database.py**: Handles all database operations using SQLite. Defines the schema, CRUD operations, and soft-deletion logic for all entities.
- **custom_widgets.py**: Defines custom Qt widgets (e.g., line edits, combo boxes, buttons) with enhanced keyboard navigation and styling.
- **styles.py**: Central stylesheet and color palette for the application. Provides functions for consistent UI styling.
- **dashboard_tab.py**: Implements the dashboard tab, showing today's stats, waiting list, and quick actions.
- **patients_tab.py**: Manages patient records (add, edit, delete, search, restore).
- **appointments_tab.py**: Manages appointments (schedule, update, cancel, search).
- **checkups_tab.py**: Manages checkups (record, edit, delete, mark as paid, search).
- **invoices_tab.py**: Manages invoices (create, edit, delete, mark as paid, search).
- **expenses_tab.py**: Manages clinic expenses (add, edit, delete, search).
- **cash_tab.py**: Manages cash transactions, filters, and balance display.
- **trash_tab.py**: Allows restoring or permanently deleting soft-deleted records (patients, appointments, checkups, invoices, expenses).
- **clinic.db**: SQLite database file storing all persistent data.
- **requirements.txt**: Python dependencies for the project.
- **README.md**: Main documentation and usage guide.

## Directory Layout

```
clinc-app/
  main.py
  login.py
  main_window.py
  database.py
  custom_widgets.py
  styles.py
  dashboard_tab.py
  patients_tab.py
  appointments_tab.py
  checkups_tab.py
  invoices_tab.py
  expenses_tab.py
  cash_tab.py
  trash_tab.py
  clinic.db
  requirements.txt
  README.md
```

## Data Flow

- User launches `main.py` → Login window (`login.py`) → On success, main window (`main_window.py`) with tabs.
- Each tab is a separate module and interacts with the database via `database.py`.
- UI styling is managed by `styles.py` and custom widgets in `custom_widgets.py`.

---

For more details, see the individual module documentation files. 