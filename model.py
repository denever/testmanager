from sqlalchemy import engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, Boolean, ForeignKey, Text
from sqlalchemy.orm import relationship
from sqlalchemy.schema import UniqueConstraint
from sqlalchemy.types import Enum

engine = engine.create_engine('sqlite:///prova.db')
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

    def __str__(self):
        return 'Alumn %s %s %s' % (self.surname, self.name, self.dsa)

class AlumnClass(Base):
    __tablename__ = 'classes'

    id = Column(Integer, primary_key=True)
    name = Column(String, unique=True)
    alumns = relationship("Alumn", backref='belongs')

    def dsa_alumns(self):
        return [alumn for alumn in self.alumns if alumn.dsa]

    def __repr__(self):
        return "<%s: %s %s>" % (self.__tablename__, self.id, self.name)

class Topic(Base):
    __tablename__ = 'topics'

    id = Column(Integer, primary_key=True)
    did_unit = Column(String, unique=True)
    title = Column(String)
    questions = relationship("Question", backref='topic')

    def __repr__(self):
        return "<%s: %s %s>" % (self.__tablename__, self.id, self.title)

class Question(Base):
    __tablename__ = 'questions'

    id = Column(Integer, primary_key=True)
    question = Column(String)
    answers = Column(Text)
    qtype = Column(Enum('BC', 'SC', 'MC', 'OC'))
    topic_id = Column(Integer, ForeignKey('topics.id'))

    def __init__(self, qtype, question, answers):
        self.qtype = qtype
        self.question = question
        self.answers = answers

    def __repr__(self):
        return "<%s: %s %s>" % (self.__tablename__, self.qtype, self.question)

Base.metadata.create_all(engine)
