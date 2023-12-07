import pytest
from camel_card import Hand, CardType, HandsEvaluator


class TestPart1:
    test_data = "32T3K 765\n"\
                "T55J5 684\n"\
                "KK677 28\n"\
                "KTJJT 220\n"\
                "QQQJA 483"

    split_data = test_data.splitlines(keepends=False)

    def test_four_of_a_kind_draw(self):
        hand_1 = Hand("33332")
        hand_2 = Hand("2AAAA")
        assert hand_1.get_strongest_type() == CardType.FourOfAKind
        assert hand_2.get_strongest_type() == CardType.FourOfAKind

        assert hand_1.second_ordering_rule(hand_2) == hand_1  # Because of the first 3 in hand_1

        assert hand_1.compare_hands(hand_2) == hand_1

    @pytest.mark.parametrize("line_str, expected_type", [[split_data[0], CardType.OnePair],
                                                         [split_data[1], CardType.ThreeOfAKind],
                                                         [split_data[2], CardType.TwoPair],
                                                         [split_data[3], CardType.TwoPair],
                                                         [split_data[4], CardType.ThreeOfAKind],
                                                         ["AAAAA ",      CardType.FiveOfAKind],
                                                         ["AAQAA ",      CardType.FourOfAKind],
                                                         ["AAQQA ",      CardType.FulLHouse],
                                                         ["AAQQA ",      CardType.FulLHouse],
                                                         ["1234A ",      CardType.HighCard],
                                                         ])
    def test_highest_type(self, line_str, expected_type):
        hand_str, _ = line_str.split(" ")
        hand = Hand(hand_str)
        assert hand.get_strongest_type() == expected_type

    def test_ranking(self):
        expected_results = [765, 220, 28, 684, 483]
        evaluator = HandsEvaluator(self.split_data)
        ranked_hands = evaluator.rank_hands()

        result_list = []
        total_winning = 0
        for i in range(len(ranked_hands)):
            _, bidding = ranked_hands[i]
            result_list.append(bidding)
            total_winning += bidding * (i + 1)
        assert result_list == expected_results
        assert total_winning == 6440

    def test_part_1(self):  # For part 1 test
        with open("./test_data.txt", "r") as file:
            lines = file.readlines()

        evaluator = HandsEvaluator(lines)
        ranked_hands = evaluator.rank_hands()

        total_winning = 0
        for i in range(len(ranked_hands)):
            _, bidding = ranked_hands[i]
            total_winning += bidding * (i + 1)
        print("Total Winning:", total_winning)
        assert total_winning == 250058342
