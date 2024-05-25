import os

from spectrumlab_publisher.document import Document
from spectrumlab_publisher.journal import Journal

from spectrumlab_viewer.data import Data
from spectrumlab_viewer.line import Line
from spectrumlab_viewer.viewer import Viewer, ViewerMode


if __name__ == '__main__':
    filedir = os.path.join('.', 'data', 'spectrum-fragment-with-scintillation-peak')

    viewer = Viewer(
        mode=ViewerMode.spectrum_fragment_with_scintillation_peak,
        journal=Journal.ISSN_2073_1442,
        document=Document.article,
    )
    viewer.show(
        Data.load(
            filedir=filedir,
            filenames=[
                'spectrum.txt',
                'scintillation-peak.txt',
            ]
        ),
        line=Line(
            symbol='Au',
            wavelength=267.595,
        ),
        dn=100,
    )
