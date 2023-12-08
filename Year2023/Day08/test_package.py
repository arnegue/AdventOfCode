import pytest
from PackageMap import MapEvaluator, Position


class TestPart1:
    test_data = "RL\n" \
                "\n" \
                "AAA = (BBB, CCC)\n" \
                "BBB = (DDD, EEE)\n" \
                "CCC = (ZZZ, GGG)\n" \
                "DDD = (DDD, DDD)\n" \
                "EEE = (EEE, EEE)\n" \
                "GGG = (GGG, GGG)\n" \
                "ZZZ = (ZZZ, ZZZ)"

    split_data = test_data.splitlines(keepends=False)

    @pytest.mark.parametrize("name", ["AAA", "BBB", "CCC", "DDD", "EEE", "GGG", "ZZZ"])
    def test_map_parsing(self, name):
        evaluator = MapEvaluator(self.split_data)
        assert name in evaluator.position_dict

    def test_count(self):
        evaluator = MapEvaluator(self.split_data)
        actual_count = evaluator.count_way_to_finish("AAA", "ZZZ")
        assert actual_count == 2

    def test_count_2(self):
        test_data = "LLR\n" \
                    "\n" \
                    "AAA = (BBB, BBB)\n" \
                    "BBB = (AAA, ZZZ)\n" \
                    "ZZZ = (ZZZ, ZZZ)"

        evaluator = MapEvaluator(test_data.splitlines(keepends=False))
        actual_count = evaluator.count_way_to_finish("AAA", "ZZZ")
        assert actual_count == 6

    def test_part_1(self):  # For part 1 test
        with open("./test_data.txt", "r") as file:
            lines = file.read().splitlines(keepends=False)

        evaluator = MapEvaluator(lines)
        actual_count = evaluator.count_way_to_finish("AAA", "ZZZ")
        print("Count:", actual_count)
        assert actual_count == 16697

