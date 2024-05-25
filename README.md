# spectrumlab-viewer

**spectrumlab-viewer** - библиотека отображения графиков спектров, получаемых с [ПО Атом](https://www.vmk.ru/product/programmnoe_obespechenie/atom.html).


## Author Information:
Павел Ващенко (vaschenko@vmk.ru)

[ВМК-Оптоэлектроника](https://www.vmk.ru/), г. Новосибирск 2024 г.


## Installation
Для установки следует выполнить команду `pip install git+https://github.com/Exinker/spectrumlab-viewer.git`.


## Usage
Для использования приложения требуется сохранить график спектра в режиме `Расширенный текст` (по умолчанию в текущую директорию).
Пример использования приложения приведен ниже:
```python
from spectrumlab_publisher.document import Document
from spectrumlab_publisher.journal import Journal

from spectrumlab_viewer.data import Datum
from spectrumlab_viewer.line import Line
from spectrumlab_viewer.viewer import Viewer


viewer = Viewer(
    journal=Journal.ISSN_2073_1442,
    document=Document.article,
)
viewer.show(
    datum=Datum.load(filename='noname.txt'),
    line=Line(
        symbol='Ni',
        wavelength=221.6479,
    ),
    dn=100,
)

```
