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
from PySide6.QtWidgets import (QApplication, QDialog, QFrame, QGraphicsView,
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
        self.preview = QGraphicsView(self.horizontalLayoutWidget)
        self.preview.setObjectName(u"preview")
        self.preview.setAutoFillBackground(True)

        self.horizontalLayout.addWidget(self.preview)

        self.verticalLayout = QVBoxLayout()
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.label = QLabel(self.horizontalLayoutWidget)
        self.label.setObjectName(u"label")

        self.verticalLayout.addWidget(self.label)

        self.address = QLineEdit(self.horizontalLayoutWidget)
        self.address.setObjectName(u"address")
        sizePolicy = QSizePolicy(QSizePolicy.MinimumExpanding, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.address.sizePolicy().hasHeightForWidth())
        self.address.setSizePolicy(sizePolicy)

        self.verticalLayout.addWidget(self.address)

        self.connect_button = QPushButton(self.horizontalLayoutWidget)
        self.connect_button.setObjectName(u"connect_button")
        sizePolicy.setHeightForWidth(self.connect_button.sizePolicy().hasHeightForWidth())
        self.connect_button.setSizePolicy(sizePolicy)

        self.verticalLayout.addWidget(self.connect_button)

        self.line = QFrame(self.horizontalLayoutWidget)
        self.line.setObjectName(u"line")
        self.line.setFrameShape(QFrame.HLine)
        self.line.setFrameShadow(QFrame.Sunken)

        self.verticalLayout.addWidget(self.line)

        self.label_2 = QLabel(self.horizontalLayoutWidget)
        self.label_2.setObjectName(u"label_2")

        self.verticalLayout.addWidget(self.label_2)

        self.distance = QLineEdit(self.horizontalLayoutWidget)
        self.distance.setObjectName(u"distance")
        sizePolicy.setHeightForWidth(self.distance.sizePolicy().hasHeightForWidth())
        self.distance.setSizePolicy(sizePolicy)

        self.verticalLayout.addWidget(self.distance)

        self.verticalSpacer = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)

        self.verticalLayout.addItem(self.verticalSpacer)

        self.add_button = QPushButton(self.horizontalLayoutWidget)
        self.add_button.setObjectName(u"add_button")

        self.verticalLayout.addWidget(self.add_button)


        self.horizontalLayout.addLayout(self.verticalLayout)


        self.retranslateUi(AddCameraDialog)

        QMetaObject.connectSlotsByName(AddCameraDialog)
    # setupUi

    def retranslateUi(self, AddCameraDialog):
        AddCameraDialog.setWindowTitle(QCoreApplication.translate("AddCameraDialog", u"Dialog", None))
        self.label.setText(QCoreApplication.translate("AddCameraDialog", u"Address", None))
        self.connect_button.setText(QCoreApplication.translate("AddCameraDialog", u"Connect", None))
        self.label_2.setText(QCoreApplication.translate("AddCameraDialog", u"Distance", None))
        self.add_button.setText(QCoreApplication.translate("AddCameraDialog", u"Add", None))
    # retranslateUi

