from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *

class Card(QGraphicsPixmapItem):

    def __init__(self, card_id):
        super(Card, self).__init__()
        #"DM-01_S1_110"

        self.player = None
        self.zone = None
        self.tapped = False
        self.face_up = False

        self.setShapeMode(QGraphicsPixmapItem.BoundingRectShape)
        self.setFlag(QGraphicsItem.ItemIsMovable)
        self.setFlag(QGraphicsItem.ItemSendsGeometryChanges)
        self.setTransformOriginPoint(50, 50)
        
        self.face = QPixmap('assets/{}.jpg'.format(card_id)).scaled(100, 100, Qt.KeepAspectRatio)
        self.back = QPixmap('assets/back.jpg').scaled(100, 100, Qt.KeepAspectRatio)
        self.setPixmap(self.face)

    def show_back(self):
        self.setPixmap(self.back)


class BaseZone(QGraphicsRectItem):

    def __init__(self, position, offset, cards):
        super(BaseZone, self).__init__()
        
        self.setRect(QRectF(QRect(0, 0, 100, 100)))
        self.setZValue(-1)
        self.cards = []
        self.position = position
        self.offset = offset
        self.setPos(*self.position)
        
        for card in cards:
            self.add(card) 
    
    def add(self, card):
        self.cards.append(card)
        card.zone = self
        self.update()
    
    def remove(self, card):
        self.cards.remove(card)
        self.update()

    def update(self):
        for i,card in enumerate(self.cards):
            card.setPos(self.pos() + QPointF(i*self.offset, 0))

class Player():
    
    def __init__(self, cards):


        self.inplay = BaseZone((100, 50), 10, cards[:4])
        self.shields = BaseZone((500, 50), 10, cards[4:8])
        self.deck = BaseZone((900, 50), 10, cards[8:])
        #self.grave = BaseZone((1000, 100), 50, cards)
        #self.mana = BaseZone((1300, 100), 50, cards)
        #self.hand = BaseZone((1600, 100), 50, cards)



class Game(QMainWindow):
     
    def __init__(self):
        super(Game, self).__init__()

        view = QGraphicsView()
        self.scene = QGraphicsScene()
        self.scene.setSceneRect(QRectF(0, 0, 1300, 700))
        self.scene.setBackgroundBrush(QColor(15,150,5))
        view.setScene(self.scene)


        all_cards = []
        card_names = ['0', '1', '2', '3', '4', '5', 'DM-01_S1_110',
        '0', '1', '2', '3', '4', '5', 'DM-01_S1_110']
        for c in card_names:
            card = Card(c)
            self.scene.addItem(card)
            all_cards.append(card)

        self.setCentralWidget(view)
        self.setFixedSize(1300, 700)
        
        
        player1 = Player(all_cards)
        self.scene.addItem(player1.inplay)        
        self.scene.addItem(player1.shields)        
        self.scene.addItem(player1.deck)        
        #self.scene.addItem(player1.grave)        
        #self.scene.addItem(player1.mana)        
        #self.scene.addItem(player1.hand)        

        self.show()


if __name__ == '__main__':
    app = QApplication([])
    window = Game()
    app.exec_()
