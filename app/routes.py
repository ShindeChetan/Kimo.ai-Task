from fastapi import APIRouter, HTTPException, Query
from typing import List, Optional
from bson.objectid import ObjectId
from .database import course_collection, course_helper
from .models import Course

router = APIRouter()

# Endpoint to list all courses with sorting and filtering
@router.get("/courses", response_description="List all courses")
async def list_courses(sort_by: str = "name", domain: Optional[str] = None):
    query = {}
    if domain:
        query["domain"] = domain
    courses = []
    async for course in course_collection.find(query):
        courses.append(course_helper(course))
    if sort_by == "name":
        courses.sort(key=lambda x: x['name'])
    elif sort_by == "date":
        courses.sort(key=lambda x: x['date'], reverse=True)
    return courses

# Endpoint to get a specific course by ID
@router.get("/courses/{course_id}", response_description="Get a single course")
async def get_course(course_id: str):
    course = await course_collection.find_one({"_id": ObjectId(course_id)})
    if course:
        return course_helper(course)
    raise HTTPException(status_code=404, detail=f"Course {course_id} not found")

# Endpoint to get a specific chapter by course ID and chapter name
@router.get("/courses/{course_id}/chapters/{chapter_name}", response_description="Get a single chapter")
async def get_chapter(course_id: str, chapter_name: str):
    course = await course_collection.find_one({"_id": ObjectId(course_id)})
    if course:
        for chapter in course["chapters"]:
            if chapter["name"] == chapter_name:
                return chapter
        raise HTTPException(status_code=404, detail="Chapter not found")
    raise HTTPException(status_code=404, detail="Course not found")

@router.post("/courses/{course_id}/chapters/{chapter_name}/rate", response_description="Rate a chapter")
async def rate_chapter(course_id: str, chapter_name: str, rating: str = Query(..., regex="^(positive|negative)$")):
    course = await course_collection.find_one({"_id": ObjectId(course_id)})
    if course:
        for chapter in course["chapters"]:
            if chapter["name"] == chapter_name:
                if "rating" not in chapter:
                    chapter["rating"] = {"positive": 0, "negative": 0}
                
                chapter["rating"][rating] += 1

                await course_collection.update_one({"_id": ObjectId(course_id)}, {"$set": {"chapters": course["chapters"]}})
                return {"message": "Rating updated"}
        
        raise HTTPException(status_code=404, detail="Chapter not found")
    
    raise HTTPException(status_code=404, detail="Course not found")

