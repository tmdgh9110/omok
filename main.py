import sys
import numpy as np
import cv2
import time
import os

from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QVBoxLayout
from PyQt5.QtGui import QPixmap, QImage
from PyQt5.QtCore import Qt


class Omok(QWidget):

    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.board_size = 21
        self.board = np.zeros([self.board_size, self.board_size])


if __name__ == '__main__':
    app = QApplication(sys.argv)
    a = Omok()
    sys.exit(app.exec_())
