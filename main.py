import sys
import random
from PyQt6.QtGui import QPainter, QColor
from PyQt6.QtWidgets import QWidget, QApplication, QPushButton, QInputDialog


class RandomFlag(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setGeometry(300, 300, 700, 700)
        self.setWindowTitle('Рисование')
        self.button = QPushButton('КНОПКА', self)
        self.button.move(70, 20)
        self.do_paint = False
        self.button.clicked.connect(self.run)
        self.button.clicked.connect(self.paint)

    def paintEvent(self, event):
        if self.do_paint:
            qp = QPainter()
            qp.begin(self)
            self.draw_elipse(qp)
            qp.end()

    def paint(self):
        self.do_paint = True
        self.repaint()

    def run(self):
        self.paint()

    def draw_elipse(self, qp):
        r = random.randint(10, 400)
        qp.setBrush(QColor(255, 255, 0))
        qp.drawEllipse(20, 20, r, r)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = RandomFlag()
    ex.show()
    sys.exit(app.exec())
