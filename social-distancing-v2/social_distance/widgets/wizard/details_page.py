from PySide6.QtWidgets import QWizardPage, QLabel, QLineEdit, QDoubleSpinBox, QGridLayout


class DetailsPage(QWizardPage):
    def __init__(self, parent=None):
        super(DetailsPage, self).__init__(parent)
        self.setTitle("Square side length")
        self.setSubTitle("Input square side length")

        layout = QGridLayout(self)
        layout.addWidget(QLabel("Square side length:"), 0, 0)

        self._length_edit = QDoubleSpinBox()
        self._length_edit.setRange(0.1, 100)
        self._length_edit.setSingleStep(0.1)
        self._length_edit.setValue(1)
        self._length_edit.setSuffix(" m")

        layout.addWidget(self._length_edit, 0, 1)

        layout.addWidget(QLabel("Camera name:"), 1, 0)

        self._camera_name_edit = QLineEdit()
        self._camera_name_edit.setText(self.field("address"))

        layout.addWidget(self._camera_name_edit, 1, 1)

        self.setLayout(layout)
        self.registerField("side_length", self._length_edit, "value", "valueChanged")
        self.registerField("camera_name", self._camera_name_edit)

    def initializePage(self) -> None:
        self._camera_name_edit.setText(self.field("address"))
