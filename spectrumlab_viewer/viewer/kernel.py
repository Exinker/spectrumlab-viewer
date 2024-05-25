from enum import Enum
from typing import Callable

import matplotlib.pyplot as plt
import matplotlib.patches as patches
import numpy as np

from spectrumlab_publisher import publish, LETTERS
from spectrumlab_publisher.document import Document
from spectrumlab_publisher.journal import Journal

from spectrumlab_viewer.data import Data, Datum
from spectrumlab_viewer.line import Line
from spectrumlab_viewer.types import Array


class ViewerMode(Enum):
    spectrum_fragment_scaler = 'spectrum-fragment-scaler'
    spectrum_fragment_with_scintillation_peak = 'spectrum-fragment-with-scintillation-peak'


class FactoryKernel:

    def __init__(self, journal: Journal | None, document: Document | None):
        self.journal = journal
        self.document = document

    def create(self, mode: ViewerMode) -> Callable[[Datum, Line, int], None]:

        if mode == ViewerMode.spectrum_fragment_scaler:

            @publish.setup(journal=self.journal, document=self.document)
            def wrapped(data: Data, line: Line, dn: int = 100) -> None:
                assert len(data) == 1, 'overlapping of spectra is not supported yet!'

                datum = data[0]
                n0 = np.argmin(np.abs(datum.wavelength - line.wavelength))

                #
                fig, axs = plt.subplots(nrows=3, figsize=(self.journal.width, self.journal.width*3/4), tight_layout=True, gridspec_kw={'height_ratios': [1, 1, 1.75]})

                # full spectrum
                plt.sca(axs[0])

                plt.text(
                    .05, .9,
                    fr'$\it{LETTERS[0]}$',
                    transform=plt.gca().transAxes,
                )

                for crystal in np.unique(datum.crystal):
                    number = datum.number[datum.crystal == crystal]
                    plt.step(
                        datum.wavelength[number],
                        datum.intensity[number],
                        color='black',  linestyle='-', linewidth=0.5,
                    )

                number = datum.number[datum.crystal == datum.crystal[n0]]
                plt.gca().add_patch(
                    patches.Rectangle(
                        *_determine_rectandle(
                            datum=datum,
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

                number = datum.number[datum.crystal == datum.crystal[n0]]
                plt.step(
                    datum.wavelength[number],
                    datum.intensity[number],
                    color='black',  linestyle='-', linewidth=0.5,
                )

                number = datum.number[(n0 - dn//2 < datum.number) & (datum.number < n0 + dn//2)]
                plt.gca().add_patch(
                    patches.Rectangle(
                        *_determine_rectandle(
                            datum=datum,
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

                number = datum.number[(datum.number > n0 - dn//2) & (datum.number < n0 + dn//2)]
                plt.step(
                    datum.wavelength[number],
                    datum.intensity[number],
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

            return wrapped

        if mode == ViewerMode.spectrum_fragment_with_scintillation_peak:

            @publish.setup(journal=self.journal, document=self.document)
            def wrapped(data: Data, line: Line, dn: int = 100) -> None:
                assert len(data) == 2, 'couple of spectra are supported only!'

                #
                fig, ax = plt.subplots(figsize=(self.journal.width/3, self.journal.width/3), tight_layout=True)

                # spectrum
                datum = data[0]
                n0 = np.argmin(np.abs(datum.wavelength - line.wavelength))

                number = datum.number[(datum.number > n0 - dn//2) & (datum.number < n0 + dn//2)]
                plt.step(
                    datum.wavelength[number],
                    datum.intensity[number],
                    color='black',  linestyle='-', linewidth=1,
                )

                plt.axvline(
                    line.wavelength,
                    color='red', linestyle='--', linewidth=1.0,
                )
                plt.text(
                    0.51, .95,
                    f'{line}',
                    transform=ax.transAxes,
                    fontsize=8,
                    ha='left', va='bottom',
                    color='red',
                )

                # scintillation peak
                datum = data[1]
                n0 = np.argmin(np.abs(datum.wavelength - line.wavelength))

                number = datum.number[(datum.number > n0 - dn//2) & (datum.number < n0 + dn//2)]
                plt.step(
                    datum.wavelength[number],
                    datum.intensity[number],
                    color='blue',  linestyle='-', linewidth=1,
                )

                #
                plt.xlabel(r'$\lambda$, $нм$')
                plt.ylabel('Интенсивность, отн. ед.')

                #
                plt.show()

            return wrapped

        raise ValueError(f'ViewerMode: {mode} is not supported yet!')


# --------        utils        --------
def _determine_rectandle(datum: Datum, number: Array[int], dy: float = 0.05):
    x0 = min(datum.wavelength[number])
    rx = max(datum.wavelength[number]) - x0
    y0 = min(datum.intensity)
    ry = max(datum.intensity) - y0

    return (x0, y0 - ry*dy/2), rx, ry + ry*dy
