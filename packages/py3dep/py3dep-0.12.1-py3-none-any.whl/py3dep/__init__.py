"""Top-level package for Py3DEP."""
from .exceptions import (
    InvalidInputType,
    MissingAttribute,
    MissingColumns,
    MissingCRS,
    MissingDependency,
)
from .print_versions import show_versions
from .py3dep import elevation_bycoords, elevation_bygrid, get_map
from .utils import deg2mpm, fill_depressions

try:
    import importlib.metadata as metadata
except ImportError:
    import importlib_metadata as metadata  # type: ignore[no-redef]

try:
    __version__ = metadata.version("py3dep")
except Exception:
    __version__ = "999"

__all__ = [
    # Functions
    "fill_depressions",
    "get_map",
    "deg2mpm",
    "elevation_bycoords",
    "elevation_bygrid",
    "show_versions",
    # Exceptions
    "MissingColumns",
    "MissingCRS",
    "MissingDependency",
    "MissingAttribute",
    "InvalidInputType",
    # Constants
    "__version__",
]
