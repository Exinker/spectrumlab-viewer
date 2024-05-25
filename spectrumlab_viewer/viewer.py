from dataclasses import dataclass, field
from typing import Callable

from spectrumlab_publisher.document import Document
from spectrumlab_publisher.journal import Journal

from .data import Datum
from .shower import FactoryShower, ShowerKind
from .line import Line


@dataclass
class Viewer:
    kind: ShowerKind

    journal: Journal | None = field(default=Journal.DEBUG)
    document: Document | None = field(default=None)

    @property
    def handler(self) -> Callable[[Datum, Line, int], None]:
        return FactoryShower(journal=self.journal, document=self.document).create(
            kind=self.kind,
        )

    def show(self, datum: Datum, line: Line, dn: int = 100) -> None:
        self.handler(
            datum=datum,
            line=line,
            dn=dn,
        )
