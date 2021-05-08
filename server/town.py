from lib import Point

TOWN_START_X = 10
TOWN_START_Y = 10
TOWN_END_X = 200
TOWN_END_Y = 200


def isInTown(mettingPoint: Point, gradient: Point) -> bool:
    location = Point(mettingPoint.x - gradient.x, mettingPoint.y - gradient.y)
    return TOWN_END_X > location.x >= TOWN_START_X and TOWN_END_Y > location.y >= TOWN_START_Y
