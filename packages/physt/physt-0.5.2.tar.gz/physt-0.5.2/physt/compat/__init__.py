"""Histograms types and function for various external libraries."""

try:
    from . import pandas
except ImportError:
    pass


try:
    from . import dask
except ImportError:
    pass


try:
    from . import geant4
except ImportError:
    pass


# TODO: Make xarray a compat too.
