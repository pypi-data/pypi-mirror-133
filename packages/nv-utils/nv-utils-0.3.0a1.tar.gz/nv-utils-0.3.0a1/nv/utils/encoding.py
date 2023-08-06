from importlib.util import find_spec
from io import StringIO
from pathlib import Path

from nv.utils.decorators import requires


if find_spec('charset_normalizer'):
    import charset_normalizer
else:
    charset_normalizer = None


@requires('charset_normalizer')
def detect_encoding(fp: Path | str) -> str:
    """
    Detects the file type and returns a file-like object with the contents of the file.
    :param fp: path to the file or file-like object.
    :return: file-like object with the contents of the file.
    """
    results = charset_normalizer.from_path(Path(fp))
    return results.best().encoding


@requires('charset_normalizer')
def decode(fp: Path | str) -> StringIO:
    """
    Detects the file type and returns a file-like object with the contents of the file.
    :param fp: path to the file or file-like object.
    :return: file-like object with the contents of the file.
    """
    results = charset_normalizer.from_path(Path(fp))
    return StringIO(str(results.best()))
