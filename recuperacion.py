# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'recuperacion_de_contraseniaEAEqrx.ui'
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
from PySide6.QtWidgets import (QApplication, QGridLayout, QLabel, QLineEdit,
    QMainWindow, QMenuBar, QPushButton, QSizePolicy,
    QSpacerItem, QWidget)

class Ui_RecuperarContrasea(object):
    def setupUi(self, RecuperarContrasea):
        if not RecuperarContrasea.objectName():
            RecuperarContrasea.setObjectName(u"RecuperarContrasea")
        RecuperarContrasea.resize(860, 504)
        RecuperarContrasea.setStyleSheet(u"background-color: rgb(1, 3, 20);")
        self.centralwidget = QWidget(RecuperarContrasea)
        self.centralwidget.setObjectName(u"centralwidget")
        self.gridLayout_3 = QGridLayout(self.centralwidget)
        self.gridLayout_3.setObjectName(u"gridLayout_3")
        self.horizontalSpacer_4 = QSpacerItem(839, 108, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.gridLayout_3.addItem(self.horizontalSpacer_4, 0, 0, 1, 5)

        self.horizontalSpacer = QSpacerItem(367, 108, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.gridLayout_3.addItem(self.horizontalSpacer, 1, 0, 1, 2)

        self.label = QLabel(self.centralwidget)
        self.label.setObjectName(u"label")
        self.label.setMinimumSize(QSize(80, 80))
        self.label.setMaximumSize(QSize(90, 90))
        self.label.setPixmap(QPixmap(u"Icono_sinfondo.png"))
        self.label.setScaledContents(True)

        self.gridLayout_3.addWidget(self.label, 1, 2, 1, 1)

        self.horizontalSpacer_2 = QSpacerItem(367, 108, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.gridLayout_3.addItem(self.horizontalSpacer_2, 1, 3, 1, 2)

        self.verticalSpacer = QSpacerItem(298, 159, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        self.gridLayout_3.addItem(self.verticalSpacer, 2, 0, 1, 1)

        self.gridLayout_2 = QGridLayout()
        self.gridLayout_2.setObjectName(u"gridLayout_2")
        self.label_5 = QLabel(self.centralwidget)
        self.label_5.setObjectName(u"label_5")
        self.label_5.setMaximumSize(QSize(16777215, 15))
        self.label_5.setStyleSheet(u"background-color: rgb(1, 3, 20);")

        self.gridLayout_2.addWidget(self.label_5, 2, 0, 1, 1)

        self.loginButton = QPushButton(self.centralwidget)
        self.loginButton.setObjectName(u"loginButton")
        self.loginButton.setMaximumSize(QSize(16777215, 16777215))
        font = QFont()
        font.setFamilies([u"Arial"])
        font.setPointSize(11)
        font.setBold(True)
        self.loginButton.setFont(font)
        self.loginButton.setStyleSheet(u"border-color: rgb(0, 0, 0);\n"
"background-color: rgb(255, 255, 255);")

        self.gridLayout_2.addWidget(self.loginButton, 3, 0, 1, 1)

        self.gridLayout = QGridLayout()
        self.gridLayout.setObjectName(u"gridLayout")
        self.label_2 = QLabel(self.centralwidget)
        self.label_2.setObjectName(u"label_2")
        self.label_2.setMinimumSize(QSize(20, 20))
        self.label_2.setMaximumSize(QSize(50, 50))
        self.label_2.setPixmap(QPixmap(u"User.png"))
        self.label_2.setScaledContents(True)

        self.gridLayout.addWidget(self.label_2, 3, 0, 1, 1)

        self.label_3 = QLabel(self.centralwidget)
        self.label_3.setObjectName(u"label_3")

        self.gridLayout.addWidget(self.label_3, 2, 1, 1, 1)

        self.label_6 = QLabel(self.centralwidget)
        self.label_6.setObjectName(u"label_6")

        self.gridLayout.addWidget(self.label_6, 0, 1, 1, 1)

        self.lineEdit = QLineEdit(self.centralwidget)
        self.lineEdit.setObjectName(u"lineEdit")
        self.lineEdit.setStyleSheet(u"background-color: rgb(255, 255, 255);")

        self.gridLayout.addWidget(self.lineEdit, 3, 1, 1, 1)


        self.gridLayout_2.addLayout(self.gridLayout, 1, 0, 1, 1)

        self.label_4 = QLabel(self.centralwidget)
        self.label_4.setObjectName(u"label_4")

        self.gridLayout_2.addWidget(self.label_4, 4, 0, 1, 1)


        self.gridLayout_3.addLayout(self.gridLayout_2, 2, 1, 1, 3)

        self.verticalSpacer_3 = QSpacerItem(298, 159, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        self.gridLayout_3.addItem(self.verticalSpacer_3, 2, 4, 1, 1)

        self.horizontalSpacer_3 = QSpacerItem(839, 48, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.gridLayout_3.addItem(self.horizontalSpacer_3, 3, 0, 1, 5)

        RecuperarContrasea.setCentralWidget(self.centralwidget)
        self.menubar = QMenuBar(RecuperarContrasea)
        self.menubar.setObjectName(u"menubar")
        self.menubar.setGeometry(QRect(0, 0, 860, 33))
        RecuperarContrasea.setMenuBar(self.menubar)

        self.retranslateUi(RecuperarContrasea)
        self.loginButton.clicked.connect(RecuperarContrasea.enviarmail)

        QMetaObject.connectSlotsByName(RecuperarContrasea)
    # setupUi

    def retranslateUi(self, RecuperarContrasea):
        RecuperarContrasea.setWindowTitle(QCoreApplication.translate("RecuperarContrasea", u"MainWindow", None))
        self.label.setText("")
        self.label_5.setText("")
        self.loginButton.setText(QCoreApplication.translate("RecuperarContrasea", u"ENVIAR E-MAIL", None))
        self.label_2.setText("")
        self.label_3.setText("")
        self.label_6.setText("")
        self.lineEdit.setPlaceholderText(QCoreApplication.translate("RecuperarContrasea", u"Ingrese su correo", None))
        self.label_4.setText("")
    # retranslateUi

