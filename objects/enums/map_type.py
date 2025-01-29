#
# Created by Basheer Abdulmalik
#
# Wed, 29-Jan-25
#

from enum import Enum

class MapType(Enum):
    """
    This enum holds the file names of all availabel maps on the game.

    Sample Usecase:
    ---------------

    mapType = MapType.test
    file = open(os.path.join("Media", "Maps", mapType.value))
    """

    test = "testMap.csv"
