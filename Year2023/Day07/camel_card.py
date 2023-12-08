import functools
import enum


class CardType(enum.IntEnum):
    FiveOfAKind = 7
    FourOfAKind = 6
    FulLHouse = 5
    ThreeOfAKind = 4
    TwoPair = 3
    OnePair = 2
    HighCard = 1


class Hand(object):
    def __init__(self, list_cards):
        self._list_cards = self.cards_to_numbers(list_cards)
        self.strongest_type: CardType = None

    def get_count(self, searched_card):
        return self._list_cards.count(searched_card)

    def _get_x_of_a_kind(self, amount, ignore_card=None):
        for i in range(len(self._list_cards)):
            searched_card = self.get_card(i)
            if ignore_card is not None and searched_card == ignore_card:
                continue
            count = self.get_count(searched_card)
            if count >= amount:
                return searched_card
        return None

    def has_five_of_a_kind(self):
        return self._get_x_of_a_kind(5) is not None

    def has_four_of_a_kind(self):
        return self._get_x_of_a_kind(4) is not None

    def has_full_house(self):
        searched_card = self._get_x_of_a_kind(3)
        if searched_card:
            pair = self._get_x_of_a_kind(2, ignore_card=searched_card)
            if pair:
                return True
        return False

    def has_three_of_a_kind(self):
        return self._get_x_of_a_kind(3) is not None

    def has_two_pair(self):
        first_pair = self._get_x_of_a_kind(2)
        if first_pair:
            second_pair = self._get_x_of_a_kind(2, ignore_card=first_pair)
        else:
            return False
        return first_pair and second_pair

    def has_one_pair(self):
        return self._get_x_of_a_kind(2) is not None

    def get_high_card(self):
        return max(self._list_cards)

    def get_card(self, i):
        return self._list_cards[i]

    def second_ordering_rule(self, other):
        for i in range(len(self._list_cards)):
            own_card = self.get_card(i)
            other_card = other.get_card(i)

            if own_card > other_card:
                return self
            elif own_card < other_card:
                return other
        raise Exception("Both hands are equally strong")

    def get_strongest_type(self) -> CardType:
        if self.strongest_type is not None:
            return self.strongest_type
        for card_type, function_ in ((CardType.FiveOfAKind,  self.has_five_of_a_kind),
                                     (CardType.FourOfAKind,  self.has_four_of_a_kind),
                                     (CardType.FulLHouse,    self.has_full_house),
                                     (CardType.ThreeOfAKind, self.has_three_of_a_kind),
                                     (CardType.TwoPair,      self.has_two_pair),
                                     (CardType.OnePair,      self.has_one_pair),
                                     (CardType.HighCard,     self.get_high_card)):
            return_card = function_()
            if return_card:
                self.strongest_type = card_type
                return self.strongest_type
        raise Exception("Shouldn't come here")

    def compare_hands(self, other):
        own_strongest_type = self.get_strongest_type()
        other_strongest_type = other.get_strongest_type()

        if own_strongest_type > other_strongest_type:
            return self
        elif other_strongest_type > own_strongest_type:
            return other
        elif own_strongest_type == own_strongest_type:
            return self.second_ordering_rule(other)
        else:
            raise Exception("Shouldn't come here")

    card_map = {
        "A": 14,
        "K": 13,
        "Q": 12,
        "J": 11,
        "T": 10
    }

    @classmethod
    def has_value(cls, card: str) -> int:
        if card in cls.card_map:
            return cls.card_map[card]
        else:
            return int(card)

    @classmethod
    def cards_to_numbers(cls, cards: str):
        list_cards = []
        for char in cards:
            list_cards.append(cls.has_value(char))
        return list_cards


class Part2Hand(Hand):
    def __init__(self, list_cards):
        self.__class__.card_map["J"] = 0  # New instead of 11
        super().__init__(list_cards)
        self._joker_count = None

    def compare_hands(self, other):
        own_strongest_type = self.get_strongest_type()
        other_strongest_type = other.get_strongest_type()

        if own_strongest_type > other_strongest_type:
            return self
        elif other_strongest_type > own_strongest_type:
            return other
        elif own_strongest_type == own_strongest_type:
            own_jokers = self.get_amount_jokers()
            other_jokers = other.get_amount_jokers()
            if own_jokers == 5:
                return self
            elif other_jokers == 5:
                return other
            elif own_jokers < other_jokers:
                return self
            elif own_jokers > other_jokers:
                return other
            else:
                return self.second_ordering_rule(other)
        else:
            raise Exception("Shouldn't come here")

    def get_amount_jokers(self):
        if self._joker_count is None:
            self._joker_count = self.get_count(self.card_map["J"])
        return self._joker_count

    def _get_x_of_a_kind(self, amount, ignore_card=None):
        for i in range(len(self._list_cards)):
            searched_card = self.get_card(i)
            if ignore_card is not None and searched_card == ignore_card:
                continue
            count = self.get_count(searched_card)
            if count + self.get_amount_jokers() >= amount:
                return searched_card
        return None


class HandsEvaluator(object):
    def __init__(self, evaluation_string, hands_class=Hand):
        self.list_tuple_hand_bidings = []
        self.Hand = hands_class
        self.get_tuples(evaluation_string)

    def get_tuples(self, evaluation_string):
        for line in evaluation_string:
            hand_str, biding_factor_str = line.split(" ")
            new_hand = self.Hand(hand_str)
            biding_factor = int(biding_factor_str)
            new_tuple = (new_hand, biding_factor)
            self.list_tuple_hand_bidings.append(new_tuple)

    def rank_hands(self):
        sorted_l = sorted(self.list_tuple_hand_bidings, key=functools.cmp_to_key(self.compare))
        return sorted_l

    @staticmethod
    def compare(tuple_1, tuple_2):
        if tuple_1[0].compare_hands(tuple_2[0]) == tuple_1[0]:
            return +1
        else:
            return -1

