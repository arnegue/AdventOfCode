import re
from dataclasses import dataclass


def get_numbers_from_line(line):
    numbers = re.findall(r'\d+', line)
    return [int(number) for number in numbers]


@dataclass
class Race:
    id: int
    time: int
    record_distance: int


class ToyBoat(object):
    def __init__(self):
        self.speed_mm_per_ms = 0

    def push_button(self, hold_time_ms):
        self.speed_mm_per_ms += hold_time_ms

    def get_distance(self, drive_time_ms: int):
        return self.speed_mm_per_ms * drive_time_ms


class SpeedEvaluator(object):
    def __init__(self, data):
        time_line = get_numbers_from_line(data[0])
        distance_record_line = get_numbers_from_line(data[1])

        self.race_list = []
        for i in range(len(time_line)):
            new_race = Race(id=i, time=time_line[i], record_distance=distance_record_line[i])
            self.race_list.append(new_race)

    def generate_solutions_to_beat_record(self, race_id):
        solutions = []
        race = self.race_list[race_id]

        for i in range(race.time):
            temp_toy_boat = ToyBoat()
            temp_toy_boat.push_button(hold_time_ms=i)
            time_left = race.time - i
            if time_left > 0:
                moved_distance_in_race = temp_toy_boat.get_distance(drive_time_ms=time_left)
                if moved_distance_in_race > race.record_distance:
                    solutions.append(i)
        return solutions


