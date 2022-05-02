from PySide6.QtWidgets import QWizardPage, QVBoxLayout

from social_distance.widgets.top_view_preview import TopViewPreview


class PreviewSettingsPage(QWizardPage):
    def __init__(self, parent):
        super(PreviewSettingsPage, self).__init__(parent)
        self.parent = parent
        self.setTitle("Preview settings")
        self.setSubTitle("Select preview settings")

        self.top_view_preview = TopViewPreview(self)
        self.top_view_preview.data_changed.connect(self.data_changed)

        layout = QVBoxLayout()
        layout.addWidget(self.top_view_preview)
        self.setLayout(layout)

    def data_changed(self, data):
        square, side_length = data
        self.parent.preview_square = square
        self.parent.preview_side_length = side_length

    def initializePage(self) -> None:
        frame = self.parent.frame
        square = self.parent.square
        self.top_view_preview.init(frame, square)
