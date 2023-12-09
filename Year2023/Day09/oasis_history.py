import re


def get_numbers_from_line(line: str) -> list[int]:
    numbers = re.findall(r'-*\d+', line)
    return [int(number) for number in numbers]


class OasisHistoryParser:
    def __init__(self, history_lines: str):
        self.history_list: list[list[int]] = [get_numbers_from_line(history_lines)]

    @classmethod
    def are_all_zeros(cls, number_list: list[int]):
        return sum(number_list) == 0

    def step_1_zeros(self):
        current_line_index = 0
        while True:
            numbers = self.history_list[current_line_index]
            next_numbers = self.step_1_get_next_numbers(numbers)
            self.history_list.append(next_numbers)
            if self.are_all_zeros(next_numbers):
                break
            current_line_index += 1

    @classmethod
    def step_1_get_next_numbers(cls, numbers: list[int]) -> list[int]:
        next_numbers = []
        for i in range(1, len(numbers)):
            difference = numbers[i] - numbers[i - 1]
            next_numbers.append(difference)
        return next_numbers

    def step_2_backwards(self):
        for i in range(len(self.history_list) - 2, 0, -1):
            current_line = self.history_list[i]
            previous_line = self.history_list[i-1]
            calc_value = current_line[-1] + previous_line[-1]
            previous_line.append(calc_value)

