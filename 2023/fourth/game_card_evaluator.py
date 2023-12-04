import re


class Card:
    def __init__(self, line: str):
        self.line = line

        self.id = -1
        self.winning_numbers = []
        self.own_numbers = []

    def evaluate_data(self):
        id_, rest = self.line.split(":")
        self.id = int(next(re.finditer(r'\d+', id_)).group())

        possible_numbers, won_numbers = rest.split("|")

        self.winning_numbers = self.get_numbers_from_line(possible_numbers)
        self.own_numbers = self.get_numbers_from_line(won_numbers)

    def get_amount_winning_numbers(self) -> int:
        amount_winning_numbers = 0
        for possible_number in self.own_numbers:
            if possible_number in self.winning_numbers:
                amount_winning_numbers += 1
        return amount_winning_numbers

    @classmethod
    def get_winning_points(cls, amount_winning_numbers: int) -> int:
        temp_points = 0
        for i in range(amount_winning_numbers):
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


class GameCard(Card):
    def __init__(self, line: str):
        super().__init__(line)
        self.amount = 1


class GameEvaluator(object):
    def __init__(self, list_cards: []):
        self.card_dict = {}
        for card in list_cards:
            self.card_dict[card.id] = card

    def evaluate_wins(self):
        for card_id, card in self.card_dict.items():
            for _ in range(card.amount):
                winning_numbers = card.get_amount_winning_numbers()
                for o in range(winning_numbers):
                    new_card_id = card.id + o + 1  # Plus one, we don't want to copy the own card
                    self.card_dict[new_card_id].amount += 1

    def get_amount_cards(self):
        card_amount = 0
        for card in self.card_dict.values():
            card_amount += card.amount
        return card_amount
