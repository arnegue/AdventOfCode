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
        expected_data = [123, 321, 456, 984]
        evaluator = PartEvaluator(test_data)
        parts = evaluator.evaluate_parts()
        parts.sort()
        assert parts == expected_data

    def test_part_sum_test_data(self):  # For part 1 test
        with open("./test_data.txt", "r") as file:
            lines = file.read()

        evaluator = PartEvaluator(lines)
        parts = evaluator.evaluate_parts()
        print("Part_sum:", sum(parts))
        assert sum(parts) not in (338464, 302629)


class TestPart2:
    test_data = "467..114..\n"\
                "...*......\n"\
                "..35..633.\n"\
                "......#...\n"\
                "617*......\n"\
                ".....+.58.\n"\
                "..592.....\n"\
                "......755.\n"\
                "...$.*....\n"\
                ".664.598.."

    def test_gear_ratio(self):
        evaluator = PartEvaluator(self.test_data)
        parts = evaluator.evaluate_gears()
        ratio = evaluator.calculate_gear_ratio(parts)
        assert ratio == 467835

    def test_custom_gear_ratio(self):
        test_data = "123*415.456\n" \
                    "...43......\n" \
                    "...........\n" \
                    "678*129*45.\n" \
                    "...........\n" \
                    "321*321....\n" \
                    "...........\n" \
                    "213*.......\n" \
                    "....76.....\n" \
                    "...........\n" \
                    "678*.......\n" \
                    "....2......\n" \
                    "3*.....*3*9\n" \
                    "...........\n" \
                    "12*34*2.2*2\n" \
                    "...........\n" \
                    "...7.......\n" \
                    "...*.......\n" \
                    "...8.......\n" \
                    "...*.......\n" \
                    "...9.......\n" \
                    "6..........\n" \
                    "*..........\n" \
                    "5..........\n" \
                    "*..........\n"
        evaluator = PartEvaluator(test_data)
        parts = evaluator.evaluate_gears()
        actual_ratio = evaluator.calculate_gear_ratio(parts)
        assert actual_ratio == (678 * 129) + (129 * 45) + (321 * 321) + (213 * 76) + (678 * 2) + (3 * 9) + (12 * 34) + (34 * 2) + (2 * 2) + (7 * 8) + (8 * 9) + (6 * 5)

    def test_part_sum_test_data(self):  # For part 2 test
        with open("./test_data.txt", "r") as file:
            lines = file.read()

        evaluator = PartEvaluator(lines)
        parts = evaluator.evaluate_gears()
        actual_ratio = evaluator.calculate_gear_ratio(parts)
        print("GearRation:", actual_ratio)
