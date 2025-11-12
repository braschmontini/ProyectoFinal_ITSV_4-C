# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'proyecto.ui'
##
## Created by: Qt User Interface Compiler version 6.9.3
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
from PySide6.QtWidgets import (QApplication, QComboBox, QFrame, QGridLayout,
    QGroupBox, QHBoxLayout, QLCDNumber, QLabel,
    QListWidget, QListWidgetItem, QMainWindow, QProgressBar,
    QPushButton, QSizePolicy, QSpacerItem, QSpinBox,
    QStatusBar, QVBoxLayout, QWidget)

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        if not MainWindow.objectName():
            MainWindow.setObjectName(u"MainWindow")
        MainWindow.resize(866, 472)
        self.centralwidget = QWidget(MainWindow)
        self.centralwidget.setObjectName(u"centralwidget")
        self.verticalLayout = QVBoxLayout(self.centralwidget)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.labelTitle = QLabel(self.centralwidget)
        self.labelTitle.setObjectName(u"labelTitle")
        font = QFont()
        font.setPointSize(16)
        font.setBold(True)
        self.labelTitle.setFont(font)
        self.labelTitle.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.verticalLayout.addWidget(self.labelTitle)

        self.hLayoutCabinas = QHBoxLayout()
        self.hLayoutCabinas.setObjectName(u"hLayoutCabinas")
        self.groupFree = QGroupBox(self.centralwidget)
        self.groupFree.setObjectName(u"groupFree")
        self.vboxFree = QVBoxLayout(self.groupFree)
        self.vboxFree.setObjectName(u"vboxFree")
        self.listFree = QListWidget(self.groupFree)
        self.listFree.setObjectName(u"listFree")

        self.vboxFree.addWidget(self.listFree)

        self.gridLayout = QGridLayout()
        self.gridLayout.setObjectName(u"gridLayout")
        self.labelSelect = QLabel(self.groupFree)
        self.labelSelect.setObjectName(u"labelSelect")

        self.gridLayout.addWidget(self.labelSelect, 0, 0, 1, 1)

        self.comboBox = QComboBox(self.groupFree)
        self.comboBox.setObjectName(u"comboBox")

        self.gridLayout.addWidget(self.comboBox, 0, 1, 1, 1)

        self.horizontalSpacer = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.gridLayout.addItem(self.horizontalSpacer, 0, 2, 1, 1)

        self.labelCredits = QLabel(self.groupFree)
        self.labelCredits.setObjectName(u"labelCredits")

        self.gridLayout.addWidget(self.labelCredits, 0, 3, 1, 1)

        self.spinCreditos = QSpinBox(self.groupFree)
        self.spinCreditos.setObjectName(u"spinCreditos")
        self.spinCreditos.setMinimum(1)
        self.spinCreditos.setMaximum(60)
        self.spinCreditos.setValue(1)

        self.gridLayout.addWidget(self.spinCreditos, 0, 4, 1, 1)

        self.horizontalSpacer_2 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.gridLayout.addItem(self.horizontalSpacer_2, 0, 5, 1, 1)

        self.pushIniciar = QPushButton(self.groupFree)
        self.pushIniciar.setObjectName(u"pushIniciar")

        self.gridLayout.addWidget(self.pushIniciar, 0, 6, 1, 1)


        self.vboxFree.addLayout(self.gridLayout)


        self.hLayoutCabinas.addWidget(self.groupFree)


        self.verticalLayout.addLayout(self.hLayoutCabinas)

        self.hLayoutTimerOptions = QHBoxLayout()
        self.hLayoutTimerOptions.setObjectName(u"hLayoutTimerOptions")
        self.groupTimer = QGroupBox(self.centralwidget)
        self.groupTimer.setObjectName(u"groupTimer")
        self.vboxTimer = QVBoxLayout(self.groupTimer)
        self.vboxTimer.setObjectName(u"vboxTimer")
        self.lcdTime = QLCDNumber(self.groupTimer)
        self.lcdTime.setObjectName(u"lcdTime")
        self.lcdTime.setFrameShape(QFrame.Shape.NoFrame)
        self.lcdTime.setSmallDecimalPoint(False)
        self.lcdTime.setDigitCount(10)
        self.lcdTime.setProperty(u"value", 0.000000000000000)
        self.lcdTime.setProperty(u"intValue", 0)

        self.vboxTimer.addWidget(self.lcdTime)

        self.progressTime = QProgressBar(self.groupTimer)
        self.progressTime.setObjectName(u"progressTime")
        self.progressTime.setValue(0)

        self.vboxTimer.addWidget(self.progressTime)


        self.hLayoutTimerOptions.addWidget(self.groupTimer)

        self.groupWashOptions = QGroupBox(self.centralwidget)
        self.groupWashOptions.setObjectName(u"groupWashOptions")
        self.gridWash = QGridLayout(self.groupWashOptions)
        self.gridWash.setObjectName(u"gridWash")
        self.btnJabon = QPushButton(self.groupWashOptions)
        self.btnJabon.setObjectName(u"btnJabon")

        self.gridWash.addWidget(self.btnJabon, 0, 1, 1, 1)

        self.btnDeseng = QPushButton(self.groupWashOptions)
        self.btnDeseng.setObjectName(u"btnDeseng")

        self.gridWash.addWidget(self.btnDeseng, 1, 1, 1, 1)

        self.btnCera = QPushButton(self.groupWashOptions)
        self.btnCera.setObjectName(u"btnCera")

        self.gridWash.addWidget(self.btnCera, 1, 0, 1, 1)

        self.btnAgua = QPushButton(self.groupWashOptions)
        self.btnAgua.setObjectName(u"btnAgua")

        self.gridWash.addWidget(self.btnAgua, 0, 0, 1, 1)

        self.btnEnjuague = QPushButton(self.groupWashOptions)
        self.btnEnjuague.setObjectName(u"btnEnjuague")

        self.gridWash.addWidget(self.btnEnjuague, 2, 0, 1, 2)


        self.hLayoutTimerOptions.addWidget(self.groupWashOptions)

        self.groupQR = QGroupBox(self.centralwidget)
        self.groupQR.setObjectName(u"groupQR")
        self.vboxQR = QVBoxLayout(self.groupQR)
        self.vboxQR.setObjectName(u"vboxQR")
        self.labelQR = QLabel(self.groupQR)
        self.labelQR.setObjectName(u"labelQR")
        self.labelQR.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.vboxQR.addWidget(self.labelQR)


        self.hLayoutTimerOptions.addWidget(self.groupQR)


        self.verticalLayout.addLayout(self.hLayoutTimerOptions)

        self.statusbar = QStatusBar(self.centralwidget)
        self.statusbar.setObjectName(u"statusbar")

        self.verticalLayout.addWidget(self.statusbar)

        MainWindow.setCentralWidget(self.centralwidget)

        self.retranslateUi(MainWindow)
        self.pushIniciar.clicked.connect(MainWindow.creditos)

        QMetaObject.connectSlotsByName(MainWindow)
    # setupUi

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QCoreApplication.translate("MainWindow", u"AquaManager", None))
        self.labelTitle.setText(QCoreApplication.translate("MainWindow", u"AquaManager - Panel de Control", None))
        self.groupFree.setTitle(QCoreApplication.translate("MainWindow", u"Boxes:", None))
        self.labelSelect.setText(QCoreApplication.translate("MainWindow", u"Box seleccionada:", None))
        self.labelCredits.setText(QCoreApplication.translate("MainWindow", u"Cr\u00e9ditos:", None))
        self.pushIniciar.setText(QCoreApplication.translate("MainWindow", u"Asignar cr\u00e9ditos", None))
        self.groupTimer.setTitle(QCoreApplication.translate("MainWindow", u"Tiempo restante", None))
        self.groupWashOptions.setTitle(QCoreApplication.translate("MainWindow", u"Opcion de lavado seleccionado", None))
        self.btnJabon.setText(QCoreApplication.translate("MainWindow", u"Agua con Jab\u00f3n", None))
        self.btnDeseng.setText(QCoreApplication.translate("MainWindow", u"Desengrasante", None))
        self.btnCera.setText(QCoreApplication.translate("MainWindow", u" Agua con Cera", None))
        self.btnAgua.setText(QCoreApplication.translate("MainWindow", u"Agua", None))
        self.btnEnjuague.setText(QCoreApplication.translate("MainWindow", u"Enjuague final", None))
        self.groupQR.setTitle(QCoreApplication.translate("MainWindow", u"QR de pago", None))
        self.labelQR.setText(QCoreApplication.translate("MainWindow", u"[QR - vinculado a cuenta]", None))
    # retranslateUi

