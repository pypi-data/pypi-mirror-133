"""One-dimensional histograms."""
from __future__ import annotations

from abc import ABC, abstractmethod
import dataclasses
from typing import TYPE_CHECKING

import numpy as np

from physt import bin_utils
from physt.histogram_base import HistogramBase
from physt.statistics import Statistics, INVALID_STATISTICS
from physt.util import deprecation_alias


if TYPE_CHECKING:
    from typing import TypeVar, Any, Dict, Mapping, Optional, Tuple, Type, Union

    import xarray
    import pandas

    from physt.binnings import BinningBase, BinningLike
    from physt.typing_aliases import ArrayLike, DTypeLike, Axis

    Histogram1DType = TypeVar("Histogram1DType", bound="Histogram1D")


# TODO: Fix I/O with binning


class ObjectWithBinning(ABC):
    """Mixin with shared methods for 1D objects that have a binning.

    Note: Used to share behaviour between Histogram1D and HistogramCollection.
    """

    # TODO: Rename to something better

    @property
    @abstractmethod
    def binning(self) -> BinningBase:
        """The binning itself."""

    @property
    def ndim(self) -> int:
        return 1

    @property
    def bins(self) -> np.ndarray:
        """Array of all bin edges.

        Returns
        -------
        Wide-format [[leftedge1, rightedge1], ... [leftedgeN, rightedgeN]]
        """
        # TODO: Read-only copy
        return self.binning.bins  # TODO: or this should be read-only copy?

    @property
    def numpy_bins(self) -> np.ndarray:
        """Bins in the format of numpy."""
        # TODO: If not consecutive, does not make sense
        # TODO: Deprecate
        return self.binning.numpy_bins

    @property
    def edges(self) -> np.ndarray:
        return self.numpy_bins

    @property
    def bin_left_edges(self) -> np.ndarray:
        """Left edges of all bins."""
        return self.bins[..., 0]

    @property
    def bin_right_edges(self) -> np.ndarray:
        """Right edges of all bins."""
        return self.bins[..., 1]

    def get_bin_left_edges(self, i):
        assert i == 0
        return self.bin_left_edges

    def get_bin_right_edges(self, i):
        assert i == 0
        return self.bin_right_edges

    @property
    def min_edge(self) -> float:
        """Left edge of the first bin."""
        return self.bin_left_edges[0]

    @property
    def max_edge(self) -> float:
        """Right edge of the last bin."""
        return self.bin_right_edges[-1]

    @property
    def bin_centers(self) -> np.ndarray:
        """Centers of all bins."""
        return (self.bin_left_edges + self.bin_right_edges) / 2

    @property
    def bin_widths(self) -> np.ndarray:
        """Widths of all bins."""
        return self.bin_right_edges - self.bin_left_edges

    @property
    def total_width(self) -> float:
        """Total width of all bins.

        In inconsecutive histograms, the missing intervals are not counted in.
        """
        return self.bin_widths.sum().item()

    @property
    def bin_sizes(self) -> np.ndarray:
        return self.bin_widths


class Histogram1D(ObjectWithBinning, HistogramBase):
    """One-dimensional histogram data.

    The bins can be of different widths.

    The bins need not be consecutive. However, some functionality may not be available
    for non-consecutive bins (like keeping information about underflow and overflow).

    These are the basic attributes that can be used in the constructor (see there)
    Other attributes are dynamic.
    """

    def __init__(
        self,
        binning: BinningLike,
        frequencies: Optional[ArrayLike] = None,
        errors2: Optional[ArrayLike] = None,
        *,
        keep_missed: bool = True,
        stats: Optional[Statistics] = None,
        overflow: Optional[float] = 0.0,
        underflow: Optional[float] = 0.0,
        inner_missed: Optional[float] = 0.0,
        axis_name: Optional[str] = None,
        **kwargs,
    ):
        """Constructor

        Parameters
        ----------
        binning: The binning
        frequencies: The bin contents.
        keep_missed: Whether to keep track of underflow/overflow when filling with new values.
        underflow: Weight of observations that were smaller than the minimum bin.
        overflow: Weight of observations that were larger than the maximum bin.
        name: Name of the histogram (will be displayed as plot title)
        axis_name: Name of the characteristics that is histogrammed (will be displayed on x axis)
        errors2: Quadratic errors of individual bins. If not set, defaults to frequencies.
        stats: The statistics to use. If not set, defaults INVALID_STATISTICS.
        """
        missed = [
            underflow,
            overflow,
            inner_missed,
        ]
        if axis_name:
            kwargs["axis_names"] = [axis_name]

        HistogramBase.__init__(
            self, [binning], frequencies, errors2, keep_missed=keep_missed, **kwargs
        )

        if frequencies is None:
            self._stats = Statistics()
        else:
            self._stats = stats or INVALID_STATISTICS

        if self.keep_missed:
            self._missed = np.array(missed, dtype=self.dtype)
        else:
            self._missed = np.zeros(3, dtype=self.dtype)

    def copy(self, *, include_frequencies: bool = True) -> "Histogram1D":
        # Overriden to include the statistics as well
        a_copy = super().copy(include_frequencies=include_frequencies)
        if include_frequencies:
            a_copy._stats = dataclasses.replace(self.statistics)
        return a_copy

    @property
    def statistics(self) -> Statistics:
        return self._stats

    @property
    def axis_name(self) -> str:
        return self.axis_names[0]

    @axis_name.setter
    def axis_name(self, value: str):
        self.axis_names = (value,)

    def select(
        self, axis, index, *, force_copy: bool = False
    ) -> Union["Histogram1D", Tuple[np.ndarray, float]]:
        """Alias for [] to be compatible with HistogramND."""
        if axis == 0:
            if index == slice(None) and not force_copy:
                return self
            return self[index]
        else:
            raise ValueError("In Histogram1D.select(), axis must be 0.")

    def __getitem__(
        self, index: Union[int, slice, np.ndarray]
    ) -> Union["Histogram1D", Tuple[np.ndarray, float]]:
        """Select sub-histogram or get one bin.

        Parameters
        ----------
        index : int or slice or bool masked array or array with indices
            In most cases, this has same semantics as for numpy.ndarray.__getitem__


        Returns
        -------
        Histogram1D or tuple
            Depending on the parameters, a sub-histogram or content of one bin are returned.
        """
        underflow = np.nan
        overflow = np.nan
        keep_missed = False
        if isinstance(index, int):
            return self.bins[index], self.frequencies[index]
        if isinstance(index, np.ndarray):
            if index.dtype == bool:
                if index.shape != (self.bin_count,):
                    raise IndexError("Cannot index with masked array of a wrong dimension")
        elif isinstance(index, slice):
            keep_missed = self.keep_missed
            # TODO: Fix this
            if index.step:
                raise IndexError("Cannot change the order of bins")
            if index.step == 1 or index.step is None:
                underflow = self.underflow
                overflow = self.overflow
                if index.start:
                    underflow += self.frequencies[0 : index.start].sum()
                if index.stop:
                    overflow += self.frequencies[index.stop :].sum()
        # Masked arrays or item list or ...
        return self.__class__(
            self._binning.as_static(copy=False)[index],
            self.frequencies[index],
            self.errors2[index],
            overflow=overflow,
            keep_missed=keep_missed,
            underflow=underflow,
            dtype=self.dtype,
            name=self.name,
            axis_name=self.axis_name,
        )

    @property
    def _binning(self) -> BinningBase:
        """Adapter property for HistogramBase interface"""
        return self._binnings[0]

    @_binning.setter
    def _binning(self, value: BinningBase):
        self._binnings = [value]

    @property
    def binning(self) -> BinningBase:
        """The binning.

        Note: Please, do not try to update the object itself.
        """
        return self._binning

    @property
    def numpy_like(self) -> Tuple[np.ndarray, np.ndarray]:
        """Same result as would the numpy.histogram function return."""
        return self.frequencies, self.numpy_bins

    @property
    def cumulative_frequencies(self) -> np.ndarray:
        """Cumulative frequencies.

        Note: underflow values are not considered
        """
        return self._frequencies.cumsum()

    @property
    def underflow(self):
        if not self.keep_missed:
            return np.nan
        return self._missed[0]

    @underflow.setter
    def underflow(self, value):
        self._missed[0] = value

    @property
    def overflow(self):
        if not self.keep_missed:
            return np.nan
        return self._missed[1]

    @overflow.setter
    def overflow(self, value):
        self._missed[1] = value

    @property
    def inner_missed(self):
        if not self.keep_missed:
            return np.nan
        return self._missed[2]

    @inner_missed.setter
    def inner_missed(self, value):
        self._missed[2] = value

    @np.deprecate(message="Please use .statistics.mean instead.")
    def mean(self) -> float:
        return self.statistics.mean()

    @np.deprecate(message="Please use .statistics.min instead.")
    def min(self) -> float:
        return self.statistics.min

    @np.deprecate(message="Please use .statistics.max instead.")
    def max(self) -> float:
        return self.statistics.max

    @np.deprecate(message="Please use .statistics.std instead.")
    def std(self) -> float:  # , ddof=0):
        return self.statistics.std()

    @np.deprecate(message="Please use .statistics.variance instead.")
    def variance(self) -> float:  # , ddof: int = 0) -> float:
        return self.statistics.variance()

    def find_bin(self, value: float, axis: Optional[Axis] = None) -> Optional[int]:
        """Index of bin corresponding to a value.

        Returns
        -------
        index of bin to which value belongs
            (-1=underflow, N=overflow, None=not found - inconsecutive)
        """
        if axis is not None:
            self._get_axis(axis)  # Check that it is valid
        if not np.isscalar(value):
            raise ValueError(f"Non-scalar value for 1D histogram: {value}")
        ixbin = np.searchsorted(self.bin_left_edges, value, side="right").item()
        if ixbin == 0:
            return -1
        if ixbin == self.bin_count:
            if value <= self.bin_right_edges[-1]:
                return ixbin - 1
            else:
                return self.bin_count
        if value < self.bin_right_edges[ixbin - 1]:
            return ixbin - 1
        if ixbin == self.bin_count:
            return self.bin_count
        return None

    def fill(self, value: float, weight: float = 1, **kwargs) -> Optional[int]:
        """Update histogram with a new value.

        Parameters
        ----------
        value: Value to be added.
        weight: Weight assigned to the value.

        Returns
        -------
        index of bin which was incremented (-1=underflow, N=overflow, None=not found)

        Note: If a gap in unconsecutive bins is matched, underflow & overflow are not valid anymore.
        Note: Name was selected because of the eponymous method in ROOT
        """
        self._coerce_dtype(type(weight))
        if self._binning.is_adaptive():
            bin_map = self._binning.force_bin_existence(value)
            self._reshape_data(self._binning.bin_count, bin_map)

        ixbin = self.find_bin(value)
        if ixbin is None:
            self.overflow = np.nan
            self.underflow = np.nan
        elif ixbin == -1 and self.keep_missed:
            self.underflow += weight
        elif ixbin == self.bin_count and self.keep_missed:
            self.overflow += weight
        else:
            self._frequencies[ixbin] += weight
            self._errors2[ixbin] += weight ** 2
            self._stats = dataclasses.replace(
                self.statistics,
                weight=self.statistics.weight + weight,
                sum=self.statistics.sum + weight * value,
                sum2=self.statistics.sum2 + weight * value ** 2,
                min=min(self.statistics.min, value),
                max=max(self.statistics.max, value),
            )

        return ixbin

    def fill_n(
        self, values: ArrayLike, weights: Optional[ArrayLike] = None, *, dropna: bool = True
    ) -> None:
        # TODO: Unify with HistogramBase
        values = np.asarray(values)
        if dropna:
            values = values[~np.isnan(values)]
        if self._binning.is_adaptive():
            map = self._binning.force_bin_existence(values)
            self._reshape_data(self._binning.bin_count, map)
        if weights is not None:
            weights = np.asarray(weights)
            self._coerce_dtype(weights.dtype)
        (frequencies, errors2, underflow, overflow, stats) = calculate_frequencies(
            values,
            self._binning,
            dtype=self.dtype,
            weights=weights,
            validate_bins=False,
        )
        self._frequencies += frequencies
        self._errors2 += errors2
        # TODO: check that adaptive does not produce under-/over-flows?
        if self.keep_missed:
            self.underflow += underflow
            self.overflow += overflow
        self._stats += stats

    def __eq__(self, other: Any) -> bool:
        if not isinstance(other, self.__class__):
            return False
        # TODO: Change to something in binning itself
        if not np.allclose(other.bins, self.bins, equal_nan=True):
            return False
        if not np.allclose(other.frequencies, self.frequencies, equal_nan=True):
            return False
        if other.keep_missed != self.keep_missed:
            return False
        if self.keep_missed:
            if not np.allclose(other.overflow, self.overflow, equal_nan=True):
                return False
            if not np.allclose(other.underflow, self.underflow, equal_nan=True):
                return False
            if not np.allclose(other.inner_missed, self.inner_missed, equal_nan=True):
                return False
        if not np.allclose(other.errors2, self.errors2, equal_nan=True):
            return False
        if not other.name == self.name:
            return False
        if not other.axis_name == self.axis_name:
            return False
        return True

    @classmethod
    def _kwargs_from_dict(cls, a_dict: Mapping[str, Any]) -> Dict[str, Any]:
        kwargs = HistogramBase._kwargs_from_dict(a_dict)  # type: ignore
        kwargs["binning"] = kwargs.pop("binnings")[0]
        return kwargs

    def to_xarray(self) -> "xarray.Dataset":
        """Convert to xarray.Dataset"""
        # TODO: Move this to physt.compat.xarray
        import xarray as xr

        data_vars: Dict[str, Any] = {
            "frequencies": xr.DataArray(self.frequencies, dims="bin"),
            "errors2": xr.DataArray(self.errors2, dims="bin"),
            "bins": xr.DataArray(self.bins, dims=("bin", "x01")),
        }
        coords: Dict[str, Any] = {}
        attrs: Dict[str, Any] = {
            "underflow": self.underflow,
            "overflow": self.overflow,
            "inner_missed": self.inner_missed,
            "keep_missed": self.keep_missed,
        }
        attrs.update(self._meta_data)
        # TODO: Add stats
        return xr.Dataset(data_vars, coords, attrs)  # type: ignore

    @classmethod
    def from_xarray(cls, arr: "xarray.Dataset") -> "Histogram1D":
        """Convert form xarray.Dataset

        Parameters
        ----------
        arr: The data in xarray representation
        """
        kwargs = {
            "frequencies": arr["frequencies"],
            "binning": arr["bins"],
            "errors2": arr["errors2"],
            "overflow": arr.attrs["overflow"],
            "underflow": arr.attrs["underflow"],
            "keep_missed": arr.attrs["keep_missed"],
        }
        # TODO: Add stats
        return cls(**kwargs)

    @classmethod
    def from_calculate_frequencies(
        cls: Type["Histogram1DType"],
        data: Optional[np.ndarray],
        binning: BinningBase,
        weights: Optional[ArrayLike] = None,
        *,
        validate_bins: bool = True,
        already_sorted: bool = False,
        keep_missed: bool = True,
        dtype: Optional[DTypeLike] = None,
        **kwargs,
    ) -> "Histogram1DType":
        """Construct the histogram from values and bins."""
        if data is None:
            frequencies: Optional[np.ndarray] = None
            errors2: Optional[np.ndarray] = None
            underflow: float = 0.0
            overflow: float = 0.0
            stats: Optional[Statistics] = None
        else:
            frequencies, errors2, underflow, overflow, stats = calculate_frequencies(
                data=data,
                binning=binning,
                weights=weights,
                validate_bins=validate_bins,
                already_sorted=already_sorted,
                dtype=dtype,
            )
            if not keep_missed:
                underflow = 0.0
                overflow = 0.0

        return cls(
            binning=binning,
            frequencies=frequencies,
            errors2=errors2,
            stats=stats,
            underflow=underflow,
            overflow=overflow,
            keep_missed=keep_missed,
            dtype=dtype,
            **kwargs,
        )


def calculate_frequencies(
    data: ArrayLike,
    binning: BinningBase,
    weights: Optional[ArrayLike] = None,
    *,
    validate_bins: bool = True,
    already_sorted: bool = False,
    dtype: Optional[DTypeLike] = None,
) -> Tuple[np.ndarray, np.ndarray, float, float, Statistics]:
    """Get frequencies and bin errors from the data.

    Parameters
    ----------
    data : Data items to work on.
    binning : A set of bins.
    weights : Weights of the items.
    validate_bins : If True (default), bins are validated to be in ascending order.
    already_sorted : If True, the data being entered are already sorted, no need to sort them once more.
    dtype: Underlying type for the histogram.
        (If weights are specified, default is float. Otherwise long.)

    Returns
    -------
    frequencies : Bin contents
    errors2 :  Error squares of the bins
    underflow : Weight of items smaller than the first bin
    overflow : Weight of items larger than the last bin
    stats: The statistics (computed or empty)

    Note
    ----
    Checks that the bins are in a correct order (not necessarily consecutive).
    Does not check for numerical overflows in bins.
    """

    # TODO: Is it possible to merge with histogram_nd.calculate_frequencies?

    underflow = np.nan
    overflow = np.nan

    # Ensure correct binning
    bins = binning.bins  # bin_utils.make_bin_array(bins)
    if validate_bins:
        if bins.shape[0] == 0:
            raise ValueError("Cannot have histogram with 0 bins.")
        if not bin_utils.is_rising(bins):
            raise ValueError("Bins must be rising.")

    # Prepare 1D numpy array of data
    data_array: np.ndarray = np.asarray(data)
    if data_array.ndim > 1:
        # TODO: Perhaps disallow this?
        data_array = data_array.flatten()

    # Prepare 1D numpy array of weights
    if weights is not None:
        weights_array: np.ndarray = np.asarray(weights)
        if weights_array.ndim > 1:
            weights_array = weights_array.flatten()

        # Check compatibility of weights
        if weights_array.shape != data_array.shape:
            raise ValueError(
                f"Weights must have the same shape as data, {weights_array.shape} != {data_array.shape}"
            )
    else:
        weights_array = np.ones_like(data_array, dtype=int)

    # Prepare dtype
    inferred_dtype: np.dtype = np.dtype(dtype or weights_array.dtype)
    if inferred_dtype.kind in "iu" and weights_array.dtype.kind == "f":
        raise ValueError("Integer histogram requested but float weights entered.")

    # Data sorting
    if not already_sorted:
        sort_order = np.argsort(data_array)  # Memory: another copy
        data_array = data_array[sort_order]  # Memory: another copy
        weights_array = weights_array[sort_order]
        del sort_order

    # Fill frequencies and errors
    frequencies = np.zeros(bins.shape[0], dtype=inferred_dtype)
    errors2 = np.zeros(bins.shape[0], dtype=inferred_dtype)
    for xbin, bin in enumerate(bins):
        start = np.searchsorted(data_array, bin[0], side="left")
        stop = np.searchsorted(data_array, bin[1], side="left")

        if xbin == 0:
            underflow = weights_array[0:start].sum()
        if xbin == len(bins) - 1:
            stop = np.searchsorted(data_array, bin[1], side="right")  # TODO: Understand and explain
            overflow = weights_array[stop:].sum()

        frequencies[xbin] = weights_array[start:stop].sum()
        errors2[xbin] = (weights_array[start:stop] ** 2).sum()

    # Underflow and overflow don't make sense for unconsecutive binning.
    if not bin_utils.is_consecutive(bins):
        underflow = np.nan
        overflow = np.nan

    # Statistics
    if not data_array.size:
        stats = Statistics()
    else:
        stats = Statistics(
            sum=(data_array * weights_array).sum(),
            sum2=(data_array ** 2 * weights_array).sum(),
            min=float(data_array.min()),
            max=float(data_array.max()),
            weight=float(weights_array.sum()),
        )
    return frequencies, errors2, underflow, overflow, stats
