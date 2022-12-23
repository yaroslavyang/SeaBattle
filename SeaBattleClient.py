from PyQt6.QtGui import *
from PyQt6.QtWidgets import *
import socket as sock
import json
from threading import Thread
import sys
from BattleField import BattleField


class SeaBattle(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Sea Battle")
        self.setFixedSize(1200, 700)
        self.setObjectName('window')
        self.setStyleSheet('#window {background: #353659}')
        self.cells = [[0 for i in range(10)] for i in range(10)]
        self.enemy_cells = [[0 for i in range(10)] for i in range(10)]
        self.last_shoots = []
        self.battle_field = BattleField()
        self.setUI()
        self.show()

    def setUI(self):
        for i in range(10):
            for j in range(10):
                width = 40
                cell = QPushButton(self)
                cell.setGeometry(100 + width * i, 140 + width * j, width, width)
                cell.setObjectName('cell')
                cell.setStyleSheet("#cell {background: #9798bd;}")
                cell.setEnabled(False)
                cell.setFont(QFont('Arial', 16))
                self.cells[i][j] = cell
        self._init_enemy_field()
        self.update_field_button = QPushButton(self)
        self.update_field_button.setText('Refresh field')
        self.update_field_button.move(100, 560)
        self._style_button(self.update_field_button)
        self.update_field_button.clicked.connect(self.generate_ships)
        self.start_game_button = QPushButton(self)
        self.start_game_button.setText('Start game')
        self.start_game_button.move(230, 560)
        self.start_game_button.clicked.connect(self._start_game)
        self._style_button(self.start_game_button)
        self.main_text = QLabel(self)
        self._style_text(self.main_text)
        self.main_text.setGeometry(500, 40, 300, 50)
        self.second_text = QLabel(self)
        self._style_text(self.second_text)
        self.second_text.setGeometry(570, 620, 300, 30)
        self.generate_ships()

    def _init_enemy_field(self):
        for i in range(10):
            for j in range(10):
                width = 40
                cell = QPushButton(self)
                cell.setGeometry(690 + width * i, 140 + width * j, width, width)
                cell.setObjectName('cell')
                cell.setStyleSheet("#cell {background: #9798bd;}")
                cell.setEnabled(False)
                cell.setAccessibleName(str(i) + str(j))
                cell.clicked.connect(self._shoot)
                self.enemy_cells[i][j] = cell

    def reset_cells_background(self):
        for i in self.cells:
            for j in i:
                j.setStyleSheet("#cell {background: #9798bd;}")

    def generate_ships(self):
        self.reset_cells_background()
        self.battle_field.place_ships()
        ships = self.battle_field.get_ships()
        for ship in ships:
            for coordinate in ship:
                i = coordinate[0]
                j = coordinate[1]
                self.cells[i][j].setStyleSheet('#cell {background: #fff};')

    def _style_button(self, button: QPushButton):
        button.setFont(QFont('MS Shell Dlg 2', 12))
        button.setObjectName('btn')
        button.setStyleSheet('#btn {background: #353659; color: #fff;}')

    def _style_text(self, label:QLabel):
        label.setFont(QFont('MS Shell Dlg 2', 12))
        label.setObjectName('text')
        label.setStyleSheet('#text {color: #fff;}')

    def _change_main_text(self, text):
        self.main_text.setText(text)

    def _change_second_text(self, text):
        self.second_text.setText(text)

    def _start_game(self):
        self.socket = sock.socket()
        self.socket.connect(("localhost", 3000))
        self.socket.sendall(json.dumps(self.battle_field.get_ships()).encode('utf-8'))
        self.start_game_button.deleteLater()
        self.update_field_button.deleteLater()
        self._change_main_text('Waiting second player...')
        self.t1 = Thread(target=self._get_data_from_server, daemon=True)
        self.t1.start()

    def _get_data_from_server(self):
        while True:
            data = self.socket.recv(1024).decode('utf-8')
            try:
                last_shoot = self.last_shoots[-1]
                button = self.enemy_cells[int(last_shoot[0])][int(last_shoot[1])]
            except IndexError:
                button = None
            if data == '1':
                self._change_main_text('Your turn')
                for i in range(10):
                    for j in range(10):
                        self.enemy_cells[i][j].setEnabled(True)
            elif data == '2':
                self._change_main_text('Enemy turn')
                for i in range(10):
                    for j in range(10):
                        self.enemy_cells[i][j].setEnabled(False)
            elif data == 'hit':
                button.setStyleSheet("#cell {background: #ed2147;}")
                self._change_second_text('You hitted enemy ship')
            elif data == 'destroyed':
                button.setStyleSheet("#cell {background: #ed2147;}")
                self._change_second_text('You destroyed enemy ship')
            elif data == 'miss':
                button.setStyleSheet("#cell {background: #21beed;}")
                self._change_second_text('You missed')
                self._change_role()
            elif len(data) == 2:
                i = int(data[0])
                j = int(data[1])
                button = self.cells[i][j]
                button.setText('x')
                coordinate = (i, j)
                ships = self.battle_field.get_ships()
                is_miss = True
                for ship in ships:
                    if coordinate in ship:
                        self._change_second_text('Enemy hitted your ship')
                        is_miss = False
                if is_miss:
                    self._change_role()
                    self._change_second_text('Enemy missed')
            elif data == 'win':
                self._disable_enemy_field()
                self._change_main_text('You win')
            elif data == 'lose':
                self._disable_enemy_field()
                self._change_main_text('You lose')

    def _shoot(self):
        button = self.sender()
        coordinate = button.accessibleName()
        self.last_shoots.append(coordinate)
        self.socket.sendall(coordinate.encode('utf-8'))

    def _change_role(self):
        if self.enemy_cells[0][0].isEnabled():
            self._change_main_text('Enemy turn')
        else:
            self._change_main_text('Your turn')
        for i in self.enemy_cells:
            for j in i:
                if j.isEnabled():
                    j.setEnabled(False)
                else:
                    j.setEnabled(True)

    def _disable_enemy_field(self):
        for i in self.enemy_cells:
            for j in i:
                j.setEnabled(False)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = SeaBattle()
    sys.exit(app.exec())