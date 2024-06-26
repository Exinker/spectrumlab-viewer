from spectrumlab_publisher.document import Document
from spectrumlab_publisher.journal import Journal

from spectrumlab_viewer.data import Data
from spectrumlab_viewer.line import Line
from spectrumlab_viewer.viewer import Viewer, ViewerMode


if __name__ == '__main__':
    viewer = Viewer(
        mode=ViewerMode.spectrum_fragment_scaler,
        journal=Journal.ISSN_2073_1442,
        document=Document.article,
    )
    viewer.show(
        Data.load(
            filedir='./data/spectrum-fragment-scaler',
        ),
        line=Line(
            symbol='W',
            wavelength=315.9181,
        ),
        dn=100,
    )
