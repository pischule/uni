from PySide6.QtGui import QImage


def open_image_to_qimage(cvImg):
    height, width, channel = cvImg.shape
    bytes_per_line = 3 * width
    return QImage(cvImg.data, width, height, bytes_per_line, QImage.Format_RGB888)