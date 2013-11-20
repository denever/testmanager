from sqlalchemy.orm import sessionmaker
from model import engine, Alumn, AlumnClass, Question
import sys

try:
    from termcolor import colored
except ImportError:
    print 'Please install termcolor module'
    def colored(color, string):
        return string

def select_class(session):
    print 'Alumns in a class'
    for cls in session.query(AlumnClass).order_by(AlumnClass.id):
        print '\t', cls.id, cls.name

    cls_id = raw_input('Select a class id: ')

    if not cls_id: return False

    return cls_id

def print_alumns(session, cls_id):
    cls = session.query(AlumnClass).filter(AlumnClass.id == cls_id).first()

    if not cls: return False

    for alumn in cls.alumns:
        print '\t', alumn.id, alumn.surname, alumn.name, 'DSA:', colored('Yes', 'yellow') if alumn.dsa else 'No'
    return True


if __name__ == '__main__':
    Session = sessionmaker(bind=engine)
    session = Session()

    loop = True
    while loop:
        cls_id = select_class(session)
        if not cls_id: continue
        loop = print_alumns(session, cls_id)
#        loop = False if raw_input("Continue? ") in ("N",'n','No','no') else print_alumns()
