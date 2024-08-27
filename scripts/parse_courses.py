import json
from pymongo import MongoClient

client = MongoClient("mongodb://localhost:27017")
db = client.kimo_courses
course_collection = db.courses

def load_courses(json_file):
    with open(json_file) as f:
        courses = json.load(f)
    return courses

def insert_courses(courses):
    course_collection.insert_many(courses)

if __name__ == "__main__":
    courses = load_courses("courses.json")
    insert_courses(courses)
    print("Courses inserted successfully")
