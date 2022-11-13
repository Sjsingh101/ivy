# local
from typing import (
    Optional,
    Union,
    Sequence,
    Tuple,
    NamedTuple,
    Literal,
    Callable,
    Any,
    List,
)
import jax.numpy as jnp
from numbers import Number

# local
from ivy.functional.backends.jax import JaxArray


def moveaxis(
    a: JaxArray,
    source: Union[int, Sequence[int]],
    destination: Union[int, Sequence[int]],
    /,
    *,
    out: Optional[JaxArray] = None,
) -> JaxArray:
    return jnp.moveaxis(a, source, destination)


def heaviside(
    x1: JaxArray,
    x2: JaxArray,
    /,
    *,
    out: Optional[JaxArray] = None,
) -> JaxArray:
    return jnp.heaviside(x1, x2)


def flipud(
    m: JaxArray,
    /,
    *,
    out: Optional[JaxArray] = None,
) -> JaxArray:
    return jnp.flipud(m)


def vstack(
    arrays: Sequence[JaxArray],
    /,
    *,
    out: Optional[JaxArray] = None,
) -> JaxArray:
    return jnp.vstack(arrays)


def hstack(
    arrays: Sequence[JaxArray],
    /,
    *,
    out: Optional[JaxArray] = None,
) -> JaxArray:
    return jnp.hstack(arrays)


def rot90(
    m: JaxArray,
    /,
    *,
    k: Optional[int] = 1,
    axes: Optional[Tuple[int, int]] = (0, 1),
    out: Optional[JaxArray] = None,
) -> JaxArray:
    return jnp.rot90(m, k, axes)


def top_k(
    x: JaxArray,
    k: int,
    /,
    *,
    axis: Optional[int] = -1,
    largest: Optional[bool] = True,
    out: Optional[Tuple[JaxArray, JaxArray]] = None,
) -> Tuple[JaxArray, JaxArray]:
    if not largest:
        indices = jnp.argsort(x, axis=axis)
        indices = jnp.take(indices, jnp.arange(k), axis=axis)
    else:
        x *= -1
        indices = jnp.argsort(x, axis=axis)
        indices = jnp.take(indices, jnp.arange(k), axis=axis)
        x *= -1
    topk_res = NamedTuple("top_k", [("values", JaxArray), ("indices", JaxArray)])
    val = jnp.take_along_axis(x, indices, axis=axis)
    return topk_res(val, indices)


def fliplr(
    m: JaxArray,
    /,
    *,
    out: Optional[JaxArray] = None,
) -> JaxArray:
    return jnp.fliplr(m)


def i0(
    x: JaxArray,
    /,
    *,
    out: Optional[JaxArray] = None,
) -> JaxArray:
    return jnp.i0(x)


def _flat_array_to_1_dim_array(x):
    return x.reshape((1,)) if x.shape == () else x


def pad(
    input: JaxArray,
    pad_width: Union[Sequence[Sequence[int]], JaxArray, int],
    /,
    *,
    mode: Optional[
        Union[
            Literal[
                "constant",
                "edge",
                "linear_ramp",
                "maximum",
                "mean",
                "median",
                "minimum",
                "reflect",
                "symmetric",
                "wrap",
                "empty",
            ],
            Callable,
        ]
    ] = "constant",
    stat_length: Optional[Union[Sequence[Sequence[int]], int]] = None,
    constant_values: Optional[Union[Sequence[Sequence[Number]], Number]] = 0,
    end_values: Optional[Union[Sequence[Sequence[Number]], Number]] = 0,
    reflect_type: Optional[Literal["even", "odd"]] = "even",
    out: Optional[JaxArray] = None,
    **kwargs: Optional[Any],
) -> JaxArray:
    if callable(mode):
        return jnp.pad(
            _flat_array_to_1_dim_array(input),
            pad_width,
            mode=mode,
            **kwargs,
        )
    if mode in ["maximum", "mean", "median", "minimum"]:
        return jnp.pad(
            _flat_array_to_1_dim_array(input),
            pad_width,
            mode=mode,
            stat_length=stat_length,
        )
    elif mode == "constant":
        return jnp.pad(
            _flat_array_to_1_dim_array(input),
            pad_width,
            mode=mode,
            constant_values=constant_values,
        )
    elif mode == "linear_ramp":
        return jnp.pad(
            _flat_array_to_1_dim_array(input),
            pad_width,
            mode=mode,
            end_values=end_values,
        )
    elif mode in ["reflect", "symmetric"]:
        return jnp.pad(
            _flat_array_to_1_dim_array(input),
            pad_width,
            mode=mode,
            reflect_type=reflect_type,
        )
    else:
        return jnp.pad(
            _flat_array_to_1_dim_array(input),
            pad_width,
            mode=mode,
        )


def vsplit(
    ary: JaxArray,
    indices_or_sections: Union[int, Tuple[int]],
    /,
    *,
    out: Optional[JaxArray] = None,
) -> JaxArray:
    return jnp.vsplit(ary, indices_or_sections)


def dsplit(
    ary: JaxArray,
    indices_or_sections: Union[int, Tuple[int]],
    /,
    *,
    out: Optional[JaxArray] = None,
) -> JaxArray:
    return jnp.dsplit(ary, indices_or_sections)


def dstack(
    arrays: Sequence[JaxArray],
    /,
    *,
    out: Optional[JaxArray] = None,
) -> JaxArray:
    return jnp.dstack(arrays)


def atleast_2d(*arys: JaxArray) -> List[JaxArray]:
    return jnp.atleast_2d(*arys)
