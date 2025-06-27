from PySide6.QtWidgets import (QMainWindow, QWidget, QVBoxLayout, QTabWidget,
                             QLabel, QPushButton, QMessageBox)
from PySide6.QtCore import Qt
from PySide6.QtGui import QFont
from database import Database
from patients_tab import PatientsTab
from appointments_tab import AppointmentsTab
from checkups_tab import CheckupsTab
from invoices_tab import InvoicesTab
from expenses_tab import ExpensesTab
from cash_tab import CashTab
from trash_tab import TrashTab
from styles import MAIN_STYLE, COLORS
from dashboard_tab import DashboardTab

class MainWindow(QMainWindow):
    def __init__(self, user):
        super().__init__()
        self.user = user
        self.db = Database()
        self.init_ui()

    def init_ui(self):
        self.setWindowTitle('نظام إدارة العيادة')
        self.setMinimumSize(1200, 800)
        self.setStyleSheet(MAIN_STYLE)

        # Create central widget and layout
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        layout = QVBoxLayout(central_widget)
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(15)

        # Header with user info
        header_layout = QVBoxLayout()
        user_info = QLabel(f'مرحباً {self.user[1]} ({self.user[3]})')
        user_info.setObjectName('header')
        header_layout.addWidget(user_info)
        layout.addLayout(header_layout)

        # Create tab widget
        self.tabs = QTabWidget()
        self.tabs.setLayoutDirection(Qt.RightToLeft)

        # Add Dashboard tab first
        self.dashboard_tab = DashboardTab(self.db, add_patient_callback=self.open_add_patient_dialog, call_next_callback=self.call_next_patient)
        self.tabs.addTab(self.dashboard_tab, 'لوحة التحكم')

        # Add other tabs
        self.patients_tab = PatientsTab(self.db)
        self.appointments_tab = AppointmentsTab(self.db)
        self.checkups_tab = CheckupsTab(self.db)
        self.invoices_tab = InvoicesTab(self.db)
        self.expenses_tab = ExpensesTab(self.db)
        self.cash_tab = CashTab(self.db)

        self.tabs.addTab(self.patients_tab, 'المرضى')
        self.tabs.addTab(self.appointments_tab, 'المواعيد')
        self.tabs.addTab(self.checkups_tab, 'الكشف')
        self.tabs.addTab(self.invoices_tab, 'الفواتير')
        self.tabs.addTab(self.expenses_tab, 'المصروفات')
        self.tabs.addTab(self.cash_tab, 'إدارة النقدية')

        # Add trash tab only for doctors
        if self.user[3] == 'Doctor':
            self.trash_tab = TrashTab(self.db)
            self.tabs.addTab(self.trash_tab, 'سلة المهملات')

        layout.addWidget(self.tabs)

        # Set RTL layout
        self.setLayoutDirection(Qt.RightToLeft)

    def open_add_patient_dialog(self):
        # TODO: Implement or connect to the add patient dialog
        if hasattr(self.patients_tab, 'open_add_patient_dialog'):
            self.patients_tab.open_add_patient_dialog()

    def call_next_patient(self):
        # TODO: Implement logic to mark next patient as in progress
        pass

    def closeEvent(self, event):
        reply = QMessageBox.question(self, 'تأكيد الخروج',
                                   'هل أنت متأكد من رغبتك في الخروج؟',
                                   QMessageBox.Yes | QMessageBox.No,
                                   QMessageBox.No)
        if reply == QMessageBox.Yes:
            event.accept()
        else:
            event.ignore() 