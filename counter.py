import asyncio
from asyncio import sleep as asleep
from time import ctime
from mayura import Component, Interval, Div


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
        self.div = await Div() 
        await counter.count_subscribe(self.update_div)

    async def update_div(self, count):
        await self.div.text_set(f'count: {count}')

async def main():
    app = await App()
    for i in range(10):
        print('just waiting!')
        await asleep(1)

asyncio.run(main())
