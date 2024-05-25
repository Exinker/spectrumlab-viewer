from dataclasses import dataclass, field
from typing import Callable

from spectrumlab_publisher.document import Document
from spectrumlab_publisher.journal import Journal

from spectrumlab_viewer.data import Data
from spectrumlab_viewer.line import Line

from .kernel import FactoryKernel, ViewerMode


@dataclass
class Viewer:
    mode: ViewerMode

    journal: Journal | None = field(default=Journal.DEBUG)
    document: Document | None = field(default=None)

    @property
    def kernel(self) -> Callable[[Data, Line, int], None]:
        return FactoryKernel(journal=self.journal, document=self.document).create(
            mode=self.mode,
        )

    def show(self, data: Data, line: Line, dn: int = 100) -> None:
        self.kernel(
            data=data,
            line=line,
            dn=dn,
        )
