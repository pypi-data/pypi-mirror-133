import sys

from PySide6.QtGui import QColor
from PySide6.QtWidgets import QPushButton, QApplication, QColorDialog, QMainWindow


class ColorSelectButton(QPushButton):
    def __init__(self):
        super(ColorSelectButton, self).__init__()

        self.color = QColor("white")

        self.css = f"""
            background-color: {self.color.name()};
            border: none;
            border-radius: 10px;
        """
        self.setStyleSheet(self.css)

        self.clicked.connect(
           lambda: self.onclick()
        )

    def onclick(self):
        color_dialog = QColorDialog()
        self.color = color_dialog.getColor(initial=self.color)
        print(self.color.name())
        self.setStyleSheet(self.css+f"background-color: {self.color.name()}")

    def return_color(self):
        print(self.color)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    widget = ColorSelectButton()
    widget.show()
    sys.exit(app.exec())

