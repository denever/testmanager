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

if __name__ == '__main__':
    Session = sessionmaker(bind=engine)
    session = Session()

    loop = True
    data = dict()
    while loop:
        data['name'] = raw_input("Class name: ")
        if not data['name']: break
        ac = AlumnClass(name=data['name'])
        print ac
        session.add(ac)
        session.commit()
        print 'Class %(name)s created.' % data
        loop = False if raw_input('Create another class? ') in ("N",'n','No','no') else True

    data = dict()
    loop = True
    while loop:
        data['name'] = raw_input("Name: ")
        data['surname'] = raw_input("Surame: ")
        data['dsa'] = True if raw_input("dsa: ") in ("Y",'y','Yes','yes') else False
        alumn = Alumn(**data)
        print 'Alumn %(surname)s %(name)s %(dsa)s created.' % data
        print alumn
        alumn.belongs = session.query(AlumnClass).first()
        session.add(alumn)
        session.commit()
        loop = False if raw_input("Continue? ") in ("N",'n','No','no') else True
