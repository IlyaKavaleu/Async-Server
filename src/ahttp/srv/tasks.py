import asyncio


async def start(app):
    print('Start Server')
    await asyncio.sleep(1)


async def stop(app):
    await asyncio.sleep(1)
    print('Start Server')


async def ss(app):
    print('Start Application')
    await asyncio.sleep(1)
    yield
    await asyncio.sleep(1)
    print('Stop Application')


async def ss2(app):
    print('Start Application 2')
    await asyncio.sleep(1)
    yield
    await asyncio.sleep(1)
    print('Start Application 2')
