import sys
from PySide6.QtWidgets import QApplication
from login import LoginWindow
from styles import MAIN_STYLE

def main():
    app = QApplication(sys.argv)
    
    # Set application style
    app.setStyle('Fusion')
    app.setStyleSheet(MAIN_STYLE)
    
    # Create and show login window
    login_window = LoginWindow()
    login_window.show()
    
    sys.exit(app.exec())

if __name__ == '__main__':
    main() 