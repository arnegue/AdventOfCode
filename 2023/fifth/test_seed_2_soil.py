import pytest

from seed_2_soil_evaluator import MapParser


class TestPart1:
    test_data = "seed-to-soil map:\n" \
                "50 98 2\n" \
                "52 50 48"

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

    def test_values(self):
        map_parser = MapParser(self.test_data)
        result_map = self.generate_result_map()

        assert len(map_parser.map) == len(result_map)
        for i in range(len(map_parser.map)):
            assert map_parser.map[i] == result_map[i], f"index {i} is not equal"
        assert map_parser.map == result_map

    @pytest.mark.parametrize("seed_number, soil_number", [[79, 81],
                                                          [14, 14],
                                                          [55, 57],
                                                          [13, 13]])
    def test_specific_values(self, seed_number, soil_number):
        map_parser = MapParser(self.test_data)
        assert map_parser.map[seed_number] == soil_number
