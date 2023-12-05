import pytest

from seed_2_soil_evaluator import DataParser, Part2DataParser


class TestPart1:
    test_data = "seeds: 79 14 55 13\n" \
                "\n" \
                "seed-to-soil map:\n" \
                "50 98 2\n" \
                "52 50 48\n" \
                "\n" \
                "soil-to-fertilizer map:\n" \
                "0 15 37\n" \
                "37 52 2\n" \
                "39 0 15\n" \
                "\n" \
                "fertilizer-to-water map:\n" \
                "49 53 8\n" \
                "0 11 42\n" \
                "42 0 7\n" \
                "57 7 4\n" \
                "\n" \
                "water-to-light map:\n" \
                "88 18 7\n" \
                "18 25 70\n" \
                "\n" \
                "light-to-temperature map:\n" \
                "45 77 23\n" \
                "81 45 19\n" \
                "68 64 13\n" \
                "\n" \
                "temperature-to-humidity map:\n" \
                "0 69 1\n" \
                "1 0 69\n" \
                "\n" \
                "humidity-to-location map:\n" \
                "60 56 37\n" \
                "56 93 4"

    @staticmethod
    def generate_result_map():
        result_map = {}
        for i in range(0, 50):
            result_map[i] = i

        for i in range(50, 98):
            result_map[i] = i + 2

        for i in range(98, 100):
            result_map[i] = 50 + (i - 98)

        return result_map

    @pytest.mark.skip("This test doesn't work anymore after optimization")
    def test_values(self):
        data_parser = DataParser(self.test_data)
        map_parser = data_parser.get_map_parser("seed")
        result_map = self.generate_result_map()

        assert len(map_parser._map) == len(result_map)
        for i in range(len(map_parser._map)):
            assert map_parser._map[i] == result_map[i], f"index {i} is not equal"
        assert map_parser._map == result_map

    @pytest.mark.parametrize("seed_number, soil_number", [[79, 81],
                                                          [14, 14],
                                                          [55, 57],
                                                          [13, 13]])
    def test_specific_values(self, seed_number, soil_number):
        data_parser = DataParser(self.test_data)
        map_parser = data_parser.get_map_parser("seed")
        assert map_parser.get_destination_value(seed_number) == soil_number

    @pytest.mark.parametrize("seed_number, location", [[79, 82],
                                                       [14, 43],
                                                       [55, 86],
                                                       [13, 35]])
    def test_source_to_destination(self, seed_number, location):
        data_parser = DataParser(self.test_data)
        result_value = data_parser.get_source_to_destination(source="seed", destination="location", source_value=seed_number)
        assert result_value == location

    def test_lowest_location(self):
        data_parser = DataParser(self.test_data)
        lowest_location = data_parser.get_lowest_location_number()
        assert lowest_location == 35

    def test_lowest_location_part_1(self):  # For part 1 test
        with open("./test_data.txt", "r") as file:
            lines = file.read()

        data_parser = DataParser(lines)
        lowest_location = data_parser.get_lowest_location_number()
        print("Lowest location:", lowest_location)
        assert lowest_location == 403695602


class TestPart2:
    def test_lowest_location(self):
        data_parser = Part2DataParser(TestPart1.test_data)
        lowest_location = data_parser.get_lowest_location_number()
        assert lowest_location == 46

    def test_lowest_location_part_2(self):  # For part 2 test
        with open("./test_data.txt", "r") as file:
            lines = file.read()

        data_parser = Part2DataParser(lines)
        lowest_location = data_parser.get_lowest_location_number()
        print("Lowest location:", lowest_location)

