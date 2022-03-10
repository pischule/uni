from PySide6.QtGui import QImage, Qt, QPixmap
from PySide6.QtWidgets import QDialog, QWidget, QApplication, QStyle

from gui.ui.add_camera_dialog import Ui_AddCameraDialog

import cv2

class AddCameraDialog(QDialog, Ui_AddCameraDialog):
    def __init__(self):
        super().__init__()
        self.setupUi(self)

        self.connectButton.clicked.connect(self.try_connect)
        self.address.textChanged.connect(self.reset_connect_button)

        self.frame = None

    def try_connect(self):
        print("try_connect")
        print(f'{self.address.text()}')
        try:
            cap = cv2.VideoCapture(self.address.text())
            if cap.isOpened():
                ret, frame = cap.read()
                if ret:
                    self.frame = frame
                    self.show_frame()
                else:
                    self.connect_error()
            else:
                self.connect_error()
        except Exception as e:
            self.connect_error()
            print(e)
        finally:
            cap.release()
        print("try_connect")

    def connect_success(self):
        self.address.setStyleSheet('background-color: green')
        print("get_camera_preview")

    def connect_error(self):
        self.address.setStyleSheet('background-color: red')

    def reset_connect_button(self, event):
        self.address.setStyleSheet('')
        print("reset_connect_button")

    def show_frame(self):
        print("show_frame")
        self.previewLabel.setPixmap(QPixmap.fromImage(self.convertToQImage(self.frame)))

    def convertToQImage(self, frame) -> QImage:
        # https://stackoverflow.com/a/55468544/6622587
        rgb_image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        h, w, ch = rgb_image.shape
        bytes_per_line = ch * w
        convert_to_qt_format = QImage(rgb_image.data, w, h, bytes_per_line, QImage.Format_RGB888)
        return convert_to_qt_format.scaled(640, 480, Qt.KeepAspectRatio)


if __name__ == "__main__":
    import sys

    app = QApplication(sys.argv)
    ui = AddCameraDialog()
    ui.show()
    sys.exit(app.exec())
