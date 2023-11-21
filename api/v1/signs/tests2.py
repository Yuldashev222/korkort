import asyncio
import time


async def long_operation():
    print('starting long operation')
    await asyncio.sleep(5)
    print('Long operation completed')


async def main():
    print('start')
    task = asyncio.create_task(long_operation())
    await task
    print('end')

asyncio.run(main())

