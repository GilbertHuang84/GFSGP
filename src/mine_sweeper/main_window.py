import sys
from functools import partial

from PyQt5 import QtWidgets, QtCore

from gamer import MineSweeper


class MainWindow(QtWidgets.QWidget):
    def __init__(self):
        super(MainWindow, self).__init__()

        default_row, default_column, default_mines_count = 10, 10, 10
        self.row_count = default_row
        self.column_count = default_column
        self.mines_count = default_mines_count
        self.button_dict = None

        layout = QtWidgets.QVBoxLayout()
        top_banner = QtWidgets.QHBoxLayout()

        mines_count_label = QtWidgets.QLabel()
        mines_count_label.setText('{}'.format(default_mines_count))
        statue_button = QtWidgets.QPushButton()
        cost_time_label = QtWidgets.QLabel('000')

        top_banner.addWidget(mines_count_label)
        top_banner.addWidget(statue_button)
        top_banner.addWidget(cost_time_label)
        top_banner.setAlignment(QtCore.Qt.AlignCenter)

        game_context_layer = QtWidgets.QGridLayout()
        self.game_context_layer = game_context_layer

        self.gamer = MineSweeper()
        self.statue_button = statue_button
        self.init_press()

        layout.addLayout(top_banner)
        layout.addLayout(game_context_layer)
        self.setLayout(layout)
        self.setWindowTitle('Mine Sweeper by Gilbert Huang')

        statue_button.clicked.connect(self.init_press)

    def init_press(self):
        for i in reversed(range(self.game_context_layer.count())):
            self.game_context_layer.itemAt(i).widget().setParent(None)

        row_count = self.row_count
        column_count = self.column_count
        mines_count = self.mines_count
        self.gamer.initialize(row_count, column_count, mines_count)

        button_dict = {}
        for row_index in range(row_count):
            for column_index in range(column_count):
                current_index = column_count * row_index + column_index
                press_button = QtWidgets.QPushButton()
                press_button.setText(' ')
                self.game_context_layer.addWidget(press_button, row_index, column_index)
                press_button.clicked.connect(partial(self.button_press, current_index))
                button_dict[current_index] = press_button
        self.statue_button.setText('^_^')
        self.button_dict = button_dict

    def button_press(self, current_index):
        current_row = int(current_index / self.column_count)
        current_column = current_index - current_row * self.column_count
        self.gamer.step(current_row, current_column, 1)

        if self.gamer.is_failed():
            self.statue_button.setText('-_-!')
        elif self.gamer.is_done():
            self.statue_button.setText('Perfect!')

        for row_index in range(self.row_count):
            for column_index in range(self.column_count):
                temp_index = self.column_count * row_index + column_index
                if self.gamer.status[row_index, column_index] > 0:
                    mine_distribute = self.gamer.mine_distribute[row_index, column_index]
                    if mine_distribute >= 0:
                        self.button_dict[temp_index].setText('{}'.format(int(mine_distribute)))
                elif self.gamer.status[row_index, column_index] < 0:
                    self.button_dict[temp_index].setText('{}'.format(int(self.gamer.status[row_index, column_index])))


if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    main_window = MainWindow()
    main_window.setGeometry(0, 0, 400, 300)
    main_window.move(50, 50)
    main_window.show()
    sys.exit(app.exec_())
