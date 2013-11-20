from sqlalchemy.orm import sessionmaker
from model import engine, Alumn, AlumnClass, Question
import sys

try:
    from termcolor import colored
except ImportError:
    print 'Please install termcolor module'
    def colored(color, string):
        return string

if __name__ == '__main__':
    Session = sessionmaker(bind=engine)
    session = Session()

    for cls in session.query(AlumnClass).order_by(AlumnClass.id):
        print '\t', cls.id, cls.name, cls.subject        
