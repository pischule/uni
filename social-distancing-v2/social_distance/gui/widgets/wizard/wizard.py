from PySide6.QtWidgets import QWizard

from social_distance.gui.widgets.wizard.camera_wizard_page import CamaraUrlPage
from social_distance.gui.widgets.wizard.details_page import DetailsPage
from social_distance.gui.widgets.wizard.roi_page import RoiPage
from social_distance.gui.widgets.wizard.square_edit_page import SquareEditPage


class CameraAddWizard(QWizard):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.addPage(CamaraUrlPage(self))
        self.addPage(RoiPage(self))
        self.addPage(SquareEditPage(self))
        self.addPage(DetailsPage(self))
        # self.addPage(PreviewSettingsPage(self))

        self.setWizardStyle(QWizard.ModernStyle)
        self.setWindowTitle("Add a new camera")


if __name__ == "__main__":
    import sys
    from PySide6.QtWidgets import QApplication

    app = QApplication(sys.argv)
    demo = CameraAddWizard()
    demo.show()
    app.exec()

    print(f'address: {demo.field("address")}')
    print(f'camera_name: {demo.field("camera_name")}')
    print(f'square_length: {demo.field("square_length")}')
    print(f'square_polygon: {demo.field("square_polygon")}')
    print(f'roi_polygon: {demo.field("roi_polygon")}')
    print(f'preview_transform: {demo.field("preview_transform")}')
