from app.db import engine


async def on_shutdown():
    await engine.dispose()
