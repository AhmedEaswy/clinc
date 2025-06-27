from PySide6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit,
                             QPushButton, QTableWidget, QTableWidgetItem, QMessageBox,
                             QDialog, QFormLayout, QDateTimeEdit, QComboBox, QTextEdit,
                             QDoubleSpinBox)
from PySide6.QtCore import Qt, QDateTime
from database import Database

class AddInvoiceDialog(QDialog):
    def __init__(self, db, parent=None):
        super().__init__(parent)
        self.db = db
        self.init_ui()

    def init_ui(self):
        self.setWindowTitle('إضافة فاتورة جديدة')
        self.setMinimumWidth(400)
        layout = QFormLayout(self)

        # Patient selection
        self.patient_combo = QComboBox()
        self.load_patients()
        layout.addRow('المريض:', self.patient_combo)

        # Amount
        self.amount_input = QDoubleSpinBox()
        self.amount_input.setRange(0, 1000000)
        self.amount_input.setSuffix(' جنيه')
        layout.addRow('المبلغ:', self.amount_input)

        # Description
        self.description_input = QTextEdit()
        layout.addRow('الوصف:', self.description_input)

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

class InvoicesTab(QWidget):
    def __init__(self, db):
        super().__init__()
        self.db = db
        self.init_ui()
        self.load_invoices()

    def init_ui(self):
        layout = QVBoxLayout(self)

        # Search bar
        search_layout = QHBoxLayout()
        self.search_input = QLineEdit()
        self.search_input.setPlaceholderText('بحث عن فاتورة...')
        self.search_input.textChanged.connect(self.search_invoices)
        search_layout.addWidget(self.search_input)
        layout.addLayout(search_layout)

        # Add invoice button
        add_button = QPushButton('إضافة فاتورة جديدة')
        add_button.clicked.connect(self.add_invoice)
        layout.addWidget(add_button)

        # Invoices table
        self.table = QTableWidget()
        self.table.setColumnCount(6)
        self.table.setHorizontalHeaderLabels(['الرقم', 'المريض', 'المبلغ', 'الوصف', 'حالة الدفع', 'تاريخ الإنشاء'])
        self.table.setSelectionBehavior(QTableWidget.SelectRows)
        self.table.setEditTriggers(QTableWidget.NoEditTriggers)
        layout.addWidget(self.table)

        # Action buttons
        buttons_layout = QHBoxLayout()
        self.edit_button = QPushButton('تعديل')
        self.delete_button = QPushButton('حذف')
        self.mark_paid_button = QPushButton('تحديد كمدفوع')
        
        self.edit_button.clicked.connect(self.edit_invoice)
        self.delete_button.clicked.connect(self.delete_invoice)
        self.mark_paid_button.clicked.connect(self.mark_as_paid)
        
        buttons_layout.addWidget(self.edit_button)
        buttons_layout.addWidget(self.delete_button)
        buttons_layout.addWidget(self.mark_paid_button)
        layout.addLayout(buttons_layout)

    def load_invoices(self):
        invoices = self.db.get_all_invoices()
        self.table.setRowCount(len(invoices))
        
        for row, invoice in enumerate(invoices):
            self.table.setItem(row, 0, QTableWidgetItem(str(invoice[0])))
            self.table.setItem(row, 1, QTableWidgetItem(invoice[5]))  # patient_name
            self.table.setItem(row, 2, QTableWidgetItem(str(invoice[2])))
            self.table.setItem(row, 3, QTableWidgetItem(invoice[3]))
            self.table.setItem(row, 4, QTableWidgetItem('مدفوع' if invoice[4] else 'غير مدفوع'))
            self.table.setItem(row, 5, QTableWidgetItem(str(invoice[6])))

    def search_invoices(self):
        search_text = self.search_input.text().lower()
        for row in range(self.table.rowCount()):
            show_row = False
            for col in range(self.table.columnCount()):
                item = self.table.item(row, col)
                if item and search_text in item.text().lower():
                    show_row = True
                    break
            self.table.setRowHidden(row, not show_row)

    def add_invoice(self):
        dialog = AddInvoiceDialog(self.db, self)
        if dialog.exec_():
            patient_id = dialog.patient_combo.currentData()
            amount = dialog.amount_input.value()
            description = dialog.description_input.toPlainText()
            is_paid = dialog.payment_status.currentText() == 'مدفوع'

            self.db.add_invoice(patient_id, amount, description)
            if is_paid:
                self.db.mark_invoice_as_paid(patient_id, amount)
            self.load_invoices()

    def edit_invoice(self):
        selected_rows = self.table.selectedItems()
        if not selected_rows:
            QMessageBox.warning(self, 'خطأ', 'الرجاء اختيار فاتورة للتعديل')
            return

        row = selected_rows[0].row()
        invoice_id = int(self.table.item(row, 0).text())
        
        dialog = AddInvoiceDialog(self.db, self)
        # Set current values
        current_patient = self.table.item(row, 1).text()
        current_amount = float(self.table.item(row, 2).text())
        current_description = self.table.item(row, 3).text()
        current_payment_status = self.table.item(row, 4).text()

        dialog.patient_combo.setCurrentText(current_patient)
        dialog.amount_input.setValue(current_amount)
        dialog.description_input.setText(current_description)
        dialog.payment_status.setCurrentText(current_payment_status)

        if dialog.exec_():
            patient_id = dialog.patient_combo.currentData()
            amount = dialog.amount_input.value()
            description = dialog.description_input.toPlainText()
            is_paid = dialog.payment_status.currentText() == 'مدفوع'

            self.db.update_invoice(invoice_id, patient_id, amount, description)
            if is_paid:
                self.db.mark_invoice_as_paid(patient_id, amount)
            self.load_invoices()

    def delete_invoice(self):
        selected_rows = self.table.selectedItems()
        if not selected_rows:
            QMessageBox.warning(self, 'خطأ', 'الرجاء اختيار فاتورة للحذف')
            return

        reply = QMessageBox.question(self, 'تأكيد الحذف',
                                   'هل أنت متأكد من رغبتك في حذف هذه الفاتورة؟',
                                   QMessageBox.Yes | QMessageBox.No,
                                   QMessageBox.No)

        if reply == QMessageBox.Yes:
            row = selected_rows[0].row()
            invoice_id = int(self.table.item(row, 0).text())
            self.db.delete_invoice(invoice_id)
            self.load_invoices()

    def mark_as_paid(self):
        selected_rows = self.table.selectedItems()
        if not selected_rows:
            QMessageBox.warning(self, 'خطأ', 'الرجاء اختيار فاتورة لتحديدها كمدفوعة')
            return

        row = selected_rows[0].row()
        invoice_id = int(self.table.item(row, 0).text())
        patient_id = self.db.get_invoice_patient_id(invoice_id)
        amount = float(self.table.item(row, 2).text())

        self.db.mark_invoice_as_paid(patient_id, amount)
        self.load_invoices() 