# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'app.ui'
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
from PySide6.QtWidgets import (QApplication, QHBoxLayout, QHeaderView, QLabel,
    QMainWindow, QPushButton, QSizePolicy, QTableWidget,
    QTableWidgetItem, QVBoxLayout, QWidget)

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        if not MainWindow.objectName():
            MainWindow.setObjectName(u"MainWindow")
        MainWindow.setEnabled(True)
        MainWindow.resize(900, 700)
        MainWindow.setMinimumSize(QSize(900, 700))
        self.centralwidget = QWidget(MainWindow)
        self.centralwidget.setObjectName(u"centralwidget")
        self.centralwidget.setEnabled(True)
        self.centralwidget.setStyleSheet(u"#centralwidget {\n"
"    background: qlineargradient(x1:0, y1:0, x2:1, y2:1, stop:0 #2c3e50, stop:1 #000000);\n"
"}")
        self.verticalLayout_2 = QVBoxLayout(self.centralwidget)
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.layout_buttons = QHBoxLayout()
        self.layout_buttons.setObjectName(u"layout_buttons")
        self.btn_load = QPushButton(self.centralwidget)
        self.btn_load.setObjectName(u"btn_load")
        self.btn_load.setEnabled(True)
        self.btn_load.setMinimumSize(QSize(0, 35))
        self.btn_load.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        self.btn_load.setStyleSheet(u"QPushButton {\n"
"    background-color: #34495e;\n"
"    color: white;\n"
"    border-radius: 8px;\n"
"    font-weight: bold;\n"
"    font-family: \"Segoe UI\";\n"
"}\n"
"QPushButton:hover {\n"
"    background-color: #3498db;\n"
"}\n"
"")

        self.layout_buttons.addWidget(self.btn_load)

        self.btn_rdh = QPushButton(self.centralwidget)
        self.btn_rdh.setObjectName(u"btn_rdh")
        self.btn_rdh.setMinimumSize(QSize(0, 35))
        self.btn_rdh.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        self.btn_rdh.setStyleSheet(u"#btn_rdh {\n"
"    background-color: qlineargradient(spread:pad, x1:0, y1:0, x2:1, y2:0, \n"
"        stop:0 #f39c12, \n"
"        stop:1 #e67e22);\n"
"    \n"
"    color: white;\n"
"    font-weight: bold;\n"
"    font-size: 13px;\n"
"    border-radius: 8px;       \n"
"    min-height: 35px;\n"
"}\n"
"\n"
"#btn_rdh:hover {\n"
"    background-color: qlineargradient(spread:pad, x1:0, y1:0, x2:1, y2:0, \n"
"        stop:0 #ffb347, \n"
"        stop:1 #f39c12);\n"
"    border: 1px solid #ffffff; \n"
"}\n"
"\n"
"#btn_rdh:pressed {\n"
"    background-color: qlineargradient(spread:pad, x1:0, y1:0, x2:1, y2:0, \n"
"        stop:0 #d35400, \n"
"        stop:1 #e67e22);\n"
" \n"
"}")

        self.layout_buttons.addWidget(self.btn_rdh)

        self.btn_save_stego = QPushButton(self.centralwidget)
        self.btn_save_stego.setObjectName(u"btn_save_stego")
        self.btn_save_stego.setMinimumSize(QSize(0, 35))
        self.btn_save_stego.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        self.btn_save_stego.setStyleSheet(u"QPushButton {\n"
"    background-color: #34495e;\n"
"    color: white;\n"
"    border-radius: 8px;\n"
"    font-weight: bold;\n"
"    font-family: \"Segoe UI\";\n"
"}\n"
"QPushButton:hover {\n"
"    background-color: #3498db;\n"
"}\n"
"")

        self.layout_buttons.addWidget(self.btn_save_stego)

        self.bth_save_restore = QPushButton(self.centralwidget)
        self.bth_save_restore.setObjectName(u"bth_save_restore")
        self.bth_save_restore.setMinimumSize(QSize(0, 35))
        self.bth_save_restore.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        self.bth_save_restore.setStyleSheet(u"QPushButton {\n"
"    background-color: #34495e;\n"
"    color: white;\n"
"    border-radius: 8px;\n"
"    font-weight: bold;\n"
"    font-family: \"Segoe UI\";\n"
"}\n"
"QPushButton:hover {\n"
"    background-color: #3498db;\n"
"}\n"
"")

        self.layout_buttons.addWidget(self.bth_save_restore)

        self.btn_clear = QPushButton(self.centralwidget)
        self.btn_clear.setObjectName(u"btn_clear")
        self.btn_clear.setMinimumSize(QSize(35, 35))
        self.btn_clear.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        self.btn_clear.setStyleSheet(u"QPushButton {\n"
"    background-color: #34495e;\n"
"    color: white;\n"
"    border-radius: 8px;\n"
"    font-weight: bold;\n"
"    font-family: \"Segoe UI\";\n"
"}\n"
"QPushButton:hover {\n"
"    background-color: #3498db;\n"
"}\n"
"")

        self.layout_buttons.addWidget(self.btn_clear)


        self.verticalLayout_2.addLayout(self.layout_buttons)

        self.layout_img = QHBoxLayout()
        self.layout_img.setObjectName(u"layout_img")
        self.img_ori = QLabel(self.centralwidget)
        self.img_ori.setObjectName(u"img_ori")
        sizePolicy = QSizePolicy(QSizePolicy.Policy.Ignored, QSizePolicy.Policy.Ignored)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.img_ori.sizePolicy().hasHeightForWidth())
        self.img_ori.setSizePolicy(sizePolicy)
        self.img_ori.setStyleSheet(u"QLabel {\n"
"    background-color: rgba(255, 255, 255, 10); \n"
"    border: 2px solid #555;\n"
"    border-radius: 5px; \n"
"    padding: 5px;\n"
"}\n"
"QLabel:hover {\n"
"    border: 2px solid #3498db; \n"
"}")
        self.img_ori.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.layout_img.addWidget(self.img_ori)

        self.img_stego = QLabel(self.centralwidget)
        self.img_stego.setObjectName(u"img_stego")
        self.img_stego.setEnabled(True)
        sizePolicy.setHeightForWidth(self.img_stego.sizePolicy().hasHeightForWidth())
        self.img_stego.setSizePolicy(sizePolicy)
        self.img_stego.setStyleSheet(u"QLabel {\n"
"    background-color: rgba(255, 255, 255, 10); \n"
"    border: 2px solid #555;\n"
"    border-radius: 5px; \n"
"    padding: 5px;\n"
"}\n"
"QLabel:hover {\n"
"    border: 2px solid #3498db; \n"
"}")
        self.img_stego.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.layout_img.addWidget(self.img_stego)

        self.img_restored = QLabel(self.centralwidget)
        self.img_restored.setObjectName(u"img_restored")
        sizePolicy.setHeightForWidth(self.img_restored.sizePolicy().hasHeightForWidth())
        self.img_restored.setSizePolicy(sizePolicy)
        self.img_restored.setStyleSheet(u"QLabel {\n"
"    background-color: rgba(255, 255, 255, 10); \n"
"    border: 2px solid #555;\n"
"    border-radius: 5px; \n"
"    padding: 5px;\n"
"}\n"
"QLabel:hover {\n"
"    border: 2px solid #3498db; \n"
"}")
        self.img_restored.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.layout_img.addWidget(self.img_restored)


        self.verticalLayout_2.addLayout(self.layout_img)

        self.layout_hist = QHBoxLayout()
        self.layout_hist.setObjectName(u"layout_hist")
        self.hist_ori = QLabel(self.centralwidget)
        self.hist_ori.setObjectName(u"hist_ori")
        sizePolicy.setHeightForWidth(self.hist_ori.sizePolicy().hasHeightForWidth())
        self.hist_ori.setSizePolicy(sizePolicy)
        self.hist_ori.setMinimumSize(QSize(0, 0))
        self.hist_ori.setStyleSheet(u"QLabel {\n"
"    background-color: rgba(255, 255, 255, 10); \n"
"    border: 2px solid #555;\n"
"    border-radius: 5px; \n"
"    padding: 5px;\n"
"}\n"
"QLabel:hover {\n"
"    border: 2px solid #3498db; \n"
"}")
        self.hist_ori.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.layout_hist.addWidget(self.hist_ori)

        self.hist_stego = QLabel(self.centralwidget)
        self.hist_stego.setObjectName(u"hist_stego")
        sizePolicy.setHeightForWidth(self.hist_stego.sizePolicy().hasHeightForWidth())
        self.hist_stego.setSizePolicy(sizePolicy)
        self.hist_stego.setMinimumSize(QSize(0, 0))
        self.hist_stego.setStyleSheet(u"QLabel {\n"
"    background-color: rgba(255, 255, 255, 10); \n"
"    border: 2px solid #555;\n"
"    border-radius: 5px; \n"
"    padding: 5px;\n"
"}\n"
"QLabel:hover {\n"
"    border: 2px solid #3498db; \n"
"}")
        self.hist_stego.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.layout_hist.addWidget(self.hist_stego)

        self.hist_restore = QLabel(self.centralwidget)
        self.hist_restore.setObjectName(u"hist_restore")
        sizePolicy.setHeightForWidth(self.hist_restore.sizePolicy().hasHeightForWidth())
        self.hist_restore.setSizePolicy(sizePolicy)
        self.hist_restore.setMinimumSize(QSize(0, 0))
        self.hist_restore.setStyleSheet(u"QLabel {\n"
"    background-color: rgba(255, 255, 255, 10); \n"
"    border: 2px solid #555;\n"
"    border-radius: 5px; \n"
"    padding: 5px;\n"
"}\n"
"QLabel:hover {\n"
"    border: 2px solid #3498db; \n"
"}")
        self.hist_restore.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.layout_hist.addWidget(self.hist_restore)


        self.verticalLayout_2.addLayout(self.layout_hist)

        self.layout_metrics = QVBoxLayout()
        self.layout_metrics.setObjectName(u"layout_metrics")
        self.metrics = QTableWidget(self.centralwidget)
        self.metrics.setObjectName(u"metrics")
        font = QFont()
        font.setPointSize(10)
        font.setBold(True)
        self.metrics.setFont(font)
        self.metrics.setStyleSheet(u"/* B\u1ea3ng Metrics */\n"
"QTableWidget {\n"
"    background-color: #1e1e1e;\n"
"    gridline-color: #3d3d3d;\n"
"    color: #ffffff;\n"
"    border-radius: 8px;\n"
"}\n"
"\n"
"QHeaderView::section {\n"
"    background-color: #1a1a2e;\n"
"    color: #00d4ff;\n"
"    font-weight: bold;\n"
"    border: none;\n"
"}")

        self.layout_metrics.addWidget(self.metrics)


        self.verticalLayout_2.addLayout(self.layout_metrics)

        self.verticalLayout_2.setStretch(1, 2)
        self.verticalLayout_2.setStretch(2, 2)
        self.verticalLayout_2.setStretch(3, 1)
        MainWindow.setCentralWidget(self.centralwidget)

        self.retranslateUi(MainWindow)

        QMetaObject.connectSlotsByName(MainWindow)
    # setupUi

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QCoreApplication.translate("MainWindow", u"MainWindow", None))
        self.btn_load.setText(QCoreApplication.translate("MainWindow", u"Load Image", None))
        self.btn_rdh.setText(QCoreApplication.translate("MainWindow", u"Run RDH", None))
        self.btn_save_stego.setText(QCoreApplication.translate("MainWindow", u"Save Stego", None))
        self.bth_save_restore.setText(QCoreApplication.translate("MainWindow", u"Save Restored", None))
        self.btn_clear.setText(QCoreApplication.translate("MainWindow", u"Clear", None))
#if QT_CONFIG(tooltip)
        self.img_ori.setToolTip(QCoreApplication.translate("MainWindow", u"Original image", None))
#endif // QT_CONFIG(tooltip)
        self.img_ori.setText("")
#if QT_CONFIG(tooltip)
        self.img_stego.setToolTip(QCoreApplication.translate("MainWindow", u"Stego image", None))
#endif // QT_CONFIG(tooltip)
        self.img_stego.setText("")
#if QT_CONFIG(tooltip)
        self.img_restored.setToolTip(QCoreApplication.translate("MainWindow", u"Restored image", None))
#endif // QT_CONFIG(tooltip)
        self.img_restored.setText("")
#if QT_CONFIG(tooltip)
        self.hist_ori.setToolTip(QCoreApplication.translate("MainWindow", u"Original Histogram", None))
#endif // QT_CONFIG(tooltip)
        self.hist_ori.setText("")
#if QT_CONFIG(tooltip)
        self.hist_stego.setToolTip(QCoreApplication.translate("MainWindow", u"Stego histogram", None))
#endif // QT_CONFIG(tooltip)
        self.hist_stego.setText("")
#if QT_CONFIG(tooltip)
        self.hist_restore.setToolTip(QCoreApplication.translate("MainWindow", u"Restored histogram", None))
#endif // QT_CONFIG(tooltip)
        self.hist_restore.setText("")
    # retranslateUi

