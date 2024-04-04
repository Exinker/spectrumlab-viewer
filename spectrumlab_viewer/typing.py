from typing import TypeAlias, NewType

from numpy.typing import NDArray


# --------        structures        --------
Array: TypeAlias = NDArray


# --------        temperature units        --------
Kelvin = NewType('Kelvin', float)
Celsius = NewType('Celsius', float)


# --------        time units        --------
Second = NewType('Second', float)
MilliSecond = NewType('MilliSecond', float)
MicroSecond = NewType('MicroSecond', int)

Hz = NewType('Hz', float)

# --------        spacial units        --------
Inch = NewType('Inch', float)

Meter = NewType('Meter', float)
CentiMeter = NewType('CentiMeter', float)
MilliMeter = NewType('MilliMeter', float)
MicroMeter = NewType('MicroMeter', float)
NanoMeter = NewType('NanoMeter', float)
PicoMeter = NewType('Pico', float)

Number = NewType('Number', float)


# --------        value units        --------
Absorbance = NewType('Absorbance', float)
Electron = NewType('Electron', float)
Percent = NewType('Percent', float)

U: TypeAlias = Absorbance | Electron | Percent


# --------        other units        --------
Symbol = NewType('Symbol', str)
