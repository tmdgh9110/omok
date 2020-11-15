import sys
import numpy as np
import cv2
import time
import os

from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QVBoxLayout
from PyQt5.QtGui import QPixmap, QImage
from PyQt5.QtCore import Qt

global x, y
x, y = 500, 100


class Omok(QWidget):

    class ImgLabel(QLabel):

        def __init__(self, vBox):
            super().__init__()
            self.board_size = 21
            self.board = np.zeros([self.board_size, self.board_size])
            self.viewBox = vBox
            self.pos = list()
            self.initUI()

        def initUI(self):
            self.background_img = cv2.cvtColor(cv2.imread(
                'resource/board.png'), cv2.COLOR_BGR2RGB)

            stone_0 = cv2.cvtColor(cv2.imread(
                'resource/stone_0.png'), cv2.COLOR_BGR2RGB)

            stone_0_s = cv2.cvtColor(cv2.imread(
                'resource/stone_0_s.png'), cv2.COLOR_BGR2RGB)

            stone_1 = cv2.cvtColor(cv2.imread(
                'resource/stone_1.png'), cv2.COLOR_BGR2RGB)

            stone_1_s = cv2.cvtColor(cv2.imread(
                'resource/stone_1_s.png'), cv2.COLOR_BGR2RGB)

            self.stone_list = dict()
            self.stone_list[-1] = [stone_0, stone_0_s]
            self.stone_list[1] = [stone_1, stone_1_s]
            self.h, self.w, self.c = self.background_img.shape
            qImg_board = QImage(self.background_img, self.w, self.h,
                                3 * self.w, QImage.Format_RGB888)
            self.turn = -1
            self.setPixmap(QPixmap(qImg_board))
            self.background_img_histroy = self.background_img.copy()
            self.viewBox.addWidget(self)

        def mousePressEvent(self, event):
            self.pos = self.putStone(event.x(), event.y(), self.pos)

        def checkBoard(self, y, x):
            count = 1
            preset = list()
            preset.append([1, 1])
            preset.append([-1, -1])
            preset.append([-1, 1])
            preset.append([1, -1])
            preset.append([1, 0])
            preset.append([-1, 0])
            preset.append([0, 1])
            preset.append([0, -1])
            temp = self.board[y, x]
            print(temp)
            i = 0
            x_temp, y_temp = x, y
            while (i <= 7):
                p_x, p_y = preset[i][0], preset[i][1]
                x_temp, y_temp = x_temp + p_x, y_temp + p_y
                if temp == self.board[y_temp, x_temp]:
                    count += 1
                else:
                    x_temp, y_temp = x, y
                    i += 1
                    if i % 2 == 0:
                        count = 1
                if count == 5:
                    print("끝")
                    break

        def putStone(self, pos_x, pos_y, pos):
            set_0 = 39
            start, end, center = 0, 783, 40
            offset = 15
            ball_size = 35
            step = 17
            real_x, real_y = pos_x - set_0, pos_y - set_0
            if real_x >= end + offset or real_x <= start - offset or real_y >= end + offset or real_y <= start - offset:
                print("fatal")
                print(real_x, real_y)
            check_x, check_y = real_x // set_0, real_y // set_0
            r_list = [(check_x * set_0), (check_y * set_0)]
            if real_x <= (check_x * set_0) + offset and real_x >= (check_x * set_0) - offset and real_y <= (check_y * set_0) + offset and real_y >= (check_y * set_0) - offset:
                if r_list == pos:
                    self.background_img[(check_y * set_0) + set_0 - step + 1: (check_y * set_0) + set_0 + step + 2,
                                        (check_x * set_0) + set_0 - step + 1: (check_x * set_0) + set_0 + step+2] = self.stone_list[self.turn][0]
                    qImg_board = QImage(self.background_img, self.w, self.h,
                                        3 * self.w, QImage.Format_RGB888)
                    self.setPixmap(QPixmap(qImg_board))
                    self.background_img_histroy = self.background_img.copy()
                    self.board[check_y, check_x] = self.turn
                    self.checkBoard(check_y, check_x)
                    self.turn *= - 1
                    self.pos = list()
                else:
                    self.background_img = self.background_img_histroy.copy()
                    self.background_img[(check_y * set_0) + set_0 - step + 1: (check_y * set_0) + set_0 + step+2,
                                        (check_x * set_0) + set_0 - step + 1: (check_x * set_0) + set_0 + step+2] = self.stone_list[self.turn][1]
                    qImg_board = QImage(self.background_img, self.w, self.h,
                                        3 * self.w, QImage.Format_RGB888)
                    self.setPixmap(QPixmap(qImg_board))

            return r_list

    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.save_path = 'result'
        self.name = str(time.gmtime(time.time()))
        self.save_txt = os.path.join(self.save_path, self.name + '.txt')
        self.save_bmp = os.path.join(self.save_path, self.name + '.bmp')

        self.viewBox = QVBoxLayout()
        self.board_label = self.ImgLabel(self.viewBox)

        self.setLayout(self.viewBox)
        self.setWindowTitle("Omok")
        self.show()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    a = Omok()
    sys.exit(app.exec_())
