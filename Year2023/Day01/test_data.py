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


class TestPart2:
    test_data_part_2 = ["two1nine",
                        "eightwothree",
                        "abcone2threexyz",
                        "xtwone3four",
                        "4nineeightseven2",
                        "zoneight234",
                        "7pqrstsixteen"]

    @staticmethod
    @pytest.mark.parametrize(("line", "expected_result"), ([test_data_part_2[0], 29],
                                                           [test_data_part_2[1], 83],
                                                           [test_data_part_2[2], 13],
                                                           [test_data_part_2[3], 24],
                                                           [test_data_part_2[4], 42],
                                                           [test_data_part_2[5], 14],
                                                           [test_data_part_2[6], 76]))
    def test_single_lines(line, expected_result):
        assert TestDataEvaluatorPart2.evaluate_line(line) == expected_result

    @staticmethod
    @pytest.mark.parametrize(("line", "expected_result"), (["12", 12],
                                                           ["onetwo", 12],
                                                           ["1two1", 11],
                                                           ["eightwothree.", 83],
                                                           ["sevenine", 79],
                                                           ["3lsevenonebpgfgonethreeeightwos", 32],
                                                           ["898xyxchoasuhz", 88],
                                                           ["1cf", 11],
                                                           ["four4rjrkzvfive2cfl7fourfive", 45]))
    def test_custom_lines(line, expected_result):
        assert TestDataEvaluatorPart2.evaluate_line(line) == expected_result

    @classmethod
    def test_evaluate_result(cls):
        evaluator = TestDataEvaluatorPart2(cls.test_data_part_2)
        result = evaluator.evaluate_calibration_data()
        assert result == 281

    @staticmethod
    def test_all_test_data():
        with open("./test_data.txt", "r") as file:
            lines = file.readlines()
        evaluator = TestDataEvaluatorPart2(lines)
        result = evaluator.evaluate_calibration_data()
        print("Result is", result)
        assert result == 56017
