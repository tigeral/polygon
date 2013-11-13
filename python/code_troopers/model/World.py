from math import *
from TrooperStance import TrooperStance


class World:
    def __init__(self, move_index, width, height, players, troopers, bonuses, cells, cell_visibilities):
        self.move_index = move_index
        self.width = width
        self.height = height
        self.players = players
        self.troopers = troopers
        self.bonuses = bonuses
        self.cells = cells
        self.cell_visibilities = cell_visibilities

    def is_visible(self, max_range,
                   viewer_x, viewer_y, viewer_stance,
                   object_x, object_y, object_stance):
        stance_count = 0

        for enum_key, enum_value in TrooperStance.__dict__.items():
            if not str(enum_key).startswith("__"):
                stance_count += 1

        min_stance_index = min(viewer_stance, object_stance)
        return hypot(object_x - viewer_x, object_y - viewer_y) <= max_range and ord(self.cell_visibilities[
            viewer_x * self.height * self.width * self.height * stance_count
            + viewer_y * self.width * self.height * stance_count
            + object_x * self.height * stance_count
            + object_y * stance_count
            + min_stance_index
        ]) == 1