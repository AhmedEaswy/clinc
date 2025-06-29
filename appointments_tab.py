from PySide6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit,
                             QPushButton, QTableWidget, QTableWidgetItem, QMessageBox,
                             QDialog, QFormLayout, QDateTimeEdit, QComboBox, QTextEdit, QHeaderView)
from PySide6.QtCore import Qt, QDateTime
from database import Database

class AddAppointmentDialog(QDialog):
    def __init__(self, db, parent=None):
        super().__init__(parent)
        self.db = db
        self.init_ui()

    def init_ui(self):
        self.setWindowTitle('إضافة موعد جديد')
        self.setMinimumWidth(400)
        layout = QFormLayout(self)

        # Patient selection
        self.patient_combo = QComboBox()
        self.load_patients()
        layout.addRow('المريض:', self.patient_combo)

        # Date and time selection
        self.datetime_input = QDateTimeEdit()
        self.datetime_input.setDateTime(QDateTime.currentDateTime())
        self.datetime_input.setCalendarPopup(True)
        self.datetime_input.setStyleSheet("background-color: white;")
        layout.addRow('التاريخ والوقت:', self.datetime_input)

        # Type selection
        self.type_combo = QComboBox()
        self.type_combo.addItems(['جراحة', 'كشف', 'استشارة'])
        layout.addRow('نوع الموعد:', self.type_combo)

        # Notes
        self.notes_input = QTextEdit()
        layout.addRow('ملاحظات:', self.notes_input)

        # Buttons
        buttons_layout = QHBoxLayout()
        save_button = QPushButton('حفظ')
        cancel_button = QPushButton('إلغاء')
        
        save_button.clicked.connect(self.accept)
        cancel_button.clicked.connect(self.reject)
        
        buttons_layout.addWidget(save_button)
        buttons_layout.addWidget(cancel_button)
        layout.addRow(buttons_layout)

    def load_patients(self):
        patients = self.db.get_all_patients()
        for patient in patients:
            self.patient_combo.addItem(patient[1], patient[0])

class AppointmentsTab(QWidget):
    def __init__(self, db):
        super().__init__()
        self.db = db
        self.init_ui()
        self.load_appointments()

    def init_ui(self):
        layout = QVBoxLayout(self)

        # Search bar
        search_layout = QHBoxLayout()
        self.search_input = QLineEdit()
        self.search_input.setPlaceholderText('بحث عن موعد...')
        self.search_input.textChanged.connect(self.search_appointments)
        search_layout.addWidget(self.search_input)
        layout.addLayout(search_layout)

        # Add appointment button
        add_button = QPushButton('إضافة موعد جديد')
        add_button.clicked.connect(self.add_appointment)
        layout.addWidget(add_button)

        # Appointments table
        self.table = QTableWidget()
        self.table.setColumnCount(4)
        self.table.setHorizontalHeaderLabels(['الرقم', 'المريض', 'التاريخ والوقت', 'ملاحظات'])
        self.table.setSelectionBehavior(QTableWidget.SelectRows)
        self.table.setEditTriggers(QTableWidget.NoEditTriggers)
        self.table.verticalHeader().setDefaultSectionSize(60)  # Set minimum row height
        self.table.horizontalHeader().setMinimumSectionSize(120)  # Set minimum column width
        self.table.horizontalHeader().setStretchLastSection(True)
        # self.table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeToContents)
        # self.table.verticalHeader().setSectionResizeMode(QHeaderView.ResizeToContents)
        layout.addWidget(self.table)

        # Action buttons
        buttons_layout = QHBoxLayout()
        self.edit_button = QPushButton('تعديل')
        self.cancel_button = QPushButton('إلغاء الموعد')
        
        self.edit_button.clicked.connect(self.edit_appointment)
        self.cancel_button.clicked.connect(self.cancel_appointment)
        
        buttons_layout.addWidget(self.edit_button)
        buttons_layout.addWidget(self.cancel_button)
        layout.addLayout(buttons_layout)

    def load_appointments(self):
        appointments = self.db.get_all_appointments()
        self.table.setRowCount(len(appointments))
        for row, appointment in enumerate(appointments):
            self.table.setItem(row, 0, QTableWidgetItem(str(appointment[0])))  # id
            self.table.setItem(row, 1, QTableWidgetItem(appointment[9]))      # patient_name
            self.table.setItem(row, 2, QTableWidgetItem(str(appointment[3]))) # appointment_date
            self.table.setItem(row, 3, QTableWidgetItem(appointment[5]))      # notes

    def search_appointments(self):
        search_text = self.search_input.text().lower()
        for row in range(self.table.rowCount()):
            show_row = False
            for col in range(self.table.columnCount()):
                item = self.table.item(row, col)
                if item and search_text in item.text().lower():
                    show_row = True
                    break
            self.table.setRowHidden(row, not show_row)

    def add_appointment(self):
        dialog = AddAppointmentDialog(self.db, self)
        if dialog.exec_():
            patient_id = dialog.patient_combo.currentData()
            appointment_date = dialog.datetime_input.dateTime().toString('yyyy-MM-dd HH:mm:ss')
            appt_type = dialog.type_combo.currentText()
            notes = dialog.notes_input.toPlainText()
            doctor_id = 1  # Assuming the current user is the doctor

            # Add appointment with type in notes (or extend DB if needed)
            self.db.add_appointment(patient_id, doctor_id, appointment_date, f'نوع: {appt_type}\n{notes}')
            # Add invoice for this appointment
            description = f'موعد {appt_type} للمريض رقم {patient_id}'
            self.db.add_invoice(patient_id, 0, description)
            self.load_appointments()

    def edit_appointment(self):
        selected_rows = self.table.selectedItems()
        if not selected_rows:
            QMessageBox.warning(self, 'خطأ', 'الرجاء اختيار موعد للتعديل')
            return

        row = selected_rows[0].row()
        appointment_id = int(self.table.item(row, 0).text())
        
        dialog = AddAppointmentDialog(self.db, self)
        # Set current values
        current_patient = self.table.item(row, 1).text()
        current_datetime = QDateTime.fromString(self.table.item(row, 2).text(), 'yyyy-MM-dd HH:mm:ss')
        current_notes = self.table.item(row, 4).text()

        dialog.patient_combo.setCurrentText(current_patient)
        dialog.datetime_input.setDateTime(current_datetime)
        dialog.notes_input.setText(current_notes)

        if dialog.exec_():
            patient_id = dialog.patient_combo.currentData()
            appointment_date = dialog.datetime_input.dateTime().toString('yyyy-MM-dd HH:mm:ss')
            notes = dialog.notes_input.toPlainText()
            doctor_id = 1  # Assuming the current user is the doctor

            self.db.update_appointment(appointment_id, patient_id, doctor_id, appointment_date, notes)
            self.load_appointments()

    def cancel_appointment(self):
        selected_rows = self.table.selectedItems()
        if not selected_rows:
            QMessageBox.warning(self, 'خطأ', 'الرجاء اختيار موعد للإلغاء')
            return

        reply = QMessageBox.question(self, 'تأكيد الإلغاء',
                                   'هل أنت متأكد من رغبتك في إلغاء هذا الموعد؟',
                                   QMessageBox.Yes | QMessageBox.No,
                                   QMessageBox.No)

        if reply == QMessageBox.Yes:
            row = selected_rows[0].row()
            appointment_id = int(self.table.item(row, 0).text())
            self.db.cancel_appointment(appointment_id)
            self.load_appointments() 