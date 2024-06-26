from enum import Enum
from typing import Callable

import matplotlib.pyplot as plt
import matplotlib.patches as patches
import numpy as np

from spectrumlab_publisher import publish, LETTERS
from spectrumlab_publisher.document import Document
from spectrumlab_publisher.journal import Journal

from spectrumlab_viewer.data import AbstractDatum, Burnout, Data, Spectrum
from spectrumlab_viewer.line import Line
from spectrumlab_viewer.types import Array, U


class ViewerMode(Enum):
    spectrum_fragment_scaler = 'spectrum-fragment-scaler'
    spectrum_fragment_with_scintillation_peak = 'spectrum-fragment-with-scintillation-peak'
    burnout_with_scintillation_peaks = 'burnout-with-scintillation-peaks'


class FactoryKernel:

    def __init__(self, journal: Journal | None, document: Document | None):
        self.journal = journal
        self.document = document

    def create(self, mode: ViewerMode) -> Callable[[AbstractDatum, Line, int], None]:

        if mode == ViewerMode.spectrum_fragment_scaler:

            @publish.setup(journal=self.journal, document=self.document)
            def wrapped(data: Data[Spectrum], line: Line, dn: int = 100) -> None:
                assert len(data) == 1, 'overlapping of spectra is not supported yet!'
                assert all(isinstance(datum, Spectrum) for datum in data), 'only spectrum data are supported!'

                spectrum = data[0]
                n0 = np.argmin(np.abs(spectrum.wavelength - line.wavelength))

                #
                fig, axs = plt.subplots(nrows=3, figsize=(self.journal.width, self.journal.width*3/4), tight_layout=True, gridspec_kw={'height_ratios': [1, 1, 1.75]})

                # full spectrum
                plt.sca(axs[0])

                plt.text(
                    .05, .9,
                    fr'$\it{LETTERS[0]}$',
                    transform=plt.gca().transAxes,
                )

                for crystal in np.unique(spectrum.crystal):
                    number = spectrum.number[spectrum.crystal == crystal]
                    plt.step(
                        spectrum.wavelength[number],
                        spectrum.intensity[number],
                        color='black',  linestyle='-', linewidth=0.5,
                    )

                number = spectrum.number[spectrum.crystal == spectrum.crystal[n0]]
                plt.gca().add_patch(
                    patches.Rectangle(
                        *_determine_rectandle(
                            spectrum=spectrum,
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

                number = spectrum.number[spectrum.crystal == spectrum.crystal[n0]]
                plt.step(
                    spectrum.wavelength[number],
                    spectrum.intensity[number],
                    color='black',  linestyle='-', linewidth=0.5,
                )

                number = spectrum.number[(n0 - dn//2 < spectrum.number) & (spectrum.number < n0 + dn//2)]
                plt.gca().add_patch(
                    patches.Rectangle(
                        *_determine_rectandle(
                            spectrum=spectrum,
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

                number = spectrum.number[(spectrum.number > n0 - dn//2) & (spectrum.number < n0 + dn//2)]
                plt.step(
                    spectrum.wavelength[number],
                    spectrum.intensity[number],
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
            def wrapped(data: Data[Spectrum], line: Line, dn: int = 100) -> None:
                assert len(data) == 2, 'couple of spectra are supported only!'
                assert all(isinstance(datum, Spectrum) for datum in data), 'only spectrum data are supported!'

                #
                fig, ax = plt.subplots(figsize=(self.journal.width/2, self.journal.width/3), tight_layout=True)

                # spectrum
                spectrum = data[0]
                n0 = np.argmin(np.abs(spectrum.wavelength - line.wavelength))

                number = spectrum.number[(spectrum.number > n0 - dn//2) & (spectrum.number < n0 + dn//2)]
                plt.step(
                    spectrum.wavelength[number],
                    spectrum.intensity[number],
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
                spectrum = data[1]
                n0 = np.argmin(np.abs(spectrum.wavelength - line.wavelength))

                number = spectrum.number[(spectrum.number > n0 - dn//2) & (spectrum.number < n0 + dn//2)]
                plt.step(
                    spectrum.wavelength[number],
                    spectrum.intensity[number],
                    color='blue',  linestyle='-', linewidth=1,
                )

                #
                plt.xlabel(r'$\lambda$, $нм$')
                plt.ylabel('Интенсивность, отн. ед.')

                #
                plt.show()

            return wrapped

        if mode == ViewerMode.burnout_with_scintillation_peaks:

            @publish.setup(journal=self.journal, document=self.document)
            def wrapped(data: Data[Burnout], threshold: U, cursor: int | None = None) -> None:
                assert len(data) == 1, 'overlapping of burnouts is not supported yet!'
                assert all(isinstance(datum, Burnout) for datum in data), 'only burnout data are supported!'

                #
                fig, ax = plt.subplots(figsize=(self.journal.width/1.5, self.journal.width/3), tight_layout=True)

                # spectrum
                burnout = data[0]

                plt.step(
                    burnout.time,
                    burnout.intensity,
                    color='black',  linestyle='-', linewidth=1,
                )

                index = []
                for t in range(1, burnout.n_times-1):
                    is_maxima = (burnout.intensity[t - 1] <= burnout.intensity[t] > burnout.intensity[t + 1]) or (burnout.intensity[t - 1] < burnout.intensity[t] >= burnout.intensity[t + 1])
                    if is_maxima and (burnout.intensity[t] > threshold):
                        index.append(t)

                plt.scatter(
                    burnout.time[index],
                    burnout.intensity[index],
                    marker='|', c='#009300', linewidths=2, alpha=.5,
                )

                plt.axhline(
                    threshold,
                    color='grey', linestyle='--', linewidth=0.5,
                )

                if cursor:
                    plt.axvline(
                        burnout.time[cursor],
                        color='blue', linestyle='--', linewidth=1.0,
                    )
                    plt.text(
                        burnout.time[cursor], max(burnout.intensity),
                        f' t = {burnout.time[cursor]}, с',
                        # transform=ax.transAxes,
                        fontsize=8,
                        ha='left', va='bottom',
                        color='blue',
                    )

                #
                plt.xlabel(r'$t$, $c$')
                plt.ylabel('Интенсивность, отн. ед.')

                #
                plt.show()

            return wrapped

        raise ValueError(f'ViewerMode: {mode} is not supported yet!')


# --------        utils        --------
def _determine_rectandle(spectrum: Spectrum, number: Array[int], dy: float = 0.05):
    x0 = min(spectrum.wavelength[number])
    rx = max(spectrum.wavelength[number]) - x0
    y0 = min(spectrum.intensity)
    ry = max(spectrum.intensity) - y0

    return (x0, y0 - ry*dy/2), rx, ry + ry*dy
