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


class ShowerKind(Enum):
    spectrum_fragment_scaler = 'spectrum-fragment-scaler'


class FactoryShower:

    def __init__(self, journal: Journal | None, document: Document | None):
        self.journal = journal
        self.document = document

    def create(self, kind: ShowerKind) -> Callable[[Data, Line, int], None]:

        if kind == ShowerKind.spectrum_fragment_scaler:

            @publish.setup(journal=self.journal, document=self.document)
            def shower(data: Data, line: Line, dn: int = 100) -> None:
                n0 = np.argmin(np.abs(data.wavelength - line.wavelength))

                #
                fig, axs = plt.subplots(nrows=3, figsize=(self.journal.width, self.journal.width*3/4), tight_layout=True, gridspec_kw={'height_ratios': [1, 1, 1.75]})

                # full spectrum
                plt.sca(axs[0])

                plt.text(
                    .05, .9,
                    fr'$\it{LETTERS[0]}$',
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
                    fr'$\it{LETTERS[1]}$',
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
                    fr'$\it{LETTERS[2]}$',
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

            return shower

        raise ValueError(f'ShowerKind: {kind} is not supported yet!')


# --------        utils        --------
def _determine_rectandle(data: Data, number: Array[int], dy: float = 0.05):
    x0 = min(data.wavelength[number])
    rx = max(data.wavelength[number]) - x0
    y0 = min(data.intensity)
    ry = max(data.intensity) - y0

    return (x0, y0 - ry*dy/2), rx, ry + ry*dy
