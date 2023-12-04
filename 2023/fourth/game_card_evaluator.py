import re


class Card:
    def __init__(self, line: str):
        self.line = line

        self.id = -1
        self.winning_numbers = []
        self.own_numbers = []

    def evaluate_data(self):
        id_, rest = self.line.split(":")
        possible_numbers, won_numbers = rest.split("|")

        self.winning_numbers = self.get_numbers_from_line(possible_numbers)
        self.own_numbers = self.get_numbers_from_line(won_numbers)

    def get_winning_points(self):
        temp_points = 0
        for possible_number in self.own_numbers:
            if possible_number in self.winning_numbers :
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

