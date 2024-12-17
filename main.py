from fastapi import FastAPI, HTTPException, Depends
from pydantic import BaseModel
from sqlalchemy import Column, Integer, String, Float, Boolean, create_engine
from sqlalchemy.orm import sessionmaker, declarative_base, Session
from typing import Optional, List

# Database connection URL
DATABASE_URL = "postgresql://postgres:#Kalpesh2810@localhost:5432/fastapi_db"

# SQLAlchemy setup
engine = create_engine(DATABASE_URL)  # Connect to PostgreSQL
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

# SQLAlchemy Model for Courses
class CourseDB(Base):
    __tablename__ = "courses"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    price = Column(Float, nullable=False)
    is_early_bird = Column(Boolean, default=False)

# Create tables in the database
Base.metadata.create_all(bind=engine)

# Pydantic Model for validation
class CourseSchema(BaseModel):
    id: Optional[int] = None
    name: str
    price: float
    is_early_bird: Optional[bool] = None

    class Config:
        orm_mode = True

# FastAPI app instance
app = FastAPI()

# Dependency to get a database session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Root endpoint
@app.get("/")
def read_root():
    return {"message": "Hello, Welcome to FastAPI with PostgreSQL!"}

# Retrieve all courses
@app.get("/courses", response_model=List[CourseSchema])
def get_courses(db: Session = Depends(get_db)):
    return db.query(CourseDB).all()

# Retrieve a single course by ID
@app.get("/courses/{course_id}", response_model=CourseSchema)
def get_course(course_id: int, db: Session = Depends(get_db)):
    course = db.query(CourseDB).filter(CourseDB.id == course_id).first()
    if not course:
        raise HTTPException(status_code=404, detail="Course not found")
    return course

# Add a new course
@app.post("/courses", response_model=CourseSchema)
def create_course(course: CourseSchema, db: Session = Depends(get_db)):
    new_course = CourseDB(**course.dict())
    db.add(new_course)
    db.commit()
    db.refresh(new_course)
    return new_course

# Update a course
@app.put("/courses/{course_id}", response_model=CourseSchema)
def update_course(course_id: int, course: CourseSchema, db: Session = Depends(get_db)):
    existing_course = db.query(CourseDB).filter(CourseDB.id == course_id).first()
    if not existing_course:
        raise HTTPException(status_code=404, detail="Course not found")
    for key, value in course.dict().items():
        setattr(existing_course, key, value)
    db.commit()
    db.refresh(existing_course)
    return existing_course

# Delete a course
@app.delete("/courses/{course_id}")
def delete_course(course_id: int, db: Session = Depends(get_db)):
    course = db.query(CourseDB).filter(CourseDB.id == course_id).first()
    if not course:
        raise HTTPException(status_code=404, detail="Course not found")
    db.delete(course)
    db.commit()
    return {"message": "Course deleted successfully"}





# from fastapi import FastAPI, HTTPException
# from pydantic import BaseModel
# from typing import Optional, List

# app = FastAPI()

# fakedb = []  #  database (list)

# # Course Model
# class Course(BaseModel):
#     id: int
#     name: str
#     price: float
#     is_early_bird: Optional[bool] = None

# @app.get("/")
# def read_root():
#     return {"greetings": "Hello Kalpesh from this side"}

# # Retrieve all courses
# @app.get("/courses", response_model=List[Course])
# def get_courses():
#     return fakedb

# # Retrieve a specific course by ID
# @app.get("/courses/{course_id}", response_model=Course)
# def get_a_course(course_id: int):
#     if course_id - 1 >= len(fakedb) or course_id <= 0:
#         raise HTTPException(status_code=404, detail="Course not found")
#     return fakedb[course_id - 1]

# # Add a new course
# @app.post("/courses", response_model=Course)
# def add_course(course: Course):
#     fakedb.append(course.dict())
#     return fakedb[-1]

# # Delete a course
# @app.delete("/courses/{course_id}")
# def delete_course(course_id: int):
#     if course_id - 1 >= len(fakedb) or course_id <= 0:
#         raise HTTPException(status_code=404, detail="Course not found")
#     deleted_course = fakedb.pop(course_id - 1)
#     return {"task": "deletion successful", "deleted_course": deleted_course}

# # Update a course (full update)
# @app.put("/courses/{course_id}", response_model=Course)
# def update_course(course_id: int, updated_course: Course):
#     if course_id - 1 >= len(fakedb) or course_id <= 0:
#         raise HTTPException(status_code=404, detail="Course not found")
#     fakedb[course_id - 1] = updated_course.dict()
#     return fakedb[course_id - 1]

# # Partially update a course (e.g., change specific fields)
# @app.patch("/courses/{course_id}", response_model=Course)
# def patch_course(course_id: int, name: Optional[str] = None, price: Optional[float] = None):
#     if course_id - 1 >= len(fakedb) or course_id <= 0:
#         raise HTTPException(status_code=404, detail="Course not found")
    
#     course = fakedb[course_id - 1]
    
#     # Update only fields provided
#     if name:
#         course["name"] = name
#     if price:
#         course["price"] = price
    
#     fakedb[course_id - 1] = course
#     return course

# # Retrieve courses with a price filter
# @app.get("/courses/filter/")
# def filter_courses_by_price(min_price: float = 0.0, max_price: float = float('inf')):
#     filtered_courses = [course for course in fakedb if min_price <= course["price"] <= max_price]
#     return filtered_courses











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

