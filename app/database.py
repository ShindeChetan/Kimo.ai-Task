from motor.motor_asyncio import AsyncIOMotorClient
from bson.objectid import ObjectId

MONGO_DETAILS = "mongodb://localhost:27017"
client = AsyncIOMotorClient(MONGO_DETAILS)
database = client.kimo_courses
course_collection = database.get_collection("courses")

def course_helper(course) -> dict:
    return {
        "id": str(course["_id"]),
        "name": course["name"],
        "date": course["date"],
        "description": course["description"],
        "domain": course["domain"],
        "chapters": course["chapters"]
    }
