from typing import NamedTuple
from subprocess import Popen, PIPE

from modules.weather_2line.exceptions import CantGetCoordinates


class Coordinates(NamedTuple):
    latitude: float
    longitude: float


def get_coords() -> Coordinates:
    "returns cirrent coords from whereami util"

    def execute_whereami() -> str:
        """returns output like (17.8, 122.4)
        from program 55° 39' 55" N,37° 28' 39" E"""
        process = Popen(["whereami"], stdout=PIPE)
        output, err = process.communicate()

        exit_code = process.wait()

        if err is not None or exit_code != 0:
            raise CantGetCoordinates

        return output.split("[K")[-1].split("\n")[0]

    def clear_whereami_output(whereami_output: str) -> Coordinates:

        clear_output = list(
            map(
                lambda element: float(
                    ".".join([el[:2] for el in element.split()[:-1]][:2])
                ),
                whereami_output.split(","),
            )
        )

        return Coordinates(*clear_output)

    # whereami_output = execute_whereami()

    # return clear_whereami_output(whereami_output)
    return Coordinates(55.3955, 37.2839)
