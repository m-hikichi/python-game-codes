from enum import Enum, unique
import random
import numpy as np


class Dungeon:
    MIN_ROOM_WIDTH = 3
    MIN_ROOM_HEIGHT = 3
    ROOM_MARGIN = 1

    class Area(Enum):
        WALL = "■"
        ROOM = " "
        LOAD = "X"

    def __init__(self, dungeon_width, dungeon_height):
        self.__dungeon_width = dungeon_width
        self.__dungeon_height = dungeon_height

        self.__dungeon_map = np.full((self.__dungeon_height, self.__dungeon_width), Dungeon.Area.WALL)
        self.__generate_dungeon()

    def __str__(self) -> str:
        dungeon_representation = ""
        for rows in self.__dungeon_map:
            for area in rows:
                dungeon_representation += area.value
            dungeon_representation += "\n"
        return dungeon_representation

    def __generate_dungeon(self):
        class Node:
            def __init__(self):
                self.left_node = None
                self.right_node = None
                self.boundary_line = None
                self.split_direction = None
                self.sub_map = None

        class BinaryTree:
            def __init__(self):
                self.root = None

            @staticmethod
            def get_leaf_node(node):
                if node.left_node is not None:
                    yield from BinaryTree.get_leaf_node(node.left_node)
                if node.right_node is not None:
                    yield from BinaryTree.get_leaf_node(node.right_node)
                if node.left_node is None and node.right_node is None:
                    yield node

            @staticmethod
            def get_internal_node(node):
                if node.left_node is not None:
                    yield from BinaryTree.get_internal_node(node.left_node)
                if node.right_node is not None:
                    yield from BinaryTree.get_internal_node(node.right_node)
                if node.left_node is not None or node.right_node is not None:
                    yield node

        @unique
        class SplitDirection(Enum):
            HORIZON = "Horizon"
            VERTICAL = "Vertical"

        def split_map(sub_map):
            split_directions = []
            sub_map_height, sub_map_width = sub_map.shape
            if sub_map_width > (Dungeon.MIN_ROOM_WIDTH+(Dungeon.ROOM_MARGIN*2))*2+1:
                split_directions.append(SplitDirection.HORIZON)
            if sub_map_height > (Dungeon.MIN_ROOM_HEIGHT+(Dungeon.ROOM_MARGIN*2))*2+1:
                split_directions.append(SplitDirection.VERTICAL)

            node = Node()
            node.sub_map = sub_map

            if len(split_directions) == 0:
                return node

            split_direction = random.choice(split_directions)
            if split_direction == SplitDirection.HORIZON:
                split_x = random.randint(Dungeon.MIN_ROOM_WIDTH+(Dungeon.ROOM_MARGIN*2)+1, sub_map_width-(Dungeon.MIN_ROOM_WIDTH+(Dungeon.ROOM_MARGIN*2)+1))
                node.boundary_line = split_x
                node.split_direction = split_direction
                node.left_node = split_map(sub_map[:, 0:split_x])
                node.right_node = split_map(sub_map[:, split_x+1:sub_map_width])
                return node
            if split_direction == SplitDirection.VERTICAL:
                split_y = random.randint(Dungeon.MIN_ROOM_HEIGHT+(Dungeon.ROOM_MARGIN*2)+1, sub_map_height-(Dungeon.MIN_ROOM_HEIGHT+(Dungeon.ROOM_MARGIN*2)+1))
                node.boundary_line = split_y
                node.split_direction = split_direction
                node.left_node = split_map(sub_map[0:split_y, :])
                node.right_node = split_map(sub_map[split_y+1:sub_map_height, :])
                return node

        def create_room(sub_map):
            sub_map_height, sub_map_width = sub_map.shape

            if Dungeon.MIN_ROOM_WIDTH+(Dungeon.ROOM_MARGIN*2) > sub_map_width or Dungeon.MIN_ROOM_HEIGHT+(Dungeon.ROOM_MARGIN*2) > sub_map_height:
                return

            room_width = random.randint(Dungeon.MIN_ROOM_WIDTH, sub_map_width-(Dungeon.ROOM_MARGIN*2))
            room_height = random.randint(Dungeon.MIN_ROOM_HEIGHT, sub_map_height-(Dungeon.ROOM_MARGIN*2))
            room_left_upper_x = random.randint(0+Dungeon.ROOM_MARGIN, sub_map_width-(room_width+Dungeon.ROOM_MARGIN))
            room_left_upper_y = random.randint(0+Dungeon.ROOM_MARGIN, sub_map_height-(room_height+Dungeon.ROOM_MARGIN))

            sub_map[room_left_upper_y:room_left_upper_y+room_height, room_left_upper_x:room_left_upper_x+room_width] = Dungeon.Area.ROOM

        def create_load(sub_binary_tree_map):
            left_node = list(BinaryTree.get_leaf_node(sub_binary_tree_map.left_node))[-1]
            left_node_map_x = np.where(left_node.sub_map==Dungeon.Area.ROOM)[1][-1]
            left_node_map_y = np.where(left_node.sub_map==Dungeon.Area.ROOM)[0][-1]
            left_node_sub_map_height, left_node_sub_map_width = left_node.sub_map.shape
            if sub_binary_tree_map.split_direction == SplitDirection.HORIZON:
                left_node.sub_map[left_node_map_y, left_node_map_x:left_node_sub_map_width] = Dungeon.Area.LOAD
            if sub_binary_tree_map.split_direction == SplitDirection.VERTICAL:
                left_node.sub_map[left_node_map_y:left_node_sub_map_height, left_node_map_x] = Dungeon.Area.LOAD

            right_node = list(BinaryTree.get_leaf_node(sub_binary_tree_map.right_node))[0]
            right_node_map_x = np.where(right_node.sub_map==Dungeon.Area.ROOM)[1][0]
            right_node_map_y = np.where(right_node.sub_map==Dungeon.Area.ROOM)[0][0]
            right_node_sub_map_height, right_node_sub_map_width = right_node.sub_map.shape
            if sub_binary_tree_map.split_direction == SplitDirection.HORIZON:
                right_node.sub_map[right_node_map_y, 0:right_node_map_x+1] = Dungeon.Area.LOAD
            if sub_binary_tree_map.split_direction == SplitDirection.VERTICAL:
                right_node.sub_map[0:right_node_map_y+1, right_node_map_x] = Dungeon.Area.LOAD

            if sub_binary_tree_map.split_direction == SplitDirection.HORIZON:
                (top, bottom) = tuple(sorted(set(np.where(sub_binary_tree_map.sub_map==Dungeon.Area.LOAD)[0])))
                sub_binary_tree_map.sub_map[top:bottom+1, sub_binary_tree_map.boundary_line] = Dungeon.Area.LOAD
            if sub_binary_tree_map.split_direction == SplitDirection.VERTICAL:
                (left, right) = tuple(sorted(set(np.where(sub_binary_tree_map.sub_map==Dungeon.Area.LOAD)[1])))
                sub_binary_tree_map.sub_map[sub_binary_tree_map.boundary_line, left:right+1] = Dungeon.Area.LOAD
            sub_binary_tree_map.sub_map[sub_binary_tree_map.sub_map==Dungeon.Area.LOAD] = Dungeon.Area.ROOM

        binary_tree_map = BinaryTree()
        binary_tree_map.root = split_map(self.__dungeon_map)
        for node in BinaryTree.get_leaf_node(binary_tree_map.root):
            create_room(node.sub_map)
        for node in BinaryTree.get_internal_node(binary_tree_map.root):
            create_load(node)
