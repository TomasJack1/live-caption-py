# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'subtitle.ui'
##
## Created by: Qt User Interface Compiler version 6.9.0
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
    QSizePolicy, QVBoxLayout, QWidget)

class Ui_Form(object):
    def setupUi(self, Form):
        if not Form.objectName():
            Form.setObjectName(u"Form")
        Form.resize(1202, 165)
        Form.setMinimumSize(QSize(1200, 65))
        Form.setMaximumSize(QSize(16777215, 16777215))
        font = QFont()
        font.setPointSize(24)
        Form.setFont(font)
        Form.setTabletTracking(False)
        Form.setContextMenuPolicy(Qt.ContextMenuPolicy.NoContextMenu)
        icon = QIcon(QIcon.fromTheme(u"applications-system"))
        Form.setWindowIcon(icon)
        Form.setAutoFillBackground(False)
        Form.setStyleSheet(u"background: transparent;")
        self.horizontalLayout = QHBoxLayout(Form)
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.horizontalLayout.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout = QVBoxLayout()
        self.verticalLayout.setSpacing(0)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.drag_widget = QFrame(Form)
        self.drag_widget.setObjectName(u"drag_widget")
        sizePolicy = QSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.drag_widget.sizePolicy().hasHeightForWidth())
        self.drag_widget.setSizePolicy(sizePolicy)
        self.drag_widget.setMinimumSize(QSize(1200, 0))
        self.drag_widget.setMaximumSize(QSize(16777215, 20))
        self.drag_widget.setCursor(QCursor(Qt.CursorShape.OpenHandCursor))
        self.drag_widget.setMouseTracking(False)
        self.drag_widget.setToolTipDuration(6)
        self.drag_widget.setFrameShadow(QFrame.Shadow.Raised)

        self.verticalLayout.addWidget(self.drag_widget)

        self.frame = QFrame(Form)
        self.frame.setObjectName(u"frame")
        self.frame.setFrameShape(QFrame.Shape.NoFrame)
        self.frame.setFrameShadow(QFrame.Shadow.Raised)
        self.plainTextEdit = QLabel(self.frame)
        self.plainTextEdit.setObjectName(u"plainTextEdit")
        self.plainTextEdit.setGeometry(QRect(0, 10, 1191, 131))
        self.plainTextEdit.setMinimumSize(QSize(0, 0))
        font1 = QFont()
        font1.setPointSize(36)
        self.plainTextEdit.setFont(font1)
        self.plainTextEdit.setTextFormat(Qt.TextFormat.PlainText)
        self.plainTextEdit.setAlignment(Qt.AlignmentFlag.AlignLeading|Qt.AlignmentFlag.AlignLeft|Qt.AlignmentFlag.AlignTop)
        self.plainTextEdit.setWordWrap(True)
        self.plainTextEdit.setTextInteractionFlags(Qt.TextInteractionFlag.NoTextInteraction)

        self.verticalLayout.addWidget(self.frame)


        self.horizontalLayout.addLayout(self.verticalLayout)


        self.retranslateUi(Form)

        QMetaObject.connectSlotsByName(Form)
    # setupUi

    def retranslateUi(self, Form):
        Form.setWindowTitle(QCoreApplication.translate("Form", u"\u5b9e\u65f6\u5b57\u5e55", None))
        self.plainTextEdit.setText(QCoreApplication.translate("Form", u"TextLabel", None))
    # retranslateUi

