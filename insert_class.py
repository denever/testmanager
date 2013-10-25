from sqlalchemy.orm import sessionmaker
from model import engine, Alumn, AlumnClass, Question

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
