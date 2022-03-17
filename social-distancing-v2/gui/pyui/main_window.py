# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'mainwindow.ui'
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
from PySide6.QtWidgets import (QApplication, QCheckBox, QComboBox, QDoubleSpinBox,
    QFrame, QGraphicsView, QGridLayout, QHBoxLayout,
    QLabel, QMainWindow, QMenuBar, QPushButton,
    QSizePolicy, QSpacerItem, QStatusBar, QVBoxLayout,
    QWidget)

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        if not MainWindow.objectName():
            MainWindow.setObjectName(u"MainWindow")
        MainWindow.resize(754, 438)
        sizePolicy = QSizePolicy(QSizePolicy.Maximum, QSizePolicy.Maximum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(MainWindow.sizePolicy().hasHeightForWidth())
        MainWindow.setSizePolicy(sizePolicy)
        self.centralwidget = QWidget(MainWindow)
        self.centralwidget.setObjectName(u"centralwidget")
        sizePolicy.setHeightForWidth(self.centralwidget.sizePolicy().hasHeightForWidth())
        self.centralwidget.setSizePolicy(sizePolicy)
        self.gridLayout = QGridLayout(self.centralwidget)
        self.gridLayout.setObjectName(u"gridLayout")
        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.cameraGraphicsView = QGraphicsView(self.centralwidget)
        self.cameraGraphicsView.setObjectName(u"cameraGraphicsView")
        sizePolicy1 = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        sizePolicy1.setHorizontalStretch(1)
        sizePolicy1.setVerticalStretch(1)
        sizePolicy1.setHeightForWidth(self.cameraGraphicsView.sizePolicy().hasHeightForWidth())
        self.cameraGraphicsView.setSizePolicy(sizePolicy1)

        self.horizontalLayout.addWidget(self.cameraGraphicsView)

        self.verticalLayout = QVBoxLayout()
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.cameraLabel = QLabel(self.centralwidget)
        self.cameraLabel.setObjectName(u"cameraLabel")

        self.verticalLayout.addWidget(self.cameraLabel)

        self.horizontalLayout_3 = QHBoxLayout()
        self.horizontalLayout_3.setSpacing(0)
        self.horizontalLayout_3.setObjectName(u"horizontalLayout_3")
        self.cameraComboBox = QComboBox(self.centralwidget)
        self.cameraComboBox.setObjectName(u"cameraComboBox")

        self.horizontalLayout_3.addWidget(self.cameraComboBox)

        self.addCameraPushButton = QPushButton(self.centralwidget)
        self.addCameraPushButton.setObjectName(u"addCameraPushButton")

        self.horizontalLayout_3.addWidget(self.addCameraPushButton)


        self.verticalLayout.addLayout(self.horizontalLayout_3)

        self.cameraLine = QFrame(self.centralwidget)
        self.cameraLine.setObjectName(u"cameraLine")
        self.cameraLine.setFrameShape(QFrame.HLine)
        self.cameraLine.setFrameShadow(QFrame.Sunken)

        self.verticalLayout.addWidget(self.cameraLine)

        self.detectionCheckBox = QCheckBox(self.centralwidget)
        self.detectionCheckBox.setObjectName(u"detectionCheckBox")

        self.verticalLayout.addWidget(self.detectionCheckBox)

        self.detectionLine = QFrame(self.centralwidget)
        self.detectionLine.setObjectName(u"detectionLine")
        self.detectionLine.setFrameShape(QFrame.HLine)
        self.detectionLine.setFrameShadow(QFrame.Sunken)

        self.verticalLayout.addWidget(self.detectionLine)

        self.horizontalLayout_4 = QHBoxLayout()
        self.horizontalLayout_4.setObjectName(u"horizontalLayout_4")
        self.distanceLabel = QLabel(self.centralwidget)
        self.distanceLabel.setObjectName(u"distanceLabel")

        self.horizontalLayout_4.addWidget(self.distanceLabel)

        self.distanceSpinBox = QDoubleSpinBox(self.centralwidget)
        self.distanceSpinBox.setObjectName(u"distanceSpinBox")
        self.distanceSpinBox.setValue(2.000000000000000)

        self.horizontalLayout_4.addWidget(self.distanceSpinBox)


        self.verticalLayout.addLayout(self.horizontalLayout_4)

        self.verticalSpacer = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)

        self.verticalLayout.addItem(self.verticalSpacer)


        self.horizontalLayout.addLayout(self.verticalLayout)


        self.gridLayout.addLayout(self.horizontalLayout, 0, 0, 1, 1)

        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QMenuBar(MainWindow)
        self.menubar.setObjectName(u"menubar")
        self.menubar.setGeometry(QRect(0, 0, 754, 24))
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QStatusBar(MainWindow)
        self.statusbar.setObjectName(u"statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)

        QMetaObject.connectSlotsByName(MainWindow)
    # setupUi

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QCoreApplication.translate("MainWindow", u"MainWindow", None))
        self.cameraLabel.setText(QCoreApplication.translate("MainWindow", u"Camera:", None))
        self.addCameraPushButton.setText(QCoreApplication.translate("MainWindow", u"+", None))
        self.detectionCheckBox.setText(QCoreApplication.translate("MainWindow", u"Detection", None))
        self.distanceLabel.setText(QCoreApplication.translate("MainWindow", u"Distance", None))
        self.distanceSpinBox.setSuffix(QCoreApplication.translate("MainWindow", u" m", None))
    # retranslateUi

