import csv
import os
from dataclasses import dataclass
from typing import Callable

import numpy as np

from .config import FILEDIR
from .typing import Array, NanoMeter, U


@dataclass
class Data:
    wavelength: Array[NanoMeter]
    intensity: Array[U]
    crystal: Array[int]
    clipped: Array[bool]

    @property
    def n_numbers(self) -> int:
        return len(self.wavelength)

    @property
    def number(self) -> Array[int]:
        return np.arange(self.n_numbers)


# --------        utils        --------
def convert(string: str, kernel: Callable = float) -> bool | int | float:
    string = string.strip().replace(',', '.')

    return kernel(string)


def load_data(filename: str, filedir: str | None = None) -> Data:
    filedir = filedir or os.path.join('.')
    filepath = os.path.join(filedir, filename)

    #
    data = []
    for line in csv.reader(open(filepath, 'r'), delimiter='\t'):
        data.append([
            convert(item, kernel=kernel)
            for item, kernel in zip(line, [float, float, int, bool])
        ])

    data = np.array(data)

    #
    return Data(
        wavelength=data[:, 0],
        intensity=data[:, 1],
        crystal=data[:, 2],
        clipped=data[:, 3],
    )
