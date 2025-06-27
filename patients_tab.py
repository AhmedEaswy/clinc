from PySide6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit,
                             QPushButton, QTableWidget, QTableWidgetItem, QMessageBox,
                             QDialog, QFormLayout, QSpinBox)
from PySide6.QtCore import Qt
from database import Database

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
        self.table.setColumnCount(6)
        self.table.setHorizontalHeaderLabels(['الرقم', 'الاسم', 'العمر', 'رقم الهاتف', 'العنوان', 'الرصيد'])
        self.table.setSelectionBehavior(QTableWidget.SelectRows)
        self.table.setEditTriggers(QTableWidget.NoEditTriggers)
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