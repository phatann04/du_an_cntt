# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'compare.ui'
##
## Created by: Qt User Interface Compiler version 6.11.0
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
from PySide6.QtWidgets import (QApplication, QHBoxLayout, QLabel, QLineEdit,
    QMainWindow, QMenuBar, QPushButton, QSizePolicy,
    QStatusBar, QVBoxLayout, QWidget)

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        if not MainWindow.objectName():
            MainWindow.setObjectName(u"MainWindow")
        MainWindow.resize(974, 670)
        self.centralwidget = QWidget(MainWindow)
        self.centralwidget.setObjectName(u"centralwidget")
        self.centralwidget.setStyleSheet(u"background-color: white;")
        self.verticalLayout = QVBoxLayout(self.centralwidget)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.verticalLayout_5 = QVBoxLayout()
        self.verticalLayout_5.setObjectName(u"verticalLayout_5")
        self.input_widget = QWidget(self.centralwidget)
        self.input_widget.setObjectName(u"input_widget")
        self.input_widget.setStyleSheet(u"QWidget#input_widget,\n"
"QWidget#metrics_widget,\n"
"QWidget#chart_widget {\n"
"    border: 1px solid #ccc;\n"
"    background-color: white;\n"
"}")
        self.loadImage = QPushButton(self.input_widget)
        self.loadImage.setObjectName(u"loadImage")
        self.loadImage.setGeometry(QRect(20, 140, 161, 51))
        self.loadImage.setStyleSheet(u"QPushButton {\n"
"    border: 1px solid #cccccc;\n"
"    background-color: rgb(218, 218, 218);\n"
"    border-radius: 6px;\n"
"    padding: 6px;\n"
"}\n"
"\n"
"QPushButton:hover {\n"
"    background-color: rgb(200, 200, 200);\n"
"    border: 1px solid #999999;\n"
"}\n"
"\n"
"QPushButton:pressed {\n"
"    background-color: rgb(180, 180, 180);\n"
"}")
        self.compare = QPushButton(self.input_widget)
        self.compare.setObjectName(u"compare")
        self.compare.setGeometry(QRect(200, 140, 161, 51))
        self.compare.setStyleSheet(u"QPushButton {\n"
"    border: 1px solid #cccccc;\n"
"    background-color: rgb(218, 218, 218);\n"
"    border-radius: 6px;\n"
"    padding: 6px;\n"
"}\n"
"\n"
"QPushButton:hover {\n"
"    background-color: rgb(200, 200, 200);\n"
"    border: 1px solid #999999;\n"
"}\n"
"\n"
"QPushButton:pressed {\n"
"    background-color: rgb(180, 180, 180);\n"
"}")
        self.label = QLabel(self.input_widget)
        self.label.setObjectName(u"label")
        self.label.setGeometry(QRect(20, 40, 151, 16))
        self.label_2 = QLabel(self.input_widget)
        self.label_2.setObjectName(u"label_2")
        self.label_2.setGeometry(QRect(20, 90, 171, 16))
        self.threshold = QLineEdit(self.input_widget)
        self.threshold.setObjectName(u"threshold")
        self.threshold.setGeometry(QRect(210, 40, 113, 21))
        self.k_pairs = QLineEdit(self.input_widget)
        self.k_pairs.setObjectName(u"k_pairs")
        self.k_pairs.setGeometry(QRect(210, 90, 113, 21))
        self.label_4 = QLabel(self.input_widget)
        self.label_4.setObjectName(u"label_4")
        self.label_4.setGeometry(QRect(10, 10, 51, 16))
        font = QFont()
        font.setPointSize(10)
        font.setBold(True)
        self.label_4.setFont(font)
        self.image = QLabel(self.input_widget)
        self.image.setObjectName(u"image")
        self.image.setGeometry(QRect(530, 10, 311, 181))
        self.image.setStyleSheet(u"")

        self.verticalLayout_5.addWidget(self.input_widget)


        self.verticalLayout.addLayout(self.verticalLayout_5)

        self.horizontalLayout_9 = QHBoxLayout()
        self.horizontalLayout_9.setObjectName(u"horizontalLayout_9")
        self.verticalLayout_2 = QVBoxLayout()
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.metrics_widget = QWidget(self.centralwidget)
        self.metrics_widget.setObjectName(u"metrics_widget")
        self.metrics_widget.setAutoFillBackground(False)
        self.metrics_widget.setStyleSheet(u"QWidget#input_widget,\n"
"QWidget#metrics_widget,\n"
"QWidget#chart_widget {\n"
"    border: 1px solid #ccc;\n"
"    background-color: white;\n"
"}")

        self.verticalLayout_2.addWidget(self.metrics_widget)


        self.horizontalLayout_9.addLayout(self.verticalLayout_2)

        self.verticalLayout_6 = QVBoxLayout()
        self.verticalLayout_6.setObjectName(u"verticalLayout_6")
        self.chart_widget = QWidget(self.centralwidget)
        self.chart_widget.setObjectName(u"chart_widget")
        self.chart_widget.setAutoFillBackground(False)
        self.chart_widget.setStyleSheet(u"QWidget#input_widget,\n"
"QWidget#metrics_widget,\n"
"QWidget#chart_widget {\n"
"    border: 1px solid #ccc;\n"
"    background-color: white;\n"
"}")

        self.verticalLayout_6.addWidget(self.chart_widget)


        self.horizontalLayout_9.addLayout(self.verticalLayout_6)

        self.horizontalLayout_9.setStretch(0, 4)
        self.horizontalLayout_9.setStretch(1, 6)

        self.verticalLayout.addLayout(self.horizontalLayout_9)

        self.verticalLayout.setStretch(0, 1)
        self.verticalLayout.setStretch(1, 2)
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QMenuBar(MainWindow)
        self.menubar.setObjectName(u"menubar")
        self.menubar.setGeometry(QRect(0, 0, 974, 22))
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QStatusBar(MainWindow)
        self.statusbar.setObjectName(u"statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)

        QMetaObject.connectSlotsByName(MainWindow)
    # setupUi

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QCoreApplication.translate("MainWindow", u"Compare HS & DE", None))
        self.loadImage.setText(QCoreApplication.translate("MainWindow", u"LOAD IMAGE", None))
        self.compare.setText(QCoreApplication.translate("MainWindow", u"RUN COMPARE", None))
        self.label.setText(QCoreApplication.translate("MainWindow", u"DE - THRESHOLD (T):", None))
        self.label_2.setText(QCoreApplication.translate("MainWindow", u"HS - NUMBER OF PAIRS P-Z (k):", None))
        self.threshold.setText(QCoreApplication.translate("MainWindow", u"8", None))
        self.k_pairs.setText(QCoreApplication.translate("MainWindow", u"3", None))
        self.label_4.setText(QCoreApplication.translate("MainWindow", u"1. Input", None))
        self.image.setText("")
    # retranslateUi

