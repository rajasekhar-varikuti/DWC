# Import necessary modules and classes
from sqlalchemy import create_engine, Column, Integer, String, DateTime
import sqlalchemy
from sqlalchemy.orm import sessionmaker

# Database setup
DATABASE_URL = "sqlite:///./test.db"
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = sqlalchemy.orm.declarative_base()


class Customers(Base):
    __tablename__ = "customers"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    email = Column(String, index = True)
    status = Column(String)
    source = Column(String)

class Campaigns(Base):
    __tablename__ = 'campaigns'
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    status = Column(String)
    budget = Column(String)
    start_date = Column(DateTime)
    end_date = Column(DateTime)
    source = Column(String)

class TaskManger(Base):
    __tablename__ = 'taskmanager'
    id = Column(Integer, primary_key=True, index=True)
    task_id = Column(String)
    status = Column(String)


Base.metadata.create_all(bind=engine)



# Dependency to get the database session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()