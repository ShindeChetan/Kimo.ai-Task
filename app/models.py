from pydantic import BaseModel
from typing import List, Dict

class Chapter(BaseModel):
    name: str
    text: str
    rating: Dict[str, int] = {"positive": 0, "negative": 0}

class Course(BaseModel):
    name: str
    date: int
    description: str
    domain: List[str]
    chapters: List[Chapter]

