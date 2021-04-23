import pytest

pytest.importorskip("hypothesis")

from xarray import DataArray, Dataset, Variable

from .. import assert_allclose
from . import base
from .base import strategies

sparse = pytest.importorskip("sparse")


def create(op, shape):
    def convert(arr):
        if arr.ndim == 0:
            return arr

        return sparse.COO.from_numpy(arr)

    return strategies.numpy_array(shape).map(convert)


def as_dense(obj):
    if isinstance(obj, Variable) and isinstance(obj.data, sparse.COO):
        new_obj = obj.copy(data=obj.data.todense())
    elif isinstance(obj, DataArray):
        ds = obj._to_temp_dataset()
        dense = as_dense(ds)
        new_obj = obj._from_temp_dataset(dense)
    elif isinstance(obj, Dataset):
        variables = {name: as_dense(var) for name, var in obj.variables.items()}
        coords = {
            name: var for name, var in variables.items() if name in obj._coord_names
        }
        data_vars = {
            name: var for name, var in variables.items() if name not in obj._coord_names
        }

        new_obj = Dataset(coords=coords, data_vars=data_vars, attrs=obj.attrs)
    else:
        new_obj = obj

    return new_obj


@pytest.mark.apply_marks(
    {
        "test_reduce": {
            "[cumprod]": pytest.mark.skip(reason="cumprod not implemented by sparse"),
            "[cumsum]": pytest.mark.skip(reason="cumsum not implemented by sparse"),
            "[median]": pytest.mark.skip(reason="median not implemented by sparse"),
            "[std]": pytest.mark.skip(reason="nanstd not implemented by sparse"),
            "[var]": pytest.mark.skip(reason="nanvar not implemented by sparse"),
        }
    }
)
class TestVariableReduceMethods(base.VariableReduceTests):
    @staticmethod
    def create(op, shape):
        return create(op, shape)

    def check_reduce(self, obj, op, *args, **kwargs):
        actual = as_dense(getattr(obj, op)(*args, **kwargs))
        expected = getattr(as_dense(obj), op)(*args, **kwargs)

        assert_allclose(actual, expected)


@pytest.mark.apply_marks(
    {
        "test_reduce": {
            "[cumprod]": pytest.mark.skip(reason="cumprod not implemented by sparse"),
            "[cumsum]": pytest.mark.skip(reason="cumsum not implemented by sparse"),
            "[median]": pytest.mark.skip(reason="median not implemented by sparse"),
            "[std]": pytest.mark.skip(reason="nanstd not implemented by sparse"),
            "[var]": pytest.mark.skip(reason="nanvar not implemented by sparse"),
        }
    }
)
class TestDataArrayReduceMethods(base.DataArrayReduceTests):
    @staticmethod
    def create(op, shape):
        return create(op, shape)

    def check_reduce(self, obj, op, *args, **kwargs):
        actual = as_dense(getattr(obj, op)(*args, **kwargs))
        expected = getattr(as_dense(obj), op)(*args, **kwargs)

        assert_allclose(actual, expected)


@pytest.mark.apply_marks(
    {
        "test_reduce": {
            "[cumprod]": pytest.mark.skip(reason="cumprod not implemented by sparse"),
            "[cumsum]": pytest.mark.skip(reason="cumsum not implemented by sparse"),
            "[median]": pytest.mark.skip(reason="median not implemented by sparse"),
            "[std]": pytest.mark.skip(reason="nanstd not implemented by sparse"),
            "[var]": pytest.mark.skip(reason="nanvar not implemented by sparse"),
        }
    }
)
class TestDatasetReduceMethods(base.DatasetReduceTests):
    @staticmethod
    def create(op, shape):
        return create(op, shape)

    def check_reduce(self, obj, op, *args, **kwargs):
        actual = as_dense(getattr(obj, op)(*args, **kwargs))
        expected = getattr(as_dense(obj), op)(*args, **kwargs)

        assert_allclose(actual, expected)
