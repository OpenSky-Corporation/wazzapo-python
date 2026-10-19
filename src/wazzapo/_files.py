"""Файл для загрузки в media.upload: путь, bytes или открытый файл."""

from __future__ import annotations

import mimetypes
import os
from pathlib import Path
from typing import IO, Optional, Tuple, Union

FileInput = Union[str, "os.PathLike[str]", bytes, IO[bytes]]

_DEFAULT_TYPE = "application/octet-stream"


def _file_part(
    file: FileInput, filename: Optional[str] = None, content_type: Optional[str] = None
) -> dict[str, Tuple[str, bytes, str]]:
    """Поле file формы multipart: (имя, содержимое, тип)."""
    if isinstance(file, (str, os.PathLike)):
        path = Path(file)
        content = path.read_bytes()
        name = filename or path.name
    elif isinstance(file, (bytes, bytearray)):
        content = bytes(file)
        name = filename or "file"
    else:
        content = file.read()
        name = filename or Path(getattr(file, "name", "file") or "file").name
    ctype = content_type or mimetypes.guess_type(name)[0] or _DEFAULT_TYPE
    return {"file": (name, content, ctype)}
