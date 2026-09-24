from fastapi import FastAPI
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