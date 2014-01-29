from sqlalchemy.orm import sessionmaker
from model import engine, Alumn, AlumnClass, Question
from utils import print_alumns, select_class, safe_prompt

if __name__ == '__main__':
    Session = sessionmaker(bind=engine)
    session = Session()

    print 'Select class where to add alumn'
    current_class = None
    while True:
        current_class = select_class(session)
        if not current_class: continue
        break

    data = dict()
    while True:
        data['surname'] = safe_prompt(session, "Surname: ")
        data['name'] = safe_prompt(session, "Name: ")
        data['dsa'] = True if safe_prompt(session, "dsa: ") in ("Y",'y','Yes','yes') else False
        alumn = Alumn(**data)
        alumn.belongs = current_class
        print 'Alumn %(surname)s %(name)s %(dsa)s created.' % data
        print alumn
        session.add(alumn)
        session.commit()
        print_alumns(session, current_class)
