from secrets import choice
from collections import deque

UNIQUE_COORDINATES = set()
LAST5_LAT = deque([], maxlen=5)
LAST5_LON = deque([], maxlen=5)
COORD_ACCURACY = 0.0001


def need_to_change(lat: str, lon: str) -> bool:
    lat_f, lon_f = float(lat), float(lon)

    same_lat = any((prev for prev in LAST5_LAT
                    if abs(lat_f-float(prev)) < COORD_ACCURACY))

    same_lon = any((prev for prev in LAST5_LON
                    if abs(lon_f-float(prev)) < COORD_ACCURACY))

    return (same_lat and same_lon) or (lat, lon) in UNIQUE_COORDINATES


def change_coord_or_not(coord: str) -> str:
    # make mantissa's l ength 6 and turn it to int
    head, tail = coord.split('.')
    tail = int(f"{tail:0<6}"[:6])
    tail = abs(tail + choice((-100, 0, 100)))

    return f"{head}.{tail:0>6}"


def make_unique_coordinates(lat: str, lon: str) -> tuple[str, str]:

    while need_to_change(lat, lon):
        lat = change_coord_or_not(lat)
        lon = change_coord_or_not(lon)

    LAST5_LAT.append(lat)
    LAST5_LON.append(lon)
    UNIQUE_COORDINATES.add((lat, lon))
    return (lat, lon)
