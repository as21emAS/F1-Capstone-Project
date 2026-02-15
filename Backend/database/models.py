from sqlalchemy import Column, Integer, String, Float, Date, ForeignKey, Time
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship


Base = declarative_base()

class Driver(Base):
    __tablename__ = "drivers"
    
    driver_id = Column(Integer, primary_key=True)
    name = Column(String)
    nationality = Column(String)
    date_of_birth = Column(Date)
   