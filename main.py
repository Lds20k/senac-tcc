#!/usr/bin/python3
# -*- coding: utf-8 -*-

from PIL import Image
import cv2
import numpy as np
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QImage, QPixmap, QPalette, QPainter, QColor
from PyQt5.QtPrintSupport import QPrintDialog, QPrinter
from PyQt5.QtWidgets import QLabel, QSizePolicy, QScrollArea, QMessageBox, QMainWindow, QMenu, QAction, \
    qApp, QFileDialog

from PyQt5.QtWidgets import (QWidget, QApplication, QVBoxLayout, QPushButton, 
                             QDesktopWidget, QLabel, QGridLayout, QMainWindow)
from PyQt5.QtCore import Qt, QTimer, QSize, QRect
from PyQt5.QtGui import QIcon

class Message(QWidget):
    def __init__(self, title, message, parent=None):
        QWidget.__init__(self, parent)
        self.setLayout(QGridLayout())
        self.titleLabel = QLabel(title, self)
        self.titleLabel.setStyleSheet("font-size: 18px; font-weight: bold; padding: 0;")
        self.messageLabel = QLabel(message, self)
        self.messageLabel.setStyleSheet("font-size: 12px; font-weight: normal; padding: 0;")
        self.buttonClose = QPushButton(self)
        self.buttonClose.setIcon(QIcon.fromTheme("window-close"))
        self.buttonClose.setFlat(True)
        self.buttonClose.setFixedSize(32, 32)
        self.buttonClose.setIconSize(QSize(16, 16))
        self.layout().addWidget(self.titleLabel)
        self.layout().addWidget(self.messageLabel, 2, 0)
        self.layout().addWidget(self.buttonClose, 0, 1)

class Notification(QWidget):
    def __init__(self, parent = None):        
        super(QWidget, self).__init__(parent = None)
        self.setWindowFlags(Qt.FramelessWindowHint | Qt.WindowStaysOnTopHint)      
        self.setStyleSheet("background: #00FF00; padding: 0;")
        self.mainLayout = QVBoxLayout(self)
        

    def setNotify(self, title, message, timeout):
        self.m = Message(title, message)
        self.mainLayout.addWidget(self.m)
        self.m.buttonClose.clicked.connect(self.onClicked)
        self.show()
        QTimer.singleShot(timeout, 0, self.closeMe)
        
    def closeMe(self):
        self.close()
        self.m.close()
    
    def onClicked(self):
        self.close()
            
class Window(QMainWindow):
    def __init__(self, parent=None):
        QWidget.__init__(self, parent)
        btn = QPushButton(QIcon.fromTheme("info"), "show Notify")
        btn.setFixedWidth(110)
        btn.setFixedHeight(30)
        self.setCentralWidget(btn)
        btn.clicked.connect(self.showNotification)
        
    def showNotification(self):
        self.notification = Notification()
        self.notification.setNotify("Message Title", "Message line 1\nMessage line 2\nMessage line 3", 3000)
        




class QImageViewer(QMainWindow):
    def __init__(self):
        super().__init__()

        self.printer = QPrinter()
        self.scaleFactor = 0.0

        self.imageLabel = QLabel()
        self.imageLabel.setBackgroundRole(QPalette.Base)
        self.imageLabel.setSizePolicy(QSizePolicy.Ignored, QSizePolicy.Ignored)
        self.imageLabel.setScaledContents(True)

        self.scrollArea = QScrollArea()
        self.scrollArea.setBackgroundRole(QPalette.Dark)
        self.scrollArea.setWidget(self.imageLabel)
        self.scrollArea.setVisible(False)

        self.setCentralWidget(self.scrollArea)

        self.createActions()
        self.createMenus()

        self.setWindowTitle("Image Viewer")
        self.showMaximized()

    def open(self):
        options = QFileDialog.Options()
        # fileName = QFileDialog.getOpenFileName(self, "Open File", QDir.currentPath())
        fileName, _ = QFileDialog.getOpenFileName(self, 'QFileDialog.getOpenFileName()', '',
                                                  'Images (*.png *.jpeg *.jpg *.bmp *.gif)', options=options)
        if fileName:
            self.img = QImage(fileName)
            if self.img.isNull():
                QMessageBox.information(self, "Image Viewer", "Cannot load %s." % fileName)
                return

            self.imageLabel.setPixmap(QPixmap.fromImage(self.img))
            self.imageLabel.mousePressEvent = self.createMask

            self.scaleFactor = 1.0

            self.scrollArea.setVisible(True)
            self.printAct.setEnabled(True)
            self.fitToWindowAct.setEnabled(True)
            self.updateActions()

            if not self.fitToWindowAct.isChecked():
                self.imageLabel.adjustSize()

        self.showNotification("AVISO", "Selecione uma parte da imagem para gerar um mapa", 3000)

    def createMask(self, event):
        x = event.pos().x()
        y = event.pos().y()
        c = self.img.pixel(x,y)
        rgb_color = QColor(c).getRgb()[:3]

        width = self.img.width()
        height = self.img.height()

        image = Image.new('RGB', (width, height))

        for x_in in range(width):
            for y_in in range(height):
                pxl = self.img.pixel(x_in, y_in)
                pxl_color = QColor(pxl).getRgb()[:3]
                
                if rgb_color == pxl_color:
                    image.putpixel((x_in, y_in), (255, 255, 255))
                else:
                    image.putpixel((x_in, y_in), (0, 0, 0))

        image.save('output.png')
        
        # Load image as grayscale and obtain bounding box coordinates
        img_in = cv2.imread('output.png', 0)
        height, width = img_in.shape
        x,y,w,h = cv2.boundingRect(img_in)

        # Create new blank image and shift ROI to new coordinates
        mask = np.zeros(img_in.shape, dtype=np.uint8)
        ROI = img_in[y:y+h, x:x+w]
        x = width//2 - ROI.shape[0]//2 
        y = height//2 - ROI.shape[1]//2
        if x > 0 and y > 0: 
            mask[y:y+h, x:x+w] = ROI
            # Save the image to a file
            cv2.imwrite('output_centralized.png', mask)
        else:
            image.save('output_centralized.png')

    def print_(self):
        dialog = QPrintDialog(self.printer, self)
        if dialog.exec_():
            painter = QPainter(self.printer)
            rect = painter.viewport()
            size = self.imageLabel.pixmap().size()
            size.scale(rect.size(), Qt.KeepAspectRatio)
            painter.setViewport(rect.x(), rect.y(), size.width(), size.height())
            painter.setWindow(self.imageLabel.pixmap().rect())
            painter.drawPixmap(0, 0, self.imageLabel.pixmap())

    def zoomIn(self):
        self.scaleImage(1.25)

    def zoomOut(self):
        self.scaleImage(0.8)

    def normalSize(self):
        self.imageLabel.adjustSize()
        self.scaleFactor = 1.0

    def fitToWindow(self):
        fitToWindow = self.fitToWindowAct.isChecked()
        self.scrollArea.setWidgetResizable(fitToWindow)
        if not fitToWindow:
            self.normalSize()

        self.updateActions()
    
    def showNotification(self, title, body, time_interval):
        print("notificação")
        self.notification = Notification()
        self.notification.setNotify(title, body, time_interval)
        r = QRect(self.x() + round(self.width() / 2) - round(self.notification.width() / 2), 
                                        self.y() + 26, self.notification.m.messageLabel.width() + 30, self.notification.m.messageLabel.height())
        self.notification.setGeometry(r)

    def about(self):
        QMessageBox.about(self, "About Image Viewer",
                          "<p>The <b>Image Viewer</b> example shows how to combine "
                          "QLabel and QScrollArea to display an image. QLabel is "
                          "typically used for displaying text, but it can also display "
                          "an image. QScrollArea provides a scrolling view around "
                          "another widget. If the child widget exceeds the size of the "
                          "frame, QScrollArea automatically provides scroll bars.</p>"
                          "<p>The example demonstrates how QLabel's ability to scale "
                          "its contents (QLabel.scaledContents), and QScrollArea's "
                          "ability to automatically resize its contents "
                          "(QScrollArea.widgetResizable), can be used to implement "
                          "zooming and scaling features.</p>"
                          "<p>In addition the example shows how to use QPainter to "
                          "print an image.</p>")

    def createActions(self):
        self.openAct = QAction("&Open...", self, shortcut="Ctrl+O", triggered=self.open)
        self.printAct = QAction("&Print...", self, shortcut="Ctrl+P", enabled=False, triggered=self.print_)
        self.exitAct = QAction("E&xit", self, shortcut="Ctrl+Q", triggered=self.close)
        self.zoomInAct = QAction("Zoom &In (25%)", self, shortcut="Ctrl++", enabled=False, triggered=self.zoomIn)
        self.zoomOutAct = QAction("Zoom &Out (25%)", self, shortcut="Ctrl+-", enabled=False, triggered=self.zoomOut)
        self.normalSizeAct = QAction("&Normal Size", self, shortcut="Ctrl+S", enabled=False, triggered=self.normalSize)
        self.fitToWindowAct = QAction("&Fit to Window", self, enabled=False, checkable=True, shortcut="Ctrl+F",
                                      triggered=self.fitToWindow)
        self.aboutAct = QAction("&About", self, triggered=self.about)
        self.aboutQtAct = QAction("About &Qt", self, triggered=qApp.aboutQt)
       



    def createMenus(self):
        self.fileMenu = QMenu("&File", self)
        self.fileMenu.addAction(self.openAct)
        self.fileMenu.addAction(self.printAct)
        self.fileMenu.addSeparator()
        self.fileMenu.addAction(self.exitAct)

        self.helpMenu = QMenu("&Help", self)
        self.helpMenu.addAction(self.aboutAct)
        self.helpMenu.addAction(self.aboutQtAct)

        self.menuBar().addMenu(self.fileMenu)
        self.menuBar().addMenu(self.helpMenu)

    def updateActions(self):
        self.zoomInAct.setEnabled(not self.fitToWindowAct.isChecked())
        self.zoomOutAct.setEnabled(not self.fitToWindowAct.isChecked())
        self.normalSizeAct.setEnabled(not self.fitToWindowAct.isChecked())

    def scaleImage(self, factor):
        self.scaleFactor *= factor
        self.imageLabel.resize(self.scaleFactor * self.imageLabel.pixmap().size())

        self.adjustScrollBar(self.scrollArea.horizontalScrollBar(), factor)
        self.adjustScrollBar(self.scrollArea.verticalScrollBar(), factor)

        self.zoomInAct.setEnabled(self.scaleFactor < 3.0)
        self.zoomOutAct.setEnabled(self.scaleFactor > 0.333)

    def adjustScrollBar(self, scrollBar, factor):
        scrollBar.setValue(int(factor * scrollBar.value()
                               + ((factor - 1) * scrollBar.pageStep() / 2)))


if __name__ == '__main__':
    import sys
    from PyQt5.QtWidgets import QApplication

    app = QApplication(sys.argv)
    imageViewer = QImageViewer()
    imageViewer.show()
    sys.exit(app.exec_())
    # TODO QScrollArea support mouse
    # base on https://github.com/baoboa/pyqt5/blob/master/examples/widgets/imageviewer.py
    #
    # if you need Two Image Synchronous Scrolling in the window by PyQt5 and Python 3
    # please visit https://gist.github.com/acbetter/e7d0c600fdc0865f4b0ee05a17b858f2



    # quando abrir a imagem a gente aparece o load diferenciado e coisar com a IA
    # Depois que terminar vai abrir a notificação
    # Selecione uma parte da imagem para gerar um mapa
    # 