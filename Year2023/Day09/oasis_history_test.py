import pytest
from oasis_history import OasisHistoryParser


class TestPart1:
    test_data = "0 3 6 9 12 15\n" \
                "1 3 6 10 15 21\n" \
                "10 13 16 21 30 45"

    split_data = test_data.splitlines(keepends=False)

    @pytest.mark.parametrize("line, number_list_len", [[split_data[0], 3],
                                                       [split_data[1], 4],
                                                       [split_data[2], 5]])
    def test_step_1_zeros(self, line, number_list_len):
        ohp = OasisHistoryParser(line)
        ohp.step_1_zeros()
        assert len(ohp.history_list) == number_list_len

    @pytest.mark.parametrize("line, last_value", [[split_data[0], 18],
                                                  [split_data[1], 28],
                                                  [split_data[2], 68]])
    def test_step_2(self, line, last_value):
        ohp = OasisHistoryParser(line)
        ohp.step_1_zeros()
        ohp.step_2_backwards()
        assert ohp.history_list[0][-1] == last_value

    def test_step_3(self):
        results = []
        for line in self.split_data:
            ohp = OasisHistoryParser(line)
            ohp.step_1_zeros()
            ohp.step_2_backwards()
            results.append(ohp.history_list[0][-1])
        assert sum(results) == 114  # 18 + 28 + 68

    def test_part_1(self):  # For part 1 test
        with open("./test_data.txt", "r") as file:
            lines = file.readlines()

        results = []
        for line in lines:
            ohp = OasisHistoryParser(line)
            ohp.step_1_zeros()
            ohp.step_2_backwards()
            results.append(ohp.history_list[0][-1])

        sum_results = sum(results)
        print("Sum: ", sum_results)
        assert sum_results == 1647269739

    def test_custom_data(self):
        line = "-4 -8 -12 -16 -20 -24 -28 -32 -36 -40 -44 -48 -52 -56 -60 -64 -68 -72 -76 -80 -84"
        ohp = OasisHistoryParser(line)
        ohp.step_1_zeros()
        assert len(ohp.history_list) == 3
