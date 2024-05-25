import csv
import os
from dataclasses import dataclass
from typing import Callable

import numpy as np

from .types import Array, NanoMeter, U


@dataclass
class Datum:
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

    # --------        factory        --------
    @classmethod
    def load(cls, filename: str, filedir: str | None = None) -> 'Datum':
        filedir = filedir or os.path.join('.')

        # load
        filepath = os.path.join(filedir, filename)
        lines = csv.reader(open(filepath, 'r'), delimiter='\t')

        # parse
        dat = []
        for line in lines:
            dat.append([
                convert(item, kernel=kernel)
                for item, kernel in zip(line, [float, float, int, bool])
            ])

        dat = np.array(dat)

        #
        return Datum(
            wavelength=dat[:-2048, 0],
            intensity=dat[:-2048, 1],
            crystal=dat[:-2048, 2],
            clipped=dat[:-2048, 3],
        )


# --------        utils        --------
def convert(string: str, kernel: Callable = float) -> bool | int | float:
    string = string.strip().replace(',', '.')

    return kernel(string)
