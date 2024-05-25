from spectrumlab_publisher.document import Document
from spectrumlab_publisher.journal import Journal

from spectrumlab_viewer.data import Burnout, Data
from spectrumlab_viewer.viewer import Viewer, ViewerMode


if __name__ == '__main__':
    viewer = Viewer(
        mode=ViewerMode.burnout_with_scintillation_peaks,
        journal=Journal.ISSN_2073_1442,
        document=Document.article,
    )
    viewer.show(
        Data.load(
            filedir='./data/burnout-with-scintillation-peaks',
            filenames=[
                'burnout.txt',
            ],
            kinds=[
                Burnout,
            ],
        ),
        threshold=0.5,
        cursor=6086,
    )
