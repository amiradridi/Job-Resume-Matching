async def init(database):
    if not database.is_connected:
        await database.connect()