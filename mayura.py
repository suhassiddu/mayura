import functools
import inspect
from asyncio import create_task as atask, sleep as asleep


def _force_async(fn):
    if inspect.iscoroutinefunction(fn):
        return fn

    async def wrapped(*args, **kwargs):
        return fn(*args, **kwargs)

    return wrapped


async def _new(cls, *args, **kwargs):
    return object.__new__(cls)


def asyncinit(obj):
    if not inspect.isclass(obj):
        raise ValueError("decorated object must be a class")
    if obj.__new__ is object.__new__:
        cls_new = _new
    else:
        cls_new = _force_async(obj.__new__)

    @functools.wraps(obj.__new__)
    async def new(cls, *args, **kwargs):
        state = getattr(cls, 'state', {})
        state = state if isinstance(state, dict) else {}
        for name, init_value in state.items():
            var_name = f'_{name}'

            async def getter(self):
                return getattr(self, var_name)

            async def setter(self, value):
                setattr(self, var_name, value)
                for listener in getattr(self, f'{name}_listeners'):
                    atask(listener(getattr(self, var_name)))

            async def subscribe(self, listener):
                getattr(self, f'{name}_listeners', []).append(listener)

            setattr(cls, f'{name}_get', getter)
            setattr(cls, f'{name}_set', setter)
            setattr(cls, f'{name}_subscribe', subscribe)

        self = await cls_new(cls, *args, **kwargs)
        
        for name, init_value in state.items():
            var_name = f'_{name}'
            setattr(self, var_name, init_value)
            setattr(self, f'{name}_listeners', [])

        cls_init = _force_async(self.__init__)
        self._coroutine = atask(cls_init(*args, **kwargs))
        return self

    obj.__new__ = new
    return obj

@asyncinit
class Component:
    pass

class Interval(Component):
    state = {
        'tick': False
    }

    async def __init__(self, delay=1):
        while True:
            await self.tick_set(True)
            # spike wave
            self._tick = False
            await asleep(delay)

__all__ = ['Component', 'Interval']
