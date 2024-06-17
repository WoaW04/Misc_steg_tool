# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'LSBWindow.ui'
##
## Created by: Qt User Interface Compiler version 6.5.0
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide6.QtCore import (QCoreApplication, QDate, QDateTime, QLocale,
    QMetaObject, QObject, QPoint, QRect,
    QSize, QTime, QUrl, Qt)
from PySide6.QtGui import (QAction, QBrush, QColor, QConicalGradient,
    QCursor, QFont, QFontDatabase, QGradient,
    QIcon, QImage, QKeySequence, QLinearGradient,
    QPainter, QPalette, QPixmap, QRadialGradient,
    QTransform)
from PySide6.QtWidgets import (QApplication, QCheckBox, QFrame, QHBoxLayout,
    QLabel, QLineEdit, QMainWindow, QPlainTextEdit,
    QProgressBar, QPushButton, QSizePolicy, QSpacerItem,
    QStatusBar, QTabWidget, QVBoxLayout, QWidget)

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        if not MainWindow.objectName():
            MainWindow.setObjectName(u"MainWindow")
        MainWindow.resize(754, 608)
        MainWindow.setAutoFillBackground(False)
        MainWindow.setStyleSheet(u"")
        self.actionAbout = QAction(MainWindow)
        self.actionAbout.setObjectName(u"actionAbout")
        self.centralwidget = QWidget(MainWindow)
        self.centralwidget.setObjectName(u"centralwidget")
        self.verticalLayout_5 = QVBoxLayout(self.centralwidget)
        self.verticalLayout_5.setObjectName(u"verticalLayout_5")
        self.tabWidget = QTabWidget(self.centralwidget)
        self.tabWidget.setObjectName(u"tabWidget")
        self.tab = QWidget()
        self.tab.setObjectName(u"tab")
        self.verticalLayout_6 = QVBoxLayout(self.tab)
        self.verticalLayout_6.setObjectName(u"verticalLayout_6")
        self.horizontalLayout_2 = QHBoxLayout()
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.horizontalSpacer_5 = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout_2.addItem(self.horizontalSpacer_5)

        self.label_3 = QLabel(self.tab)
        self.label_3.setObjectName(u"label_3")

        self.horizontalLayout_2.addWidget(self.label_3)

        self.lineEdit = QLineEdit(self.tab)
        self.lineEdit.setObjectName(u"lineEdit")

        self.horizontalLayout_2.addWidget(self.lineEdit)

        self.pushButton = QPushButton(self.tab)
        self.pushButton.setObjectName(u"pushButton")
        self.pushButton.setAutoFillBackground(False)
        self.pushButton.setAutoDefault(True)

        self.horizontalLayout_2.addWidget(self.pushButton)

        self.horizontalSpacer_6 = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout_2.addItem(self.horizontalSpacer_6)


        self.verticalLayout_6.addLayout(self.horizontalLayout_2)

        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.label = QLabel(self.tab)
        self.label.setObjectName(u"label")

        self.horizontalLayout.addWidget(self.label)

        self.label_2 = QLabel(self.tab)
        self.label_2.setObjectName(u"label_2")

        self.horizontalLayout.addWidget(self.label_2)


        self.verticalLayout_6.addLayout(self.horizontalLayout)

        self.horizontalLayout_5 = QHBoxLayout()
        self.horizontalLayout_5.setObjectName(u"horizontalLayout_5")
        self.horizontalSpacer_4 = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout_5.addItem(self.horizontalSpacer_4)

        self.verticalLayout_2 = QVBoxLayout()
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.verticalLayout = QVBoxLayout()
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.label_7 = QLabel(self.tab)
        self.label_7.setObjectName(u"label_7")

        self.verticalLayout.addWidget(self.label_7)

        self.plainTextEdit = QPlainTextEdit(self.tab)
        self.plainTextEdit.setObjectName(u"plainTextEdit")

        self.verticalLayout.addWidget(self.plainTextEdit)


        self.verticalLayout_2.addLayout(self.verticalLayout)

        self.verticalSpacer_2 = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)

        self.verticalLayout_2.addItem(self.verticalSpacer_2)

        self.horizontalLayout_3 = QHBoxLayout()
        self.horizontalLayout_3.setObjectName(u"horizontalLayout_3")
        self.label_9 = QLabel(self.tab)
        self.label_9.setObjectName(u"label_9")

        self.horizontalLayout_3.addWidget(self.label_9)

        self.lineEdit_2 = QLineEdit(self.tab)
        self.lineEdit_2.setObjectName(u"lineEdit_2")
        self.lineEdit_2.setInputMethodHints(Qt.ImhHiddenText|Qt.ImhNoAutoUppercase|Qt.ImhNoPredictiveText|Qt.ImhSensitiveData)
        self.lineEdit_2.setEchoMode(QLineEdit.Password)

        self.horizontalLayout_3.addWidget(self.lineEdit_2)

        self.checkBox = QCheckBox(self.tab)
        self.checkBox.setObjectName(u"checkBox")

        self.horizontalLayout_3.addWidget(self.checkBox)


        self.verticalLayout_2.addLayout(self.horizontalLayout_3)

        self.verticalSpacer_9 = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)

        self.verticalLayout_2.addItem(self.verticalSpacer_9)

        self.horizontalLayout_6 = QHBoxLayout()
        self.horizontalLayout_6.setObjectName(u"horizontalLayout_6")
        self.label_11 = QLabel(self.tab)
        self.label_11.setObjectName(u"label_11")

        self.horizontalLayout_6.addWidget(self.label_11)

        self.progressBar = QProgressBar(self.tab)
        self.progressBar.setObjectName(u"progressBar")
        self.progressBar.setValue(0)
        self.progressBar.setTextVisible(True)

        self.horizontalLayout_6.addWidget(self.progressBar)


        self.verticalLayout_2.addLayout(self.horizontalLayout_6)

        self.verticalSpacer = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)

        self.verticalLayout_2.addItem(self.verticalSpacer)

        self.pushButton_2 = QPushButton(self.tab)
        self.pushButton_2.setObjectName(u"pushButton_2")

        self.verticalLayout_2.addWidget(self.pushButton_2, 0, Qt.AlignHCenter)


        self.horizontalLayout_5.addLayout(self.verticalLayout_2)

        self.horizontalSpacer = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout_5.addItem(self.horizontalSpacer)

        self.line = QFrame(self.tab)
        self.line.setObjectName(u"line")
        self.line.setFrameShape(QFrame.VLine)
        self.line.setFrameShadow(QFrame.Sunken)

        self.horizontalLayout_5.addWidget(self.line)

        self.horizontalSpacer_2 = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout_5.addItem(self.horizontalSpacer_2)

        self.verticalLayout_4 = QVBoxLayout()
        self.verticalLayout_4.setObjectName(u"verticalLayout_4")
        self.horizontalLayout_4 = QHBoxLayout()
        self.horizontalLayout_4.setObjectName(u"horizontalLayout_4")
        self.label_10 = QLabel(self.tab)
        self.label_10.setObjectName(u"label_10")

        self.horizontalLayout_4.addWidget(self.label_10)

        self.lineEdit_3 = QLineEdit(self.tab)
        self.lineEdit_3.setObjectName(u"lineEdit_3")
        self.lineEdit_3.setInputMethodHints(Qt.ImhHiddenText|Qt.ImhNoAutoUppercase|Qt.ImhNoPredictiveText|Qt.ImhSensitiveData)
        self.lineEdit_3.setEchoMode(QLineEdit.Password)

        self.horizontalLayout_4.addWidget(self.lineEdit_3)

        self.checkBox_2 = QCheckBox(self.tab)
        self.checkBox_2.setObjectName(u"checkBox_2")

        self.horizontalLayout_4.addWidget(self.checkBox_2)


        self.verticalLayout_4.addLayout(self.horizontalLayout_4)

        self.verticalSpacer_4 = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)

        self.verticalLayout_4.addItem(self.verticalSpacer_4)

        self.pushButton_3 = QPushButton(self.tab)
        self.pushButton_3.setObjectName(u"pushButton_3")

        self.verticalLayout_4.addWidget(self.pushButton_3, 0, Qt.AlignHCenter)

        self.verticalSpacer_8 = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)

        self.verticalLayout_4.addItem(self.verticalSpacer_8)

        self.horizontalLayout_7 = QHBoxLayout()
        self.horizontalLayout_7.setObjectName(u"horizontalLayout_7")
        self.label_13 = QLabel(self.tab)
        self.label_13.setObjectName(u"label_13")

        self.horizontalLayout_7.addWidget(self.label_13)

        self.progressBar_2 = QProgressBar(self.tab)
        self.progressBar_2.setObjectName(u"progressBar_2")
        self.progressBar_2.setEnabled(True)
        self.progressBar_2.setMaximum(100)
        self.progressBar_2.setValue(0)
        self.progressBar_2.setTextVisible(True)

        self.horizontalLayout_7.addWidget(self.progressBar_2)


        self.verticalLayout_4.addLayout(self.horizontalLayout_7)

        self.verticalSpacer_3 = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)

        self.verticalLayout_4.addItem(self.verticalSpacer_3)

        self.verticalLayout_3 = QVBoxLayout()
        self.verticalLayout_3.setObjectName(u"verticalLayout_3")
        self.label_12 = QLabel(self.tab)
        self.label_12.setObjectName(u"label_12")

        self.verticalLayout_3.addWidget(self.label_12)

        self.plainTextEdit_2 = QPlainTextEdit(self.tab)
        self.plainTextEdit_2.setObjectName(u"plainTextEdit_2")
        self.plainTextEdit_2.setReadOnly(True)

        self.verticalLayout_3.addWidget(self.plainTextEdit_2)


        self.verticalLayout_4.addLayout(self.verticalLayout_3)


        self.horizontalLayout_5.addLayout(self.verticalLayout_4)

        self.horizontalSpacer_3 = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout_5.addItem(self.horizontalSpacer_3)


        self.verticalLayout_6.addLayout(self.horizontalLayout_5)

        self.tabWidget.addTab(self.tab, "")
        self.tab_2 = QWidget()
        self.tab_2.setObjectName(u"tab_2")
        self.verticalLayout_11 = QVBoxLayout(self.tab_2)
        self.verticalLayout_11.setObjectName(u"verticalLayout_11")
        self.horizontalLayout_13 = QHBoxLayout()
        self.horizontalLayout_13.setObjectName(u"horizontalLayout_13")
        self.label_4 = QLabel(self.tab_2)
        self.label_4.setObjectName(u"label_4")

        self.horizontalLayout_13.addWidget(self.label_4)

        self.label_5 = QLabel(self.tab_2)
        self.label_5.setObjectName(u"label_5")

        self.horizontalLayout_13.addWidget(self.label_5)


        self.verticalLayout_11.addLayout(self.horizontalLayout_13)

        self.horizontalLayout_8 = QHBoxLayout()
        self.horizontalLayout_8.setObjectName(u"horizontalLayout_8")
        self.horizontalSpacer_7 = QSpacerItem(13, 17, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout_8.addItem(self.horizontalSpacer_7)

        self.verticalLayout_7 = QVBoxLayout()
        self.verticalLayout_7.setObjectName(u"verticalLayout_7")
        self.verticalLayout_8 = QVBoxLayout()
        self.verticalLayout_8.setObjectName(u"verticalLayout_8")
        self.label_8 = QLabel(self.tab_2)
        self.label_8.setObjectName(u"label_8")

        self.verticalLayout_8.addWidget(self.label_8)

        self.horizontalLayout_15 = QHBoxLayout()
        self.horizontalLayout_15.setObjectName(u"horizontalLayout_15")
        self.lineEdit_4 = QLineEdit(self.tab_2)
        self.lineEdit_4.setObjectName(u"lineEdit_4")

        self.horizontalLayout_15.addWidget(self.lineEdit_4)

        self.pushButton_4 = QPushButton(self.tab_2)
        self.pushButton_4.setObjectName(u"pushButton_4")

        self.horizontalLayout_15.addWidget(self.pushButton_4)


        self.verticalLayout_8.addLayout(self.horizontalLayout_15)


        self.verticalLayout_7.addLayout(self.verticalLayout_8)

        self.verticalSpacer_5 = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)

        self.verticalLayout_7.addItem(self.verticalSpacer_5)

        self.horizontalLayout_9 = QHBoxLayout()
        self.horizontalLayout_9.setObjectName(u"horizontalLayout_9")
        self.label_14 = QLabel(self.tab_2)
        self.label_14.setObjectName(u"label_14")

        self.horizontalLayout_9.addWidget(self.label_14)

        self.lineEdit_5 = QLineEdit(self.tab_2)
        self.lineEdit_5.setObjectName(u"lineEdit_5")
        self.lineEdit_5.setInputMethodHints(Qt.ImhHiddenText|Qt.ImhNoAutoUppercase|Qt.ImhNoPredictiveText|Qt.ImhSensitiveData)
        self.lineEdit_5.setEchoMode(QLineEdit.Password)

        self.horizontalLayout_9.addWidget(self.lineEdit_5)

        self.checkBox_3 = QCheckBox(self.tab_2)
        self.checkBox_3.setObjectName(u"checkBox_3")

        self.horizontalLayout_9.addWidget(self.checkBox_3)


        self.verticalLayout_7.addLayout(self.horizontalLayout_9)

        self.verticalSpacer_10 = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)

        self.verticalLayout_7.addItem(self.verticalSpacer_10)

        self.horizontalLayout_10 = QHBoxLayout()
        self.horizontalLayout_10.setObjectName(u"horizontalLayout_10")
        self.label_15 = QLabel(self.tab_2)
        self.label_15.setObjectName(u"label_15")

        self.horizontalLayout_10.addWidget(self.label_15)

        self.progressBar_3 = QProgressBar(self.tab_2)
        self.progressBar_3.setObjectName(u"progressBar_3")
        self.progressBar_3.setValue(0)
        self.progressBar_3.setTextVisible(True)

        self.horizontalLayout_10.addWidget(self.progressBar_3)


        self.verticalLayout_7.addLayout(self.horizontalLayout_10)

        self.verticalSpacer_6 = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)

        self.verticalLayout_7.addItem(self.verticalSpacer_6)

        self.pushButton_5 = QPushButton(self.tab_2)
        self.pushButton_5.setObjectName(u"pushButton_5")

        self.verticalLayout_7.addWidget(self.pushButton_5, 0, Qt.AlignHCenter)


        self.horizontalLayout_8.addLayout(self.verticalLayout_7)

        self.horizontalSpacer_8 = QSpacerItem(13, 17, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout_8.addItem(self.horizontalSpacer_8)

        self.line_2 = QFrame(self.tab_2)
        self.line_2.setObjectName(u"line_2")
        self.line_2.setFrameShape(QFrame.VLine)
        self.line_2.setFrameShadow(QFrame.Sunken)

        self.horizontalLayout_8.addWidget(self.line_2)

        self.horizontalSpacer_9 = QSpacerItem(13, 17, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout_8.addItem(self.horizontalSpacer_9)

        self.verticalLayout_9 = QVBoxLayout()
        self.verticalLayout_9.setObjectName(u"verticalLayout_9")
        self.horizontalLayout_11 = QHBoxLayout()
        self.horizontalLayout_11.setObjectName(u"horizontalLayout_11")
        self.label_16 = QLabel(self.tab_2)
        self.label_16.setObjectName(u"label_16")

        self.horizontalLayout_11.addWidget(self.label_16)

        self.lineEdit_6 = QLineEdit(self.tab_2)
        self.lineEdit_6.setObjectName(u"lineEdit_6")
        self.lineEdit_6.setInputMethodHints(Qt.ImhHiddenText|Qt.ImhNoAutoUppercase|Qt.ImhNoPredictiveText|Qt.ImhSensitiveData)
        self.lineEdit_6.setEchoMode(QLineEdit.Password)

        self.horizontalLayout_11.addWidget(self.lineEdit_6)

        self.checkBox_4 = QCheckBox(self.tab_2)
        self.checkBox_4.setObjectName(u"checkBox_4")

        self.horizontalLayout_11.addWidget(self.checkBox_4)


        self.verticalLayout_9.addLayout(self.horizontalLayout_11)

        self.verticalSpacer_7 = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)

        self.verticalLayout_9.addItem(self.verticalSpacer_7)

        self.pushButton_6 = QPushButton(self.tab_2)
        self.pushButton_6.setObjectName(u"pushButton_6")

        self.verticalLayout_9.addWidget(self.pushButton_6, 0, Qt.AlignHCenter)

        self.verticalSpacer_11 = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)

        self.verticalLayout_9.addItem(self.verticalSpacer_11)

        self.horizontalLayout_12 = QHBoxLayout()
        self.horizontalLayout_12.setObjectName(u"horizontalLayout_12")
        self.label_17 = QLabel(self.tab_2)
        self.label_17.setObjectName(u"label_17")

        self.horizontalLayout_12.addWidget(self.label_17)

        self.progressBar_4 = QProgressBar(self.tab_2)
        self.progressBar_4.setObjectName(u"progressBar_4")
        self.progressBar_4.setEnabled(True)
        self.progressBar_4.setMaximum(100)
        self.progressBar_4.setValue(0)
        self.progressBar_4.setTextVisible(True)

        self.horizontalLayout_12.addWidget(self.progressBar_4)


        self.verticalLayout_9.addLayout(self.horizontalLayout_12)

        self.verticalSpacer_12 = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)

        self.verticalLayout_9.addItem(self.verticalSpacer_12)

        self.verticalLayout_10 = QVBoxLayout()
        self.verticalLayout_10.setObjectName(u"verticalLayout_10")
        self.label_18 = QLabel(self.tab_2)
        self.label_18.setObjectName(u"label_18")

        self.verticalLayout_10.addWidget(self.label_18)

        self.plainTextEdit_3 = QPlainTextEdit(self.tab_2)
        self.plainTextEdit_3.setObjectName(u"plainTextEdit_3")
        self.plainTextEdit_3.setMaximumSize(QSize(16777215, 192))

        self.verticalLayout_10.addWidget(self.plainTextEdit_3)


        self.verticalLayout_9.addLayout(self.verticalLayout_10)


        self.horizontalLayout_8.addLayout(self.verticalLayout_9)

        self.horizontalSpacer_10 = QSpacerItem(13, 17, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout_8.addItem(self.horizontalSpacer_10)


        self.verticalLayout_11.addLayout(self.horizontalLayout_8)

        self.tabWidget.addTab(self.tab_2, "")

        self.verticalLayout_5.addWidget(self.tabWidget)

        MainWindow.setCentralWidget(self.centralwidget)
        self.statusbar = QStatusBar(MainWindow)
        self.statusbar.setObjectName(u"statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)

        self.tabWidget.setCurrentIndex(0)


        QMetaObject.connectSlotsByName(MainWindow)
    # setupUi

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QCoreApplication.translate("MainWindow", u"Steganography Software", None))
        self.actionAbout.setText(QCoreApplication.translate("MainWindow", u"About", None))
        self.label_3.setText(QCoreApplication.translate("MainWindow", u"\u8f93\u5165\u56fe\u50cf\u6587\u4ef6\uff1a", None))
        self.pushButton.setText(QCoreApplication.translate("MainWindow", u"\u9009\u62e9\u6587\u4ef6", None))
        self.label.setText(QCoreApplication.translate("MainWindow", u"<html><head/><body><p align=\"center\"><span style=\" font-size:20pt; font-weight:600; color:#5500ff;\">\u6587\u672c\u9690\u5199</span></p></body></html>", None))
        self.label_2.setText(QCoreApplication.translate("MainWindow", u"<html><head/><body><p align=\"center\"><span style=\" font-size:20pt; font-weight:600; color:#5500ff;\">\u6587\u672c\u63d0\u53d6</span></p></body></html>", None))
        self.label_7.setText(QCoreApplication.translate("MainWindow", u"\u8f93\u5165\u9700\u8981\u9690\u5199\u7684\u6587\u672c\uff1a", None))
        self.label_9.setText(QCoreApplication.translate("MainWindow", u"\u8f93\u5165\u5bc6\u7801\uff08\u53ef\u9009\uff09\uff1a", None))
        self.checkBox.setText(QCoreApplication.translate("MainWindow", u"\u663e\u793a\u5bc6\u7801", None))
        self.label_11.setText(QCoreApplication.translate("MainWindow", u"\u8fdb\u5ea6\uff1a", None))
        self.pushButton_2.setText(QCoreApplication.translate("MainWindow", u"\u9690\u5199\u5e76\u4fdd\u5b58", None))
        self.label_10.setText(QCoreApplication.translate("MainWindow", u"\u8f93\u5165\u5bc6\u7801\uff08\u53ef\u9009\uff09\uff1a", None))
        self.checkBox_2.setText(QCoreApplication.translate("MainWindow", u"\u663e\u793a\u5bc6\u7801", None))
        self.pushButton_3.setText(QCoreApplication.translate("MainWindow", u"\u63d0\u53d6", None))
        self.label_13.setText(QCoreApplication.translate("MainWindow", u"\u8fdb\u5ea6\uff1a", None))
        self.label_12.setText(QCoreApplication.translate("MainWindow", u"\u63d0\u53d6\u7684\u9690\u5199\u6587\u672c\uff1a", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab), QCoreApplication.translate("MainWindow", u"\u6587\u672c", None))
        self.label_4.setText(QCoreApplication.translate("MainWindow", u"<html><head/><body><p align=\"center\"><span style=\" font-size:20pt; font-weight:600; color:#5500ff;\">\u6587\u4ef6\u9690\u5199</span></p></body></html>", None))
        self.label_5.setText(QCoreApplication.translate("MainWindow", u"<html><head/><body><p align=\"center\"><span style=\" font-size:20pt; font-weight:600; color:#5500ff;\">\u6587\u4ef6\u63d0\u53d6</span></p></body></html>", None))
        self.label_8.setText(QCoreApplication.translate("MainWindow", u"\u8f93\u5165\u9700\u8981\u9690\u5199\u7684\u6587\u4ef6\uff1a", None))
        self.pushButton_4.setText(QCoreApplication.translate("MainWindow", u"\u9009\u62e9\u6587\u4ef6", None))
        self.label_14.setText(QCoreApplication.translate("MainWindow", u"\u8f93\u5165\u5bc6\u7801\uff08\u53ef\u9009\uff09\uff1a", None))
        self.checkBox_3.setText(QCoreApplication.translate("MainWindow", u"\u663e\u793a\u5bc6\u7801", None))
        self.label_15.setText(QCoreApplication.translate("MainWindow", u"\u8fdb\u5ea6\uff1a", None))
        self.pushButton_5.setText(QCoreApplication.translate("MainWindow", u"\u9690\u5199\u5e76\u4fdd\u5b58", None))
        self.label_16.setText(QCoreApplication.translate("MainWindow", u"\u8f93\u5165\u5bc6\u7801\uff08\u53ef\u9009\uff09\uff1a", None))
        self.checkBox_4.setText(QCoreApplication.translate("MainWindow", u"\u663e\u793a\u5bc6\u7801", None))
        self.pushButton_6.setText(QCoreApplication.translate("MainWindow", u"\u63d0\u53d6", None))
        self.label_17.setText(QCoreApplication.translate("MainWindow", u"\u8fdb\u5ea6\uff1a", None))
        self.label_18.setText(QCoreApplication.translate("MainWindow", u"\u63d0\u53d6\u7684\u9690\u5199\u6587\u4ef6\uff1a", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_2), QCoreApplication.translate("MainWindow", u"\u6587\u4ef6", None))
    # retranslateUi

