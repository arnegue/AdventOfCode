from enum import IntEnum


class TestDataEvaluatorPart1(object):
    def __init__(self, content: [str]):
        self._content = content

    def evaluate_calibration_data(self) -> int:
        temp_no = 0
        for line in self._content:
            temp_no += self.evaluate_line(line)
        return temp_no

    @classmethod
    def evaluate_line(cls, line):
        left_char = cls.get_left_char_digit(line)
        right_char = cls.get_right_char_digit(line)
        no = int(left_char + right_char)
        return no

    @staticmethod
    def get_left_char_digit(line):
        for char in line:
            if str.isdigit(char):
                return char
        raise Exception("Did not find a digit")

    @staticmethod
    def get_right_char_digit(line):
        for char in line[::-1]:
            if str.isdigit(char):
                return char
        raise Exception("Did not find a digit")

