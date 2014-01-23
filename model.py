from sqlalchemy import engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, Boolean, ForeignKey, Text
from sqlalchemy.orm import relationship
from sqlalchemy.schema import UniqueConstraint
from sqlalchemy.types import Enum, Date

engine = engine.create_engine('sqlite:///prova.db')
Base = declarative_base()

class Alumn(Base):
    __tablename__ = 'alumns'
    id = Column(Integer, primary_key=True)
    name = Column(String)
    surname = Column(String)
    dsa = Column(Boolean)
    class_id = Column(Integer, ForeignKey('classes.id'))
    tests = relationship("Test", backref="alumn")

    UniqueConstraint('surname', 'name', name='uix_1')

    def __init__(self, name, surname, dsa=False):
        self.name = name
        self.surname = surname
        self.dsa = dsa

    def __repr__(self):
        return "<%s: %s %s %s>" % (self.__tablename__, self.surname, self.name, self.dsa)

    def __str__(self):
        return '%s %s' % (self.surname, self.name)

class AlumnClass(Base):
    __tablename__ = 'classes'

    id = Column(Integer, primary_key=True)
    name = Column(String, unique=True)
    alumns = relationship("Alumn", backref='belongs')
    subject_id = Column(Integer, ForeignKey('subjects.id'))
    
    def dsa_alumns(self):
        return [alumn for alumn in self.alumns if alumn.dsa]

    def __repr__(self):
        return "<%s: %s %s>" % (self.__tablename__, self.id, self.name)

    def __str__(self):
        return self.name

class Subject(Base):
    __tablename__ = 'subjects'
    id = Column(Integer, primary_key=True)
    name = Column(String)
    topics = relationship("Topic", backref='subject')
    classes = relationship("AlumnClass", backref='subject')
    
    def __repr__(self):
        return "<%s: %s %s>" % (self.__tablename__, self.id, self.name)

    def __str__(self):
        return self.name

class Topic(Base):
    __tablename__ = 'topics'

    id = Column(Integer, primary_key=True)
    did_unit = Column(String, unique=True)
    title = Column(String)
    questions = relationship("Question", backref='topic')
    subject_id = Column(Integer, ForeignKey('subjects.id'))

    def __repr__(self):
        return "<%s: %s %s>" % (self.__tablename__, self.id, self.title)

    def __str__(self):
         return "%s %s Questions count: %s" % (self.did_unit, self.title, len(self.questions))

class Question(Base):
    __tablename__ = 'questions'

    id = Column(Integer, primary_key=True)
    question = Column(String)
    #answers = Column(Text)
    answers = relationship("Answer", backref='question')    
    qtype = Column(Enum('BC', 'SC', 'MC', 'OC'))
    topic_id = Column(Integer, ForeignKey('topics.id'))

    def __init__(self, qtype, question):
        self.qtype = qtype
        self.question = question

    def __repr__(self):
        return "<%s: %s %s>" % (self.__tablename__, self.qtype, self.question)
        return "%s Question (UD: %s) (Type %s): %s" % (self.id, self.topic.did_unit, self.qtype, self.question)#, self.answers)

    def __str__(self):
        return "%s (UD: %s, Tipo: %s)" % (self.question, self.topic.did_unit, self.qtype)

    @property
    def answers_count(self):
        return len(self.answers)

class Answer(Base):
    __tablename__ = 'answers'

    id = Column(Integer, primary_key=True)    
    question_id = Column(Integer, ForeignKey('questions.id'))
    answer_text = Column(Text)
    correct = Column(Boolean)

    def __init__(self, text, correct=False):
        self.answer_text = text
        self.correct = correct

    def __repr__(self):
        return "<%s: %s %s>" % (self.__tablename__, self.answer_text,
                                self.correct)

    def __str__(self):
        return self.answer_text
        
class TestQuestionAssoc(Base):
    __tablename__ = 'test_question_assoc'
    left_id = Column(Integer, ForeignKey('tests.id'), primary_key=True)
    right_id = Column(Integer, ForeignKey('questions.id'), primary_key=True)
    position = Column(Integer(50))
    question = relationship("Question")

class Test(Base):
    __tablename__ = 'tests'

    id = Column(Integer, primary_key=True)
    title = Column(String)
    date = Column(Date)
    alumn_id = Column(Integer, ForeignKey('alumns.id'))
    questions = relationship("TestQuestionAssoc")
    printed = Column(Boolean)
    submitted = Column(Boolean)
    vote = Column(Integer)

    def __init__(self, title, date, alumn, printed=False, submitted=True, vote=0):
        self.title = title
        self.date = date
        self.alumn = alumn
        self.printed = printed
        self.submitted = submitted
        self.vote = vote

Base.metadata.create_all(engine)
