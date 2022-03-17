import sys

import PySide6
from PySide6 import QtWidgets, QtCore
from PySide6.QtCore import QPoint
from PySide6.QtGui import QImage, QPolygon
from PySide6.QtWidgets import QMainWindow, QApplication

from gui.model.camera_model import Camera
from gui.thread.camera_thread import CameraThread
from gui.pyui.main_window import Ui_MainWindow
from gui.wizard import CameraAddWizard


class MainWindow(QMainWindow, Ui_MainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        self.camThread = CameraThread(self)
        self.camThread.changePixmap.connect(self.set_image)
        self.camThread.start()
        self.setupUi(self)

        self._cameras = [
            # ("0",),
            # ('../../video/vid0.mp4',),
            # ('../../video/vid1.mp4',),
            # ('../../video/vid2.avi',),
            ('../../video/vid2.avi',
             1,
             [(-132.49023090586147, 173.9253996447602), (-47.57371225577265, 206.66429840142095),
              (-2.0461811722912966, 162.15985790408524), (-74.1740674955595, 145.27886323268206)],
             [(-172.38336347197108, 69.7866184448463), (-86.45207956600362, 48.95479204339964),
              (13.01989150090416, 55.725135623869804), (12.499095840867994, 146.86437613019893),
              (-172.38336347197108, 147.90596745027125)])
        ]
        print(Camera.from_wizard(*self._cameras[0][1::]))

        self._scene = QtWidgets.QGraphicsScene(self)

        self._pixmap_item = QtWidgets.QGraphicsPixmapItem()
        self._scene.addItem(self._pixmap_item)
        self.cameraGraphicsView.fitInView(self._pixmap_item, QtCore.Qt.KeepAspectRatio)
        self.cameraGraphicsView.setScene(self._scene)

        for k in self._cameras:
            self.cameraComboBox.addItem(k[0])

        self.addCameraPushButton.clicked.connect(self.add_camera)

        self.camThread.update_video_source(self._cameras[0][0])
        self.cameraComboBox.currentIndexChanged.connect(self.switch_camera)


    def resizeEvent(self, event: PySide6.QtGui.QResizeEvent) -> None:
        self.cameraGraphicsView.fitInView(self._pixmap_item, QtCore.Qt.KeepAspectRatio)
        super().resizeEvent(event)


    def set_image(self, image: QImage):
        pixmap = PySide6.QtGui.QPixmap.fromImage(image)
        self._pixmap_item.setPixmap(pixmap)
        self.cameraGraphicsView.fitInView(self._pixmap_item, QtCore.Qt.KeepAspectRatio)


    def add_camera(self):
        dlg = CameraAddWizard(self)
        if not dlg.exec():
            return
        address = dlg.field("address")
        square_length = dlg.field("square_length")
        square_polygon: QPolygon = dlg.field("square_polygon")
        roi_polygon: QPolygon = dlg.field("roi_polygon")
        print('address:', address)
        print('square_length:', square_length)
        print('square_polygon:', [p.toTuple() for p in square_polygon.toList()])
        print('roi_polygon:', [p.toTuple() for p in roi_polygon.toList()])

        self._cameras.append((address, address))
        self.cameraComboBox.addItem(address)
        p


@QtCore.Slot(int)
def switch_camera(self, index: int):
    self.camThread.update_video_source(self._cameras[index][0])


def closeEvent(self, event: PySide6.QtGui.QCloseEvent) -> None:
    self.camThread.quit()
    self.camThread.wait()


if __name__ == '__main__':
    app = QApplication(sys.argv)

    window = MainWindow()
    window.show()
    app.exec()
