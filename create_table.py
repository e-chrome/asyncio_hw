from sqlalchemy import (
    Column,
    Integer,
    String,
    create_engine,
)

from sqlalchemy.ext.declarative import declarative_base

PG_DSN = 'postgresql://app:1234@127.0.0.1:5431/netology'

engine = create_engine(PG_DSN)
Base = declarative_base()


class People(Base):
    __tablename__ = 'People'

    id = Column(Integer, primary_key=True)
    birth_year = Column(String(255))
    eye_color = Column(String(255))
    films = Column(String(255))
    gender = Column(String(255))
    hair_color = Column(String(255))
    height = Column(String(255))
    homeworld = Column(String(255))
    mass = Column(String(255))
    name = Column(String(255))
    skin_color = Column(String(255))
    species = Column(String(255))
    starships = Column(String(255))
    vehicles = Column(String(255))


async def create_table():
    if not engine.dialect.has_table(engine.connect(), 'People'):
        Base.metadata.create_all(engine)

