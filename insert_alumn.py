from sqlalchemy.orm import sessionmaker
from model import engine, Alumn, AlumnClass, Question
from utils import print_alumns, select_class, safe_prompt

if __name__ == '__main__':
    Session = sessionmaker(bind=engine)
    session = Session()

    data = dict()
    while True:
        data['surname'] = safe_prompt(session, "Surname: ")
        data['name'] = safe_prompt(session, "Name: ")
        data['dsa'] = True if safe_prompt(session, "dsa: ") in ("Y",'y','Yes','yes') else False
        alumn = Alumn(**data)
        print 'Alumn %(surname)s %(name)s %(dsa)s created.' % data
        print alumn

        cls = None
        while True:
            cls = select_class(session)
            if not cls: continue
            alumn.belongs = cls
            break
        session.add(alumn)
        session.commit()
        print_alumns(session, cls)
