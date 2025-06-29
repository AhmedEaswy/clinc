# Database Schema: Clinic Management System

This document describes the SQLite database schema, main tables, and their relationships for AI and developer reference.

## Main Tables

- **users**
  - `id` (INTEGER, PK)
  - `username` (TEXT, UNIQUE, NOT NULL)
  - `password` (TEXT, NOT NULL)
  - `role` (TEXT, NOT NULL) — 'Doctor' or 'Secretary'
  - `created_at` (TIMESTAMP)
  - `updated_at` (TIMESTAMP)

- **patients**
  - `id` (INTEGER, PK)
  - `name` (TEXT, NOT NULL)
  - `age` (INTEGER)
  - `phone` (TEXT)
  - `address` (TEXT)
  - `balance` (REAL, DEFAULT 0)
  - `created_at` (TIMESTAMP)
  - `updated_at` (TIMESTAMP)
  - `is_deleted` (INTEGER, DEFAULT 0)

- **appointments**
  - `id` (INTEGER, PK)
  - `patient_id` (INTEGER, FK → patients.id)
  - `doctor_id` (INTEGER, FK → users.id)
  - `appointment_date` (TIMESTAMP)
  - `status` (TEXT, DEFAULT 'scheduled')
  - `notes` (TEXT)
  - `created_at` (TIMESTAMP)
  - `updated_at` (TIMESTAMP)
  - `is_deleted` (INTEGER, DEFAULT 0)

- **checkups**
  - `id` (INTEGER, PK)
  - `patient_id` (INTEGER, FK → patients.id)
  - `doctor_id` (INTEGER, FK → users.id)
  - `checkup_date` (TIMESTAMP)
  - `diagnosis` (TEXT)
  - `treatment` (TEXT)
  - `cost` (REAL)
  - `is_paid` (INTEGER, DEFAULT 0)
  - `created_at` (TIMESTAMP)
  - `updated_at` (TIMESTAMP)
  - `is_deleted` (INTEGER, DEFAULT 0)

- **invoices**
  - `id` (INTEGER, PK)
  - `patient_id` (INTEGER, FK → patients.id)
  - `amount` (REAL)
  - `description` (TEXT)
  - `is_paid` (INTEGER, DEFAULT 0)
  - `created_at` (TIMESTAMP)
  - `updated_at` (TIMESTAMP)
  - `is_deleted` (INTEGER, DEFAULT 0)

- **expenses**
  - `id` (INTEGER, PK)
  - `amount` (REAL)
  - `description` (TEXT)
  - `expense_date` (TIMESTAMP)
  - `created_at` (TIMESTAMP)
  - `updated_at` (TIMESTAMP)
  - `is_deleted` (INTEGER, DEFAULT 0)

- **cash_transactions**
  - `id` (INTEGER, PK)
  - `type` (TEXT) — 'income' or 'expense'
  - `amount` (REAL)
  - `description` (TEXT)
  - `reference_id` (INTEGER) — links to checkup, invoice, or expense
  - `reference_type` (TEXT) — 'checkup', 'invoice', or 'expense'
  - `transaction_date` (TIMESTAMP)
  - `created_at` (TIMESTAMP)
  - `updated_at` (TIMESTAMP)

## Relationships

- Each **appointment** links a patient and a doctor.
- Each **checkup** links a patient and a doctor.
- Each **invoice** links to a patient.
- Each **cash transaction** can reference a checkup, invoice, or expense.

## Soft Deletion

- The `is_deleted` field in most tables allows for soft deletion (records are hidden but not removed).
- The Trash tab in the UI allows restoring or permanently deleting these records.

---

For more details, see `database.py` and the UI tabs that interact with these tables. 