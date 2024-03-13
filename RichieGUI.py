import sys

from PyQt5.QtWidgets import QDialog, QPushButton, QVBoxLayout, QApplication


class PopupWindow(QDialog):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Popup Window")

        # Add a button to the popup window
        button = QPushButton("Close")
        button.clicked.connect(self.close)

        # Add the button to a layout
        layout = QVBoxLayout()
        layout.addWidget(button)

        self.setLayout(layout)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = PopupWindow()
    window.show()  # Show the window
    sys.exit(app.exec_())