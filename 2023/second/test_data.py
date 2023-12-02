import pytest

from game_content import Game, Color, SetCubes, Cube


class TestPart1(object):
    test_data = "Game 1: 3 blue, 4 red; 1 red, 2 green, 6 blue; 2 green\n" \
                "Game 2: 1 blue, 2 green; 3 green, 4 blue, 1 red; 1 green, 1 blue\n" \
                "Game 3: 8 green, 6 blue, 20 red; 5 blue, 4 red, 13 green; 5 green, 1 red\n" \
                "Game 4: 1 green, 3 red, 6 blue; 3 green, 6 red; 3 green, 15 blue, 14 red\n" \
                "Game 5: 6 red, 1 blue, 3 green; 2 blue, 1 red, 2 green\n"
    split_data = test_data.splitlines(keepends=False)

    @classmethod
    @pytest.mark.parametrize(("test_line", "expected_results"), ([split_data[0], Game(1, [SetCubes([(3, Cube(Color.blue)), (4, Cube(Color.red))]),
                                                                                          SetCubes([(1, Cube(Color.red)), (2, Cube(Color.green)), (6, Cube(Color.blue))]),
                                                                                          SetCubes([(2, Cube(Color.green))]),
                                                                                          ])],
                                                                 [split_data[1], Game(2, [SetCubes([(1, Cube(Color.blue)), (2, Cube(Color.green))]),
                                                                                          SetCubes([(3, Cube(Color.green)), (4, Cube(Color.blue)), (1, Cube(Color.red))]),
                                                                                          SetCubes([(1, Cube(Color.green)), (1, Cube(Color.blue))]),
                                                                                          ])],
                                                                 [split_data[2], Game(3, [SetCubes([(8, Cube(Color.green)), (6, Cube(Color.blue)), (20, Cube(Color.red))]),
                                                                                          SetCubes([(5, Cube(Color.blue)), (4, Cube(Color.red)), (13, Cube(Color.green))]),
                                                                                          SetCubes([(5, Cube(Color.green)), (1, Cube(Color.red))]),
                                                                                          ])],
                                                                 [split_data[3], Game(4, [SetCubes([(1, Cube(Color.green)), (3, Cube(Color.red)), (6, Cube(Color.blue))]),
                                                                                          SetCubes([(3, Cube(Color.green)), (6, Cube(Color.red))]),
                                                                                          SetCubes([(3, Cube(Color.green)), (15, Cube(Color.blue)), (14, Cube(Color.red))]),
                                                                                          ])],
                                                                 [split_data[4], Game(5, [SetCubes([(6, Cube(Color.red)), (1, Cube(Color.blue)), (3, Cube(Color.green))]),
                                                                                          SetCubes([(2, Cube(Color.blue)), (1, Cube(Color.red)), (2, Cube(Color.green))])
                                                                                          ])]))
    def test_parse_string(cls, test_line, expected_results):
        test_game = Game.parse_string(test_line)

        assert test_game == expected_results

    @pytest.mark.parametrize("test_line, expected_result", [[split_data[0], True],
                                                            [split_data[1], True],
                                                            [split_data[2], False],
                                                            [split_data[3], False],
                                                            [split_data[4], True]])
    def test_possible_game(self, test_line, expected_result):
        set_cubes = SetCubes([(12, Cube(Color.red)), (13, Cube(Color.green)), (14, Cube(Color.blue))])
        test_game = Game.parse_string(test_line)
        assert expected_result == test_game.game_possible(set_cubes)

    def test_other_games_possible(self):  # For part 1 test
        set_cubes = SetCubes([(12, Cube(Color.red)), (13, Cube(Color.green)), (14, Cube(Color.blue))])

        with open("./test_data.txt", "r") as file:
            lines = file.readlines()

        possible_game_sum = 0
        for line in lines:
            test_game = Game.parse_string(line)
            if test_game.game_possible(set_cubes):
                possible_game_sum += test_game.game_id
        print("Possible games_no:", possible_game_sum)
