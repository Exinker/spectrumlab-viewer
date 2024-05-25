import os

from spectrumlab_publisher.document import Document
from spectrumlab_publisher.journal import Journal

from spectrumlab_viewer.data import load_data
from spectrumlab_viewer.line import Line
from spectrumlab_viewer.shower import ShowerKind
from spectrumlab_viewer.viewer import Viewer


if __name__ == '__main__':
    filename = os.path.join('.', 'data', 'Grand-2 (poly I).txt')

    viewer = Viewer(
        kind=ShowerKind.spectrum_fragment_scaler,
        journal=Journal.ISSN_2073_1442,
        document=Document.article,
    )
    viewer.show(
        data=load_data(
            filename=filename,
        ),
        line=Line(
            symbol='W',
            wavelength=315.9181,
        ),
        dn=100,
    )
