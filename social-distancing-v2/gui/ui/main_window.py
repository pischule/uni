# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'main_window.ui'
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
from PySide6.QtWidgets import (QApplication, QCheckBox, QComboBox, QHBoxLayout,
    QLabel, QListView, QPushButton, QSizePolicy,
    QSpacerItem, QVBoxLayout, QWidget)

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        if not MainWindow.objectName():
            MainWindow.setObjectName(u"MainWindow")
        MainWindow.resize(809, 477)
        self.verticalLayoutWidget = QWidget(MainWindow)
        self.verticalLayoutWidget.setObjectName(u"verticalLayoutWidget")
        self.verticalLayoutWidget.setGeometry(QRect(19, 19, 781, 451))
        self.verticalLayout = QVBoxLayout(self.verticalLayoutWidget)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.label_2 = QLabel(self.verticalLayoutWidget)
        self.label_2.setObjectName(u"label_2")

        self.horizontalLayout.addWidget(self.label_2)

        self.camerasComboBox = QComboBox(self.verticalLayoutWidget)
        self.camerasComboBox.setObjectName(u"camerasComboBox")
        sizePolicy = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.camerasComboBox.sizePolicy().hasHeightForWidth())
        self.camerasComboBox.setSizePolicy(sizePolicy)

        self.horizontalLayout.addWidget(self.camerasComboBox)

        self.addCameraButton = QPushButton(self.verticalLayoutWidget)
        self.addCameraButton.setObjectName(u"addCameraButton")

        self.horizontalLayout.addWidget(self.addCameraButton)

        self.horizontalSpacer = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout.addItem(self.horizontalSpacer)

        self.detectionEnabledCheckBox = QCheckBox(self.verticalLayoutWidget)
        self.detectionEnabledCheckBox.setObjectName(u"detectionEnabledCheckBox")

        self.horizontalLayout.addWidget(self.detectionEnabledCheckBox)


        self.verticalLayout.addLayout(self.horizontalLayout)

        self.horizontalLayout_2 = QHBoxLayout()
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.videoLabel = QLabel(self.verticalLayoutWidget)
        self.videoLabel.setObjectName(u"videoLabel")
        self.videoLabel.setAlignment(Qt.AlignCenter)

        self.horizontalLayout_2.addWidget(self.videoLabel)

        self.verticalLayout_2 = QVBoxLayout()
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.label = QLabel(self.verticalLayoutWidget)
        self.label.setObjectName(u"label")
        sizePolicy1 = QSizePolicy(QSizePolicy.Minimum, QSizePolicy.Preferred)
        sizePolicy1.setHorizontalStretch(0)
        sizePolicy1.setVerticalStretch(0)
        sizePolicy1.setHeightForWidth(self.label.sizePolicy().hasHeightForWidth())
        self.label.setSizePolicy(sizePolicy1)

        self.verticalLayout_2.addWidget(self.label)

        self.statsList = QListView(self.verticalLayoutWidget)
        self.statsList.setObjectName(u"statsList")
        sizePolicy2 = QSizePolicy(QSizePolicy.Minimum, QSizePolicy.Expanding)
        sizePolicy2.setHorizontalStretch(0)
        sizePolicy2.setVerticalStretch(0)
        sizePolicy2.setHeightForWidth(self.statsList.sizePolicy().hasHeightForWidth())
        self.statsList.setSizePolicy(sizePolicy2)

        self.verticalLayout_2.addWidget(self.statsList)


        self.horizontalLayout_2.addLayout(self.verticalLayout_2)


        self.verticalLayout.addLayout(self.horizontalLayout_2)


        self.retranslateUi(MainWindow)

        QMetaObject.connectSlotsByName(MainWindow)
    # setupUi

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QCoreApplication.translate("MainWindow", u"Widget", None))
        self.label_2.setText(QCoreApplication.translate("MainWindow", u"Camera", None))
        self.addCameraButton.setText(QCoreApplication.translate("MainWindow", u"+", None))
        self.detectionEnabledCheckBox.setText(QCoreApplication.translate("MainWindow", u"Detection", None))
        self.videoLabel.setText(QCoreApplication.translate("MainWindow", u"Loading...", None))
        self.label.setText(QCoreApplication.translate("MainWindow", u"Stats", None))
    # retranslateUi

