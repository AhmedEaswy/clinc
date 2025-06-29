from PySide6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit,
                             QPushButton, QTableWidget, QTableWidgetItem, QMessageBox,
                             QDialog, QFormLayout, QDateTimeEdit, QComboBox, QTextEdit,
                             QDoubleSpinBox)
from PySide6.QtCore import Qt, QDateTime
from database import Database

class CashTab(QWidget):
    def __init__(self, db):
        super().__init__()
        self.db = db
        self.init_ui()
        self.load_transactions()
        self.update_balance()

    def init_ui(self):
        layout = QVBoxLayout(self)

        # Balance display
        balance_layout = QHBoxLayout()
        balance_label = QLabel('الرصيد الحالي:')
        self.balance_value = QLabel('0 جنيه')
        self.balance_value.setStyleSheet('font-size: 18px; font-weight: bold;')
        balance_layout.addWidget(balance_label)
        balance_layout.addWidget(self.balance_value)
        layout.addLayout(balance_layout)

        # Filters
        filters_layout = QHBoxLayout()
        
        # Date range
        self.start_date = QDateTimeEdit()
        self.start_date.setDateTime(QDateTime.currentDateTime().addDays(-30))
        self.start_date.setCalendarPopup(True)
        self.start_date.setStyleSheet("background-color: white;")
        self.end_date = QDateTimeEdit()
        self.end_date.setDateTime(QDateTime.currentDateTime())
        self.end_date.setCalendarPopup(True)
        self.end_date.setStyleSheet("background-color: white;")
        
        filters_layout.addWidget(QLabel('من:'))
        filters_layout.addWidget(self.start_date)
        filters_layout.addWidget(QLabel('إلى:'))
        filters_layout.addWidget(self.end_date)

        # Transaction type filter
        self.type_filter = QComboBox()
        self.type_filter.addItems(['الكل', 'دخل', 'مصروف'])
        filters_layout.addWidget(QLabel('النوع:'))
        filters_layout.addWidget(self.type_filter)

        # Apply filters button
        apply_filters_button = QPushButton('تطبيق')
        apply_filters_button.clicked.connect(self.apply_filters)
        filters_layout.addWidget(apply_filters_button)

        # Print report button
        print_report_button = QPushButton('طباعة تقرير')
        print_report_button.clicked.connect(self.print_report)
        filters_layout.addWidget(print_report_button)

        layout.addLayout(filters_layout)

        # Transactions table
        self.table = QTableWidget()
        self.table.setColumnCount(6)
        self.table.setHorizontalHeaderLabels(['الرقم', 'النوع', 'المبلغ', 'الوصف', 'التاريخ', 'المرجع'])
        self.table.setSelectionBehavior(QTableWidget.SelectRows)
        self.table.setEditTriggers(QTableWidget.NoEditTriggers)
        self.table.verticalHeader().setDefaultSectionSize(60)  # Set minimum row height
        self.table.horizontalHeader().setMinimumSectionSize(120)  # Set minimum column width
        self.table.horizontalHeader().setStretchLastSection(True)
        # self.table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeToContents)
        # self.table.verticalHeader().setSectionResizeMode(QHeaderView.ResizeToContents)
        layout.addWidget(self.table)

    def load_transactions(self):
        transactions = self.db.get_all_transactions()
        self.table.setRowCount(len(transactions))
        
        for row, transaction in enumerate(transactions):
            self.table.setItem(row, 0, QTableWidgetItem(str(transaction[0])))
            self.table.setItem(row, 1, QTableWidgetItem('دخل' if transaction[1] == 'income' else 'مصروف'))
            self.table.setItem(row, 2, QTableWidgetItem(str(transaction[2])))
            self.table.setItem(row, 3, QTableWidgetItem(transaction[3]))
            self.table.setItem(row, 4, QTableWidgetItem(str(transaction[6])))
            self.table.setItem(row, 5, QTableWidgetItem(f"{transaction[5]} ({transaction[4]})"))

    def update_balance(self):
        balance = self.db.get_cash_balance()
        self.balance_value.setText(f"{balance} جنيه")
        self.balance_value.setStyleSheet(
            f'font-size: 18px; font-weight: bold; color: {"green" if balance >= 0 else "red"};'
        )

    def apply_filters(self):
        start_date = self.start_date.dateTime().toString('yyyy-MM-dd HH:mm:ss')
        end_date = self.end_date.dateTime().toString('yyyy-MM-dd HH:mm:ss')
        transaction_type = self.type_filter.currentText()

        transactions = self.db.get_filtered_transactions(start_date, end_date, transaction_type)
        self.table.setRowCount(len(transactions))
        
        for row, transaction in enumerate(transactions):
            self.table.setItem(row, 0, QTableWidgetItem(str(transaction[0])))
            self.table.setItem(row, 1, QTableWidgetItem('دخل' if transaction[1] == 'income' else 'مصروف'))
            self.table.setItem(row, 2, QTableWidgetItem(str(transaction[2])))
            self.table.setItem(row, 3, QTableWidgetItem(transaction[3]))
            self.table.setItem(row, 4, QTableWidgetItem(str(transaction[6])))
            self.table.setItem(row, 5, QTableWidgetItem(f"{transaction[5]} ({transaction[4]})"))

        # Dynamically update balance based on filtered transactions
        balance = sum(t[2] if t[1] == 'income' else -t[2] for t in transactions)
        self.balance_value.setText(f"{balance} جنيه")
        self.balance_value.setStyleSheet(
            f'font-size: 18px; font-weight: bold; color: {"green" if balance >= 0 else "red"};'
        )

    def print_report(self):
        start_date = self.start_date.dateTime().toString('yyyy-MM-dd HH:mm:ss')
        end_date = self.end_date.dateTime().toString('yyyy-MM-dd HH:mm:ss')
        transaction_type = self.type_filter.currentText()

        transactions = self.db.get_filtered_transactions(start_date, end_date, transaction_type)
        
        # Calculate totals
        total_income = sum(t[2] for t in transactions if t[1] == 'income')
        total_expenses = sum(t[2] for t in transactions if t[1] == 'expense')
        net_profit = total_income - total_expenses

        # Create report dialog
        dialog = QDialog(self)
        dialog.setWindowTitle('تقرير النقدية')
        dialog.setMinimumWidth(600)
        layout = QVBoxLayout(dialog)

        # Report content
        report_text = QTextEdit()
        report_text.setReadOnly(True)
        
        report = f"""
        تقرير النقدية
        الفترة: من {start_date} إلى {end_date}
        نوع المعاملات: {transaction_type}

        إجمالي الدخل: {total_income} جنيه
        إجمالي المصروفات: {total_expenses} جنيه
        صافي الربح: {net_profit} جنيه

        تفاصيل المعاملات:
        """
        
        for t in transactions:
            report += f"""
            رقم المعاملة: {t[0]}
            النوع: {'دخل' if t[1] == 'income' else 'مصروف'}
            المبلغ: {t[2]} جنيه
            الوصف: {t[3]}
            التاريخ: {t[6]}
            المرجع: {t[5]} ({t[4]})
            ------------------------
            """
        
        report_text.setText(report)
        layout.addWidget(report_text)

        # Print button
        print_button = QPushButton('طباعة')
        print_button.clicked.connect(dialog.accept)
        layout.addWidget(print_button)

        dialog.exec_() 