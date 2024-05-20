from dataclasses import dataclass, field
from typing import Callable

from spectrumlab_publisher.document import Document
from spectrumlab_publisher.journal import Journal

from .data import Data
from .handler import FactoryHandler, Kind
from .line import Line


@dataclass
class Viewer:
    kind: Kind = field(default=Kind.line_location)
    document: Document | None = field(default=None)
    journal: Journal | None = field(default=Journal.DEBUG)

    @property
    def handler(self) -> Callable[[Data, Line, int], None]:
        return FactoryHandler(journal=self.journal, document=self.document).create(
            kind=self.kind,
        )

    def show(self, data: Data, line: Line, dn: int = 100) -> None:
        self.handler(
            data=data,
            line=line,
            dn=dn,
        )
