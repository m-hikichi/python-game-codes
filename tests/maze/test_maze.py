import pytest
from src.maze.maze import Maze, MazeError


@pytest.mark.parametrize(
    "width, height",
    [
        (5, 5),
        (7, 7),
    ],
)
def test_init_maze(width, height):
    # GIVEN

    # WHEN
    maze = Maze(width, height)

    # THEN
    assert maze.get_size() == (width, height)
    assert maze.get_cell(1, 1) == Maze.Cell.START


@pytest.mark.parametrize(
    "width, height",
    [
        (3, 3),
        (4, 4),
    ],
)
def test_init_maze_small(width, height):
    # GIVEN

    # WHEN
    with pytest.raises(MazeError) as e:
        maze = Maze(width, height)

    # THEN
    assert str(e.value) == "Maze size is too small."


@pytest.mark.parametrize(
    "width, height",
    [
        (6, 6),
        (8, 8),
    ],
)
def test_init_maze_even(width, height):
    # GIVEN

    # WHEN
    with pytest.raises(MazeError) as e:
        maze = Maze(width, height)

    # THEN
    assert str(e.value) == "Maze size must be specified in odd numbers."
