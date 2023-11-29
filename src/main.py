import logging
import shutil
import sys

import cv2
import numpy as np
from PIL import Image
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtPrintSupport import *
from PyQt5.QtWidgets import *
from pyqtspinner import WaitingSpinner

from efficientps_cityscapes import execute_efficientps
from generate_map import generate, OUTPUT

def cv2ImageToQImage(cv2_image):
    height, width, channel = cv2_image.shape
    bytes_per_line = 3 * width
    q_image = QImage(cv2_image.data, width, height, bytes_per_line, QImage.Format_RGB888)
    q_image = q_image.rgbSwapped()
    return q_image

class EfficientPSWorker(QObject):
    finished = pyqtSignal()
    result = pyqtSignal(QImage)
    image = None

    def run(self):
        logging.info("EfficientPSWorker em execução")
        result_image = execute_efficientps(self.image)
        logging.info(f"Imagem pos processamento com {result_image.shape[1]}x{result_image.shape[0]}")
        qtImage = QImage(result_image.data, result_image.shape[1], result_image.shape[0], QImage.Format_RGB888).rgbSwapped()
        self.result.emit(qtImage)
        self.finished.emit()
        logging.info("EfficientPSWorker finalizou a execução")

class MapWorker(QObject):
    finished = pyqtSignal()
    result = pyqtSignal(QImage)
    image = None
    points = 300

    def run(self):
        logging.info("MapWorker em execução")
        result_image = generate(self.image, points=self.points, output=OUTPUT.MAP_BIOME)
        logging.info(f"Imagem pos processamento com {result_image.shape[1]}x{result_image.shape[0]}")
        qtImage = QImage(result_image.data, result_image.shape[1], result_image.shape[0], QImage.Format_RGB888).rgbSwapped()
        self.result.emit(qtImage)
        self.finished.emit()
        logging.info("MapWorker finalizou a execução")

class QImageViewer(QMainWindow):
    def __init__(self):
        super().__init__()

        self.spinner = None
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

        self.spinner = WaitingSpinner(
            self,
            center_on_parent=True,
            disable_parent_when_spinning=True,
            roundness=100.0,
            fade=80.0,
            radius=18,
            lines=20,
            line_length=10,
            line_width=20,
            speed=1.5707963267948966
        )


    def open(self):
        options = QFileDialog.Options()
        fileName, _ = QFileDialog.getOpenFileName(self,
            'QFileDialog.getOpenFileName()',
            '',
            'Images (*.png *.jpeg *.jpg *.bmp *.gif)',
            options=options
        )

        if fileName:
            SCALE = 0.6

            image = cv2.imread(fileName)
            if image is None:
                QMessageBox.information(self, "Erro", "Não foi possivel carregar a imagem %s." % fileName)
                return

            new_width = int(1000)
            new_height = int((image.shape[0] * 1000) / image.shape[1])
            image = cv2.resize(image, (new_width, new_height))
            self.img = cv2ImageToQImage(image)

            self.imageLabel.setPixmap(QPixmap.fromImage(self.img))
            self.toggleMousePressEvent()

            self.scaleFactor = 1.0

            self.scrollArea.setVisible(True)
            self.printAct.setEnabled(True)
            self.fitToWindowAct.setEnabled(True)
            self.updateActions()

            if not self.fitToWindowAct.isChecked():
                self.imageLabel.adjustSize()

            image = self.qimage_to_cv2(self.img)

            self.runEfficientPSWorker(image)

    def qimage_to_cv2(self, qimage):
        buffer = np.array(qimage.bits().asarray(
            qimage.width() * qimage.height() * qimage.depth() // 8))
        buffer = buffer.reshape(
            (qimage.height(), qimage.width(), qimage.depth() // 8))
        cv2_image = cv2.cvtColor(buffer, cv2.COLOR_BGR2RGB)
        return cv2_image

    def createMask(self, event):

        x = event.pos().x()
        y = event.pos().y()
        c = self.img.pixel(x, y)

        width = int(self.img.width())
        height = int(self.img.height())

        image = self.qimage_to_cv2(self.img)

        seed = (x, y)
        mask = np.zeros((height+2, width+2), np.uint8)

        floodflags = 4
        floodflags |= cv2.FLOODFILL_MASK_ONLY
        floodflags |= (255 << 8)

        _, _, mask, _ = cv2.floodFill(
            image, mask, seed, (255, 0, 0), (10,)*3, (10,)*3, floodflags)
        _, binary_mask = cv2.threshold(mask, 127, 255, cv2.THRESH_BINARY)

        cv2.imwrite("output.png", binary_mask)

        img_in = cv2.imread('output.png', 0)
        height, width = img_in.shape
        x, y, w, h = cv2.boundingRect(img_in)
        croped_image = img_in[y:y+h, x:x+w]

        diff = abs(w-h) // 2
        if w > h:
            im = cv2.copyMakeBorder(croped_image, diff, diff, 0, 0, cv2.BORDER_CONSTANT,value=(0,0,0))
        else:
            im = cv2.copyMakeBorder(croped_image, 0, 0, diff, diff, cv2.BORDER_CONSTANT,value=(0,0,0))

        im = cv2.resize(im, (200, 200))
        im = cv2.copyMakeBorder(im, 50, 50, 50, 50, cv2.BORDER_CONSTANT, value=(0,0,0))
        cv2.imwrite('output_croped.png', im)

        self.runMapWorker(im)

    def print_(self):
        dialog = QPrintDialog(self.printer, self)
        if dialog.exec_():
            painter = QPainter(self.printer)
            rect = painter.viewport()
            size = self.imageLabel.pixmap().size()
            size.scale(rect.size(), Qt.KeepAspectRatio)
            painter.setViewport(rect.x(), rect.y(),
                                size.width(), size.height())
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
        self.openAct = QAction(
            "&Open...", self, shortcut="Ctrl+O", triggered=self.open)
        self.printAct = QAction(
            "&Print...", self, shortcut="Ctrl+P", enabled=False, triggered=self.print_)
        self.exitAct = QAction(
            "E&xit", self, shortcut="Ctrl+Q", triggered=self.close)
        self.zoomInAct = QAction(
            "Zoom &In (25%)", self, shortcut="Ctrl++", enabled=False, triggered=self.zoomIn)
        self.zoomOutAct = QAction(
            "Zoom &Out (25%)", self, shortcut="Ctrl+-", enabled=False, triggered=self.zoomOut)
        self.normalSizeAct = QAction(
            "&Normal Size", self, shortcut="Ctrl+S", enabled=False, triggered=self.normalSize)
        self.fitToWindowAct = QAction("&Fit to Window", self, enabled=False, checkable=True, shortcut="Ctrl+F",
                                      triggered=self.fitToWindow)
        self.aboutAct = QAction("&About", self, triggered=self.about)
        self.aboutQtAct = QAction("About &Qt", self, triggered=qApp.aboutQt)

    def start_loading(self):
        self.spinner.start()

    def stop_loading(self):
        self.spinner.stop()

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
        self.imageLabel.resize(
            self.scaleFactor * self.imageLabel.pixmap().size())

        self.adjustScrollBar(self.scrollArea.horizontalScrollBar(), factor)
        self.adjustScrollBar(self.scrollArea.verticalScrollBar(), factor)

        self.zoomInAct.setEnabled(self.scaleFactor < 3.0)
        self.zoomOutAct.setEnabled(self.scaleFactor > 0.333)

    def adjustScrollBar(self, scrollBar, factor):
        scrollBar.setValue(int(factor * scrollBar.value()
                               + ((factor - 1) * scrollBar.pageStep() / 2)))

    def update_screen_image(self, image: QImage):
        self.img = image
        self.imageLabel.setPixmap(QPixmap.fromImage(self.img))
        self.imageLabel.adjustSize()

    def runEfficientPSWorker(self, image):
        logging.info("Criando EfficientPSWorker")

        self.start_loading()
        self.thread = QThread()

        self.worker = EfficientPSWorker()
        self.worker.image = image

        self.worker.moveToThread(self.thread)

        self.thread.started.connect(self.worker.run)
        self.worker.finished.connect(self.thread.quit)
        self.worker.finished.connect(self.worker.deleteLater)
        self.thread.finished.connect(self.thread.deleteLater)
        self.worker.result.connect(self.update_screen_image)

        logging.info("Executando EfficientPSWorker")
        self.thread.start()

        self.thread.finished.connect(self.stop_loading)

    def toggleMousePressEvent(self):
        if self.imageLabel.mousePressEvent != self.createMask:
            self.imageLabel.mousePressEvent = self.createMask
        else:
            self.imageLabel.mousePressEvent = None

    def runMapWorker(self, image):
        logging.info("Criando MapWorker")
        self.toggleMousePressEvent()
        self.start_loading()
        self.thread = QThread()

        self.worker = MapWorker()
        self.worker.image = image

        self.worker.moveToThread(self.thread)

        self.thread.started.connect(self.worker.run)
        self.worker.finished.connect(self.thread.quit)
        self.worker.finished.connect(self.worker.deleteLater)
        self.thread.finished.connect(self.thread.deleteLater)
        self.worker.result.connect(self.update_screen_image)

        logging.info("Executando MapWorker")
        self.thread.start()

        self.thread.finished.connect(self.stop_loading)

if __name__ == '__main__':
    logging.basicConfig(format='[%(levelname)s] %(message)s', level=logging.DEBUG)
    logging.getLogger().setLevel(logging.INFO)

    app = QApplication(sys.argv)
    imageViewer = QImageViewer()
    imageViewer.show()

    logging.info("Aplicão iniciada")

    sys.exit(app.exec_())
