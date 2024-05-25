import csv
import os
from dataclasses import dataclass
from typing import Callable, Sequence

import numpy as np

from .types import Array, NanoMeter, U


class AbstractDatum:
    pass


@dataclass
class Spectrum(AbstractDatum):
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
    def load(cls, filepath: str) -> 'Spectrum':

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
        return Spectrum(
            wavelength=dat[:, 0],
            intensity=dat[:, 1],
            crystal=dat[:, 2],
            clipped=dat[:, 3],
        )


class Data(list):

    def __init__(self, __data: Sequence[AbstractDatum]):
        super().__init__(__data)

    # --------        factory        --------
    @classmethod
    def load(cls, filedir: str | None = None, filenames: Sequence[str] | None = None, kinds: Sequence[type[AbstractDatum]] | None = None) -> 'Data':
        filedir = filedir or os.path.join('.')
        filenames = filenames or [filename for filename in os.listdir(filedir) if filename.endswith('.txt')]

        kinds = kinds or [Spectrum] * len(filenames)
        assert len(filenames) == len(kinds)

        #
        data = []
        for filename, kind in zip(filenames, kinds):

            try:
                datum = kind.load(
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
