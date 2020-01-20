from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
import sys

class Menu(QDialog):

    def __init__(self, card):
        super(Menu, self).__init__()

        self.return_value = None
        self.setAttribute(Qt.WA_DeleteOnClose)


        layout = QVBoxLayout()

        self.b1 = QPushButton('Move left')
        self.b2 = QPushButton('Move right')
        
        self.b1.clicked.connect(self.accept)
        self.b2.clicked.connect(self.accept)
        
        self.b1.clicked.connect(lambda checked, val=self.b1.text(): self.set_return(val))
        self.b2.clicked.connect(lambda checked, val=self.b2.text(): self.set_return(val))

        layout.addWidget(self.b1)
        layout.addWidget(self.b2)

        self.imageLabel = QLabel()
        self.imageLabel.setPixmap(card.face)
        layout.addWidget(self.imageLabel)

        self.setLayout(layout)

    def set_return(self, val):
        self.return_value = val

class Card(QGraphicsPixmapItem):

    def __init__(self, n):
        super(Card, self).__init__()
        self.value = n
        self.stack = None
        self.tapped = False
        self.clickable = False

        #self.signals = Signals()
        #self.signals.clicked.connect(lambda: self.render())

        self.setShapeMode(QGraphicsPixmapItem.BoundingRectShape)
        self.setFlag(QGraphicsItem.ItemIsMovable)
        self.setFlag(QGraphicsItem.ItemSendsGeometryChanges)
        self.setTransformOriginPoint(50, 50)

        self.face = QPixmap('assets/{}.jpg'.format(n)).scaled(100, 100, Qt.KeepAspectRatio)
        self.setPixmap(self.face)
        self.update()

    def update(self):
        self.setRotation(90*self.tapped)

    def paint(self, painter, option, widget=None):
        super().paint(painter, option, widget)
        if self.clickable:
            painter.save()
            pen = QPen(QColor("red"))
            pen.setWidth(4)
            painter.setPen(pen)
            painter.drawRect(self.boundingRect())
            painter.restore()


    def mouseDoubleClickEvent(self, e):

        if self.clickable:

            if self.stack.label == '1':
                self.tapped = not self.tapped
                self.update()

            else:
                menu = Menu(self)
                menu.exec()
                print(menu.return_value)
                if menu.return_value == 'Move left':
                    self.stack.remove(self)
                    
                    pass
                #e.accept()
            #self.update()
    

        super().mouseDoubleClickEvent(e)
        e.ignore()

    

class Deck(QGraphicsRectItem):
    
    def __init__(self, label):
        super(Deck, self).__init__()
        self.label = label
        self.setRect(QRectF(QRect(0, 0, 100, 100)))
        self.setZValue(-1)
        self.cards = []

    def add(self, card):
        self.cards.append(card)
        card.stack = self
        self.update()
    
    def remove(self, card):
        self.cards.remove(card)
        self.update()
    
    def update(self):
        for i,card in enumerate(self.cards):
            card.setPos(self.pos() + QPointF(0, i*125))


class MainWindow(QMainWindow):

    def __init__(self):
        super(MainWindow, self).__init__()

        view = QGraphicsView()
        self.scene = QGraphicsScene()
        self.scene.setSceneRect(QRectF(0, 0, 1200, 600))
        self.scene.setBackgroundBrush(QColor(15,150,5))
        view.setScene(self.scene)

        cards = []
        for i in range(6):
            card = Card(i)
            self.scene.addItem(card)
            cards.append(card)
        
        self.setCentralWidget(view)
        self.setFixedSize(1200, 700)

        loc = Deck('1')
        loc.setPos(100, 50)
        self.scene.addItem(loc)

        loc2 = Deck('2')
        loc2.setPos(500, 50)
        self.scene.addItem(loc2)

        loc3 = Deck('3')
        loc3.setPos(900, 50)
        self.scene.addItem(loc3)

        loc.add(cards[0])
        loc2.add(cards[1])
        loc2.add(cards[2])
        loc3.add(cards[3])
        loc3.add(cards[4])
        loc3.add(cards[5])

        loc.cards[-1].clickable = True
        loc2.cards[-1].clickable = True
        loc3.cards[-1].clickable = True

        self.show()


if __name__ == '__main__':
    app = QApplication([])
    window = MainWindow()
    app.exec_()