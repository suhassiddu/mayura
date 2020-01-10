import asyncio
from asyncio import create_task as atask, sleep as asleep
from time import ctime
from mayura import Component, Interval


class Counter(Component):
    state = {
        'count': 0
    }

    async def __init__(self):
        interval = await Interval(1)
        await interval.tick_subscribe(self.increment)

    async def increment(self, tick):
        await self.count_set(await self.count_get() + 1)


class App(Component):
    async def __init__(self):
        counter = await Counter()
        await counter.count_subscribe(self.print_count)

    async def print_count(self, count):
        print(f'count: {count}')

async def main():
    app = await App()
    for i in range(10):
        print('just waiting!')
        await asleep(1)

asyncio.run(main())
