from enum import Enum
from typing import Callable

import matplotlib.pyplot as plt
import matplotlib.patches as patches
import numpy as np

from spectrumlab_publisher import publish, LETTERS
from spectrumlab_publisher.document import Document
from spectrumlab_publisher.journal import Journal

from spectrumlab_viewer.data import Data
from spectrumlab_viewer.line import Line
from spectrumlab_viewer.types import Array


class Kind(Enum):
    line_location = 'line-location'


class FactoryHandler:
    
    def __init__(self, journal: Journal | None = Journal.DEBUG, document: Document | None = None):
        self.journal = journal
        self.document = document

    def create(self, kind: Kind) -> Callable[[Data, Line, int], None]:

        if kind == Kind.line_location:

            @publish.setup(journal=self.journal, document=self.document)
            def handler(data: Data, line: Line, dn: int = 100) -> None:
                n0 = np.argmin(np.abs(data.wavelength - line.wavelength))

                #
                fig, axs = plt.subplots(nrows=3, figsize=(self.journal.width, self.journal.width*3/4), tight_layout=True, gridspec_kw={'height_ratios': [1, 1, 1.75]})

                # full spectrum
                plt.sca(axs[0])

                plt.text(
                    .05, .9,
                    f'$\it{LETTERS[0]}$',
                    transform=plt.gca().transAxes,
                )

                for crystal in np.unique(data.crystal):
                    number = data.number[data.crystal == crystal]
                    plt.step(
                        data.wavelength[number],
                        data.intensity[number],
                        color='black',  linestyle='-', linewidth=0.5,
                    )

                number = data.number[data.crystal == data.crystal[n0]]
                plt.gca().add_patch(
                    patches.Rectangle(
                        *_determine_rectandle(
                            data=data,
                            number=number,
                        ),
                        edgecolor='red', facecolor='none', linewidth=1.0,
                    )
                )

                # select line crystal
                plt.sca(axs[1])

                plt.text(
                    .05, .9,
                    f'$\it{LETTERS[1]}$',
                    transform=plt.gca().transAxes,
                )

                number = data.number[data.crystal == data.crystal[n0]]
                plt.step(
                    data.wavelength[number],
                    data.intensity[number],
                    color='black',  linestyle='-', linewidth=0.5,
                )

                number = data.number[(n0 - dn//2 < data.number) & (data.number < n0 + dn//2)]
                plt.gca().add_patch(
                    patches.Rectangle(
                        *_determine_rectandle(
                            data=data,
                            number=number,
                        ),
                        edgecolor='red', facecolor='none', linewidth=1.0,
                    )
                )

                plt.ylabel('Интенсивность, отн. ед.')

                # select line neighborhood
                plt.sca(axs[2])

                plt.text(
                    .05, .9,
                    f'$\it{LETTERS[2]}$',
                    transform=plt.gca().transAxes,
                )

                number = data.number[(data.number > n0 - dn//2) & (data.number < n0 + dn//2)]
                plt.step(
                    data.wavelength[number],
                    data.intensity[number],
                    color='black',  linestyle='-', linewidth=1,
                )

                plt.axvline(
                    line.wavelength,
                    color='red', linestyle='--', linewidth=1.0,
                )
                plt.text(
                    0.51, .95,
                    f'{line}',
                    transform=plt.gca().transAxes,
                    fontsize=8,
                    ha='left', va='bottom',
                    color='red',
                )

                plt.xlabel(r'$\lambda$, $нм$')

                #
                plt.show()

            return handler

        raise ValueError(f'Kind: {kind} is not supported yet!')


# --------        utils        --------
def _determine_rectandle(data: Data, number: Array[int], dy: float = 0.05):
    x0 = min(data.wavelength[number])
    rx = max(data.wavelength[number]) - x0
    y0 = min(data.intensity)
    ry = max(data.intensity) - y0

    return (x0, y0 - ry*dy/2), rx, ry + ry*dy
