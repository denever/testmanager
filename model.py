from sqlalchemy import engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, Boolean, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.orm import sessionmaker
from sqlalchemy.schema import UniqueConstraint

engine = engine.create_engine('sqlite:////home/denever/prova.db')
Base = declarative_base()

class Alumn(Base):
    __tablename__ = 'alumns'
    id = Column(Integer, primary_key=True)
    name = Column(String)
    surname = Column(String)
    dsa = Column(Boolean)
    class_id = Column(Integer, ForeignKey('classes.id'))

    UniqueConstraint('surname', 'name', name='uix_1')

    def __init__(self, name, surname, dsa=False):
        self.name = name
        self.surname = surname
        self.dsa = dsa

    def __repr__(self):
        return "<%s: %s %s %s>" % (self.__tablename__, self.surname, self.name, self.dsa)

class AlumnClass(Base):
    __tablename__ = 'classes'

    id = Column(Integer, primary_key=True)
    name = Column(String, unique=True)
    alumns = relationship("Alumn", backref='belongs')

    def __repr__(self):
        return "<%s: %s %s>" % (self.__tablename__, self.id, self.name)


Base.metadata.create_all(engine)
