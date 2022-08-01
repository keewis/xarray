# import public API
from .datatree import DataTree
from .io import open_datatree
from .mapping import TreeIsomorphismError, map_over_subtree

try:
    # NOTE: the `_version.py` file must not be present in the git repository
    #   as it is generated by setuptools at install time
    from ._version import __version__
except ImportError:  # pragma: no cover
    # Local copy or not installed with setuptools
    __version__ = "999"

__all__ = (
    "DataTree",
    "open_datatree",
    "TreeIsomorphismError",
    "map_over_subtree",
    "__version__",
)