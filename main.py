from fastapi import FastAPI, HTTPException, Request, status
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from typing import Optional
from datetime import datetime, timedelta

# Configuration
SECRET_KEY = "a9c4e7f8g2h6k9l1p3q8r5t7w0z3x4v6n8m5b7y1j2o4u6"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

# FastAPI app instance
app = FastAPI()

# Token Validation Middleware
@app.middleware("http")
async def validate_token(request: Request, call_next):
    exempt_routes = ["/", "/token", "/docs", "/openapi.json"]  # Add exempt paths
    if request.url.path not in exempt_routes:
        try:
            token = request.headers.get("Authorization")
            if not token:
                raise HTTPException(
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    detail="Authorization header missing",
                )
            token = token.split("Bearer ")[-1]
            payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
            username: str = payload.get("sub")
            if username is None:
                raise HTTPException(
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    detail="Invalid token: Missing username",
                )
        except JWTError as e:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail=f"Invalid token: {str(e)}",
            )
    response = await call_next(request)
    return response

# Example Route
@app.get("/")
def read_root():
    return {"message": "Hello, Welcome to FastAPI!"}

# Token Endpoint
@app.post("/token")
async def login():
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = jwt.encode(
        {"sub": "admin", "exp": datetime.utcnow() + access_token_expires},
        SECRET_KEY,
        algorithm=ALGORITHM,
    )
    return {"access_token": access_token, "token_type": "bearer"}

# Protected Route
@app.get("/protected")
def protected_route():
    return {"message": "You have access to this route!"}


# ###This approach organizes the API logic into separate functions and maps them explicitly using app.add_api_route().


# from fastapi import FastAPI, HTTPException, Depends, status
# from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
# from pydantic import BaseModel
# from sqlalchemy import Column, Integer, String, Float, Boolean, create_engine
# from sqlalchemy.orm import sessionmaker, declarative_base, Session
# from typing import Optional, List
# from datetime import datetime, timedelta
# from jose import JWTError, jwt
# from passlib.context import CryptContext

# # Database connection URL
# DATABASE_URL = "postgresql://postgres:#Kalpesh2810@localhost:5432/fastapi_dbb"

# # SQLAlchemy setup
# engine = create_engine(DATABASE_URL)
# SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
# Base = declarative_base()

# # Secret key and JWT configuration
# SECRET_KEY = "your_secret_key_here"
# ALGORITHM = "HS256"
# ACCESS_TOKEN_EXPIRE_MINUTES = 30

# # Password hashing setup
# pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
# oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

# # User Database (Mock User Model)
# fake_users_db = {
#     "admin": {
#         "username": "admin",
#         "hashed_password": pwd_context.hash("password123"),
#     }
# }

# # SQLAlchemy Model for Courses
# class CourseDB(Base):
#     __tablename__ = "courses"

#     id = Column(Integer, primary_key=True, index=True)
#     name = Column(String, nullable=False)
#     price = Column(Float, nullable=False)
#     is_early_bird = Column(Boolean, default=False)

# Base.metadata.create_all(bind=engine)

# # Pydantic Models
# class CourseSchema(BaseModel):
#     id: Optional[int] = None
#     name: str
#     price: float
#     is_early_bird: Optional[bool] = None

#     class Config:
#         orm_mode = True

# class Token(BaseModel):
#     access_token: str
#     token_type: str

# class TokenData(BaseModel):
#     username: Optional[str] = None

# class User(BaseModel):
#     username: str

# class UserInDB(User):
#     hashed_password: str

# # Utility functions
# def verify_password(plain_password, hashed_password):
#     return pwd_context.verify(plain_password, hashed_password)

# def get_password_hash(password):
#     return pwd_context.hash(password)

# def get_user(db, username: str):
#     if username in db:
#         user_dict = db[username]
#         return UserInDB(**user_dict)
#     return None

# def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
#     to_encode = data.copy()
#     if expires_delta:
#         expire = datetime.utcnow() + expires_delta
#     else:
#         expire = datetime.utcnow() + timedelta(minutes=15)
#     to_encode.update({"exp": expire})
#     encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
#     return encoded_jwt

# async def get_current_user(token: str = Depends(oauth2_scheme)):
#     credentials_exception = HTTPException(
#         status_code=status.HTTP_401_UNAUTHORIZED,
#         detail="Could not validate credentials",
#         headers={"WWW-Authenticate": "Bearer"},
#     )
#     try:
#         payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
#         username: str = payload.get("sub")
#         if username is None:
#             raise credentials_exception
#         token_data = TokenData(username=username)
#     except JWTError:
#         raise credentials_exception
#     user = get_user(fake_users_db, username=token_data.username)
#     if user is None:
#         raise credentials_exception
#     return user

# async def get_current_active_user(current_user: User = Depends(get_current_user)):
#     return current_user

# # Dependency to get a database session
# def get_db():
#     db = SessionLocal()
#     try:
#         yield db
#     finally:
#         db.close()

# # API endpoint logic
# def root_logic():
#     return {"message": "Hello, Welcome to FastAPI with PostgreSQL!"}

# async def login_logic(form_data: OAuth2PasswordRequestForm = Depends()):
#     user = get_user(fake_users_db, form_data.username)
#     if not user or not verify_password(form_data.password, user.hashed_password):
#         raise HTTPException(
#             status_code=status.HTTP_401_UNAUTHORIZED,
#             detail="Incorrect username or password",
#             headers={"WWW-Authenticate": "Bearer"},
#         )
#     access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
#     access_token = create_access_token(
#         data={"sub": user.username}, expires_delta=access_token_expires
#     )
#     return {"access_token": access_token, "token_type": "bearer"}

# async def get_current_user_logic(current_user: User = Depends(get_current_active_user)):
#     return current_user

# def get_courses_logic(db: Session = Depends(get_db), current_user: User = Depends(get_current_active_user)):
#     return db.query(CourseDB).all()

# def create_course_logic(course: CourseSchema, db: Session = Depends(get_db), current_user: User = Depends(get_current_active_user)):
#     new_course = CourseDB(**course.dict())
#     db.add(new_course)
#     db.commit()
#     db.refresh(new_course)
#     return new_course

# def update_course_logic(course_id: int, course: CourseSchema, db: Session = Depends(get_db), current_user: User = Depends(get_current_active_user)):
#     existing_course = db.query(CourseDB).filter(CourseDB.id == course_id).first()
#     if not existing_course:
#         raise HTTPException(status_code=404, detail="Course not found")
#     for key, value in course.dict().items():
#         setattr(existing_course, key, value)
#     db.commit()
#     db.refresh(existing_course)
#     return existing_course

# def delete_course_logic(course_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_active_user)):
#     course = db.query(CourseDB).filter(CourseDB.id == course_id).first()
#     if not course:
#         raise HTTPException(status_code=404, detail="Course not found")
#     db.delete(course)
#     db.commit()
#     return {"message": "Course deleted successfully"}

# # FastAPI app instance
# app = FastAPI()

# # Route definitions
# app.add_api_route("/", root_logic, methods=["GET"])
# app.add_api_route("/token", login_logic, methods=["POST"], response_model=Token)
# app.add_api_route("/users/me", get_current_user_logic, methods=["GET"], response_model=User)
# app.add_api_route("/courses", get_courses_logic, methods=["GET"], response_model=List[CourseSchema])
# app.add_api_route("/courses", create_course_logic, methods=["POST"], response_model=CourseSchema)
# app.add_api_route("/courses/{course_id}", update_course_logic, methods=["PUT"], response_model=CourseSchema)
# app.add_api_route("/courses/{course_id}", delete_course_logic, methods=["DELETE"])




# ###CODE WITH AUTHORIZATION AND AUTHENTICATION

# from fastapi import FastAPI, HTTPException, Depends, status
# from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
# from pydantic import BaseModel
# from sqlalchemy import Column, Integer, String, Float, Boolean, create_engine
# from sqlalchemy.orm import sessionmaker, declarative_base, Session
# from typing import Optional, List
# from datetime import datetime, timedelta
# from jose import JWTError, jwt
# from passlib.context import CryptContext

# # Database connection URL
# DATABASE_URL = "postgresql://postgres:#Kalpesh2810@localhost:5432/fastapi_dbb"

# # SQLAlchemy setup
# engine = create_engine(DATABASE_URL)
# SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
# Base = declarative_base()

# # Secret key and JWT configuration
# SECRET_KEY = "your_secret_key_here"
# ALGORITHM = "HS256"
# ACCESS_TOKEN_EXPIRE_MINUTES = 30

# # Password hashing setup
# pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
# oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

# # User Database (Mock User Model)
# fake_users_db = {
#     "admin": {
#         "username": "admin",
#         "hashed_password": pwd_context.hash("password123"),
#     }
# }

# # SQLAlchemy Model for Courses
# class CourseDB(Base):
#     __tablename__ = "courses"

#     id = Column(Integer, primary_key=True, index=True)
#     name = Column(String, nullable=False)
#     price = Column(Float, nullable=False)
#     is_early_bird = Column(Boolean, default=False)

# Base.metadata.create_all(bind=engine)

# # Pydantic Models
# class CourseSchema(BaseModel):
#     id: Optional[int] = None
#     name: str
#     price: float
#     is_early_bird: Optional[bool] = None

#     class Config:
#         orm_mode = True

# class Token(BaseModel):
#     access_token: str
#     token_type: str

# class TokenData(BaseModel):
#     username: Optional[str] = None

# class User(BaseModel):
#     username: str

# class UserInDB(User):
#     hashed_password: str

# # FastAPI app instance
# app = FastAPI()

# # Utility functions
# def verify_password(plain_password, hashed_password):
#     return pwd_context.verify(plain_password, hashed_password)

# def get_password_hash(password):
#     return pwd_context.hash(password)

# def get_user(db, username: str):
#     if username in db:
#         user_dict = db[username]
#         return UserInDB(**user_dict)
#     return None

# def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
#     to_encode = data.copy()
#     if expires_delta:
#         expire = datetime.utcnow() + expires_delta
#     else:
#         expire = datetime.utcnow() + timedelta(minutes=15)
#     to_encode.update({"exp": expire})
#     encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
#     return encoded_jwt

# async def get_current_user(token: str = Depends(oauth2_scheme)):
#     credentials_exception = HTTPException(
#         status_code=status.HTTP_401_UNAUTHORIZED,
#         detail="Could not validate credentials",
#         headers={"WWW-Authenticate": "Bearer"},
#     )
#     try:
#         payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
#         username: str = payload.get("sub")
#         if username is None:
#             raise credentials_exception
#         token_data = TokenData(username=username)
#     except JWTError:
#         raise credentials_exception
#     user = get_user(fake_users_db, username=token_data.username)
#     if user is None:
#         raise credentials_exception
#     return user

# async def get_current_active_user(current_user: User = Depends(get_current_user)):
#     return current_user

# # Dependency to get a database session
# def get_db():
#     db = SessionLocal()
#     try:
#         yield db
#     finally:
#         db.close()

# # Root endpoint
# @app.get("/")
# def read_root():
#     return {"message": "Hello, Welcome to FastAPI with PostgreSQL!"}

# # Authentication endpoint to get token
# @app.post("/token", response_model=Token)
# async def login(form_data: OAuth2PasswordRequestForm = Depends()):
#     user = get_user(fake_users_db, form_data.username)
#     if not user or not verify_password(form_data.password, user.hashed_password):
#         raise HTTPException(
#             status_code=status.HTTP_401_UNAUTHORIZED,
#             detail="Incorrect username or password",
#             headers={"WWW-Authenticate": "Bearer"},
#         )
#     access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
#     access_token = create_access_token(
#         data={"sub": user.username}, expires_delta=access_token_expires
#     )
#     return {"access_token": access_token, "token_type": "bearer"}

# # Protected routes (require token)
# @app.get("/users/me", response_model=User)
# async def read_users_me(current_user: User = Depends(get_current_active_user)):
#     return current_user

# # Retrieve all courses
# @app.get("/courses", response_model=List[CourseSchema])
# def get_courses(db: Session = Depends(get_db), current_user: User = Depends(get_current_active_user)):
#     return db.query(CourseDB).all()

# # Add a new course
# @app.post("/courses", response_model=CourseSchema)
# def create_course(course: CourseSchema, db: Session = Depends(get_db), current_user: User = Depends(get_current_active_user)):
#     new_course = CourseDB(**course.dict())
#     db.add(new_course)
#     db.commit()
#     db.refresh(new_course)
#     return new_course

# # Update a course
# @app.put("/courses/{course_id}", response_model=CourseSchema)
# def update_course(course_id: int, course: CourseSchema, db: Session = Depends(get_db), current_user: User = Depends(get_current_active_user)):
#     existing_course = db.query(CourseDB).filter(CourseDB.id == course_id).first()
#     if not existing_course:
#         raise HTTPException(status_code=404, detail="Course not found")
#     for key, value in course.dict().items():
#         setattr(existing_course, key, value)
#     db.commit()
#     db.refresh(existing_course)
#     return existing_course

# # Delete a course
# @app.delete("/courses/{course_id}")
# def delete_course(course_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_active_user)):
#     course = db.query(CourseDB).filter(CourseDB.id == course_id).first()
#     if not course:
#         raise HTTPException(status_code=404, detail="Course not found")
#     db.delete(course)
#     db.commit()
#     return {"message": "Course deleted successfully"}




# from fastapi import FastAPI, HTTPException, Depends
# from pydantic import BaseModel
# from sqlalchemy import Column, Integer, String, Float, Boolean, create_engine
# from sqlalchemy.orm import sessionmaker, declarative_base, Session
# from typing import Optional, List

# # Database connection URL
# DATABASE_URL = "postgresql://postgres:#Kalpesh2810@localhost:5432/fastapi_db"

# # SQLAlchemy setup
# engine = create_engine(DATABASE_URL)  # Connect to PostgreSQL
# SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
# Base = declarative_base()

# # SQLAlchemy Model for Courses
# class CourseDB(Base):
#     __tablename__ = "courses"

#     id = Column(Integer, primary_key=True, index=True)
#     name = Column(String, nullable=False)
#     price = Column(Float, nullable=False)
#     is_early_bird = Column(Boolean, default=False)

# # Create tables in the database
# Base.metadata.create_all(bind=engine)

# # Pydantic Model for validation
# class CourseSchema(BaseModel):
#     id: Optional[int] = None
#     name: str
#     price: float
#     is_early_bird: Optional[bool] = None

#     class Config:
#         orm_mode = True

# # FastAPI app instance
# app = FastAPI()

# # Dependency to get a database session
# def get_db():
#     db = SessionLocal()
#     try:
#         yield db
#     finally:
#         db.close()

# # Root endpoint
# @app.get("/")
# def read_root():
#     return {"message": "Hello, Welcome to FastAPI with PostgreSQL!"}

# # Retrieve all courses
# @app.get("/courses", response_model=List[CourseSchema])
# def get_courses(db: Session = Depends(get_db)):
#     return db.query(CourseDB).all()

# # Retrieve a single course by ID
# @app.get("/courses/{course_id}", response_model=CourseSchema)
# def get_course(course_id: int, db: Session = Depends(get_db)):
#     course = db.query(CourseDB).filter(CourseDB.id == course_id).first()
#     if not course:
#         raise HTTPException(status_code=404, detail="Course not found")
#     return course

# # Add a new course
# @app.post("/courses", response_model=CourseSchema)
# def create_course(course: CourseSchema, db: Session = Depends(get_db)):
#     new_course = CourseDB(**course.dict())
#     db.add(new_course)
#     db.commit()
#     db.refresh(new_course)
#     return new_course

# # Update a course
# @app.put("/courses/{course_id}", response_model=CourseSchema)
# def update_course(course_id: int, course: CourseSchema, db: Session = Depends(get_db)):
#     existing_course = db.query(CourseDB).filter(CourseDB.id == course_id).first()
#     if not existing_course:
#         raise HTTPException(status_code=404, detail="Course not found")
#     for key, value in course.dict().items():
#         setattr(existing_course, key, value)
#     db.commit()
#     db.refresh(existing_course)
#     return existing_course

# # Delete a course
# @app.delete("/courses/{course_id}")
# def delete_course(course_id: int, db: Session = Depends(get_db)):
#     course = db.query(CourseDB).filter(CourseDB.id == course_id).first()
#     if not course:
#         raise HTTPException(status_code=404, detail="Course not found")
#     db.delete(course)
#     db.commit()
#     return {"message": "Course deleted successfully"}





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

