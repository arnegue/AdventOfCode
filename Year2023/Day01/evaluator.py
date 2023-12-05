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
        left_char = cls.get_leftest_number(line)[1]
        right_char = cls.get_rightest_number(line)[1]
        no = int(left_char + right_char)
        return no

    @classmethod
    def get_leftest_number(cls, line):
        return cls.get_left_char_digit(line)

    @classmethod
    def get_rightest_number(cls, line):
        return cls.get_right_char_digit(line)

    @classmethod
    def get_left_char_digit(cls, line: str):
        for index, char in enumerate(line):
            if str.isdigit(char):
                return index, char
        raise ValueError("Did not find a digit")

    @classmethod
    def get_right_char_digit(cls, line: str):
        for index, char in enumerate(line[::-1]):
            if str.isdigit(char):
                index = len(line) - 1 - index  # Count backwards, but index is from front
                return index, char
        raise ValueError("Did not find a digit")


class TestDataEvaluatorPart2(TestDataEvaluatorPart1):
    class Digits(IntEnum):
        one = 1
        two = 2
        three = 3
        four = 4
        five = 5
        six = 6
        seven = 7
        eight = 8
        nine = 9

    @classmethod
    def get_leftest_number(cls, line):
        leftest_word, leftest_char = None, None
        try:
            leftest_word = cls.get_left_word_digit(line)
        except IndexError:
            pass  # Let's hope leftest char has some good news
        try:
            leftest_char = cls.get_left_char_digit(line)
        except ValueError:  # If there is no digit
            pass

        if leftest_word is None and leftest_char is None:
            raise Exception("Something's wrong. Didn't find anything")
        elif leftest_char is None:
            return leftest_word
        elif leftest_word is None:
            return leftest_char
        elif leftest_word[0] < leftest_char[0]:
            return leftest_word
        else:
            return leftest_char

    @classmethod
    def get_rightest_number(cls, line):
        rightest_word, rightest_char = None, None
        try:
            rightest_word = cls.get_right_word_digit(line)
        except IndexError:
            pass  # Lets' hope rightest char has some good news
        try:
            rightest_char = cls.get_right_char_digit(line)
        except ValueError:  # If there is no digit
            pass

        if rightest_word is None and rightest_char is None:
            raise Exception("Something's wrong. Didn't find anything")
        elif rightest_char is None:
            return rightest_word
        elif rightest_word is None:
            return rightest_char
        elif rightest_word[0] > rightest_char[0]:
            return rightest_word
        else:
            return rightest_char

    @classmethod
    def find_digit_words(cls, line, direction_left):
        digit_index = []
        for digit in cls.Digits:
            find_method = line.find if direction_left else line.rfind
            find_idx = find_method(digit.name)
            if find_idx >= 0:
                digit_index.append((find_idx, str(digit.value)))
        return digit_index

    @classmethod
    def get_left_word_digit(cls, line: str):
        digit_words = cls.find_digit_words(line, direction_left=True)
        first_digit = sorted(digit_words, key=lambda x: x[0])[0]
        return first_digit

    @classmethod
    def get_right_word_digit(cls, line: str):
        digit_words = cls.find_digit_words(line, direction_left=False)
        last_digit = sorted(digit_words, key=lambda x: x[0])[-1]
        return last_digit
