from typing import Callable, Optional, TypeVar

from rx import operators as ops
from rx.core import Observable, pipe
from rx.core.typing import Mapper

_T = TypeVar("_T")


def sum_(
    key_mapper: Optional[Mapper[_T, int]] = None
) -> Callable[[Observable[_T]], Observable[int]]:
    if key_mapper:
        return pipe(ops.map(key_mapper), ops.sum())

    return ops.reduce(seed=0, accumulator=lambda prev, curr: prev + curr)


__all__ = ["sum_"]
