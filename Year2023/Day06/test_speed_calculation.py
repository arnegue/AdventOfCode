import pytest

from speed_evaluator import SpeedEvaluator, Part2SpeedEvaluator


class TestPart1:
    test_data = "Time:      7  15   30\n"\
                "Distance:  9  40  200"

    split_data = test_data.splitlines(keepends=False)

    def test_speed_calculate(self):
        expected_results = range(2, 6)
        evaluator = SpeedEvaluator(self.split_data)
        solution = evaluator.generate_solutions_to_beat_record(race_id=0)
        assert solution == expected_results

    @pytest.mark.parametrize("race_id, amount_of_possibilities_to_win", [[0, 4],
                                                                         [1, 8],
                                                                         [2, 9]])
    def test_amount_solutions(self, race_id, amount_of_possibilities_to_win):
        evaluator = SpeedEvaluator(self.split_data)
        solution = evaluator.generate_solutions_to_beat_record(race_id=race_id)
        assert len(solution) == amount_of_possibilities_to_win

    def test_with_real_data(self):  # for part 1
        with open("./test_data.txt", "r") as file:
            lines = file.readlines()

        margin = 1
        evaluator = SpeedEvaluator(lines)
        for race_id in range(len(evaluator.race_list)):
            solution = evaluator.generate_solutions_to_beat_record(race_id=race_id)
            margin *= len(solution)

        print("Margin:", margin)
        assert margin == 4403592


class TestPart2:
    @pytest.mark.parametrize("race_id, amount_of_possibilities_to_win", [[0, 71503]])
    def test_amount_solutions(self, race_id, amount_of_possibilities_to_win):
        evaluator = Part2SpeedEvaluator(TestPart1.split_data)
        solution = evaluator.generate_solutions_to_beat_record(race_id=race_id)
        assert len(solution) == amount_of_possibilities_to_win

    def test_with_real_data(self): # for part 2
        with open("./test_data.txt", "r") as file:
            lines = file.readlines()

        evaluator = Part2SpeedEvaluator(lines)
        solution = evaluator.generate_solutions_to_beat_record(race_id=0)

        print("Amount of solution:", len(solution))
        assert len(solution) == 38017587
