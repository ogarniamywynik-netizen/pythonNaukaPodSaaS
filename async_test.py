import asyncio
import time

async def bez_async():
    print("Zapytanie 1 start")
    await asyncio.sleep(3)
    print("Zapytanie 1 koniec")

async def z_asyncem():
    print("Zapytanie 2 start")
    await asyncio.sleep(3)
    print("Zapytanie 2 koniec")

async def main():
    await asyncio.gather(
        bez_async(),
        z_asyncem()
    )

asyncio.run(main())