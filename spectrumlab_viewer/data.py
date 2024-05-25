import csv
import os
from dataclasses import dataclass
from typing import Callable, Sequence

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
    def load(cls, filepath: str) -> 'Datum':

        # load
        lines = csv.reader(open(filepath, 'r'), delimiter='\t')

        # parse
        dat = []
        for items in lines:
            match items:
                case wavelength, intensity:
                    dat.append((to_float(wavelength), to_float(intensity), 0, 0))
                case wavelength, intensity, crystal, clipped:
                    dat.append((to_float(wavelength), to_float(intensity), int(crystal), bool(clipped)))

        dat = np.array(dat)

        #
        return Datum(
            wavelength=dat[:, 0],
            intensity=dat[:, 1],
            crystal=dat[:, 2],
            clipped=dat[:, 3],
        )


class Data(list):

    def __init__(self, __data: Sequence[Datum]):
        super().__init__(__data)

    # --------        factory        --------
    @classmethod
    def load(cls, filedir: str | None = None, filenames: str | None = None) -> 'Data':
        filedir = filedir or os.path.join('.')
        filenames = filenames or [filename for filename in os.listdir(filedir) if filename.endswith('.txt')]

        #
        data = []
        for filename in filenames:

            try:
                datum = Datum.load(
                    filepath=os.path.join(filedir, filename),
                )

            except Exception as error:
                print(error)

            else:
                data.append(datum)

        #
        return cls(data)


# --------        utils        --------
def to_float(string: str) -> float:
    string = string.strip().replace(',', '.')

    return float(string)
