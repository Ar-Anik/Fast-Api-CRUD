from sqlalchemy import String, Integer, Column
from database import Base, engine

class Person(Base):
    __tablename__ = 'persons'

    id = Column(Integer, primary_key=True)
    firstName = Column(String(50), nullable=False)
    lastName = Column(String(50), nullable=False)
    gender = Column(String(50))

Base.metadata.create_all(engine)
