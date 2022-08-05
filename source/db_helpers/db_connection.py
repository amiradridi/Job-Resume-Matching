import motor.motor_asyncio


MONGO_DETAILS = "mongodb://matchingproject:matchingproject@mongodb"

client = motor.motor_asyncio.AsyncIOMotorClient(MONGO_DETAILS)

database = client['matchingdb']
