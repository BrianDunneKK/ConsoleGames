from TicTacToe import *
from cdkkGame import Game
from cdkkBoard import Board, GamePiece
from cdkkQtGame import *

# ----------------------------------------

class GameWindow(QMainWindow):
    def __init__(self, name : str = ""):
        super().__init__()

        if name == "":
            title = "CodederDojo Kilkenny"
        else:
            title = f"CodederDojo Kilkenny - {name}"

        self.setWindowTitle(title)
        # self.setMinimumSize(640, 480)
        self.setMinimumSize(800, 600)

        self.board_view = BoardView(self)
        self.label = QLabel("Instructions go here")

        glayout = QGridLayout()
        glayout.addWidget(QLabel(), 2, 2)
        glayout.addWidget(self.board_view, 1, 1, Qt.AlignmentFlag.AlignCenter)
        glayout.addWidget(self.label, 3, 0, 1, 3, Qt.AlignmentFlag.AlignCenter)
        glayout.setColumnStretch(0, 20)
        glayout.setColumnStretch(2, 20)
        glayout.setRowStretch(0, 20)
        glayout.setRowStretch(2, 20)

        board_view_container = QWidget()
        board_view_container.setLayout(glayout)
        self.setCentralWidget(board_view_container)

    def init(self) -> bool:
        self.game = TicTacToeGame()
        self.game.init()
        self.game.start()
        self.game.calc_options()
        self.next_turn = ""
        self.board_view.init(self.game.board, self)
        self.show()
        return True

    def select_cell(self, xcol : int, yrow : int, widget : QWidget):
        self.next_turn = self.game.board.to_gridref(xcol, yrow)
        self.next_turn = self.next_turn.upper()
        valid_msg = self.game.check(self.next_turn)
        if valid_msg != "":
            self.label.setText(f"Move {self.next_turn} is invalid: {valid_msg}")
        else:
            self.label.setText("")
            self.game.update(self.next_turn)
            self.game.calc_options()
            if self.game.game_over:
                if (self.game.status == 0 or self.game.status >= 99): 
                    self.label.setText(f"Draw game\n")
                else:
                    self.label.setText(f"Player {self.game.status} won")

            widget.update()

# ----------------------------------------

class BoardView(QWidget):
    # def __init__(self, parent: typing.Optional['QWidget'] = None, flags: Qt.WindowType = Qt.WindowType.Widget) -> None:
    #     super().__init__(parent, flags)

    def init(self, board : Board, game_window : GameWindow):
        self.board = board
        self.game_window = game_window

        layout = QGridLayout()
        self.setLayout(layout)
        self.game_piece_scaling = min(self.parent().width()/100/3, (self.parent().height() - 96)/100/3)

        for yrow in range(self.board.ysize):
            for xcol in range(self.board.xsize):
                self.add_piece_view(xcol, yrow)


    def add_piece_view(self, xcol, yrow):
        align = Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignTop
        context = {"xcol": xcol, "yrow":yrow}
        layout = typing.cast(QGridLayout, self.layout())
        piece_view = vCounter(self, self.board.get_piece(xcol, yrow), scaling=self.game_piece_scaling, context=context)
        layout.addWidget(piece_view, yrow, xcol, align)

    def select_cell(self, xcol : int, yrow : int, widget : QWidget):
        self.game_window.select_cell(xcol, yrow, widget)
        self.add_piece_view(xcol, yrow)

    def resizeEvent(self, a0: QResizeEvent) -> None:
        # To Do: Not working
        self.game_piece_scaling = min(self.parent().width()/100/3, (self.parent().height() - 96)/100/3)
        for item in self.children():
            item.update()
        return super().resizeEvent(a0)

class vCounter(QGraphicsView):
    def __init__(self, parent: typing.Optional['QWidget'] = None, piece : GamePiece = GamePiece(), \
                 scaling : int = 1, context: dict = {}) -> None:
        super().__init__(parent)
        self.piece = piece
        self.context = context
        self.setRenderHint(QPainter.RenderHint.Antialiasing)
    
        scene = QGraphicsScene(0, 0, 100, 100, self.parent())
        match self.piece.code:
            case 0:
                rect = QGraphicsRectItem(0, 0, 100, 100)
                brush = QBrush(Qt.GlobalColor.white)
                rect.setBrush(brush)
                scene.addItem(rect)
            case 1:
                line1 = QGraphicsLineItem(20, 20, 80, 80)
                line2 = QGraphicsLineItem(20, 80, 80, 20)
                blue_pen = QPen(Qt.GlobalColor.blue, 15, cap=Qt.PenCapStyle.RoundCap)
                line1.setPen(blue_pen)
                line2.setPen(blue_pen)
                scene.addItem(line1)
                scene.addItem(line2)
            case 2:
                ellipse = QGraphicsEllipseItem(20, 20, 60, 60)
                green_pen = QPen(Qt.GlobalColor.darkGreen, 10)
                ellipse.setPen(green_pen)
                scene.addItem(ellipse)

        self.setScene(scene)
        # self.scale(scaling, scaling)

    def mousePressEvent(self, e: QMouseEvent) -> None:
        p = typing.cast(BoardView, self.parent())
        p.select_cell(self.context['xcol'], self.context['yrow'], self)

# ----------------------------------------

class TicTacToeWindow(GameWindow):
    pass

class TicTacToe(cdkkQtGame):
    def init(self, title : str = "Tic Tac Toe") -> bool:
        self.window = TicTacToeWindow(title)
        self.window.init()
        return True

# ----------------------------------------

app = TicTacToe([])
app.init()
app.exec()
