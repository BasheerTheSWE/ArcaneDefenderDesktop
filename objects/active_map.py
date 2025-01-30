#
# Created by Basheer Abdulmalik
#
# Thu, 30-Jan-25
#

from dataclasses import dataclass

@dataclass
class ActiveMap:
    """
    The active map object contains only the visible tiles from a specific tile map.

    * Used to reduce the amount of required computations with larger tile maps.

    Parameters:
    -----------
    tiles : a nested list of integers representing the visible tiles.
    starting_row_index : the index of the first visible row from the provided tile map.
    starting_column_index: the index of the first visible column from the provided tile map.
    """

    tiles: list[list[int]]
    starting_row_index: int
    starting_column_index: int
