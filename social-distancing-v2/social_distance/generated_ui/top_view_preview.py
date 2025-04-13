# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'top_view_preview.ui'
##
## Created by: Qt User Interface Compiler version 6.2.4
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
from PySide6.QtWidgets import (QApplication, QGraphicsView, QGridLayout, QLabel,
    QSizePolicy, QSlider, QWidget)

class Ui_Form(object):
    def setupUi(self, Form):
        if not Form.objectName():
            Form.setObjectName(u"Form")
        Form.resize(652, 641)
        self.gridLayout = QGridLayout(Form)
        self.gridLayout.setObjectName(u"gridLayout")
        self.graphicsView = QGraphicsView(Form)
        self.graphicsView.setObjectName(u"graphicsView")
        self.graphicsView.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.graphicsView.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)

        self.gridLayout.addWidget(self.graphicsView, 1, 1, 1, 1)

        self.label = QLabel(Form)
        self.label.setObjectName(u"label")

        self.gridLayout.addWidget(self.label, 2, 1, 1, 1)

        self.horizontalSlider = QSlider(Form)
        self.horizontalSlider.setObjectName(u"horizontalSlider")
        self.horizontalSlider.setMinimum(-3000)
        self.horizontalSlider.setMaximum(3000)
        self.horizontalSlider.setValue(0)
        self.horizontalSlider.setOrientation(Qt.Horizontal)

        self.gridLayout.addWidget(self.horizontalSlider, 0, 1, 1, 1)

        self.verticalSlider = QSlider(Form)
        self.verticalSlider.setObjectName(u"verticalSlider")
        self.verticalSlider.setMinimum(-3000)
        self.verticalSlider.setMaximum(3000)
        self.verticalSlider.setValue(0)
        self.verticalSlider.setOrientation(Qt.Vertical)
        self.verticalSlider.setInvertedAppearance(True)

        self.gridLayout.addWidget(self.verticalSlider, 1, 0, 1, 1)

        self.scaleSlider = QSlider(Form)
        self.scaleSlider.setObjectName(u"scaleSlider")
        self.scaleSlider.setMinimum(1)
        self.scaleSlider.setMaximum(2000)
        self.scaleSlider.setValue(400)
        self.scaleSlider.setOrientation(Qt.Horizontal)

        self.gridLayout.addWidget(self.scaleSlider, 3, 1, 1, 1)


        self.retranslateUi(Form)

        QMetaObject.connectSlotsByName(Form)
    # setupUi

    def retranslateUi(self, Form):
        Form.setWindowTitle(QCoreApplication.translate("Form", u"Form", None))
        self.label.setText(QCoreApplication.translate("Form", u"Scale:", None))
    # retranslateUi

