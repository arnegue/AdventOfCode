import re


class MapParser(object):
    def __init__(self, map_string):
        self.source = ""
        self.destination = ""
        self.map = {}
        for i in range(100):  # Fill with default values
            self.map[i] = i

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
            self.map.update(return_dict)

    @classmethod
    def parse_line(cls, line: str) -> dict:
        numbers = re.findall(r'\d+', line)
        if len(numbers) != 3:
            raise Exception(f"Unexpected line length != 3: {len(numbers)}")

        return_dict = {}

        destination = int(numbers[0])
        source = int(numbers[1])
        range_len = int(numbers[2])

        for i in range(range_len):
            return_dict[source + i] = destination + i
        return return_dict
