import re


class PartEvaluator(object):
    def __init__(self, parts: str):
        self.parts = parts

    def evaluate_parts(self) -> list:
        parts = list()
        lines = self.parts.splitlines(keepends=False)
        for i in range(len(lines)):
            previous_line = lines[i - 1] if i > 0 else None
            current_line = lines[i]
            next_line = lines[i + 1] if i + 1 < len(lines) else None
            parts += self.get_machine_parts(previous_line, current_line, next_line)
        return parts

    @classmethod
    def get_numbers_from_line(cls, line: str):
        number_tuples = []
        for match in re.finditer(r'\d+', line):
            part_number = int(match.group())
            start_index = match.start()
            end_index = match.end()
            number_tuples.append((part_number, start_index, end_index))
        return number_tuples

    def get_machine_parts(self, previous_line, current_line, next_line) -> list:
        return_list = []
        for part_number, start_index, end_index in self.get_numbers_from_line(current_line):
            in_line = False
            if previous_line is not None:
                in_line = self.sing_in_line(previous_line, start_index, end_index)
            if not in_line:
                in_line = self.sing_in_line(current_line, start_index, end_index)
            if not in_line and next_line is not None:
                in_line = self.sing_in_line(next_line, start_index, end_index)
            if in_line:
                return_list.append(part_number)

        return return_list

    @classmethod
    def sing_in_line(cls, line, start_index, end_index) -> bool:
        start_index = start_index - 1 if start_index > 0 else start_index
        end_index = end_index + 1 if end_index + 1 < len(line) else end_index
        test_string = line[start_index:end_index]
        for char in test_string:
            if not char.isdigit() and char != ".":
                return True
        return False

    def evaluate_gears(self) -> list[tuple]:
        gear_tuples = list()
        lines = self.parts.splitlines(keepends=False)
        for i in range(len(lines)):
            previous_line = lines[i - 1] if i > 0 else None
            current_line = lines[i]
            next_line = lines[i + 1] if i + 1 < len(lines) else None
            gear_tuples += self.get_gear_tuples(previous_line, current_line, next_line)
        return gear_tuples

    def get_gear_tuples(self, previous_line, current_line, next_line):
        return_list = []
        for match in re.finditer(r'\*', current_line):
            gear_index = match.start()

            all_parts = self.get_matching_part_gear_from_line(gear_index, previous_line)
            all_parts += self.get_matching_part_gear_from_line(gear_index, current_line)
            all_parts += self.get_matching_part_gear_from_line(gear_index, next_line)

            if len(all_parts) == 2:
                return_list.append(all_parts)
        return return_list

    def get_matching_part_gear_from_line(self, gear_index, line):
        part_gears = []
        if line is not None:
            gear_start_index = gear_index - 1 if gear_index > 0 else gear_index
            gear_end_index = gear_index + 1 if gear_index + 1 < len(line) else gear_index

            for part_number, part_start_index, part_end_index in self.get_numbers_from_line(line):
                for gear_temp_idx in range(gear_start_index, gear_end_index + 1):  # TODO boundaries may not be TRUE
                    if gear_temp_idx in range(part_start_index, part_end_index):
                        part_gears.append(part_number)
                        break
        return part_gears

    @classmethod
    def calculate_gear_ratio(cls, gear_tuples):
        gear_ratio = 0
        for part_1, part_2 in gear_tuples:
            gear_ratio += part_1 * part_2
        return gear_ratio
