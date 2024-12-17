from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Optional, List

app = FastAPI()

fakedb = []  #  database (list)

# Course Model
class Course(BaseModel):
    id: int
    name: str
    price: float
    is_early_bird: Optional[bool] = None

@app.get("/")
def read_root():
    return {"greetings": "Hello Kalpesh from this side"}

# Retrieve all courses
@app.get("/courses", response_model=List[Course])
def get_courses():
    return fakedb

# Retrieve a specific course by ID
@app.get("/courses/{course_id}", response_model=Course)
def get_a_course(course_id: int):
    if course_id - 1 >= len(fakedb) or course_id <= 0:
        raise HTTPException(status_code=404, detail="Course not found")
    return fakedb[course_id - 1]

# Add a new course
@app.post("/courses", response_model=Course)
def add_course(course: Course):
    fakedb.append(course.dict())
    return fakedb[-1]

# Delete a course
@app.delete("/courses/{course_id}")
def delete_course(course_id: int):
    if course_id - 1 >= len(fakedb) or course_id <= 0:
        raise HTTPException(status_code=404, detail="Course not found")
    deleted_course = fakedb.pop(course_id - 1)
    return {"task": "deletion successful", "deleted_course": deleted_course}

# Update a course (full update)
@app.put("/courses/{course_id}", response_model=Course)
def update_course(course_id: int, updated_course: Course):
    if course_id - 1 >= len(fakedb) or course_id <= 0:
        raise HTTPException(status_code=404, detail="Course not found")
    fakedb[course_id - 1] = updated_course.dict()
    return fakedb[course_id - 1]

# Partially update a course (e.g., change specific fields)
@app.patch("/courses/{course_id}", response_model=Course)
def patch_course(course_id: int, name: Optional[str] = None, price: Optional[float] = None):
    if course_id - 1 >= len(fakedb) or course_id <= 0:
        raise HTTPException(status_code=404, detail="Course not found")
    
    course = fakedb[course_id - 1]
    
    # Update only fields provided
    if name:
        course["name"] = name
    if price:
        course["price"] = price
    
    fakedb[course_id - 1] = course
    return course

# Retrieve courses with a price filter
@app.get("/courses/filter/")
def filter_courses_by_price(min_price: float = 0.0, max_price: float = float('inf')):
    filtered_courses = [course for course in fakedb if min_price <= course["price"] <= max_price]
    return filtered_courses











# from fastapi import FastAPI
# from pydantic import BaseModel
# from typing import Optional

# app=FastAPI()

# fakedb = []

# class Course(BaseModel):
#     id: int
#     name: str
#     price: float
#     is_early_bird: Optional[bool] = None


# @app.get("/")
# def read_root():
#     return {"greetings":"Hello Kalpesh from this side"}
    
# @app.get("/courses")
# def get_courses():
#     return fakedb

# @app.get("/courses/{course_id}")
# def get_a_course(course_id:int):
#     course = course_id - 1
#     return fakedb[course]

# @app.post("/courses")
# def add_course(course:Course):
#     fakedb.append(course.dict())
#     return fakedb[-1]


# @app.delete("/courses/{course_id}")
# def delete_course(course_id:int):
#     fakedb.pop(course_id-1)
#     return {"task":"deletion successful"}

# above code is basic crud operations

