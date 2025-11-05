# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'interfazVoZWSt.ui'
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
        MainWindow.resize(878, 472)
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
        self.listaBoxes = QListWidget(self.groupFree)
        font1 = QFont()
        font1.setBold(True)
        __qlistwidgetitem = QListWidgetItem(self.listaBoxes)
        __qlistwidgetitem.setFont(font1);
        __qlistwidgetitem1 = QListWidgetItem(self.listaBoxes)
        __qlistwidgetitem1.setFont(font1);
        __qlistwidgetitem2 = QListWidgetItem(self.listaBoxes)
        __qlistwidgetitem2.setFont(font1);
        __qlistwidgetitem3 = QListWidgetItem(self.listaBoxes)
        __qlistwidgetitem3.setFont(font1);
        font2 = QFont()
        font2.setBold(True)
        font2.setUnderline(False)
        font2.setStrikeOut(False)
        __qlistwidgetitem4 = QListWidgetItem(self.listaBoxes)
        __qlistwidgetitem4.setFont(font2);
        self.listaBoxes.setObjectName(u"listaBoxes")

        self.vboxFree.addWidget(self.listaBoxes)

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

        self.GrupoopcionesBox = QHBoxLayout()
        self.GrupoopcionesBox.setObjectName(u"GrupoopcionesBox")
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


        self.GrupoopcionesBox.addWidget(self.groupTimer)

        self.groupWashOptions = QGroupBox(self.centralwidget)
        self.groupWashOptions.setObjectName(u"groupWashOptions")
        self.gridWash = QGridLayout(self.groupWashOptions)
        self.gridWash.setObjectName(u"gridWash")
        self.jabon = QLabel(self.groupWashOptions)
        self.jabon.setObjectName(u"jabon")
        self.jabon.setLayoutDirection(Qt.LayoutDirection.LeftToRight)
        self.jabon.setFrameShape(QFrame.Shape.StyledPanel)
        self.jabon.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.gridWash.addWidget(self.jabon, 1, 1, 1, 1)

        self.agua = QLabel(self.groupWashOptions)
        self.agua.setObjectName(u"agua")
        self.agua.setLayoutDirection(Qt.LayoutDirection.LeftToRight)
        self.agua.setFrameShape(QFrame.Shape.StyledPanel)
        self.agua.setFrameShadow(QFrame.Shadow.Sunken)
        self.agua.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.gridWash.addWidget(self.agua, 1, 0, 1, 1)

        self.foam = QLabel(self.groupWashOptions)
        self.foam.setObjectName(u"foam")
        self.foam.setLayoutDirection(Qt.LayoutDirection.LeftToRight)
        self.foam.setFrameShape(QFrame.Shape.StyledPanel)
        self.foam.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.gridWash.addWidget(self.foam, 2, 1, 1, 1)

        self.cera = QLabel(self.groupWashOptions)
        self.cera.setObjectName(u"cera")
        self.cera.setLayoutDirection(Qt.LayoutDirection.LeftToRight)
        self.cera.setFrameShape(QFrame.Shape.StyledPanel)
        self.cera.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.gridWash.addWidget(self.cera, 2, 0, 1, 1)

        self.desengrasante = QLabel(self.groupWashOptions)
        self.desengrasante.setObjectName(u"desengrasante")
        self.desengrasante.setLayoutDirection(Qt.LayoutDirection.LeftToRight)
        self.desengrasante.setFrameShape(QFrame.Shape.StyledPanel)
        self.desengrasante.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.gridWash.addWidget(self.desengrasante, 3, 0, 1, 2)


        self.GrupoopcionesBox.addWidget(self.groupWashOptions)

        self.groupQR = QGroupBox(self.centralwidget)
        self.groupQR.setObjectName(u"groupQR")
        self.vboxQR = QVBoxLayout(self.groupQR)
        self.vboxQR.setObjectName(u"vboxQR")
        self.labelQR = QLabel(self.groupQR)
        self.labelQR.setObjectName(u"labelQR")
        self.labelQR.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.vboxQR.addWidget(self.labelQR)


        self.GrupoopcionesBox.addWidget(self.groupQR)


        self.verticalLayout.addLayout(self.GrupoopcionesBox)

        self.statusbar = QStatusBar(self.centralwidget)
        self.statusbar.setObjectName(u"statusbar")

        self.verticalLayout.addWidget(self.statusbar)

        MainWindow.setCentralWidget(self.centralwidget)

        self.retranslateUi(MainWindow)
        self.pushIniciar.clicked.connect(MainWindow.creditos)
        self.listaBoxes.itemClicked.connect(MainWindow.seleccionarBox)

        QMetaObject.connectSlotsByName(MainWindow)
    # setupUi

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QCoreApplication.translate("MainWindow", u"AquaManager", None))
        self.labelTitle.setText(QCoreApplication.translate("MainWindow", u"AquaManager - Panel de Control", None))
        self.groupFree.setTitle(QCoreApplication.translate("MainWindow", u"Boxes:", None))

        __sortingEnabled = self.listaBoxes.isSortingEnabled()
        self.listaBoxes.setSortingEnabled(False)
        ___qlistwidgetitem = self.listaBoxes.item(0)
        ___qlistwidgetitem.setText(QCoreApplication.translate("MainWindow", u"Box1", None));
        ___qlistwidgetitem1 = self.listaBoxes.item(1)
        ___qlistwidgetitem1.setText(QCoreApplication.translate("MainWindow", u"Box2", None));
        ___qlistwidgetitem2 = self.listaBoxes.item(2)
        ___qlistwidgetitem2.setText(QCoreApplication.translate("MainWindow", u"Box3", None));
        ___qlistwidgetitem3 = self.listaBoxes.item(3)
        ___qlistwidgetitem3.setText(QCoreApplication.translate("MainWindow", u"Box4", None));
        ___qlistwidgetitem4 = self.listaBoxes.item(4)
        ___qlistwidgetitem4.setText(QCoreApplication.translate("MainWindow", u"Box5", None));
        self.listaBoxes.setSortingEnabled(__sortingEnabled)

        self.labelSelect.setText(QCoreApplication.translate("MainWindow", u"Box seleccionada:", None))
        self.labelCredits.setText(QCoreApplication.translate("MainWindow", u"Cr\u00e9ditos:", None))
        self.pushIniciar.setText(QCoreApplication.translate("MainWindow", u"Asignar cr\u00e9ditos", None))
        self.groupTimer.setTitle(QCoreApplication.translate("MainWindow", u"Tiempo restante", None))
        self.groupWashOptions.setTitle(QCoreApplication.translate("MainWindow", u"Opcion de lavado seleccionado", None))
        self.jabon.setText(QCoreApplication.translate("MainWindow", u"Hidro Jab\u00f3n", None))
        self.agua.setText(QCoreApplication.translate("MainWindow", u"Hidro Agua", None))
        self.foam.setText(QCoreApplication.translate("MainWindow", u"FOAM", None))
        self.cera.setText(QCoreApplication.translate("MainWindow", u"Hidro Cera", None))
        self.desengrasante.setText(QCoreApplication.translate("MainWindow", u"Desengrasante", None))
        self.groupQR.setTitle(QCoreApplication.translate("MainWindow", u"QR de pago", None))
        self.labelQR.setText(QCoreApplication.translate("MainWindow", u"[QR - vinculado a cuenta]", None))
    # retranslateUi

