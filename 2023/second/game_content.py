import enum
import re


def get_number_from_string(number_string: str) -> int:
    numbers = re.findall(r'\d+', number_string)
    if 0 < len(numbers) > 1:
        raise Exception(f"Did not find 1 number in \"{number_string}")
    return int(numbers[0])


class Color(enum.Enum):
    red = enum.auto()
    blue = enum.auto()
    green = enum.auto()

    @classmethod
    def get_color_from_string(cls, color_string):
        for color in cls:
            if color.name in color_string:
                return color
        raise ValueError(f"Did not find any color in string \"{color_string}\"")


class Cube(object):
    def __init__(self, color: Color):
        self.color = color

    def __eq__(self, other):
        if isinstance(other, self.__class__):
            return self.color == other.color
        else:
            return False


class SetCubes(object):
    def __init__(self, amount_cube_colors: list[tuple[int, Cube]]):
        self.amount_cube_colors = amount_cube_colors

    def get_set(self, color):
        for cube_set in self.amount_cube_colors:
            if cube_set[1].color == color:
                return cube_set
        return None

    def __eq__(self, other):
        if isinstance(other, self.__class__):
            return self.amount_cube_colors == other.amount_cube_colors
        else:
            return False


class Game(object):
    def __init__(self, game_id: int, list_sets: list[SetCubes]):
        self.game_id = game_id
        self.list_sets = list_sets

    @classmethod
    def parse_string(cls, string):
        # "Game 1: 3 blue, 4 red; 1 red, 2 green, 6 blue; 2 green"
        game_id_string, set_strings = string.split(":")  # ["Game 1", " 3 blue, 4 red; 1 red, 2 green, 6 blue; 2 green"]
        game_id = get_number_from_string(game_id_string)

        set_strings = set_strings.split(";")  # --> [" 3 blue, 4 red", " 1 red, 2 green", " 6 blue; 2 green"]
        list_sets = []
        for set_ in set_strings:
            cube_strings = set_.split(",")  # --> [" 3 blue", " 4 red"]
            list_cubes = []
            for cube_string in cube_strings:
                amount_cubes = get_number_from_string(cube_string)
                cube_color = Color.get_color_from_string(cube_string)
                list_cubes.append((amount_cubes, Cube(cube_color)))
            set_cubes = SetCubes(list_cubes)
            list_sets.append(set_cubes)
        return Game(game_id, list_sets)

    def __eq__(self, other):
        if isinstance(other, self.__class__):
            if self.game_id == other.game_id:
                if len(self.list_sets) == len(other.list_sets):
                    for set_idx, set_ in enumerate(self.list_sets):
                        other_set = other.list_sets[set_idx]
                        if set_ != other_set:
                            return False
                    return True

        return False

    def game_possible(self, possible_cubes: SetCubes) -> bool:
        max_own_colors = dict()
        for color in Color:
            max_color = 0

            for own_set in self.list_sets:
                color_set = own_set.get_set(color)
                if color_set:
                    max_color = max(max_color, color_set[0])

            max_own_colors[color] = max_color

        for color in Color:
            possible_cube = possible_cubes.get_set(color)
            if possible_cube is not None:
                if possible_cube[0] < max_own_colors[color]:
                    return False
        return True

