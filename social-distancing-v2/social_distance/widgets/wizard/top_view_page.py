from PySide6.QtWidgets import QWizardPage, QVBoxLayout

from social_distance.widgets.top_view_preview import TopViewPreview


class PreviewSettingsPage(QWizardPage):
    def __init__(self, parent):
        super(PreviewSettingsPage, self).__init__(parent)
        self.parent = parent
        self.setTitle("Preview settings")
        self.setSubTitle("Select preview settings")

        self.top_view_preview = TopViewPreview(self)
        self.top_view_preview.data_changed.connect(self.preview_square_changed)

        layout = QVBoxLayout()
        layout.addWidget(self.top_view_preview)
        self.setLayout(layout)

    def preview_square_changed(self, square):
        self.parent.preview_square = square

    def initializePage(self) -> None:
        frame = self.parent.frame
        square = self.parent.square
        self.top_view_preview.init(frame, square)
