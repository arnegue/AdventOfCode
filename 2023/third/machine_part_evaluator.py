import re


class PartEvaluator(object):
    def __init__(self, parts: str):
        self.parts = parts

    def evaluate_parts(self):
        parts = list()
        lines = self.parts.splitlines(keepends=False)
        for i in range(len(lines)):
            previous_line = lines[i - 1] if i > 0 else None
            current_line = lines[i]
            next_line = lines[i + 1] if i + 1 < len(lines) else None
            parts += self.get_machine_parts(previous_line, current_line, next_line)
        return parts

    def get_machine_parts(self, previous_line, current_line, next_line) -> list:
        return_list = []
        for match in re.finditer(r'\d+', current_line):
            part_number = int(match.group())
            start_index = match.start()
            end_index = match.end()

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

