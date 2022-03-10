# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'add_camera_dialog.ui'
##
## Created by: Qt User Interface Compiler version 6.2.3
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide6.QtCore import (QCoreApplication, QDate, QDateTime, QLocale,
    QMetaObject, QObject, QPoint, QRect,
    QSize, QTime, QUrl, Qt)
from PySide6.QtGui import (QBrush, QColor, QConicalGradient, QCursor,
    QFont, QFontDatabase, QGradient, QIcon,
    QImage, QKeySequence, QLinearGradient, QPainter,
    QPalette, QPixmap, QRadialGradient, QTransform)
from PySide6.QtWidgets import (QApplication, QDialog, QDoubleSpinBox, QFrame,
    QHBoxLayout, QLabel, QLineEdit, QPushButton,
    QSizePolicy, QSpacerItem, QVBoxLayout, QWidget)

class Ui_AddCameraDialog(object):
    def setupUi(self, AddCameraDialog):
        if not AddCameraDialog.objectName():
            AddCameraDialog.setObjectName(u"AddCameraDialog")
        AddCameraDialog.resize(800, 443)
        self.horizontalLayoutWidget = QWidget(AddCameraDialog)
        self.horizontalLayoutWidget.setObjectName(u"horizontalLayoutWidget")
        self.horizontalLayoutWidget.setGeometry(QRect(9, 9, 771, 421))
        self.horizontalLayout = QHBoxLayout(self.horizontalLayoutWidget)
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.horizontalLayout.setContentsMargins(0, 0, 0, 0)
        self.previewLabel = QLabel(self.horizontalLayoutWidget)
        self.previewLabel.setObjectName(u"previewLabel")
        sizePolicy = QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.previewLabel.sizePolicy().hasHeightForWidth())
        self.previewLabel.setSizePolicy(sizePolicy)
        self.previewLabel.setMinimumSize(QSize(500, 0))
        self.previewLabel.setAlignment(Qt.AlignCenter)

        self.horizontalLayout.addWidget(self.previewLabel)

        self.verticalLayout = QVBoxLayout()
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.label = QLabel(self.horizontalLayoutWidget)
        self.label.setObjectName(u"label")

        self.verticalLayout.addWidget(self.label)

        self.address = QLineEdit(self.horizontalLayoutWidget)
        self.address.setObjectName(u"address")
        sizePolicy1 = QSizePolicy(QSizePolicy.MinimumExpanding, QSizePolicy.Fixed)
        sizePolicy1.setHorizontalStretch(0)
        sizePolicy1.setVerticalStretch(0)
        sizePolicy1.setHeightForWidth(self.address.sizePolicy().hasHeightForWidth())
        self.address.setSizePolicy(sizePolicy1)
        self.address.setMaxLength(32767)

        self.verticalLayout.addWidget(self.address)

        self.connectButton = QPushButton(self.horizontalLayoutWidget)
        self.connectButton.setObjectName(u"connectButton")
        sizePolicy1.setHeightForWidth(self.connectButton.sizePolicy().hasHeightForWidth())
        self.connectButton.setSizePolicy(sizePolicy1)

        self.verticalLayout.addWidget(self.connectButton)

        self.line = QFrame(self.horizontalLayoutWidget)
        self.line.setObjectName(u"line")
        self.line.setFrameShape(QFrame.HLine)
        self.line.setFrameShadow(QFrame.Sunken)

        self.verticalLayout.addWidget(self.line)

        self.label_2 = QLabel(self.horizontalLayoutWidget)
        self.label_2.setObjectName(u"label_2")

        self.verticalLayout.addWidget(self.label_2)

        self.doubleSpinBox = QDoubleSpinBox(self.horizontalLayoutWidget)
        self.doubleSpinBox.setObjectName(u"doubleSpinBox")
        self.doubleSpinBox.setValue(1.000000000000000)

        self.verticalLayout.addWidget(self.doubleSpinBox)

        self.verticalSpacer = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)

        self.verticalLayout.addItem(self.verticalSpacer)

        self.addButton = QPushButton(self.horizontalLayoutWidget)
        self.addButton.setObjectName(u"addButton")

        self.verticalLayout.addWidget(self.addButton)


        self.horizontalLayout.addLayout(self.verticalLayout)


        self.retranslateUi(AddCameraDialog)

        QMetaObject.connectSlotsByName(AddCameraDialog)
    # setupUi

    def retranslateUi(self, AddCameraDialog):
        AddCameraDialog.setWindowTitle(QCoreApplication.translate("AddCameraDialog", u"Dialog", None))
        self.previewLabel.setText(QCoreApplication.translate("AddCameraDialog", u"Connecting...", None))
        self.label.setText(QCoreApplication.translate("AddCameraDialog", u"Address", None))
        self.address.setInputMask("")
        self.address.setPlaceholderText(QCoreApplication.translate("AddCameraDialog", u"rtsp://192.168.1.1:8080", None))
        self.connectButton.setText(QCoreApplication.translate("AddCameraDialog", u"Connect", None))
        self.label_2.setText(QCoreApplication.translate("AddCameraDialog", u"Distance", None))
        self.doubleSpinBox.setPrefix("")
        self.doubleSpinBox.setSuffix(QCoreApplication.translate("AddCameraDialog", u" m", None))
        self.addButton.setText(QCoreApplication.translate("AddCameraDialog", u"Add", None))
    # retranslateUi

