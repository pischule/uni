# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'mainwindow.ui'
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
from PySide6.QtWidgets import (QApplication, QComboBox, QDoubleSpinBox, QFrame,
    QGraphicsView, QGridLayout, QHBoxLayout, QLabel,
    QMainWindow, QMenuBar, QPushButton, QSizePolicy,
    QSpacerItem, QStatusBar, QVBoxLayout, QWidget)

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        if not MainWindow.objectName():
            MainWindow.setObjectName(u"MainWindow")
        MainWindow.resize(1036, 604)
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
        self.cameraGraphicsView.setAcceptDrops(False)
        self.cameraGraphicsView.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.cameraGraphicsView.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)

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

        self.modelLabel = QLabel(self.centralwidget)
        self.modelLabel.setObjectName(u"modelLabel")

        self.verticalLayout.addWidget(self.modelLabel)

        self.modelComboBox = QComboBox(self.centralwidget)
        self.modelComboBox.setObjectName(u"modelComboBox")

        self.verticalLayout.addWidget(self.modelComboBox)

        self.viewLabel = QLabel(self.centralwidget)
        self.viewLabel.setObjectName(u"viewLabel")

        self.verticalLayout.addWidget(self.viewLabel)

        self.viewComboBox = QComboBox(self.centralwidget)
        self.viewComboBox.addItem("")
        self.viewComboBox.addItem("")
        self.viewComboBox.addItem("")
        self.viewComboBox.setObjectName(u"viewComboBox")

        self.verticalLayout.addWidget(self.viewComboBox)

        self.distanceLabel = QLabel(self.centralwidget)
        self.distanceLabel.setObjectName(u"distanceLabel")

        self.verticalLayout.addWidget(self.distanceLabel)

        self.distanceSpinBox = QDoubleSpinBox(self.centralwidget)
        self.distanceSpinBox.setObjectName(u"distanceSpinBox")
        self.distanceSpinBox.setSingleStep(0.200000000000000)
        self.distanceSpinBox.setValue(2.000000000000000)

        self.verticalLayout.addWidget(self.distanceSpinBox)

        self.line = QFrame(self.centralwidget)
        self.line.setObjectName(u"line")
        self.line.setFrameShape(QFrame.HLine)
        self.line.setFrameShadow(QFrame.Sunken)

        self.verticalLayout.addWidget(self.line)

        self.label = QLabel(self.centralwidget)
        self.label.setObjectName(u"label")

        self.verticalLayout.addWidget(self.label)

        self.statisticsBodyLabel = QLabel(self.centralwidget)
        self.statisticsBodyLabel.setObjectName(u"statisticsBodyLabel")

        self.verticalLayout.addWidget(self.statisticsBodyLabel)

        self.verticalSpacer = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)

        self.verticalLayout.addItem(self.verticalSpacer)

        self.saveDataPushButton = QPushButton(self.centralwidget)
        self.saveDataPushButton.setObjectName(u"saveDataPushButton")

        self.verticalLayout.addWidget(self.saveDataPushButton)


        self.horizontalLayout.addLayout(self.verticalLayout)


        self.gridLayout.addLayout(self.horizontalLayout, 0, 0, 1, 1)

        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QMenuBar(MainWindow)
        self.menubar.setObjectName(u"menubar")
        self.menubar.setGeometry(QRect(0, 0, 1036, 24))
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QStatusBar(MainWindow)
        self.statusbar.setObjectName(u"statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)

        QMetaObject.connectSlotsByName(MainWindow)
    # setupUi

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QCoreApplication.translate("MainWindow", u"Social Distance Monitoring Tool", None))
        self.cameraLabel.setText(QCoreApplication.translate("MainWindow", u"Camera:", None))
        self.addCameraPushButton.setText(QCoreApplication.translate("MainWindow", u"+", None))
        self.modelLabel.setText(QCoreApplication.translate("MainWindow", u"Model:", None))
        self.viewLabel.setText(QCoreApplication.translate("MainWindow", u"View:", None))
        self.viewComboBox.setItemText(0, QCoreApplication.translate("MainWindow", u"Regular", None))
        self.viewComboBox.setItemText(1, QCoreApplication.translate("MainWindow", u"Top-Down", None))
        self.viewComboBox.setItemText(2, QCoreApplication.translate("MainWindow", u"Projected Circles", None))

        self.distanceLabel.setText(QCoreApplication.translate("MainWindow", u"Safe distance:", None))
        self.distanceSpinBox.setSuffix(QCoreApplication.translate("MainWindow", u" m", None))
        self.label.setText(QCoreApplication.translate("MainWindow", u"Statistics:", None))
        self.statisticsBodyLabel.setText("")
        self.saveDataPushButton.setText(QCoreApplication.translate("MainWindow", u"Save data", None))
    # retranslateUi

