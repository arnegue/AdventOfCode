import pytest
from game_card_evaluator import GameEvaluator


class TestPart1:
    dest_data = "Card 1: 41 48 83 86 17 | 83 86  6 31 17  9 48 53\n" \
                "Card 2: 13 32 20 16 61 | 61 30 68 82 17 32 24 19\n" \
                "Card 3:  1 21 53 59 44 | 69 82 63 72 16 21 14  1\n" \
                "Card 4: 41 92 73 84 69 | 59 84 76 51 58  5 54 83\n" \
                "Card 5: 87 83 26 28 32 | 88 30 70 12 93 22 82 36\n" \
                "Card 6: 31 18 13 56 72 | 74 77 10 23 35 67 36 11"

    split_data = dest_data.splitlines(keepends=False)

    @pytest.mark.parametrize(("line", "expected_points"), [
        [split_data[0], 8],
        [split_data[1], 2],
        [split_data[2], 2],
        [split_data[3], 1],
        [split_data[4], 0],
        [split_data[5], 0],
    ])
    def test_game_data(self, line, expected_points):
        evaluator = GameEvaluator(line)
        evaluator.evaluate_data()
        actual_points = evaluator.get_winning_points()
        assert actual_points == expected_points

    def test_part_sum_test_data(self):  # For part 1 test
        with open("./test_data.txt", "r") as file:
            lines = file.readlines()

        total_points = 0
        for line in lines:
            evaluator = GameEvaluator(line)
            evaluator.evaluate_data()
            total_points += evaluator.get_winning_points()
        print("Total Points:", total_points)
        assert total_points == 25571
