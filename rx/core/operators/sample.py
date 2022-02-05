from typing import Callable, Optional, TypeVar, Union, Any, cast

import rx
from rx.core import Observable, abc, typing
from rx.disposable import CompositeDisposable

_T = TypeVar("_T")


def sample_observable(
    source: Observable[_T], sampler: Observable[Any]
) -> Observable[_T]:
    def subscribe(
        observer: abc.ObserverBase[_T], scheduler: Optional[abc.SchedulerBase] = None
    ):
        at_end = False
        has_value = False
        value: _T = cast(_T, None)

        def sample_subscribe(_: Any = None) -> None:
            nonlocal has_value
            if has_value:
                has_value = False
                observer.on_next(value)

            if at_end:
                observer.on_completed()

        def on_next(new_value: _T):
            nonlocal has_value, value
            has_value = True
            value = new_value

        def on_completed():
            nonlocal at_end
            at_end = True

        return CompositeDisposable(
            source.subscribe_(on_next, observer.on_error, on_completed, scheduler),
            sampler.subscribe_(
                sample_subscribe, observer.on_error, sample_subscribe, scheduler
            ),
        )

    return Observable(subscribe)


def sample_(
    sampler: Union[typing.RelativeTime, Observable[Any]],
    scheduler: Optional[abc.SchedulerBase] = None,
) -> Callable[[Observable[_T]], Observable[_T]]:
    def sample(source: Observable[_T]) -> Observable[_T]:
        """Samples the observable sequence at each interval.

        Examples:
            >>> res = sample(source)

        Args:
            source: Source sequence to sample.

        Returns:
            Sampled observable sequence.
        """

        if isinstance(sampler, abc.ObservableBase):
            return sample_observable(source, sampler)
        else:
            return sample_observable(source, rx.interval(sampler, scheduler=scheduler))

    return sample


__all__ = ["sample_"]
