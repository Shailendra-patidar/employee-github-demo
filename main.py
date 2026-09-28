from fastapi import FastAPI
from pydantic import BaseModel
from sqlalchemy import create_engine, Column, Integer, String, Float, Boolean
from sqlalchemy.orm import declarative_base, sessionmaker

app = FastAPI(title="Employee Management API")


# Database configuration

DATABASE_URL = "sqlite:///./database/employee.db"

engine = create_engine(
    DATABASE_URL,
    connect_args={"check_same_thread": False}
)

SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine
)

Base = declarative_base()


class EmployeeCreate(BaseModel):
    name: str
    age: int
    department: str
    salary: float

# Employee table

class Employee(Base):
    __tablename__ = "employees"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    age = Column(Integer, nullable=False)
    department = Column(String, nullable=False)
    salary = Column(Float, nullable=False)
    is_active = Column(Boolean, default=True)


# Create database table

Base.metadata.create_all(bind=engine)


@app.get("/")
def home():
    return {
        "message": "Employee Management API is running"
    }

@app.get("/employees")
def get_employees():
    db = SessionLocal()

    employees = db.query(Employee).all()

    db.close()

    return employees


@app.post("/employees")
def create_employee(employee: EmployeeCreate):
    db = SessionLocal()

    new_employee = Employee(
        name=employee.name,
        age=employee.age,
        department=employee.department,
        salary=employee.salary
    )

    db.add(new_employee)
    db.commit()
    db.refresh(new_employee)

    db.close()

    return new_employee

