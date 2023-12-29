from fastapi import FastAPI
from pydantic import BaseModel
import sqlite3

app = FastAPI()

class CourseCreate(BaseModel):
    title:str
    teacher:str

class Course(BaseModel):
    id:int
def create_connection():
    conn = sqlite3.connect("courses.db")
    return conn    


@app.get("/")
def read_root():
    return {"message":" Welcome!"}

def create_table():
    conn = create_connection()
    cr = conn.cursor()
    cr.execute("""
    CREATE TABLE IF NOT EXISTS courses (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    title TEXT NOT NULL,
    teacher TEXT NOT NULL
    )
    """)
    conn.commit()
    conn.close()

    create_table()

def create_course(course: CourseCreate):
    conn = create_connection()
    cr = conn.cursor()
    cr.execute("INSERT INTO courses (title, teacher) VALUES (?,?)", (course.title, course.teacher))
    conn.commit()
    conn.close()

@app.post("/courses/")
def create_course_endpoint(course: CourseCreate):
    course_id = create_course(course)
    return {"id": course_id, **course.dict()}

