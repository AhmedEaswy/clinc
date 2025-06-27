from PySide6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit,
                             QPushButton, QTableWidget, QTableWidgetItem, QMessageBox,
                             QDialog, QFormLayout, QDateTimeEdit, QComboBox, QTextEdit,
                             QDoubleSpinBox)
from PySide6.QtCore import Qt, QDateTime
from database import Database

class AddCheckupDialog(QDialog):
    def __init__(self, db, parent=None):
        super().__init__(parent)
        self.db = db
        self.init_ui()

    def init_ui(self):
        self.setWindowTitle('إضافة كشف جديد')
        self.setMinimumWidth(500)
        layout = QFormLayout(self)

        # Patient selection
        self.patient_combo = QComboBox()
        self.load_patients()
        layout.addRow('المريض:', self.patient_combo)

        # Date and time selection
        self.datetime_input = QDateTimeEdit()
        self.datetime_input.setDateTime(QDateTime.currentDateTime())
        self.datetime_input.setCalendarPopup(True)
        layout.addRow('التاريخ والوقت:', self.datetime_input)

        # Diagnosis
        self.diagnosis_input = QTextEdit()
        layout.addRow('التشخيص:', self.diagnosis_input)

        # Treatment
        self.treatment_input = QTextEdit()
        layout.addRow('العلاج:', self.treatment_input)

        # Cost
        self.cost_input = QDoubleSpinBox()
        self.cost_input.setRange(0, 1000000)
        self.cost_input.setSuffix(' جنيه')
        layout.addRow('التكلفة:', self.cost_input)

        # Payment status
        self.payment_status = QComboBox()
        self.payment_status.addItems(['مدفوع', 'غير مدفوع'])
        layout.addRow('حالة الدفع:', self.payment_status)

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

class CheckupsTab(QWidget):
    def __init__(self, db):
        super().__init__()
        self.db = db
        self.init_ui()
        self.load_checkups()

    def init_ui(self):
        layout = QVBoxLayout(self)

        # Search bar
        search_layout = QHBoxLayout()
        self.search_input = QLineEdit()
        self.search_input.setPlaceholderText('بحث عن كشف...')
        self.search_input.textChanged.connect(self.search_checkups)
        search_layout.addWidget(self.search_input)
        layout.addLayout(search_layout)

        # Add checkup button
        add_button = QPushButton('إضافة كشف جديد')
        add_button.clicked.connect(self.add_checkup)
        layout.addWidget(add_button)

        # Checkups table
        self.table = QTableWidget()
        self.table.setColumnCount(8)
        self.table.setHorizontalHeaderLabels(['الرقم', 'المريض', 'الطبيب', 'التاريخ', 'التشخيص', 'العلاج', 'التكلفة', 'حالة الدفع'])
        self.table.setSelectionBehavior(QTableWidget.SelectRows)
        self.table.setEditTriggers(QTableWidget.NoEditTriggers)
        layout.addWidget(self.table)

        # Action buttons
        buttons_layout = QHBoxLayout()
        self.edit_button = QPushButton('تعديل')
        self.delete_button = QPushButton('حذف')
        self.mark_paid_button = QPushButton('تحديد كمدفوع')
        
        self.edit_button.clicked.connect(self.edit_checkup)
        self.delete_button.clicked.connect(self.delete_checkup)
        self.mark_paid_button.clicked.connect(self.mark_as_paid)
        
        buttons_layout.addWidget(self.edit_button)
        buttons_layout.addWidget(self.delete_button)
        buttons_layout.addWidget(self.mark_paid_button)
        layout.addLayout(buttons_layout)

    def load_checkups(self):
        checkups = self.db.get_all_checkups()
        self.table.setRowCount(len(checkups))
        
        for row, checkup in enumerate(checkups):
            self.table.setItem(row, 0, QTableWidgetItem(str(checkup[0])))
            self.table.setItem(row, 1, QTableWidgetItem(checkup[8]))  # patient_name
            self.table.setItem(row, 2, QTableWidgetItem(checkup[9]))  # doctor_name
            self.table.setItem(row, 3, QTableWidgetItem(str(checkup[3])))
            self.table.setItem(row, 4, QTableWidgetItem(checkup[4]))
            self.table.setItem(row, 5, QTableWidgetItem(checkup[5]))
            self.table.setItem(row, 6, QTableWidgetItem(str(checkup[6])))
            self.table.setItem(row, 7, QTableWidgetItem('مدفوع' if checkup[7] else 'غير مدفوع'))

    def search_checkups(self):
        search_text = self.search_input.text().lower()
        for row in range(self.table.rowCount()):
            show_row = False
            for col in range(self.table.columnCount()):
                item = self.table.item(row, col)
                if item and search_text in item.text().lower():
                    show_row = True
                    break
            self.table.setRowHidden(row, not show_row)

    def add_checkup(self):
        dialog = AddCheckupDialog(self.db, self)
        if dialog.exec_():
            patient_id = dialog.patient_combo.currentData()
            checkup_date = dialog.datetime_input.dateTime().toString('yyyy-MM-dd HH:mm:ss')
            diagnosis = dialog.diagnosis_input.toPlainText()
            treatment = dialog.treatment_input.toPlainText()
            cost = dialog.cost_input.value()
            is_paid = dialog.payment_status.currentText() == 'مدفوع'
            doctor_id = 1  # Assuming the current user is the doctor

            self.db.add_checkup(patient_id, doctor_id, checkup_date, diagnosis, treatment, cost)
            if is_paid:
                self.db.mark_checkup_as_paid(patient_id, cost)
            self.load_checkups()

    def edit_checkup(self):
        selected_rows = self.table.selectedItems()
        if not selected_rows:
            QMessageBox.warning(self, 'خطأ', 'الرجاء اختيار كشف للتعديل')
            return

        row = selected_rows[0].row()
        checkup_id = int(self.table.item(row, 0).text())
        
        dialog = AddCheckupDialog(self.db, self)
        # Set current values
        current_patient = self.table.item(row, 1).text()
        current_datetime = QDateTime.fromString(self.table.item(row, 3).text(), 'yyyy-MM-dd HH:mm:ss')
        current_diagnosis = self.table.item(row, 4).text()
        current_treatment = self.table.item(row, 5).text()
        current_cost = float(self.table.item(row, 6).text())
        current_payment_status = self.table.item(row, 7).text()

        dialog.patient_combo.setCurrentText(current_patient)
        dialog.datetime_input.setDateTime(current_datetime)
        dialog.diagnosis_input.setText(current_diagnosis)
        dialog.treatment_input.setText(current_treatment)
        dialog.cost_input.setValue(current_cost)
        dialog.payment_status.setCurrentText(current_payment_status)

        if dialog.exec_():
            patient_id = dialog.patient_combo.currentData()
            checkup_date = dialog.datetime_input.dateTime().toString('yyyy-MM-dd HH:mm:ss')
            diagnosis = dialog.diagnosis_input.toPlainText()
            treatment = dialog.treatment_input.toPlainText()
            cost = dialog.cost_input.value()
            is_paid = dialog.payment_status.currentText() == 'مدفوع'
            doctor_id = 1  # Assuming the current user is the doctor

            self.db.update_checkup(checkup_id, patient_id, doctor_id, checkup_date, diagnosis, treatment, cost)
            if is_paid:
                self.db.mark_checkup_as_paid(patient_id, cost)
            self.load_checkups()

    def delete_checkup(self):
        selected_rows = self.table.selectedItems()
        if not selected_rows:
            QMessageBox.warning(self, 'خطأ', 'الرجاء اختيار كشف للحذف')
            return

        reply = QMessageBox.question(self, 'تأكيد الحذف',
                                   'هل أنت متأكد من رغبتك في حذف هذا الكشف؟',
                                   QMessageBox.Yes | QMessageBox.No,
                                   QMessageBox.No)

        if reply == QMessageBox.Yes:
            row = selected_rows[0].row()
            checkup_id = int(self.table.item(row, 0).text())
            self.db.delete_checkup(checkup_id)
            self.load_checkups()

    def mark_as_paid(self):
        selected_rows = self.table.selectedItems()
        if not selected_rows:
            QMessageBox.warning(self, 'خطأ', 'الرجاء اختيار كشف لتحديده كمدفوع')
            return

        row = selected_rows[0].row()
        checkup_id = int(self.table.item(row, 0).text())
        patient_id = self.db.get_checkup_patient_id(checkup_id)
        cost = float(self.table.item(row, 6).text())

        self.db.mark_checkup_as_paid(patient_id, cost)
        self.load_checkups() 