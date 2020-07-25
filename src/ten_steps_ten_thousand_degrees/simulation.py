from copy import deepcopy

import numpy as np


def action_at(game_status, position):
    row, column = position
    max_row, max_column = game_status.shape

    score = 90
    next_position = None
    current_status = deepcopy(game_status)
    if current_status[row][column] >= 0:
        current_pointer = (current_status[row][column] + 1) % 4
        temp_row, temp_column = {
            0: (row - 1, column),
            1: (row, column + 1),
            2: (row + 1, column),
            3: (row, column - 1),
        }[current_pointer]
        current_status[row][column] = current_pointer

        is_out_of_range = False
        if temp_row < 0 or temp_row >= max_row:
            is_out_of_range = True
        if temp_column < 0 or temp_column >= max_column:
            is_out_of_range = True
        if not is_out_of_range and current_status[temp_row][temp_column] < 0:
            is_out_of_range = True
        if not is_out_of_range:
            next_position = (temp_row, temp_column)

    if next_position:
        temp_score, current_status = action_at(current_status, next_position)
        score += temp_score
    return score, current_status


class GameStatus(object):
    def __init__(self, status):
        self.status = status
        self.score = np.zeros(status.shape)

    def get_possible_position(self, strong_chance):
        random = np.random.random(self.status.size)
        temp_score = self.score.reshape(self.score.size)
        max_score = temp_score.max()
        if max_score > 0:
            max_score_index = self.score.argmax()
            random[max_score_index] *= np.count_nonzero(self.score) * strong_chance
            other_score = self.score.reshape(self.score.size) > 0
            other_score[max_score_index] = False
            random[other_score] *= (1 - strong_chance)
        return np.unravel_index(random.argmax(), self.score.shape)

    def test(self, position):
        score, current_status = action_at(game_status=self.status, position=position)
        self.score[position] = score
        return score, current_status


class StatusManager(object):
    def __init__(self, init_status):
        self.game_statuses = [init_status]

    def get_status(self, status):
        for game_status in self.game_statuses:
            if np.all(game_status.status == status):
                return game_status
        return GameStatus(status=status)


def run_once(game_status, status_manager, max_step):
    total_score = 0
    positions = []
    current_game_status = game_status
    for index in range(max_step):
        strong_chance = float(index + 1) / max_step
        possible_position = current_game_status.get_possible_position(strong_chance=strong_chance)
        score, status = current_game_status.test(possible_position)
        current_game_status = status_manager.get_status(status)

        total_score += score
        positions.append(possible_position)
    return total_score, positions


def main():
    init_game = np.array([[0, 0, 0, -1], [0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0]])
    # init_game = (np.random.random((6, 5)) * 4).astype(np.int16)
    game_status = GameStatus(init_game)
    max_step = 10
    max_times = 1000

    status_manager = StatusManager(game_status)
    max_total_score = 0
    max_positions = None
    for i in range(max_times):
        total_score, positions = run_once(game_status, status_manager, max_step)
        # print('Total score: {}\nSteps: {}'.format(total_score, positions))
        if total_score > max_total_score:
            max_total_score = total_score
            max_positions = positions
    print('Max total score: {}\nSteps: {}'.format(max_total_score, max_positions))


if __name__ == '__main__':
    main()
