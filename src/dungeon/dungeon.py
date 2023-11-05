from enum import Enum
import random
import numpy as np


class Dungeon:
    MIN_ROOM_WIDTH = 3
    MIN_ROOM_HEIGHT = 3
    ROOM_MARGIN = 1

    class Area(Enum):
        WALL = "■"
        ROOM = " "
        LOAD = " "

    def __init__(self, dungeon_width, dungeon_height):
        self.__dungeon_width = dungeon_width
        self.__dungeon_height = dungeon_height

        self.__dungeon_map = np.full((self.__dungeon_height, self.__dungeon_width), Dungeon.Area.WALL)
        self.__create_rooms()

    def __str__(self) -> str:
        dungeon_representation = ""
        for rows in self.__dungeon_map:
            for area in rows:
                dungeon_representation += area.value
            dungeon_representation += "\n"
        return dungeon_representation

    def __create_rooms(self):
        def split_map(sub_map):
            sub_map_height, sub_map_width = sub_map.shape

            is_horizon_split = random.choice([True, False])
            if is_horizon_split:
                if sub_map_width > (Dungeon.MIN_ROOM_WIDTH+(Dungeon.ROOM_MARGIN*2))*2:
                    split_x = random.randint(Dungeon.MIN_ROOM_WIDTH+(Dungeon.ROOM_MARGIN*2), sub_map_width-Dungeon.MIN_ROOM_WIDTH+(Dungeon.ROOM_MARGIN*2))
                    yield from split_map(sub_map[:, 0:split_x])
                    yield from split_map(sub_map[:, split_x+1:sub_map_width])
                else:
                    yield sub_map
            else:
                if sub_map_height > (Dungeon.MIN_ROOM_HEIGHT+(Dungeon.ROOM_MARGIN*2))*2:
                    split_y = random.randint(Dungeon.MIN_ROOM_HEIGHT+(Dungeon.ROOM_MARGIN*2), sub_map_height-Dungeon.MIN_ROOM_HEIGHT+(Dungeon.ROOM_MARGIN*2))
                    yield from split_map(sub_map[0:split_y, :])
                    yield from split_map(sub_map[split_y+1:sub_map_height, :])
                else:
                    yield sub_map

        def create_room(sub_map):
            sub_map_height, sub_map_width = sub_map.shape

            if Dungeon.MIN_ROOM_WIDTH+(Dungeon.ROOM_MARGIN*2) > sub_map_width or Dungeon.MIN_ROOM_HEIGHT+(Dungeon.ROOM_MARGIN*2) > sub_map_height:
                return

            room_width = random.randint(Dungeon.MIN_ROOM_WIDTH, sub_map_width-(Dungeon.ROOM_MARGIN*2))
            room_height = random.randint(Dungeon.MIN_ROOM_WIDTH, sub_map_height-(Dungeon.ROOM_MARGIN*2))
            room_left_upper_x = random.randint(0+Dungeon.ROOM_MARGIN, sub_map_width-(room_width+Dungeon.ROOM_MARGIN))
            room_left_upper_y = random.randint(0+Dungeon.ROOM_MARGIN, sub_map_height-(room_height+Dungeon.ROOM_MARGIN))

            sub_map[room_left_upper_y:room_left_upper_y+room_height, room_left_upper_x:room_left_upper_x+room_width] = Dungeon.Area.ROOM

        sub_maps = split_map(self.__dungeon_map)
        for sub_map in sub_maps:
            create_room(sub_map)
