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

class Counter(Component):
    state = {
        'count': 0
    }

    async def __init__(self):
        await Interval(
            name='interval',
            self=self,
            delay=1,
            tick_subscribe=self.increment)


class App(Component):
    async def __init__(self):
        counter = await Counter()
        self.div = await Div() 
        await counter.count_subscribe(self.update_div)

    async def update_div(self, count):
        await self.div.text_set(f'count: {count}')

class App(Component):
    async def __init__(self):
        await Counter(
            name='counter',
            self=self)
            # count_subscribe=lambda count: \
            #    self.div.text_set(f'count: {count}'))

        await Div(
            name='div',
            self=self,
            text=lambda text_set: \
                self.counter.count_subscribe(lambda count: \
                    text_set(f'count: {count}'))

async def main():
    app = await App()
    for i in range(10):
        print('just waiting!')
        await asleep(1)

asyncio.run(main())
