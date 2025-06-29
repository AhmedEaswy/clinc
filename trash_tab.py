from PySide6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit,
                             QPushButton, QTableWidget, QTableWidgetItem, QMessageBox,
                             QTabWidget)
from PySide6.QtCore import Qt
from database import Database

class TrashTab(QWidget):
    def __init__(self, db):
        super().__init__()
        self.db = db
        self.init_ui()
        self.load_trash()

    def init_ui(self):
        layout = QVBoxLayout(self)

        # Create tab widget for different types of deleted items
        self.tabs = QTabWidget()
        self.tabs.setLayoutDirection(Qt.RightToLeft)

        # Create tables for each type
        self.patients_table = QTableWidget()
        self.appointments_table = QTableWidget()
        self.checkups_table = QTableWidget()
        self.invoices_table = QTableWidget()
        self.expenses_table = QTableWidget()

        # Set up tables
        self.setup_table(self.patients_table, ['الرقم', 'الاسم', 'العمر', 'رقم الهاتف', 'العنوان', 'تاريخ الحذف'])
        self.setup_table(self.appointments_table, ['الرقم', 'المريض', 'الطبيب', 'التاريخ', 'الحالة', 'تاريخ الحذف'])
        self.setup_table(self.checkups_table, ['الرقم', 'المريض', 'الطبيب', 'التاريخ', 'التشخيص', 'تاريخ الحذف'])
        self.setup_table(self.invoices_table, ['الرقم', 'المريض', 'المبلغ', 'الوصف', 'حالة الدفع', 'تاريخ الحذف'])
        self.setup_table(self.expenses_table, ['الرقم', 'المبلغ', 'الوصف', 'التاريخ', 'تاريخ الحذف'])

        # Add tables to tabs
        self.tabs.addTab(self.patients_table, 'المرضى المحذوفين')
        self.tabs.addTab(self.appointments_table, 'المواعيد المحذوفة')
        self.tabs.addTab(self.checkups_table, 'الكشوفات المحذوفة')
        self.tabs.addTab(self.invoices_table, 'الفواتير المحذوفة')
        self.tabs.addTab(self.expenses_table, 'المصروفات المحذوفة')

        layout.addWidget(self.tabs)

        # Action buttons
        buttons_layout = QHBoxLayout()
        self.restore_button = QPushButton('استعادة')
        self.delete_button = QPushButton('حذف نهائي')
        self.empty_trash_button = QPushButton('إفراغ سلة المهملات')
        
        self.restore_button.clicked.connect(self.restore_item)
        self.delete_button.clicked.connect(self.delete_permanently)
        self.empty_trash_button.clicked.connect(self.empty_trash)
        
        buttons_layout.addWidget(self.restore_button)
        buttons_layout.addWidget(self.delete_button)
        buttons_layout.addWidget(self.empty_trash_button)
        layout.addLayout(buttons_layout)

    def setup_table(self, table, headers):
        table.setColumnCount(len(headers))
        table.setHorizontalHeaderLabels(headers)
        table.setSelectionBehavior(QTableWidget.SelectRows)
        table.setEditTriggers(QTableWidget.NoEditTriggers)
        table.verticalHeader().setDefaultSectionSize(60)  # Set minimum row height
        table.horizontalHeader().setMinimumSectionSize(120)  # Set minimum column width
        table.horizontalHeader().setStretchLastSection(True)
        # table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeToContents)
        # table.verticalHeader().setSectionResizeMode(QHeaderView.ResizeToContents)

    def load_trash(self):
        # Load deleted patients
        patients = self.db.get_deleted_patients()
        self.patients_table.setRowCount(len(patients))
        for row, patient in enumerate(patients):
            self.patients_table.setItem(row, 0, QTableWidgetItem(str(patient[0])))
            self.patients_table.setItem(row, 1, QTableWidgetItem(patient[1]))
            self.patients_table.setItem(row, 2, QTableWidgetItem(str(patient[2])))
            self.patients_table.setItem(row, 3, QTableWidgetItem(patient[3]))
            self.patients_table.setItem(row, 4, QTableWidgetItem(patient[4]))
            self.patients_table.setItem(row, 5, QTableWidgetItem(str(patient[7])))

        # Load deleted appointments
        appointments = self.db.get_deleted_appointments()
        self.appointments_table.setRowCount(len(appointments))
        for row, appointment in enumerate(appointments):
            self.appointments_table.setItem(row, 0, QTableWidgetItem(str(appointment[0])))
            self.appointments_table.setItem(row, 1, QTableWidgetItem(appointment[8]))  # patient_name
            self.appointments_table.setItem(row, 2, QTableWidgetItem(appointment[9]))  # doctor_name
            self.appointments_table.setItem(row, 3, QTableWidgetItem(str(appointment[3])))
            self.appointments_table.setItem(row, 4, QTableWidgetItem(appointment[4]))
            self.appointments_table.setItem(row, 5, QTableWidgetItem(str(appointment[7])))

        # Load deleted checkups
        checkups = self.db.get_deleted_checkups()
        self.checkups_table.setRowCount(len(checkups))
        for row, checkup in enumerate(checkups):
            self.checkups_table.setItem(row, 0, QTableWidgetItem(str(checkup[0])))
            self.checkups_table.setItem(row, 1, QTableWidgetItem(checkup[8]))  # patient_name
            self.checkups_table.setItem(row, 2, QTableWidgetItem(checkup[9]))  # doctor_name
            self.checkups_table.setItem(row, 3, QTableWidgetItem(str(checkup[3])))
            self.checkups_table.setItem(row, 4, QTableWidgetItem(checkup[4]))
            self.checkups_table.setItem(row, 5, QTableWidgetItem(str(checkup[7])))

        # Load deleted invoices
        invoices = self.db.get_deleted_invoices()
        self.invoices_table.setRowCount(len(invoices))
        for row, invoice in enumerate(invoices):
            self.invoices_table.setItem(row, 0, QTableWidgetItem(str(invoice[0])))
            self.invoices_table.setItem(row, 1, QTableWidgetItem(invoice[5]))  # patient_name
            self.invoices_table.setItem(row, 2, QTableWidgetItem(str(invoice[2])))
            self.invoices_table.setItem(row, 3, QTableWidgetItem(invoice[3]))
            self.invoices_table.setItem(row, 4, QTableWidgetItem('مدفوع' if invoice[4] else 'غير مدفوع'))
            self.invoices_table.setItem(row, 5, QTableWidgetItem(str(invoice[7])))

        # Load deleted expenses
        expenses = self.db.get_deleted_expenses()
        self.expenses_table.setRowCount(len(expenses))
        for row, expense in enumerate(expenses):
            self.expenses_table.setItem(row, 0, QTableWidgetItem(str(expense[0])))
            self.expenses_table.setItem(row, 1, QTableWidgetItem(str(expense[1])))
            self.expenses_table.setItem(row, 2, QTableWidgetItem(expense[2]))
            self.expenses_table.setItem(row, 3, QTableWidgetItem(str(expense[3])))
            self.expenses_table.setItem(row, 4, QTableWidgetItem(str(expense[6])))

    def get_current_table(self):
        current_tab = self.tabs.currentWidget()
        if current_tab == self.patients_table:
            return 'patients'
        elif current_tab == self.appointments_table:
            return 'appointments'
        elif current_tab == self.checkups_table:
            return 'checkups'
        elif current_tab == self.invoices_table:
            return 'invoices'
        elif current_tab == self.expenses_table:
            return 'expenses'
        return None

    def restore_item(self):
        current_table = self.get_current_table()
        if not current_table:
            return

        selected_rows = self.tabs.currentWidget().selectedItems()
        if not selected_rows:
            QMessageBox.warning(self, 'خطأ', 'الرجاء اختيار عنصر للاستعادة')
            return

        reply = QMessageBox.question(self, 'تأكيد الاستعادة',
                                   'هل أنت متأكد من رغبتك في استعادة هذا العنصر؟',
                                   QMessageBox.Yes | QMessageBox.No,
                                   QMessageBox.No)

        if reply == QMessageBox.Yes:
            row = selected_rows[0].row()
            item_id = int(self.tabs.currentWidget().item(row, 0).text())
            self.db.restore_item(current_table, item_id)
            self.load_trash()

    def delete_permanently(self):
        current_table = self.get_current_table()
        if not current_table:
            return

        selected_rows = self.tabs.currentWidget().selectedItems()
        if not selected_rows:
            QMessageBox.warning(self, 'خطأ', 'الرجاء اختيار عنصر للحذف النهائي')
            return

        reply = QMessageBox.question(self, 'تأكيد الحذف النهائي',
                                   'هل أنت متأكد من رغبتك في حذف هذا العنصر نهائياً؟',
                                   QMessageBox.Yes | QMessageBox.No,
                                   QMessageBox.No)

        if reply == QMessageBox.Yes:
            row = selected_rows[0].row()
            item_id = int(self.tabs.currentWidget().item(row, 0).text())
            self.db.delete_permanently(current_table, item_id)
            self.load_trash()

    def empty_trash(self):
        reply = QMessageBox.question(self, 'تأكيد إفراغ سلة المهملات',
                                   'هل أنت متأكد من رغبتك في إفراغ سلة المهملات؟\nسيتم حذف جميع العناصر نهائياً.',
                                   QMessageBox.Yes | QMessageBox.No,
                                   QMessageBox.No)

        if reply == QMessageBox.Yes:
            self.db.empty_trash()
            self.load_trash() 