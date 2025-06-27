"""
Central stylesheet module for the Clinic Management System.
Defines consistent styling across the application.
"""

# Color palette
COLORS = {
    'primary': '#1e88e5',      # Main blue
    'primary_light': '#64b5f6', # Light blue
    'primary_dark': '#1565c0',  # Dark blue
    'secondary': '#f5f9ff',    # Very light blue for backgrounds
    'accent': '#2196f3',       # Accent blue
    'success': '#4caf50',      # Green for success
    'warning': '#ff9800',      # Orange for warnings
    'error': '#f44336',        # Red for errors
    'text': '#2c3e50',         # Dark blue-gray for text
    'text_light': '#546e7a',   # Light blue-gray for secondary text
    'border': '#e0e0e0',       # Light gray for borders
    'white': '#ffffff',        # White
    'black': '#000000',        # Black
}

# Main application stylesheet
MAIN_STYLE = f"""
QMainWindow {{
    background-color: {COLORS['secondary']};
}}

QWidget {{
    font-family: 'Segoe UI', Arial, sans-serif;
    color: {COLORS['text']};
}}

/* Header styles */
QLabel#header {{
    font-size: 24px;
    font-weight: bold;
    color: {COLORS['primary_dark']};
    padding: 10px;
}}

/* Tab widget styles */
QTabWidget::pane {{
    border: 1px solid {COLORS['border']};
    background: {COLORS['white']};
    border-radius: 4px;
}}

QTabBar::tab {{
    background: {COLORS['secondary']};
    border: 1px solid {COLORS['border']};
    padding: 8px 16px;
    margin-right: 2px;
    border-top-left-radius: 4px;
    border-top-right-radius: 4px;
    color: {COLORS['text']};
}}

QTabBar::tab:selected {{
    background: {COLORS['primary']};
    color: {COLORS['white']};
}}

QTabBar::tab:hover:!selected {{
    background: {COLORS['primary_light']};
    color: {COLORS['white']};
}}

/* Button styles */
QPushButton {{
    background-color: {COLORS['primary']};
    color: {COLORS['white']};
    border: none;
    padding: 8px 16px;
    border-radius: 4px;
    font-weight: bold;
}}

QPushButton:hover {{
    background-color: {COLORS['primary_dark']};
}}

QPushButton:pressed {{
    background-color: {COLORS['primary_dark']};
}}

QPushButton:disabled {{
    background-color: {COLORS['border']};
    color: {COLORS['text_light']};
}}

/* Table styles */
QTableWidget {{
    background-color: {COLORS['white']};
    alternate-background-color: {COLORS['secondary']};
    border: 1px solid {COLORS['border']};
    border-radius: 4px;
    gridline-color: {COLORS['border']};
}}

QTableWidget::item {{
    padding: 8px;
    border-bottom: 1px solid {COLORS['border']};
}}

QTableWidget::item:selected {{
    background-color: {COLORS['primary_light']};
    color: {COLORS['white']};
}}

QHeaderView::section {{
    background-color: {COLORS['primary']};
    color: {COLORS['white']};
    padding: 8px;
    border: none;
    font-weight: bold;
}}

/* Input field styles */
QLineEdit, QTextEdit, QComboBox, QSpinBox, QDoubleSpinBox {{
    padding: 8px;
    border: 1px solid {COLORS['border']};
    border-radius: 4px;
    background-color: {COLORS['white']};
}}

QLineEdit:focus, QTextEdit:focus, QComboBox:focus, QSpinBox:focus, QDoubleSpinBox:focus {{
    border: 2px solid {COLORS['primary']};
}}

/* Dialog styles */
QDialog {{
    background-color: {COLORS['secondary']};
}}

/* Message box styles */
QMessageBox {{
    background-color: {COLORS['white']};
}}

QMessageBox QPushButton {{
    min-width: 80px;
}}

/* Form layout styles */
QFormLayout {{
    spacing: 10px;
}}

QLabel {{
    color: {COLORS['text']};
}}

/* Status bar styles */
QStatusBar {{
    background-color: {COLORS['primary']};
    color: {COLORS['white']};
}}

/* Scroll bar styles */
QScrollBar:vertical {{
    border: none;
    background: {COLORS['secondary']};
    width: 10px;
    margin: 0px;
}}

QScrollBar::handle:vertical {{
    background: {COLORS['primary_light']};
    min-height: 20px;
    border-radius: 5px;
}}

QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {{
    height: 0px;
}}

QScrollBar:horizontal {{
    border: none;
    background: {COLORS['secondary']};
    height: 10px;
    margin: 0px;
}}

QScrollBar::handle:horizontal {{
    background: {COLORS['primary_light']};
    min-width: 20px;
    border-radius: 5px;
}}

QScrollBar::add-line:horizontal, QScrollBar::sub-line:horizontal {{
    width: 0px;
}}
"""

# Message box styles
def get_message_box_style():
    return f"""
    QMessageBox {{
        background-color: {COLORS['white']};
    }}
    QMessageBox QLabel {{
        color: {COLORS['text']};
        font-size: 14px;
        padding: 10px;
    }}
    QMessageBox QPushButton {{
        background-color: {COLORS['primary']};
        color: {COLORS['white']};
        border: none;
        padding: 8px 16px;
        border-radius: 4px;
        min-width: 80px;
    }}
    QMessageBox QPushButton:hover {{
        background-color: {COLORS['primary_dark']};
    }}
    """

# Table styles
def get_table_style():
    return f"""
    QTableWidget {{
        background-color: {COLORS['white']};
        alternate-background-color: {COLORS['secondary']};
        border: 1px solid {COLORS['border']};
        border-radius: 4px;
        gridline-color: {COLORS['border']};
    }}
    QTableWidget::item {{
        padding: 8px;
        border-bottom: 1px solid {COLORS['border']};
    }}
    QTableWidget::item:selected {{
        background-color: {COLORS['primary_light']};
        color: {COLORS['white']};
    }}
    QHeaderView::section {{
        background-color: {COLORS['primary']};
        color: {COLORS['white']};
        padding: 8px;
        border: none;
        font-weight: bold;
    }}
    """

# Button styles
def get_button_style():
    return f"""
    QPushButton {{
        background-color: {COLORS['primary']};
        color: {COLORS['white']};
        border: none;
        padding: 8px 16px;
        border-radius: 4px;
        font-weight: bold;
    }}
    QPushButton:hover {{
        background-color: {COLORS['primary_dark']};
    }}
    QPushButton:pressed {{
        background-color: {COLORS['primary_dark']};
    }}
    QPushButton:disabled {{
        background-color: {COLORS['border']};
        color: {COLORS['text_light']};
    }}
    """

# Input field styles
def get_input_style():
    return f"""
    QLineEdit, QTextEdit, QComboBox, QSpinBox, QDoubleSpinBox {{
        padding: 8px;
        border: 1px solid {COLORS['border']};
        border-radius: 4px;
        background-color: {COLORS['white']};
    }}
    QLineEdit:focus, QTextEdit:focus, QComboBox:focus, QSpinBox:focus, QDoubleSpinBox:focus {{
        border: 2px solid {COLORS['primary']};
    }}
    """ 