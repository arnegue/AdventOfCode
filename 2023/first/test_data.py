import pytest
from evaluator import TestDataEvaluatorPart1, TestDataEvaluatorPart2


class TestPart1:
    test_data_part_1 = ["1abc2",
                        "pqr3stu8vwx",
                        "a1b2c3d4e5f",
                        "treb7uchet"]

    @staticmethod
    @pytest.mark.parametrize(("line", "expected_result"), ([test_data_part_1[0], 12],
                                                           [test_data_part_1[1], 38],
                                                           [test_data_part_1[2], 15],
                                                           [test_data_part_1[3], 77]))
    def test_single_lines(line, expected_result):
        assert TestDataEvaluatorPart1.evaluate_line(line) == expected_result

    @classmethod
    def test_evaluate_result(cls):
        evaluator = TestDataEvaluatorPart1(cls.test_data_part_1)
        result = evaluator.evaluate_calibration_data()
        assert result == 142

    @staticmethod
    def test_all_test_data():
        with open("./test_data.txt", "r") as file:
            lines = file.readlines()
        evaluator = TestDataEvaluatorPart1(lines)
        result = evaluator.evaluate_calibration_data()
        print("Result is", result)
        assert result == 56506
