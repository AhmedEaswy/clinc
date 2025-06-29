from PySide6.QtWidgets import (QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
                             QLabel, QMessageBox, QCheckBox, QSpacerItem, QSizePolicy)
from PySide6.QtCore import Qt
from PySide6.QtGui import QFont, QIcon
from database import Database
from styles import MAIN_STYLE, COLORS, get_input_style, get_button_style
from custom_widgets import CustomLineEdit, CustomComboBox, CustomPushButton

class LoginWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.db = Database()
        self.init_ui()

    def init_ui(self):
        self.setWindowTitle('نظام إدارة العيادة')
        self.setFixedSize(420, 480)
        self.setStyleSheet(f"""
            QMainWindow {{ background: #eaf2fa; }}
        """)

        # Centered card
        card = QWidget(self)
        card.setStyleSheet(f"""
            QWidget {{
                background: #fff;
                border: 2px solid {COLORS['primary']};
                border-radius: 16px;
            }}
        """)
        card.setFixedWidth(340)
        card.setFixedHeight(400)
        card.move((self.width() - card.width()) // 2, (self.height() - card.height()) // 2)

        card_layout = QVBoxLayout(card)
        card_layout.setContentsMargins(32, 32, 32, 32)
        card_layout.setSpacing(18)
        card.setLayout(card_layout)

        # Title
        title = QLabel('تسجيل الدخول')
        title.setStyleSheet('font-size: 28px; font-weight: bold; color: #1565c0;')
        title.setAlignment(Qt.AlignCenter)
        card_layout.addWidget(title)

        # Username
        self.username_input = CustomLineEdit()
        self.username_input.setPlaceholderText('ادخل اسم المستخدم')
        self.username_input.setStyleSheet(f"""
            {get_input_style()}
            QLineEdit {{ border: 2px solid {COLORS['primary']}; border-radius: 8px; font-size: 16px; color: {COLORS['text']}; padding-right: 12px; }}
            QLineEdit:focus {{ border: 2px solid {COLORS['primary_dark']}; }}
            QLineEdit::placeholder {{ color: {COLORS['primary']}; }}
        """)
        card_layout.addWidget(self.username_input)

        # Password
        self.password_input = CustomLineEdit()
        self.password_input.setEchoMode(CustomLineEdit.Password)
        self.password_input.setPlaceholderText('ادخل كلمة المرور')
        self.password_input.setStyleSheet(f"""
            {get_input_style()}
            QLineEdit {{ border: 2px solid {COLORS['primary']}; border-radius: 8px; font-size: 16px; color: {COLORS['text']}; padding-right: 12px; }}
            QLineEdit:focus {{ border: 2px solid {COLORS['primary_dark']}; }}
            QLineEdit::placeholder {{ color: {COLORS['primary']}; }}
        """)
        card_layout.addWidget(self.password_input)

        # Role selection
        self.role_combo = CustomComboBox()
        self.role_combo.addItems(['طبيب', 'سكرتير'])
        self.role_combo.setPlaceholderText('اختر النوع')
        self.role_combo.setStyleSheet(f"""
            {get_input_style()}
            QComboBox {{ border: 2px solid {COLORS['primary']}; border-radius: 8px; font-size: 16px; color: {COLORS['text']}; padding-right: 12px; }}
            QComboBox:focus {{ border: 2px solid {COLORS['primary_dark']}; }}
            QComboBox QAbstractItemView {{ font-size: 16px; }}
        """)
        card_layout.addWidget(self.role_combo)

        # Remember me checkbox
        remember_layout = QHBoxLayout()
        remember_layout.addStretch()
        self.remember_checkbox = QCheckBox('تذكرني')
        self.remember_checkbox.setStyleSheet(f"color: {COLORS['primary_dark']}; font-size: 14px; font-weight: bold;")
        remember_layout.addWidget(self.remember_checkbox)
        card_layout.addLayout(remember_layout)

        # Login button
        self.login_button = CustomPushButton('تسجيل الدخول')
        self.login_button.setStyleSheet(f"""
            QPushButton {{
                background: {COLORS['primary_dark']};
                color: #fff;
                border-radius: 10px;
                font-size: 18px;
                font-weight: bold;
                padding: 12px 0;
            }}
            QPushButton:hover {{ background: {COLORS['primary']}; }}
        """)
        self.login_button.setFixedHeight(44)
        self.login_button.clicked.connect(self.handle_login)
        self.login_button.setDefault(True)
        self.login_button.setAutoDefault(True)
        card_layout.addWidget(self.login_button)

        # Set tab order
        self.setTabOrder(self.username_input, self.password_input)
        self.setTabOrder(self.password_input, self.role_combo)
        self.setTabOrder(self.role_combo, self.login_button)

        # Set RTL layout
        self.setLayoutDirection(Qt.RightToLeft)
        card.setLayoutDirection(Qt.RightToLeft)

        # Center card in window
        self.central_widget = QWidget(self)
        self.setCentralWidget(self.central_widget)
        main_layout = QVBoxLayout(self.central_widget)
        main_layout.addStretch()
        main_layout.addWidget(card, alignment=Qt.AlignCenter)
        main_layout.addStretch()

    def handle_login(self):
        # Get and trim inputs
        username = self.username_input.text().strip()
        password = self.password_input.text()
        role = self.role_combo.currentText().strip()

        if not username or not password:
            QMessageBox.warning(self, 'خطأ', 'الرجاء إدخال اسم المستخدم وكلمة المرور')
            return

        # Convert role to English and proper case for database comparison
        role = 'Doctor' if role.lower() == 'طبيب' else 'Secretary'

        user = self.db.get_user(username, password)
        if user and user[0][3].lower() == role.lower():
            from main_window import MainWindow
            self.main_window = MainWindow(user[0])
            self.main_window.show()
            self.close()
        else:
            QMessageBox.warning(self, 'خطأ', 'بيانات الدخول غير صحيحة') 