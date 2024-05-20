from typing import TypeAlias, NewType

from numpy.typing import NDArray


# --------        structures        --------
Array: TypeAlias = NDArray


# --------        spacial units        --------
NanoMeter = NewType('NanoMeter', float)


# --------        value units        --------
Absorbance = NewType('Absorbance', float)
Electron = NewType('Electron', float)
Percent = NewType('Percent', float)

U: TypeAlias = Absorbance | Electron | Percent


# --------        other units        --------
Symbol = NewType('Symbol', str)
