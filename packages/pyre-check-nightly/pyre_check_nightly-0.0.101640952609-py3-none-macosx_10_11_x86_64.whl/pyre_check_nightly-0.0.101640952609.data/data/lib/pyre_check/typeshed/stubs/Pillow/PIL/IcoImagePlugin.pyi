from typing import Any

from .ImageFile import ImageFile

class IcoFile:
    buf: Any
    entry: Any
    nb_items: Any
    def __init__(self, buf): ...
    def sizes(self): ...
    def getentryindex(self, size, bpp: bool = ...): ...
    def getimage(self, size, bpp: bool = ...): ...
    def frame(self, idx): ...

class IcoImageFile(ImageFile):
    format: str
    format_description: str
    @property
    def size(self): ...
    @size.setter
    def size(self, value) -> None: ...
    im: Any
    mode: Any
    def load(self) -> None: ...
    def load_seek(self) -> None: ...
