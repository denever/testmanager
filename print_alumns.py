from sqlalchemy.orm import sessionmaker
from model import engine, Alumn, AlumnClass, Question

try:
    from termcolor import colored
except ImportError:
    print 'Please install termcolor module'

def print_alumns():
    print 'Alumns in a class'
    for cls in session.query(AlumnClass).order_by(AlumnClass.id):
        print '\t', cls.id, cls.name

    cls_id = raw_input('Select a class id: ')

    if not cls_id: return False

    cls = session.query(AlumnClass).filter(AlumnClass.id == cls_id).first()
    for alumn in cls.alumns:
        print '\t', alumn.surname, alumn.name, 'DSA:', colored('Yes', 'yellow') if alumn.dsa else 'No'
    return True


if __name__ == '__main__':
    Session = sessionmaker(bind=engine)
    session = Session()

    loop = True
    while loop:
        loop = print_alumns()
#        loop = False if raw_input("Continue? ") in ("N",'n','No','no') else print_alumns()
