# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'twr.ui'
##
## Created by: Qt User Interface Compiler version 6.6.1
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
from PySide6.QtWidgets import (QApplication, QFrame, QHBoxLayout, QLabel,
    QLineEdit, QPlainTextEdit, QPushButton, QSizePolicy,
    QSpacerItem, QTabWidget, QToolButton, QVBoxLayout,
    QWidget)

class Ui_TWR_Form(object):
    def setupUi(self, TWR_Form):
        if not TWR_Form.objectName():
            TWR_Form.setObjectName(u"TWR_Form")
        TWR_Form.resize(960, 600)
        TWR_Form.setMinimumSize(QSize(960, 600))
        TWR_Form.setMaximumSize(QSize(1000, 620))
        self.verticalLayout_5 = QVBoxLayout(TWR_Form)
        self.verticalLayout_5.setObjectName(u"verticalLayout_5")
        self.verticalLayout_4 = QVBoxLayout()
        self.verticalLayout_4.setObjectName(u"verticalLayout_4")
        self.label = QLabel(TWR_Form)
        self.label.setObjectName(u"label")
        self.label.setMinimumSize(QSize(0, 40))
        self.label.setMaximumSize(QSize(16777215, 40))
        font = QFont()
        font.setFamilies([u"\u5b8b\u4f53"])
        font.setPointSize(20)
        self.label.setFont(font)
        self.label.setAlignment(Qt.AlignCenter)

        self.verticalLayout_4.addWidget(self.label)

        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.label_2 = QLabel(TWR_Form)
        self.label_2.setObjectName(u"label_2")
        self.label_2.setMinimumSize(QSize(0, 30))
        self.label_2.setMaximumSize(QSize(16777215, 40))
        font1 = QFont()
        font1.setFamilies([u"\u5b8b\u4f53"])
        font1.setPointSize(14)
        self.label_2.setFont(font1)

        self.horizontalLayout.addWidget(self.label_2, 0, Qt.AlignRight)

        self.lineEdit_fileName = QLineEdit(TWR_Form)
        self.lineEdit_fileName.setObjectName(u"lineEdit_fileName")
        self.lineEdit_fileName.setMinimumSize(QSize(0, 20))
        self.lineEdit_fileName.setMaximumSize(QSize(16777215, 30))
        font2 = QFont()
        font2.setPointSize(10)
        self.lineEdit_fileName.setFont(font2)

        self.horizontalLayout.addWidget(self.lineEdit_fileName)

        self.toolButton_loadFile = QToolButton(TWR_Form)
        self.toolButton_loadFile.setObjectName(u"toolButton_loadFile")
        self.toolButton_loadFile.setMinimumSize(QSize(40, 30))
        self.toolButton_loadFile.setMaximumSize(QSize(16777215, 40))
        font3 = QFont()
        font3.setFamilies([u"Times New Roman"])
        font3.setPointSize(12)
        self.toolButton_loadFile.setFont(font3)

        self.horizontalLayout.addWidget(self.toolButton_loadFile)


        self.verticalLayout_4.addLayout(self.horizontalLayout)

        self.horizontalLayout_6 = QHBoxLayout()
        self.horizontalLayout_6.setObjectName(u"horizontalLayout_6")
        self.horizontalSpacer_3 = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout_6.addItem(self.horizontalSpacer_3)

        self.verticalLayout = QVBoxLayout()
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.label_3 = QLabel(TWR_Form)
        self.label_3.setObjectName(u"label_3")
        self.label_3.setMinimumSize(QSize(0, 20))
        self.label_3.setMaximumSize(QSize(16777215, 30))
        font4 = QFont()
        font4.setFamilies([u"\u5b8b\u4f53"])
        font4.setPointSize(12)
        self.label_3.setFont(font4)
        self.label_3.setAlignment(Qt.AlignCenter)

        self.verticalLayout.addWidget(self.label_3, 0, Qt.AlignHCenter|Qt.AlignTop)

        self.label_ori = QLabel(TWR_Form)
        self.label_ori.setObjectName(u"label_ori")
        sizePolicy = QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_ori.sizePolicy().hasHeightForWidth())
        self.label_ori.setSizePolicy(sizePolicy)
        self.label_ori.setMinimumSize(QSize(280, 280))
        self.label_ori.setMaximumSize(QSize(280, 280))
        self.label_ori.setFrameShape(QFrame.WinPanel)
        self.label_ori.setFrameShadow(QFrame.Sunken)
        self.label_ori.setAlignment(Qt.AlignCenter)

        self.verticalLayout.addWidget(self.label_ori, 0, Qt.AlignHCenter|Qt.AlignTop)

        self.verticalSpacer_2 = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)

        self.verticalLayout.addItem(self.verticalSpacer_2)

        self.verticalSpacer = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)

        self.verticalLayout.addItem(self.verticalSpacer)

        self.horizontalLayout_2 = QHBoxLayout()
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.pushButton_showPic = QPushButton(TWR_Form)
        self.pushButton_showPic.setObjectName(u"pushButton_showPic")
        self.pushButton_showPic.setEnabled(True)
        self.pushButton_showPic.setMinimumSize(QSize(0, 30))
        self.pushButton_showPic.setMaximumSize(QSize(120, 30))
        font5 = QFont()
        font5.setFamilies([u"\u5b8b\u4f53"])
        font5.setPointSize(11)
        self.pushButton_showPic.setFont(font5)

        self.horizontalLayout_2.addWidget(self.pushButton_showPic)

        self.pushButton_drawROI = QPushButton(TWR_Form)
        self.pushButton_drawROI.setObjectName(u"pushButton_drawROI")
        self.pushButton_drawROI.setMinimumSize(QSize(0, 30))
        self.pushButton_drawROI.setMaximumSize(QSize(120, 30))
        self.pushButton_drawROI.setFont(font5)

        self.horizontalLayout_2.addWidget(self.pushButton_drawROI)


        self.verticalLayout.addLayout(self.horizontalLayout_2)


        self.horizontalLayout_6.addLayout(self.verticalLayout)

        self.horizontalSpacer_4 = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout_6.addItem(self.horizontalSpacer_4)

        self.verticalLayout_2 = QVBoxLayout()
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.tabWidget = QTabWidget(TWR_Form)
        self.tabWidget.setObjectName(u"tabWidget")
        self.tabWidget.setMinimumSize(QSize(300, 310))
        self.tabWidget.setMaximumSize(QSize(300, 312))
        self.tabWidget.setFont(font4)
        self.tabWidget.setIconSize(QSize(16, 16))
        self.tabWidget.setElideMode(Qt.ElideNone)
        self.tab_lag = QWidget()
        self.tab_lag.setObjectName(u"tab_lag")
        self.label_lag = QLabel(self.tab_lag)
        self.label_lag.setObjectName(u"label_lag")
        self.label_lag.setGeometry(QRect(7, 2, 280, 280))
        self.label_lag.setMinimumSize(QSize(280, 280))
        self.label_lag.setMaximumSize(QSize(280, 280))
        self.label_lag.setFrameShape(QFrame.NoFrame)
        self.label_lag.setFrameShadow(QFrame.Sunken)
        self.label_lag.setAlignment(Qt.AlignCenter)
        self.tabWidget.addTab(self.tab_lag, "")
        self.tab_pha = QWidget()
        self.tab_pha.setObjectName(u"tab_pha")
        self.label_pha = QLabel(self.tab_pha)
        self.label_pha.setObjectName(u"label_pha")
        self.label_pha.setEnabled(True)
        self.label_pha.setGeometry(QRect(7, 2, 280, 280))
        self.label_pha.setMinimumSize(QSize(280, 280))
        self.label_pha.setMaximumSize(QSize(280, 280))
        self.label_pha.setFrameShape(QFrame.NoFrame)
        self.label_pha.setFrameShadow(QFrame.Sunken)
        self.label_pha.setAlignment(Qt.AlignCenter)
        self.tabWidget.addTab(self.tab_pha, "")

        self.verticalLayout_2.addWidget(self.tabWidget, 0, Qt.AlignHCenter|Qt.AlignVCenter)

        self.verticalSpacer_3 = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)

        self.verticalLayout_2.addItem(self.verticalSpacer_3)

        self.horizontalLayout_3 = QHBoxLayout()
        self.horizontalLayout_3.setObjectName(u"horizontalLayout_3")
        self.pushButton_featureExtract = QPushButton(TWR_Form)
        self.pushButton_featureExtract.setObjectName(u"pushButton_featureExtract")
        self.pushButton_featureExtract.setMinimumSize(QSize(0, 30))
        self.pushButton_featureExtract.setMaximumSize(QSize(120, 30))
        self.pushButton_featureExtract.setFont(font5)

        self.horizontalLayout_3.addWidget(self.pushButton_featureExtract)

        self.pushButton_detect = QPushButton(TWR_Form)
        self.pushButton_detect.setObjectName(u"pushButton_detect")
        self.pushButton_detect.setMinimumSize(QSize(0, 30))
        self.pushButton_detect.setMaximumSize(QSize(120, 30))
        self.pushButton_detect.setFont(font5)

        self.horizontalLayout_3.addWidget(self.pushButton_detect)


        self.verticalLayout_2.addLayout(self.horizontalLayout_3)


        self.horizontalLayout_6.addLayout(self.verticalLayout_2)

        self.verticalLayout_3 = QVBoxLayout()
        self.verticalLayout_3.setObjectName(u"verticalLayout_3")
        self.label_5 = QLabel(TWR_Form)
        self.label_5.setObjectName(u"label_5")
        self.label_5.setMinimumSize(QSize(0, 20))
        self.label_5.setMaximumSize(QSize(16777215, 30))
        self.label_5.setFont(font4)

        self.verticalLayout_3.addWidget(self.label_5, 0, Qt.AlignHCenter)

        self.label_detect = QLabel(TWR_Form)
        self.label_detect.setObjectName(u"label_detect")
        self.label_detect.setMinimumSize(QSize(280, 280))
        self.label_detect.setMaximumSize(QSize(300, 300))
        self.label_detect.setFrameShape(QFrame.StyledPanel)
        self.label_detect.setFrameShadow(QFrame.Sunken)
        self.label_detect.setAlignment(Qt.AlignCenter)

        self.verticalLayout_3.addWidget(self.label_detect, 0, Qt.AlignHCenter)

        self.verticalSpacer_4 = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)

        self.verticalLayout_3.addItem(self.verticalSpacer_4)

        self.horizontalLayout_4 = QHBoxLayout()
        self.horizontalLayout_4.setObjectName(u"horizontalLayout_4")
        self.horizontalSpacer = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout_4.addItem(self.horizontalSpacer)

        self.label_4 = QLabel(TWR_Form)
        self.label_4.setObjectName(u"label_4")
        self.label_4.setMinimumSize(QSize(0, 30))
        self.label_4.setMaximumSize(QSize(80, 30))
        self.label_4.setFont(font5)

        self.horizontalLayout_4.addWidget(self.label_4)

        self.lineEdit_numDefects = QLineEdit(TWR_Form)
        self.lineEdit_numDefects.setObjectName(u"lineEdit_numDefects")
        self.lineEdit_numDefects.setMinimumSize(QSize(180, 30))
        self.lineEdit_numDefects.setMaximumSize(QSize(200, 30))

        self.horizontalLayout_4.addWidget(self.lineEdit_numDefects)

        self.horizontalSpacer_2 = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout_4.addItem(self.horizontalSpacer_2)


        self.verticalLayout_3.addLayout(self.horizontalLayout_4)


        self.horizontalLayout_6.addLayout(self.verticalLayout_3)


        self.verticalLayout_4.addLayout(self.horizontalLayout_6)

        self.verticalSpacer_5 = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)

        self.verticalLayout_4.addItem(self.verticalSpacer_5)

        self.line = QFrame(TWR_Form)
        self.line.setObjectName(u"line")
        self.line.setMinimumSize(QSize(0, 10))
        self.line.setFrameShape(QFrame.HLine)
        self.line.setFrameShadow(QFrame.Sunken)

        self.verticalLayout_4.addWidget(self.line)

        self.plainTextEdit_logs = QPlainTextEdit(TWR_Form)
        self.plainTextEdit_logs.setObjectName(u"plainTextEdit_logs")
        sizePolicy1 = QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Preferred)
        sizePolicy1.setHorizontalStretch(0)
        sizePolicy1.setVerticalStretch(0)
        sizePolicy1.setHeightForWidth(self.plainTextEdit_logs.sizePolicy().hasHeightForWidth())
        self.plainTextEdit_logs.setSizePolicy(sizePolicy1)
        self.plainTextEdit_logs.setMinimumSize(QSize(940, 125))
        self.plainTextEdit_logs.setMaximumSize(QSize(1920, 160))
        self.plainTextEdit_logs.setFont(font2)

        self.verticalLayout_4.addWidget(self.plainTextEdit_logs)


        self.verticalLayout_5.addLayout(self.verticalLayout_4)


        self.retranslateUi(TWR_Form)

        self.tabWidget.setCurrentIndex(0)


        QMetaObject.connectSlotsByName(TWR_Form)
    # setupUi

    def retranslateUi(self, TWR_Form):
        TWR_Form.setWindowTitle(QCoreApplication.translate("TWR_Form", u"TWR_v1.0.0", None))
        self.label.setText(QCoreApplication.translate("TWR_Form", u"\u57fa\u4e8eTWR\u7684\u7ea2\u5916\u5185\u90e8\u7f3a\u9677\u667a\u80fd\u68c0\u6d4b\u7cfb\u7edf", None))
        self.label_2.setText(QCoreApplication.translate("TWR_Form", u"\u6e29\u5ea6\u6570\u636e\u6587\u4ef6\uff1a", None))
        self.lineEdit_fileName.setPlaceholderText(QCoreApplication.translate("TWR_Form", u"\u8bf7\u8f93\u5165\u6587\u4ef6\u8def\u5f84", None))
        self.toolButton_loadFile.setText(QCoreApplication.translate("TWR_Form", u"...", None))
        self.label_3.setText(QCoreApplication.translate("TWR_Form", u"\u539f\u59cb\u7ea2\u5916\u56fe\u50cf", None))
        self.label_ori.setText("")
        self.pushButton_showPic.setText(QCoreApplication.translate("TWR_Form", u"\u52a0\u8f7d\u56fe\u50cf", None))
        self.pushButton_drawROI.setText(QCoreApplication.translate("TWR_Form", u"\u7ed8\u5236ROI", None))
        self.label_lag.setText("")
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_lag), QCoreApplication.translate("TWR_Form", u"\u65f6\u6ede\u56fe", None))
        self.label_pha.setText("")
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_pha), QCoreApplication.translate("TWR_Form", u"\u76f8\u4f4d\u56fe", None))
        self.pushButton_featureExtract.setText(QCoreApplication.translate("TWR_Form", u"\u63d0\u53d6\u7279\u5f81", None))
        self.pushButton_detect.setText(QCoreApplication.translate("TWR_Form", u"\u68c0\u6d4b\u7f3a\u9677", None))
        self.label_5.setText(QCoreApplication.translate("TWR_Form", u"\u68c0\u6d4b\u7ed3\u679c", None))
        self.label_detect.setText("")
        self.label_4.setText(QCoreApplication.translate("TWR_Form", u"\u7f3a\u9677\u4e2a\u6570\uff1a", None))
        self.plainTextEdit_logs.setPlaceholderText(QCoreApplication.translate("TWR_Form", u"\u6b22\u8fce\u4f7f\u7528\u672c\u8f6f\u4ef6\uff0c\u8bf7\u5148\u5bfc\u5165\u6e29\u5ea6\u6570\u636e\u6587\u4ef6\u3002", None))
    # retranslateUi

