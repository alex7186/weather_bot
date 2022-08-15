class CantGetCoordinates(Exception):
    """Program can't get current GPS coordinates"""

    pass


class ApiServiceError(Exception):
    """Program can't connect to API"""

    pass
