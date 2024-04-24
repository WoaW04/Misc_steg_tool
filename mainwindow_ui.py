# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'mainwindow.ui'
##
## Created by: Qt User Interface Compiler version 6.5.0
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
from PySide6.QtWidgets import (QApplication, QHBoxLayout, QMainWindow, QPushButton,
    QSizePolicy, QTabWidget, QTextBrowser, QVBoxLayout,
    QWidget)

class Ui_Img_steg_tool(object):
    def setupUi(self, Img_steg_tool):
        if not Img_steg_tool.objectName():
            Img_steg_tool.setObjectName(u"Img_steg_tool")
        Img_steg_tool.setEnabled(True)
        Img_steg_tool.resize(900, 600)
        sizePolicy = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(Img_steg_tool.sizePolicy().hasHeightForWidth())
        Img_steg_tool.setSizePolicy(sizePolicy)
        self.centralwidget = QWidget(Img_steg_tool)
        self.centralwidget.setObjectName(u"centralwidget")
        sizePolicy.setHeightForWidth(self.centralwidget.sizePolicy().hasHeightForWidth())
        self.centralwidget.setSizePolicy(sizePolicy)
        self.horizontalLayout = QHBoxLayout(self.centralwidget)
        self.horizontalLayout.setSpacing(0)
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.horizontalLayout.setContentsMargins(0, 0, 0, 0)
        self.Tab = QTabWidget(self.centralwidget)
        self.Tab.setObjectName(u"Tab")
        self.Tab.setEnabled(True)
        sizePolicy.setHeightForWidth(self.Tab.sizePolicy().hasHeightForWidth())
        self.Tab.setSizePolicy(sizePolicy)
        self.MainWindow = QWidget()
        self.MainWindow.setObjectName(u"MainWindow")
        sizePolicy.setHeightForWidth(self.MainWindow.sizePolicy().hasHeightForWidth())
        self.MainWindow.setSizePolicy(sizePolicy)
        self.horizontalLayout_2 = QHBoxLayout(self.MainWindow)
        self.horizontalLayout_2.setSpacing(0)
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.horizontalLayout_2.setContentsMargins(0, 0, 0, 0)
        self.ShowImgWidget = QWidget(self.MainWindow)
        self.ShowImgWidget.setObjectName(u"ShowImgWidget")

        self.horizontalLayout_2.addWidget(self.ShowImgWidget)

        self.SideBar = QWidget(self.MainWindow)
        self.SideBar.setObjectName(u"SideBar")
        self.verticalLayout_3 = QVBoxLayout(self.SideBar)
        self.verticalLayout_3.setObjectName(u"verticalLayout_3")
        self.verticalLayout_2 = QVBoxLayout()
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.OpenImg = QPushButton(self.SideBar)
        self.OpenImg.setObjectName(u"OpenImg")

        self.verticalLayout_2.addWidget(self.OpenImg)

        self.SaveCurrentImg = QPushButton(self.SideBar)
        self.SaveCurrentImg.setObjectName(u"SaveCurrentImg")

        self.verticalLayout_2.addWidget(self.SaveCurrentImg)

        self.CleanCurrentImg = QPushButton(self.SideBar)
        self.CleanCurrentImg.setObjectName(u"CleanCurrentImg")

        self.verticalLayout_2.addWidget(self.CleanCurrentImg)


        self.verticalLayout_3.addLayout(self.verticalLayout_2)

        self.widget_3 = QWidget(self.SideBar)
        self.widget_3.setObjectName(u"widget_3")

        self.verticalLayout_3.addWidget(self.widget_3)

        self.verticalLayout_3.setStretch(0, 1)
        self.verticalLayout_3.setStretch(1, 1)

        self.horizontalLayout_2.addWidget(self.SideBar)

        self.horizontalLayout_2.setStretch(0, 3)
        self.horizontalLayout_2.setStretch(1, 1)
        self.Tab.addTab(self.MainWindow, "")
        self.BinaryWindow = QWidget()
        self.BinaryWindow.setObjectName(u"BinaryWindow")
        sizePolicy.setHeightForWidth(self.BinaryWindow.sizePolicy().hasHeightForWidth())
        self.BinaryWindow.setSizePolicy(sizePolicy)
        self.verticalLayout = QVBoxLayout(self.BinaryWindow)
        self.verticalLayout.setSpacing(0)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.ShowBinaryBrowser = QTextBrowser(self.BinaryWindow)
        self.ShowBinaryBrowser.setObjectName(u"ShowBinaryBrowser")

        self.verticalLayout.addWidget(self.ShowBinaryBrowser)

        self.ControlPanel = QWidget(self.BinaryWindow)
        self.ControlPanel.setObjectName(u"ControlPanel")

        self.verticalLayout.addWidget(self.ControlPanel)

        self.verticalLayout.setStretch(0, 1)
        self.verticalLayout.setStretch(1, 1)
        self.Tab.addTab(self.BinaryWindow, "")

        self.horizontalLayout.addWidget(self.Tab)

        Img_steg_tool.setCentralWidget(self.centralwidget)

        self.retranslateUi(Img_steg_tool)

        self.Tab.setCurrentIndex(0)


        QMetaObject.connectSlotsByName(Img_steg_tool)
    # setupUi

    def retranslateUi(self, Img_steg_tool):
        Img_steg_tool.setWindowTitle(QCoreApplication.translate("Img_steg_tool", u"Image Steg Tool", None))
        self.OpenImg.setText(QCoreApplication.translate("Img_steg_tool", u"\u6253\u5f00\u56fe\u7247", None))
        self.SaveCurrentImg.setText(QCoreApplication.translate("Img_steg_tool", u"\u4fdd\u5b58\u5f53\u524d\u56fe\u7247", None))
        self.CleanCurrentImg.setText(QCoreApplication.translate("Img_steg_tool", u"\u6e05\u9664\u5f53\u524d\u56fe\u7247", None))
        self.Tab.setTabText(self.Tab.indexOf(self.MainWindow), QCoreApplication.translate("Img_steg_tool", u"\u4e3b\u7a97\u53e3", None))
        self.Tab.setTabText(self.Tab.indexOf(self.BinaryWindow), QCoreApplication.translate("Img_steg_tool", u"\u663e\u793a\u4e8c\u8fdb\u5236", None))
    # retranslateUi

