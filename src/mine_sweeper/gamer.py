import numpy as np


class MineSweeper(object):
    def __init__(self):
        self._status = None
        self._mine_distribute = None
        self._partition = None
        self._row_count = None
        self._column_count = None
        self._mines_count = None

    def is_failed(self):
        if self._status is None or self._mine_distribute is None or self._partition is None:
            return False
        return np.any(self._status < 0)

    def is_done(self):
        return np.count_nonzero(self.status) + self._mines_count == self._row_count * self._column_count

    @staticmethod
    def _init_mines(mines_count, row_count, column_count):
        cells_count = row_count * column_count
        mine_distribute = np.zeros(cells_count)

        if mines_count <= cells_count:
            for index in range(mines_count):
                mine_distribute[index] = 1
        else:
            raise RuntimeError('Mines count is bigger than the cells count')

        for index in range(cells_count):
            switch_cell_index = np.random.randint(0, cells_count)
            temp_value = mine_distribute[switch_cell_index]
            mine_distribute[switch_cell_index] = mine_distribute[index]
            mine_distribute[index] = temp_value
        mine_distribute.resize((row_count, column_count))
        return mine_distribute

    @staticmethod
    def _init_labels(mine_distribute, row_count, column_count):
        labels = np.zeros((row_count, column_count))
        for row_index in range(0, row_count):
            for column_index in range(0, column_count):
                if mine_distribute[row_index, column_index]:
                    continue

                count = 0
                for row_delta in range(-1, 2):
                    for column_delta in range(-1, 2):
                        temp_row_index = row_index + row_delta
                        temp_column_index = column_index + column_delta
                        if temp_row_index < 0 or temp_column_index < 0:
                            continue

                        if temp_row_index >= row_count or temp_column_index >= column_count:
                            continue
                        count += mine_distribute[temp_row_index, temp_column_index]
                labels[row_index, column_index] = count
        return labels

    @classmethod
    def _iter_partition(cls, mine_distribute, labels, partition, row_index, column_index, partition_number,
                        row_count, column_count):
        for row_delta in range(-1, 2):
            for column_delta in range(-1, 2):
                temp_row_index = row_index + row_delta
                temp_column_index = column_index + column_delta
                if temp_row_index < 0 or temp_column_index < 0:
                    continue

                if temp_row_index >= row_count or temp_column_index >= column_count:
                    continue

                if mine_distribute[temp_row_index, temp_column_index] > 0:
                    continue

                if labels[temp_row_index, temp_column_index] > 0:
                    continue

                if partition[temp_row_index, temp_column_index] > 0:
                    continue

                if row_delta == 0 and column_delta == 0:
                    partition[temp_row_index, temp_column_index] = partition_number
                    continue

                cls._iter_partition(mine_distribute=mine_distribute, labels=labels, partition=partition,
                                    row_index=temp_row_index, column_index=temp_column_index,
                                    partition_number=partition_number, row_count=row_count, column_count=column_count)

    @classmethod
    def _init_partition(cls, mine_distribute, labels, row_count, column_count):
        fill_cells = mine_distribute + labels
        max_partition_id = 0
        partition = np.zeros((row_count, column_count))
        for row_index in range(0, row_count):
            for column_index in range(0, column_count):
                if fill_cells[row_index, column_index] > 0:
                    continue

                if partition[row_index, column_index] == 0:
                    max_partition_id += 1

                cls._iter_partition(mine_distribute=mine_distribute, labels=labels, partition=partition,
                                    row_index=row_index, column_index=column_index,
                                    partition_number=max_partition_id, row_count=row_count, column_count=column_count)
        return partition

    def initialize(self, row_count, column_count, mines_count):
        mine_distribute = self._init_mines(mines_count=mines_count,
                                           row_count=row_count,
                                           column_count=column_count)

        labels = self._init_labels(mine_distribute=mine_distribute,
                                   row_count=row_count,
                                   column_count=column_count)

        partition = self._init_partition(mine_distribute=mine_distribute,
                                         labels=labels,
                                         row_count=row_count,
                                         column_count=column_count)

        self._status = np.zeros((row_count, column_count))
        self._mine_distribute = mine_distribute * -1 + labels
        self._partition = partition
        self._row_count = row_count
        self._column_count = column_count
        self._mines_count = mines_count

    def step(self, row, column, mark_number):
        if self.is_failed() or self.is_done():
            return

        if mark_number == 1:
            if self._mine_distribute[row, column] == -1:
                self._status[row, column] = -1
            elif self._status[row, column] == 0:
                self._status[row, column] = 1
                if self._partition[row, column] > 0:
                    current_partition = self._partition[row, column]
                    current_partition_area = self._partition == current_partition

                    increased = np.zeros((self._row_count, self._column_count))
                    for row_index in range(0, self._row_count):
                        for column_index in range(0, self._column_count):
                            if row_index > 0:
                                if current_partition_area[row_index - 1, column_index]:
                                    increased[row_index, column_index] = 1

                            if row_index < self._row_count - 1:
                                if current_partition_area[row_index + 1, column_index]:
                                    increased[row_index, column_index] = 1

                            if column_index > 0:
                                if current_partition_area[row_index, column_index - 1]:
                                    increased[row_index, column_index] = 1

                            if column_index < self._column_count - 1:
                                if current_partition_area[row_index, column_index + 1]:
                                    increased[row_index, column_index] = 1
                    self._status[(current_partition_area + increased) > 0] = 1
        elif mark_number == -1:
            if self._status[row, column] == 0:
                if self._mine_distribute[row, column] != -1:
                    self._status[row, column] = -2

    @property
    def status(self):
        return self._status

    @property
    def mine_distribute(self):
        return self._mine_distribute

    @property
    def partition(self):
        return self._partition


def main():
    mine_sweeper = MineSweeper()
    row_count = 10
    column_count = 10
    mines_count = 20

    for game_time in range(1):
        print('{0} Game start {0}'.format('=' * 10))
        mine_sweeper.initialize(row_count, column_count, mines_count)

        for step_time in range(20):
            row_index = np.random.randint(0, row_count)
            column_index = np.random.randint(0, column_count)
            mark_number = np.random.rand()
            print('-' * 20)
            print(f'Step: {row_index}, {column_index}')
            print('Mine_distribute')
            print(mine_sweeper.mine_distribute)
            print('Partition:')
            print(mine_sweeper.partition)

            if mark_number > 0.1:
                mine_sweeper.step(row_index, column_index, 1)
            else:
                mine_sweeper.step(row_index, column_index, -1)

            print('Status:')
            print(mine_sweeper.status)

            if mine_sweeper.is_failed():
                print('{0} Game failed {0}'.format('-' * 10))
                break


if __name__ == '__main__':
    main()
