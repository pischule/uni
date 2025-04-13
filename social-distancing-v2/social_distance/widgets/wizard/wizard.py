from PySide6.QtWidgets import QWizard

from social_distance.widgets.wizard.camera_page import CamaraUrlPage
from social_distance.widgets.wizard.details_page import DetailsPage
from social_distance.widgets.wizard.top_view_page import PreviewSettingsPage
from social_distance.widgets.wizard.roi_page import RoiPage
from social_distance.widgets.wizard.square_page import SquareEditPage


class CameraAddWizard(QWizard):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.pixmap = None
        self.roi = None
        self.square = None
        self.preview_square = None
        self.preview_side_length = None

        self.addPage(CamaraUrlPage(self))
        self.addPage(RoiPage(self))
        self.addPage(SquareEditPage(self))
        self.addPage(PreviewSettingsPage(self))
        self.addPage(DetailsPage(self))

        self.setWizardStyle(QWizard.ModernStyle)
        self.setWindowTitle("Add a new camera")
        # disable background


if __name__ == "__main__":
    import sys
    from PySide6.QtWidgets import QApplication

    app = QApplication(sys.argv)
    demo = CameraAddWizard()
    demo.show()
    app.exec()

    print(f'address: {demo.field("address")}')
    print(f'camera_name: {demo.field("camera_name")}')
    print(f'side_length: {demo.field("side_length")}')
    print(f'roi: {demo.roi}')
    print(f'square: {demo.square}')
    print(f'preview_square: {demo.preview_square}')
    print(f'preview_side_length: {demo.preview_side_length}')