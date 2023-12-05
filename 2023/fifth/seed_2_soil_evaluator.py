import re
from collections import OrderedDict
from dataclasses import dataclass


def get_numbers_from_line(line):
    numbers = re.findall(r'\d+', line)
    return [int(number) for number in numbers]


class MapParser(object):
    def __init__(self, map_string):
        self.source = ""
        self.destination = ""
        self._map = OrderedDict()
        self.parse_string(map_string)

    def parse_string(self, map_string: str):
        map_string_lines = map_string.splitlines(keepends=False)
        self.parse_header(map_string_lines[0])
        self.parse_map(map_string_lines[1:])

    def parse_header(self, header: str):
        s2d = header.replace(" map:", "")
        self.source, self.destination = s2d.split("-to-")

    def parse_map(self, map_string: [str]):
        for line in map_string:
            return_dict = self.parse_line(line)
            self._map.update(return_dict)

    def get_destination_value(self, source):
        if source in self._map:
            destination, range_len = self._map[source]
            return destination
        else:
            # Get previous value in map
            previous_key = -1
            sorted_items = sorted(self._map.keys())  # Lets hope this isnt that bad
            for key in sorted_items:
                if key > source:
                    break
                previous_key = key

            if previous_key >= 0:
                destination, range_len = self._map[previous_key]
                if previous_key <= source < previous_key + range_len:
                    difference = source - previous_key
                    return destination + difference

            return source

            pass  # Todo get lowest and look if it is in range, else, return source

    @classmethod
    def parse_line(cls, line: str) -> dict:
        numbers = get_numbers_from_line(line)
        if len(numbers) != 3:
            raise Exception(f"Unexpected line length != 3: {len(numbers)}")

        return_dict = OrderedDict()

        destination = numbers[0]
        source = numbers[1]
        range_len = numbers[2]

        return_dict[source] = (destination, range_len)
        return return_dict


class DataParser(object):
    def __init__(self, data: str):
        self.searched_seeds = []
        self.map_parsers = {}
        self.parse_data(data)

    def parse_data(self, data: str):
        data = data.split("\n\n")
        self.searched_seeds = get_numbers_from_line(data[0])
        self.parse_map_parsers(data[1:])

    def parse_map_parsers(self, data):
        for data_ in data:
            new_map_parser = MapParser(data_)
            self.map_parsers[new_map_parser.source] = new_map_parser

    def get_map_parser(self, source_name) -> MapParser:
        return self.map_parsers[source_name]

    def get_source_to_destination(self, source: str, destination: str, source_value: int):
        destination_found = False
        temp_source_value = source_value
        temp_source = source
        while not destination_found:
            map_parser = self.get_map_parser(temp_source)
            temp_source_value = map_parser.get_destination_value(temp_source_value)
            temp_source = map_parser.destination
            print(temp_source, temp_source_value)
            if map_parser.destination == destination:
                destination_found = True
        return temp_source_value

    def get_lowest_location_number(self):
        location_numbers = []
        for seed_number in self.searched_seeds:
            location_number = self.get_source_to_destination(source="seed", destination="location", source_value=seed_number)
            location_numbers.append(location_number)
        return min(location_numbers)
