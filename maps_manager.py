#
# Created by Basheer Abdulmalik
#
# Wed, 29-Jan-25
#

import os
import pygame
from enum import Enum
from objects.enums.map_type import MapType
from objects.active_map import ActiveMap

class MapsManager:
    """
    The MapsManager class handles all related logic to the game's tile maps.

    * This class doesn't have to be initialized becuase it only contains static methods.
    """

    @staticmethod
    def load_map(mapType: Enum) -> list[list[int]]:
        """
        Loads a specific tile map form the project's directory.

        Parameters:
        -----------
        mapType : Enum conforming to `str` that holds the desired map's file name.

        Returns:
        --------
        A list of rows of `int` representing the content of the file map.
        * Note that a row of `-1` is considered an empty tile, or the sky. Other numbers represent the ids of specific tiles.
        """

        fileName = mapType.value
        file = open(os.path.join("Media", "Maps", fileName))
        file_content = file.read().strip().split("\n")

        return [[int(tile) for tile in row.split(",")] for row in file_content]

    @staticmethod
    def get_active_map(tile_map: list[list[int]], center_point: tuple[float, float], screen_size: tuple[float, float]) -> ActiveMap:
        """
        This method will get you the active/visible tiles on the provided screen size relative to a specific center point (player).

        * Useful to reduce required heavy computation needed for larger maps.
        * Rendering only the active tiles will make the size of the tile map irrelevent in terms of computation.
        * This method asssumes the tile size is 32x32 pixels.

        Parameters:
        -----------
        tile_map : list[list[int]] -> representing the full tile map from which the active tiles will be extracted.
        center_point: tuple[float, float] -> the players position or the camera position. i.e. the anchor point for the active map.
        screen_size: tuple[float, float] -> the width x height in pixels for the current screen size to determine the size of our active map.

        Returns:
        --------
        ActiveMap object which contains the visible tile_map, starting column index, and starting row index.
        """

        columns_count = len(tile_map[0])
        rows_count = len(tile_map)
        
        # Since the tile size will always be 32 the number of visible tiles can be calculated easily.
        # Visible tiles can be divided into rows and columns.
        # The `+4` is added just to be secure and avoid possible gaps at the edges.
        # The visible tiles count will always be `4` more than what's needed.
        visible_columns_count = screen_size[0] // 32 + 8
        visible_rows_count = screen_size[1] // 32 + 8

        center_point_column_id = center_point[0] // 32
        center_point_row_id = center_point[1] // 32

        # Calculating the id of the first and last columns in the visible map relative to the actual map.
        # For example the 100th column on the actual map could be the first visible column from the left side of the screen.
        starting_column_index = center_point_column_id - (visible_columns_count // 2)
        ending_column_index = center_point_column_id + (visible_columns_count // 2)

        # Setting bounds for the columns and making sure the visible columns aren't starting before 0 or ending after the actual columns count.
        # Making sure the id of the first column isn't a negative number, otherwise the code will break.
        if starting_column_index < 0:
            starting_column_index = 0

        if ending_column_index > columns_count - 1:
            ending_column_index = columns_count - 1602

        # Calculating the id of the first and last rows in the visible map relative to the actual map.
        starting_row_index = center_point_row_id - (visible_rows_count // 2)
        ending_row_index = center_point_row_id + (visible_rows_count // 2)

        # Setting the bounds for our rows to avoid getting a fatal error.
        if starting_row_index < 0:
            starting_row_index = 0

        if ending_row_index > rows_count - 1:
            ending_row_index = rows_count - 1

        # Getting the visible map from slicing the visible tiles out of the actual map.
        active_tiles = [row[starting_column_index:ending_column_index] for row in tile_map[starting_row_index:ending_row_index]]
        
        return ActiveMap(active_tiles, starting_row_index, starting_column_index)

    @staticmethod
    def get_hitlist(player_rect: pygame.Rect, tiles_rects: [pygame.Rect]) -> list[pygame.Rect]:
        return [rect for rect in tiles_rects if player_rect.colliderect(rect)]
