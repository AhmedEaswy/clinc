from PySide6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton, QListWidget, QListWidgetItem, QFrame, QSizePolicy, QScrollArea)
from PySide6.QtCore import Qt, QTimer
from styles import MAIN_STYLE, get_button_style, get_table_style
from custom_widgets import CustomPushButton

class DashboardTab(QWidget):
    def __init__(self, db, add_patient_callback=None, call_next_callback=None):
        super().__init__()
        self.db = db
        self.add_patient_callback = add_patient_callback
        self.call_next_callback = call_next_callback
        self.setStyleSheet(MAIN_STYLE)
        self.init_ui()
        self.refresh_timer = QTimer(self)
        self.refresh_timer.timeout.connect(self.load_waiting_list)
        self.refresh_timer.start(3000)  # Refresh every 3 seconds

    def init_ui(self):
        main_layout = QHBoxLayout(self)
        main_layout.setContentsMargins(20, 20, 20, 20)
        main_layout.setSpacing(20)
        self.setLayoutDirection(Qt.RightToLeft)

        # Sidebar stats
        stats_layout = QVBoxLayout()
        stats_layout.setSpacing(20)
        stats_layout.setAlignment(Qt.AlignTop)
        self.stats_boxes = []
        for label in ['مرضى اليوم', 'في الانتظار', 'تم الكشف']:
            box = self.create_stat_box(label, '0')
            stats_layout.addWidget(box)
            self.stats_boxes.append(box)
        stats_layout.addStretch()

        # Main content
        content_layout = QVBoxLayout()
        content_layout.setSpacing(20)
        content_layout.setAlignment(Qt.AlignTop)

        # Title and quick add
        title_row = QHBoxLayout()
        title = QLabel('لوحة التحكم')
        title.setStyleSheet('font-size: 32px; font-weight: bold; color: #222;')
        title.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
        title_row.addWidget(title)
        title_row.addStretch()
        self.quick_add_btn = CustomPushButton('إضافة مريض')
        self.quick_add_btn.setStyleSheet(get_button_style())
        self.quick_add_btn.setFixedHeight(40)
        self.quick_add_btn.setFixedWidth(160)
        self.quick_add_btn.clicked.connect(self.handle_quick_add)
        title_row.addWidget(self.quick_add_btn)
        content_layout.addLayout(title_row)

        # Waiting list section
        waiting_row = QHBoxLayout()
        waiting_label = QLabel('قائمة الانتظار')
        waiting_label.setStyleSheet('font-size: 20px; font-weight: bold; color: #1565c0;')
        waiting_row.addWidget(waiting_label)
        waiting_row.addStretch()
        self.call_next_btn = CustomPushButton('مناداة الدور التالي')
        self.call_next_btn.setStyleSheet(get_button_style())
        self.call_next_btn.setFixedHeight(36)
        self.call_next_btn.setFixedWidth(180)
        self.call_next_btn.clicked.connect(self.handle_call_next)
        waiting_row.addWidget(self.call_next_btn)
        content_layout.addLayout(waiting_row)

        # Waiting list (scrollable)
        self.waiting_list = QListWidget()
        self.waiting_list.setStyleSheet('background: #e3f0fc; border: 1px solid #1565c0; font-size: 16px;')
        self.waiting_list.setFixedHeight(260)
        content_layout.addWidget(self.waiting_list)

        main_layout.addLayout(content_layout, 3)
        main_layout.addLayout(stats_layout, 1)
        self.setLayout(main_layout)
        self.load_stats()
        self.load_waiting_list()

    def create_stat_box(self, label, value):
        box = QFrame()
        box.setStyleSheet('background: #1565c0; border-radius: 6px; border-bottom: 6px solid #1e88e5;')
        box.setFixedHeight(90)
        box.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        vbox = QVBoxLayout(box)
        vbox.setContentsMargins(10, 10, 10, 10)
        vbox.setSpacing(2)
        title = QLabel(label)
        title.setStyleSheet('color: #fff; font-size: 18px; font-weight: bold; border-bottom: 2px solid #64b5f6;')
        value_lbl = QLabel(value)
        value_lbl.setStyleSheet('color: #fff; font-size: 28px; font-weight: bold;')
        value_lbl.setAlignment(Qt.AlignCenter)
        vbox.addWidget(title)
        vbox.addWidget(value_lbl)
        vbox.addStretch()
        box.value_lbl = value_lbl
        return box

    def load_stats(self):
        # Example: fetch stats from db (replace with real queries)
        today_patients = len(self.db.get_all_patients() or [])
        waiting = len(self.get_waiting_patients())
        checked = len([p for p in self.db.get_all_patients() or [] if getattr(p, 'status', '') == 'تم الكشف'])
        self.stats_boxes[0].value_lbl.setText(str(today_patients))
        self.stats_boxes[1].value_lbl.setText(str(waiting))
        self.stats_boxes[2].value_lbl.setText(str(checked))

    def load_waiting_list(self):
        self.waiting_list.clear()
        waiting_patients = self.get_waiting_patients()
        for idx, patient in enumerate(waiting_patients, 1):
            # patient: (id, name, reason, est_wait)
            item_text = f"{idx}. {patient[1]}  |  {patient[2]}  |  {patient[3]} دقيقة"
            item = QListWidgetItem(item_text)
            item.setTextAlignment(Qt.AlignRight)
            self.waiting_list.addItem(item)
        self.load_stats()

    def get_waiting_patients(self):
        # Replace with real DB logic for waiting patients
        # Example: [(id, name, reason, est_wait)]
        # Here, we just return a static list for demonstration
        return [
            (1, 'محمد علي', 'كشف عام', 10),
            (2, 'سارة حسن', 'استشارة', 20),
        ]

    def handle_quick_add(self):
        if self.add_patient_callback:
            self.add_patient_callback()

    def handle_call_next(self):
        # Mark next patient as in progress (replace with real DB logic)
        if self.call_next_callback:
            self.call_next_callback()
        # For demo, just remove the first in the list
        if self.waiting_list.count() > 0:
            self.waiting_list.takeItem(0)
        self.load_stats() 