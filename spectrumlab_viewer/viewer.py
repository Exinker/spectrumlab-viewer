from dataclasses import dataclass, field
from typing import Callable

from spectrumlab_publisher.document import Document
from spectrumlab_publisher.journal import Journal

from .data import Data
from .shower import FactoryShower, ShowerKind
from .line import Line


@dataclass
class Viewer:
    kind: ShowerKind

    journal: Journal | None = field(default=Journal.DEBUG)
    document: Document | None = field(default=None)

    @property
    def handler(self) -> Callable[[Data, Line, int], None]:
        return FactoryShower(journal=self.journal, document=self.document).create(
            kind=self.kind,
        )

    def show(self, data: Data, line: Line, dn: int = 100) -> None:
        self.handler(
            data=data,
            line=line,
            dn=dn,
        )
