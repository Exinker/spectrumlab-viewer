import os

from spectrumlab_publisher.document import Document
from spectrumlab_publisher.journal import Journal

from spectrumlab_viewer.data import Data
from spectrumlab_viewer.line import Line
from spectrumlab_viewer.shower import ShowerKind
from spectrumlab_viewer.viewer import Viewer


if __name__ == '__main__':
    filedir = os.path.join('.', 'data', 'spectrum-fragment-scaler')

    viewer = Viewer(
        kind=ShowerKind.spectrum_fragment_scaler,
        journal=Journal.ISSN_2073_1442,
        document=Document.article,
    )
    viewer.show(
        data=Data.load(
            filedir=filedir,
        ),
        line=Line(
            symbol='W',
            wavelength=315.9181,
        ),
        dn=100,
    )
