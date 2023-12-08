

class Position(object):
    def __init__(self, name):
        self.name = name
        self.l_position = None
        self.r_position = None

    def set_l_position(self, l_position):
        self.l_position = l_position

    def set_r_position(self, r_position):
        self.r_position = r_position


class MapEvaluator(object):
    def __init__(self, map_str: [str]):
        self.position_dict: {Position} = {}
        self.instructions = map_str[0]
        self._i_index = 0
        self.create_positions(map_str[2:])

    def create_positions(self, map_str):
        for line in map_str:
            self.create_position(line)
        for line in map_str:
            self.create_chains(line)

    def create_position(self, line_str: str):
        name, rest = line_str.split(" = ")
        if name in self.position_dict:
            # Shouldn't come here I guess
            return self.position_dict[name]

        new_pos = Position(name)
        self.position_dict[name] = new_pos

    def create_chains(self, line_str: str):
        name, rest = line_str.split(" = ")
        rest = rest.replace("(", "")
        rest = rest.replace(")", "")
        l_pos_str, r_pos_str = rest.split(", ")
        own_position = self.position_dict[name]

        if l_pos_str == name:
            own_position.set_l_position(own_position)
        elif l_pos_str in self.position_dict:
            l_pos = self.position_dict[l_pos_str]
            own_position.set_l_position(l_pos)
        else:
            raise Exception("Shouldn't come here")

        if r_pos_str == name:
            own_position.set_r_position(own_position)
        elif r_pos_str in self.position_dict:
            r_pos = self.position_dict[r_pos_str]
            own_position.set_r_position(r_pos)
        else:
            raise Exception("Shouldn't come here")

    def count_way_to_finish(self, start, finish):
        temp = self.position_dict[start]
        finish = self.position_dict[finish]

        step_counter = 0
        while temp != finish:
            instruction = self._get_next_instruction()
            if instruction == "R":
                temp = temp.r_position
            else:  # "L"
                temp = temp.l_position
            step_counter += 1
        return step_counter

    def _get_next_instruction(self):
        temp_idx = self._i_index
        self._i_index += 1
        self._i_index %= len(self.instructions)

        return self.instructions[temp_idx]
