from machine_part_evaluator import PartEvaluator


class TestPart1:
    part_1_test_data = \
        "467..114..\n" \
        "...*......\n" \
        "..35..633.\n" \
        "......#...\n" \
        "617*......\n" \
        ".....+.58.\n" \
        "..592.....\n" \
        "......755.\n" \
        "...$.*....\n" \
        ".664.598.."

    def test_evaluate_part_numbers(self):
        unexpected_results = {114, 58}
        evaluator = PartEvaluator(self.part_1_test_data)
        parts = evaluator.evaluate_parts()
        assert unexpected_results not in parts

    def test_part_sum(self):
        evaluator = PartEvaluator(self.part_1_test_data)
        parts = evaluator.evaluate_parts()
        assert sum(parts) == 4361

    def test_custom_part_numbers(self):
        test_data = "123....456\n"\
                    ".........$\n"\
                    "984....123\n"\
                    "321%......"
        expected_data = {456, 123, 984, 321}
        evaluator = PartEvaluator(test_data)
        parts = evaluator.evaluate_parts()
        assert parts == expected_data

    def test_part_sum_test_data(self):  # For part 1 test
        with open("./test_data.txt", "r") as file:
            lines = file.read()

        evaluator = PartEvaluator(lines)
        parts = evaluator.evaluate_parts()
        print("Part_sum:", sum(parts))
        assert sum(parts) not in (338464, 302629)
