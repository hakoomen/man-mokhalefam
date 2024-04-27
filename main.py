import asyncio
from db import init_db
from commands import start


async def main() -> None:
    # And the run events dispatching
    await init_db()
    await start()


if __name__ == "__main__":
    asyncio.run(main())
