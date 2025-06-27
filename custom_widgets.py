from PySide6.QtWidgets import QLineEdit, QTextEdit, QComboBox, QSpinBox, QDoubleSpinBox, QPushButton
from PySide6.QtCore import Qt, QEvent

class CustomLineEdit(QLineEdit):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setTabOrder(self, self)

    def keyPressEvent(self, event):
        if event.key() == Qt.Key_Return or event.key() == Qt.Key_Enter:
            # Find the next widget in tab order
            next_widget = self.focusNextChild()
            # If no next widget or next widget is a button, trigger the button
            if not next_widget or isinstance(next_widget, QPushButton):
                # Find the default button in the parent dialog/window
                parent = self.parent()
                while parent:
                    if hasattr(parent, 'defaultButton'):
                        parent.defaultButton().click()
                        return
                    parent = parent.parent()
            # If no default button found, just move focus
            if next_widget:
                next_widget.setFocus()
        else:
            super().keyPressEvent(event)

class CustomTextEdit(QTextEdit):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setTabOrder(self, self)

    def keyPressEvent(self, event):
        if event.key() == Qt.Key_Return or event.key() == Qt.Key_Enter:
            if not event.modifiers() & Qt.ShiftModifier:  # Allow Shift+Enter for new line
                # Find the next widget in tab order
                next_widget = self.focusNextChild()
                # If no next widget or next widget is a button, trigger the button
                if not next_widget or isinstance(next_widget, QPushButton):
                    # Find the default button in the parent dialog/window
                    parent = self.parent()
                    while parent:
                        if hasattr(parent, 'defaultButton'):
                            parent.defaultButton().click()
                            return
                        parent = parent.parent()
                # If no default button found, just move focus
                if next_widget:
                    next_widget.setFocus()
                return
        super().keyPressEvent(event)

class CustomComboBox(QComboBox):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setTabOrder(self, self)

    def keyPressEvent(self, event):
        if event.key() == Qt.Key_Return or event.key() == Qt.Key_Enter:
            # Find the next widget in tab order
            next_widget = self.focusNextChild()
            # If no next widget or next widget is a button, trigger the button
            if not next_widget or isinstance(next_widget, QPushButton):
                # Find the default button in the parent dialog/window
                parent = self.parent()
                while parent:
                    if hasattr(parent, 'defaultButton'):
                        parent.defaultButton().click()
                        return
                    parent = parent.parent()
            # If no default button found, just move focus
            if next_widget:
                next_widget.setFocus()
        else:
            super().keyPressEvent(event)

class CustomSpinBox(QSpinBox):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setTabOrder(self, self)

    def keyPressEvent(self, event):
        if event.key() == Qt.Key_Return or event.key() == Qt.Key_Enter:
            # Find the next widget in tab order
            next_widget = self.focusNextChild()
            # If no next widget or next widget is a button, trigger the button
            if not next_widget or isinstance(next_widget, QPushButton):
                # Find the default button in the parent dialog/window
                parent = self.parent()
                while parent:
                    if hasattr(parent, 'defaultButton'):
                        parent.defaultButton().click()
                        return
                    parent = parent.parent()
            # If no default button found, just move focus
            if next_widget:
                next_widget.setFocus()
        else:
            super().keyPressEvent(event)

class CustomDoubleSpinBox(QDoubleSpinBox):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setTabOrder(self, self)

    def keyPressEvent(self, event):
        if event.key() == Qt.Key_Return or event.key() == Qt.Key_Enter:
            # Find the next widget in tab order
            next_widget = self.focusNextChild()
            # If no next widget or next widget is a button, trigger the button
            if not next_widget or isinstance(next_widget, QPushButton):
                # Find the default button in the parent dialog/window
                parent = self.parent()
                while parent:
                    if hasattr(parent, 'defaultButton'):
                        parent.defaultButton().click()
                        return
                    parent = parent.parent()
            # If no default button found, just move focus
            if next_widget:
                next_widget.setFocus()
        else:
            super().keyPressEvent(event)

class CustomPushButton(QPushButton):
    def __init__(self, text, parent=None):
        super().__init__(text, parent)
        self.setTabOrder(self, self)

    def keyPressEvent(self, event):
        if event.key() == Qt.Key_Return or event.key() == Qt.Key_Enter:
            self.click()
        else:
            super().keyPressEvent(event) 