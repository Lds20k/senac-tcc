import logging
import sys

import cv2
import numpy as np
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtPrintSupport import *
from PyQt5.QtWidgets import *
from pyqtspinner import WaitingSpinner

from efficientps_cityscapes import execute_efficientps
from generate_map import generate, OUTPUT

def cv2image_to_qimage(cv2_image):
    height, width, channel = cv2_image.shape
    bytes_per_line = 3 * width
    q_image = QImage(cv2_image.data, width, height, bytes_per_line, QImage.Format_RGB888)
    q_image = q_image.rgbSwapped()
    return q_image

class EfficientPSWorker(QObject):
    finished = pyqtSignal()
    result = pyqtSignal(np.ndarray)
    image = None

    def run(self):
        logging.info("EfficientPSWorker em execução")
        result_image = execute_efficientps(self.image)
        logging.info(f"Imagem pos processamento com {result_image.shape[1]}x{result_image.shape[0]}")
        self.result.emit(result_image)
        self.finished.emit()
        logging.info("EfficientPSWorker finalizou a execução")

class MapWorker(QObject):
    finished = pyqtSignal()
    result = pyqtSignal(np.ndarray)
    image = None
    points = 300

    def run(self):
        logging.info("MapWorker em execução")
        result_image = generate(self.image, points=self.points, output=OUTPUT.MAP_BIOME)
        logging.info(f"Imagem pos processamento com {result_image.shape[1]}x{result_image.shape[0]}")
        self.result.emit(result_image)
        self.finished.emit()
        logging.info("MapWorker finalizou a execução")

class QImageViewer(QMainWindow):
    def __init__(self):
        super().__init__()

        self.spinner = None
        self.printer = QPrinter()

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
            image = cv2.imread(fileName)
            if image is None:
                QMessageBox.information(self, "Erro", "Não foi possivel carregar a imagem %s." % fileName)
                return

            geometria = self.geometry()
            new_width = geometria.width() - 16
            new_height = int((image.shape[0] * new_width) / image.shape[1])
            image = cv2.resize(image, (new_width, new_height))
            self.update_screen_image(image)

            # Mudar
            self.toggleMousePressEvent()

            self.scrollArea.setVisible(True)
            self.methodMenu.setEnabled(True)

    def qimage_to_cv2(self, qimage):
        buffer = np.array(qimage.bits().asarray(
            qimage.width() * qimage.height() * qimage.depth() // 8))
        buffer = buffer.reshape(
            (qimage.height(), qimage.width(), qimage.depth() // 8))
        cv2_image = cv2.cvtColor(buffer, cv2.COLOR_BGR2RGB)
        return cv2_image

    def create_mask(self, event):
        x = event.pos().x()
        y = event.pos().y()
        # c = self.img.pixel(x, y)

        width = int(self.image.shape[1])
        height = int(self.image.shape[0])

        seed = (x, y)
        mask = np.zeros((height+2, width+2), np.uint8)

        floodflags = 4
        floodflags |= cv2.FLOODFILL_MASK_ONLY
        floodflags |= (255 << 8)

        _, _, mask, _ = cv2.floodFill(self.image, mask, seed, (255, 0, 0), (10,)*3, (10,)*3, floodflags)
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
        self.exitAct = QAction(
            "E&xit", self, shortcut="Ctrl+Q", triggered=self.close)
        self.aboutAct = QAction("&About", self, triggered=self.about)
        self.aboutQtAct = QAction("About &Qt", self, triggered=qApp.aboutQt)

        self.efficientPSFloodFill = QAction("Floodfill", self, triggered=self.runEfficientPSWorker)
        self.efficientPSColor = QAction("Color", self, triggered=self.create_mask)

        self.floodFill = QAction("Floodfill", self, triggered=self.create_mask)
        self.color = QAction("Color", self, triggered=self.create_mask)


    def start_loading(self):
        self.spinner.start()

    def stop_loading(self):
        self.spinner.stop()

    def createMenus(self):
        self.fileMenu = QMenu("&File", self)
        self.fileMenu.addAction(self.openAct)
        self.fileMenu.addSeparator()
        self.fileMenu.addAction(self.exitAct)

        self.helpMenu = QMenu("&Help", self)
        self.helpMenu.addAction(self.aboutAct)
        self.helpMenu.addAction(self.aboutQtAct)

        self.methodMenu = QMenu("&Method", self)
        self.methodMenu.addSection("EfficientPS")
        self.methodMenu.addAction(self.efficientPSFloodFill)
        self.methodMenu.addAction(self.efficientPSColor)
        self.methodMenu.addSection("Selection")
        self.methodMenu.addAction(self.floodFill)
        self.methodMenu.addAction(self.color)
        self.methodMenu.setEnabled(False)

        self.menuBar().addMenu(self.fileMenu)
        self.menuBar().addMenu(self.methodMenu)
        self.menuBar().addMenu(self.helpMenu)

    def adjustScrollBar(self, scrollBar, factor):
        scrollBar.setValue(int(factor * scrollBar.value()
                               + ((factor - 1) * scrollBar.pageStep() / 2)))

    def update_screen_image(self, image):
        self.image = image

        qImg = cv2image_to_qimage(image)
        self.imageLabel.setPixmap(QPixmap.fromImage(qImg))
        self.imageLabel.adjustSize()

    def runEfficientPSWorker(self):
        logging.info("Criando EfficientPSWorker")

        self.start_loading()
        self.thread = QThread()

        self.worker = EfficientPSWorker()
        self.worker.image = self.image

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
        if self.imageLabel.mousePressEvent != self.create_mask:
            self.imageLabel.mousePressEvent = self.create_mask
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
