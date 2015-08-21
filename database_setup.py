# Use this file to create the initial database for
# the chore list application

# import datetime

from sqlalchemy import Column, ForeignKey, Integer, String, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy import create_engine

Base = declarative_base()


class Chores(Base):
    __tablename__ = 'chores'   
    id = Column(Integer, primary_key=True)
    name = Column(String(250), nullable=False)
    worker_id = Column(Integer,ForeignKey('workers.id'))
    start_date = Column(DateTime)
    end_date = Column(DateTime)
    freq = Column(Integer)
    values = Column(String(250))


class Workers(Base):
    __tablename__ = 'workers'   
    id = Column(Integer, primary_key=True)
    name = Column(String(250), nullable=False)
    
    
engine = create_engine('sqlite:///chores.db')
Base.metadata.create_all(engine)