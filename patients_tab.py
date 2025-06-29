from PySide6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit,
                             QPushButton, QTableWidget, QTableWidgetItem, QMessageBox,
                             QDialog, QFormLayout, QSpinBox, QHeaderView)
from PySide6.QtCore import Qt
from database import Database
from functools import partial

class AddPatientDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.init_ui()

    def init_ui(self):
        self.setWindowTitle('إضافة مريض جديد')
        self.setMinimumWidth(400)
        layout = QFormLayout(self)

        self.name_input = QLineEdit()
        self.age_input = QSpinBox()
        self.age_input.setRange(0, 150)
        self.phone_input = QLineEdit()
        self.address_input = QLineEdit()

        layout.addRow('الاسم:', self.name_input)
        layout.addRow('العمر:', self.age_input)
        layout.addRow('رقم الهاتف:', self.phone_input)
        layout.addRow('العنوان:', self.address_input)

        buttons_layout = QHBoxLayout()
        save_button = QPushButton('حفظ')
        cancel_button = QPushButton('إلغاء')
        
        save_button.clicked.connect(self.accept)
        cancel_button.clicked.connect(self.reject)
        
        buttons_layout.addWidget(save_button)
        buttons_layout.addWidget(cancel_button)
        layout.addRow(buttons_layout)

class PatientsTab(QWidget):
    def __init__(self, db):
        super().__init__()
        self.db = db
        self.init_ui()
        self.load_patients()

    def init_ui(self):
        layout = QVBoxLayout(self)

        # Search bar
        search_layout = QHBoxLayout()
        self.search_input = QLineEdit()
        self.search_input.setPlaceholderText('بحث عن مريض...')
        self.search_input.textChanged.connect(self.search_patients)
        search_layout.addWidget(self.search_input)
        layout.addLayout(search_layout)

        # Add patient button
        add_button = QPushButton('إضافة مريض جديد')
        add_button.clicked.connect(self.add_patient)
        layout.addWidget(add_button)

        # Patients table
        self.table = QTableWidget()
        self.table.setColumnCount(7)
        self.table.setHorizontalHeaderLabels(['الرقم', 'الاسم', 'العمر', 'رقم الهاتف', 'العنوان', 'الرصيد', 'العمليات'])
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
        self.delete_button = QPushButton('حذف')
        
        self.edit_button.clicked.connect(self.edit_patient)
        self.delete_button.clicked.connect(self.delete_patient)
        
        buttons_layout.addWidget(self.edit_button)
        buttons_layout.addWidget(self.delete_button)
        layout.addLayout(buttons_layout)

    def load_patients(self):
        patients = self.db.get_all_patients()
        self.table.setRowCount(len(patients))
        
        for row, patient in enumerate(patients):
            self.table.setItem(row, 0, QTableWidgetItem(str(patient[0])))
            self.table.setItem(row, 1, QTableWidgetItem(patient[1]))
            self.table.setItem(row, 2, QTableWidgetItem(str(patient[2])))
            self.table.setItem(row, 3, QTableWidgetItem(patient[3]))
            self.table.setItem(row, 4, QTableWidgetItem(patient[4]))
            self.table.setItem(row, 5, QTableWidgetItem(str(patient[5])))

            # Operations column
            ops_widget = QWidget()
            ops_layout = QHBoxLayout(ops_widget)
            ops_layout.setContentsMargins(0, 0, 0, 0)
            ops_layout.setSpacing(5)
            btn_checkups = QPushButton('عرض السجل')
            btn_appointments = QPushButton('عرض المواعيد')
            btn_checkups.clicked.connect(partial(self.show_patient_checkups, patient[0], patient[1]))
            btn_appointments.clicked.connect(partial(self.show_patient_appointments, patient[0], patient[1]))
            ops_layout.addWidget(btn_checkups)
            ops_layout.addWidget(btn_appointments)
            ops_layout.addStretch()
            self.table.setCellWidget(row, 6, ops_widget)

    def search_patients(self):
        search_text = self.search_input.text().lower()
        for row in range(self.table.rowCount()):
            show_row = False
            for col in range(self.table.columnCount()):
                item = self.table.item(row, col)
                if item and search_text in item.text().lower():
                    show_row = True
                    break
            self.table.setRowHidden(row, not show_row)

    def add_patient(self):
        dialog = AddPatientDialog(self)
        if dialog.exec_():
            name = dialog.name_input.text()
            age = dialog.age_input.value()
            phone = dialog.phone_input.text()
            address = dialog.address_input.text()

            if not name:
                QMessageBox.warning(self, 'خطأ', 'الرجاء إدخال اسم المريض')
                return

            self.db.add_patient(name, age, phone, address)
            self.load_patients()

    def edit_patient(self):
        selected_rows = self.table.selectedItems()
        if not selected_rows:
            QMessageBox.warning(self, 'خطأ', 'الرجاء اختيار مريض للتعديل')
            return

        row = selected_rows[0].row()
        patient_id = int(self.table.item(row, 0).text())
        name = self.table.item(row, 1).text()
        age = int(self.table.item(row, 2).text())
        phone = self.table.item(row, 3).text()
        address = self.table.item(row, 4).text()

        dialog = AddPatientDialog(self)
        dialog.name_input.setText(name)
        dialog.age_input.setValue(age)
        dialog.phone_input.setText(phone)
        dialog.address_input.setText(address)

        if dialog.exec_():
            name = dialog.name_input.text()
            age = dialog.age_input.value()
            phone = dialog.phone_input.text()
            address = dialog.address_input.text()

            if not name:
                QMessageBox.warning(self, 'خطأ', 'الرجاء إدخال اسم المريض')
                return

            self.db.update_patient(patient_id, name, age, phone, address)
            self.load_patients()

    def delete_patient(self):
        selected_rows = self.table.selectedItems()
        if not selected_rows:
            QMessageBox.warning(self, 'خطأ', 'الرجاء اختيار مريض للحذف')
            return

        reply = QMessageBox.question(self, 'تأكيد الحذف',
                                   'هل أنت متأكد من رغبتك في حذف هذا المريض؟',
                                   QMessageBox.Yes | QMessageBox.No,
                                   QMessageBox.No)

        if reply == QMessageBox.Yes:
            row = selected_rows[0].row()
            patient_id = int(self.table.item(row, 0).text())
            self.db.delete_patient(patient_id)
            self.load_patients()

    def show_patient_checkups(self, patient_id, patient_name):
        checkups = self.db.execute_query('''
            SELECT checkup_date, diagnosis, treatment, cost, is_paid
            FROM checkups
            WHERE patient_id = ? AND is_deleted = 0
            ORDER BY checkup_date DESC
        ''', (patient_id,))
        dialog = QDialog(self)
        dialog.setWindowTitle(f'سجل الكشوفات للمريض: {patient_name}')
        dialog.setMinimumWidth(600)
        layout = QVBoxLayout(dialog)
        table = QTableWidget()
        table.setColumnCount(5)
        table.setHorizontalHeaderLabels(['التاريخ', 'التشخيص', 'العلاج', 'التكلفة', 'حالة الدفع'])
        table.setRowCount(len(checkups))
        for row, c in enumerate(checkups):
            table.setItem(row, 0, QTableWidgetItem(str(c[0])))
            table.setItem(row, 1, QTableWidgetItem(c[1]))
            table.setItem(row, 2, QTableWidgetItem(c[2]))
            table.setItem(row, 3, QTableWidgetItem(str(c[3])))
            table.setItem(row, 4, QTableWidgetItem('مدفوع' if c[4] else 'غير مدفوع'))
        layout.addWidget(table)
        close_btn = QPushButton('إغلاق')
        close_btn.clicked.connect(dialog.accept)
        layout.addWidget(close_btn)
        dialog.exec_()

    def show_patient_appointments(self, patient_id, patient_name):
        appointments = self.db.execute_query('''
            SELECT appointment_date, status, notes
            FROM appointments
            WHERE patient_id = ? AND is_deleted = 0
            ORDER BY appointment_date DESC
        ''', (patient_id,))
        dialog = QDialog(self)
        dialog.setWindowTitle(f'مواعيد المريض: {patient_name}')
        dialog.setMinimumWidth(600)
        layout = QVBoxLayout(dialog)
        table = QTableWidget()
        table.setColumnCount(3)
        table.setHorizontalHeaderLabels(['التاريخ والوقت', 'الحالة', 'ملاحظات'])
        table.setRowCount(len(appointments))
        for row, a in enumerate(appointments):
            table.setItem(row, 0, QTableWidgetItem(str(a[0])))
            table.setItem(row, 1, QTableWidgetItem(a[1]))
            table.setItem(row, 2, QTableWidgetItem(a[2]))
        layout.addWidget(table)
        close_btn = QPushButton('إغلاق')
        close_btn.clicked.connect(dialog.accept)
        layout.addWidget(close_btn)
        dialog.exec_() 