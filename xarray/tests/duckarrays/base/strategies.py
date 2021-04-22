import hypothesis.extra.numpy as npst
import hypothesis.strategies as st

import xarray as xr


def shapes(ndim=None):
    return npst.array_shapes()


dtypes = (
    npst.integer_dtypes()
    | npst.unsigned_integer_dtypes()
    | npst.floating_dtypes()
    | npst.complex_number_dtypes()
)


def numpy_array(shape=None):
    if shape is None:
        shape = npst.array_shapes()
    return npst.arrays(dtype=dtypes, shape=shape)


def create_dimension_names(ndim):
    return [f"dim_{n}" for n in range(ndim)]


@st.composite
def variable(draw, create_data, dims=None, shape=None, sizes=None):
    if sizes is not None:
        dims, sizes = zip(*draw(sizes).items())
    else:
        if shape is None:
            shape = draw(shapes())
        if dims is None:
            dims = create_dimension_names(len(shape))

    data = create_data(shape)

    return xr.Variable(dims, draw(data))


@st.composite
def data_array(draw, create_data):
    name = draw(st.none() | st.text(min_size=1))

    shape = draw(shapes())

    dims = create_dimension_names(len(shape))
    data = draw(create_data(shape))

    return xr.DataArray(
        data=data,
        name=name,
        dims=dims,
    )


def dimension_sizes(sizes):
    sizes_ = list(sizes.items())
    return st.lists(
        elements=st.sampled_from(sizes_), min_size=1, max_size=len(sizes_)
    ).map(dict)


@st.composite
def dataset(draw, create_data):
    names = st.text(min_size=1)
    sizes = draw(
        st.dictionaries(
            keys=names,
            values=st.integers(min_value=2, max_value=20),
            min_size=1,
            max_size=5,
        )
    )

    data_vars = st.dictionaries(
        keys=names,
        values=variable(create_data, sizes=dimension_sizes(sizes)),
        min_size=1,
        max_size=20,
    )

    return xr.Dataset(data_vars=draw(data_vars))


def valid_axis(ndim):
    return st.none() | st.integers(-ndim, ndim - 1)


def valid_axes(ndim):
    return valid_axis(ndim) | npst.valid_tuple_axes(ndim)
