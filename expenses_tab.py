from PySide6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit,
                             QPushButton, QTableWidget, QTableWidgetItem, QMessageBox,
                             QDialog, QFormLayout, QDateTimeEdit, QTextEdit,
                             QDoubleSpinBox)
from PySide6.QtCore import Qt, QDateTime
from database import Database

class AddExpenseDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.init_ui()

    def init_ui(self):
        self.setWindowTitle('إضافة مصروف جديد')
        self.setMinimumWidth(400)
        layout = QFormLayout(self)

        # Amount
        self.amount_input = QDoubleSpinBox()
        self.amount_input.setRange(0, 1000000)
        self.amount_input.setSuffix(' جنيه')
        layout.addRow('المبلغ:', self.amount_input)

        # Description
        self.description_input = QTextEdit()
        layout.addRow('الوصف:', self.description_input)

        # Date
        self.date_input = QDateTimeEdit()
        self.date_input.setDateTime(QDateTime.currentDateTime())
        self.date_input.setCalendarPopup(True)
        layout.addRow('التاريخ:', self.date_input)

        # Buttons
        buttons_layout = QHBoxLayout()
        save_button = QPushButton('حفظ')
        cancel_button = QPushButton('إلغاء')
        
        save_button.clicked.connect(self.accept)
        cancel_button.clicked.connect(self.reject)
        
        buttons_layout.addWidget(save_button)
        buttons_layout.addWidget(cancel_button)
        layout.addRow(buttons_layout)

class ExpensesTab(QWidget):
    def __init__(self, db):
        super().__init__()
        self.db = db
        self.init_ui()
        self.load_expenses()

    def init_ui(self):
        layout = QVBoxLayout(self)

        # Search bar
        search_layout = QHBoxLayout()
        self.search_input = QLineEdit()
        self.search_input.setPlaceholderText('بحث عن مصروف...')
        self.search_input.textChanged.connect(self.search_expenses)
        search_layout.addWidget(self.search_input)
        layout.addLayout(search_layout)

        # Add expense button
        add_button = QPushButton('إضافة مصروف جديد')
        add_button.clicked.connect(self.add_expense)
        layout.addWidget(add_button)

        # Expenses table
        self.table = QTableWidget()
        self.table.setColumnCount(5)
        self.table.setHorizontalHeaderLabels(['الرقم', 'المبلغ', 'الوصف', 'التاريخ', 'تاريخ الإنشاء'])
        self.table.setSelectionBehavior(QTableWidget.SelectRows)
        self.table.setEditTriggers(QTableWidget.NoEditTriggers)
        layout.addWidget(self.table)

        # Action buttons
        buttons_layout = QHBoxLayout()
        self.edit_button = QPushButton('تعديل')
        self.delete_button = QPushButton('حذف')
        
        self.edit_button.clicked.connect(self.edit_expense)
        self.delete_button.clicked.connect(self.delete_expense)
        
        buttons_layout.addWidget(self.edit_button)
        buttons_layout.addWidget(self.delete_button)
        layout.addLayout(buttons_layout)

    def load_expenses(self):
        expenses = self.db.get_all_expenses()
        self.table.setRowCount(len(expenses))
        
        for row, expense in enumerate(expenses):
            self.table.setItem(row, 0, QTableWidgetItem(str(expense[0])))
            self.table.setItem(row, 1, QTableWidgetItem(str(expense[1])))
            self.table.setItem(row, 2, QTableWidgetItem(expense[2]))
            self.table.setItem(row, 3, QTableWidgetItem(str(expense[3])))
            self.table.setItem(row, 4, QTableWidgetItem(str(expense[5])))

    def search_expenses(self):
        search_text = self.search_input.text().lower()
        for row in range(self.table.rowCount()):
            show_row = False
            for col in range(self.table.columnCount()):
                item = self.table.item(row, col)
                if item and search_text in item.text().lower():
                    show_row = True
                    break
            self.table.setRowHidden(row, not show_row)

    def add_expense(self):
        dialog = AddExpenseDialog(self)
        if dialog.exec_():
            amount = dialog.amount_input.value()
            description = dialog.description_input.toPlainText()
            expense_date = dialog.date_input.dateTime().toString('yyyy-MM-dd HH:mm:ss')

            if not description:
                QMessageBox.warning(self, 'خطأ', 'الرجاء إدخال وصف للمصروف')
                return

            self.db.add_expense(amount, description, expense_date)
            self.load_expenses()

    def edit_expense(self):
        selected_rows = self.table.selectedItems()
        if not selected_rows:
            QMessageBox.warning(self, 'خطأ', 'الرجاء اختيار مصروف للتعديل')
            return

        row = selected_rows[0].row()
        expense_id = int(self.table.item(row, 0).text())
        
        dialog = AddExpenseDialog(self)
        # Set current values
        current_amount = float(self.table.item(row, 1).text())
        current_description = self.table.item(row, 2).text()
        current_date = QDateTime.fromString(self.table.item(row, 3).text(), 'yyyy-MM-dd HH:mm:ss')

        dialog.amount_input.setValue(current_amount)
        dialog.description_input.setText(current_description)
        dialog.date_input.setDateTime(current_date)

        if dialog.exec_():
            amount = dialog.amount_input.value()
            description = dialog.description_input.toPlainText()
            expense_date = dialog.date_input.dateTime().toString('yyyy-MM-dd HH:mm:ss')

            if not description:
                QMessageBox.warning(self, 'خطأ', 'الرجاء إدخال وصف للمصروف')
                return

            self.db.update_expense(expense_id, amount, description, expense_date)
            self.load_expenses()

    def delete_expense(self):
        selected_rows = self.table.selectedItems()
        if not selected_rows:
            QMessageBox.warning(self, 'خطأ', 'الرجاء اختيار مصروف للحذف')
            return

        reply = QMessageBox.question(self, 'تأكيد الحذف',
                                   'هل أنت متأكد من رغبتك في حذف هذا المصروف؟',
                                   QMessageBox.Yes | QMessageBox.No,
                                   QMessageBox.No)

        if reply == QMessageBox.Yes:
            row = selected_rows[0].row()
            expense_id = int(self.table.item(row, 0).text())
            self.db.delete_expense(expense_id)
            self.load_expenses() 