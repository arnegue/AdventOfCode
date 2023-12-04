import re


class GameEvaluator:
    def __init__(self, line: str):
        self.line = line

        self.id = -1
        self.possible_winning_numbers = []
        self.won_numbers = []

    def evaluate_data(self):
        id_, rest = self.line.split(":")
        possible_numbers, won_numbers = rest.split("|")

        self.possible_winning_numbers = self.get_numbers_from_line(possible_numbers)
        self.won_numbers = self.get_numbers_from_line(won_numbers)

    def get_winning_points(self):
        temp_points = 0
        for possible_number in self.possible_winning_numbers:
            if possible_number in self.won_numbers:
                if temp_points == 0:
                    temp_points = 1
                else:
                    temp_points *= 2
        return temp_points

    @classmethod
    def get_numbers_from_line(cls, line):
        numbers = []
        for match in re.finditer(r'\d+', line):
            numbers.append(int(match.group()))
        return numbers
