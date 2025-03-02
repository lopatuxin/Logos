import sys

from PyQt6.QtCore import Qt, QSize
from PyQt6.QtGui import QFont, QIcon, QFontMetrics
from PyQt6.QtWidgets import QApplication, QWidget, QVBoxLayout, QListWidget, QLineEdit, QPushButton, QListWidgetItem, \
    QHBoxLayout, QLabel, QGridLayout, QSizePolicy


class ChatBubble(QWidget):
    def __init__(self, text):
        super().__init__()
        layout = QGridLayout()
        self.setStyleSheet("background-color: #4C9EEB; border-radius: 10px; padding: 8px;")

        message_label = QLabel(text)
        message_label.setFont(QFont("Arial", 12))
        message_label.setStyleSheet("color: white;")
        message_label.setWordWrap(True)

        font_metrics = QFontMetrics(message_label.font())
        text_width = font_metrics.boundingRect(text).width() + 20
        max_width = 250
        bubble_width = min(text_width, max_width)

        # Позволяем высоте увеличиваться в зависимости от текста
        message_label.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Preferred)

        layout.addWidget(message_label, 0, 0)
        layout.setContentsMargins(10, 5, 10, 5)
        self.setLayout(layout)
        self.setMinimumWidth(bubble_width + 30)
        self.adjustSize()


class ChatWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.message_list = QListWidget()
        self.input_field = QLineEdit()
        self.send_button = QPushButton()
        self.init_ui()

    def init_ui(self):
        self.setWindowTitle("Telegram Chat")
        self.setGeometry(100, 100, 400, 500)
        self.setStyleSheet("background-color: #17212B; color: white;")

        layout = QVBoxLayout()

        # Область сообщений
        self.message_list.setStyleSheet("border: none; background-color: #17212B;")
        layout.addWidget(self.message_list)

        # Горизонтальный layout для ввода и кнопки
        input_layout = QHBoxLayout()

        # Поле ввода
        self.input_field.setStyleSheet(
            "border: 1px solid #2F3C4A; border-radius: 10px; padding: 8px; background-color: #1E2C3B; color: white;")
        self.input_field.returnPressed.connect(self.send_message)  # Привязываем Enter к отправке
        input_layout.addWidget(self.input_field)

        # Кнопка отправки с увеличенной иконкой
        icon = QIcon("send_icon.png")
        self.send_button.setIcon(icon)
        self.send_button.setIconSize(QSize(32, 32))  # Устанавливаем размер иконки
        self.send_button.setFixedSize(50, 50)  # Размер кнопки
        self.send_button.setStyleSheet("background-color: #0088CC; border-radius: 25px; padding: 8px;")
        self.send_button.clicked.connect(self.send_message)
        input_layout.addWidget(self.send_button)

        layout.addLayout(input_layout)
        self.setLayout(layout)

    def keyPressEvent(self, event):
        if event.key() == Qt.Key.Key_Return and event.modifiers() == Qt.KeyboardModifier.ShiftModifier:
            self.input_field.insert("\n")  # Shift+Enter добавляет новую строку
        elif event.key() == Qt.Key.Key_Return:
            self.send_message()  # Просто Enter отправляет сообщение

    def send_message(self):
        message = self.input_field.text().strip()
        if message:
            bubble = ChatBubble(message)
            item = QListWidgetItem()
            item.setSizeHint(bubble.sizeHint())
            self.message_list.addItem(item)
            self.message_list.setItemWidget(item, bubble)

            self.input_field.clear()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = ChatWindow()
    window.show()
    sys.exit(app.exec())
