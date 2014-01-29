from sqlalchemy.orm import sessionmaker
from model import engine, Alumn, AlumnClass, Question
from utils import print_alumns, select_class, select_alumn, safe_prompt

if __name__ == '__main__':
    Session = sessionmaker(bind=engine)
    session = Session()

    data = dict()
    loop = True
    while loop:
        cls_id = select_class(session)
        if not cls_id: continue
        alumn = select_alumn(session, cls_id)

        data['surname'] = safe_prompt(session, "Surname: [%s]" % alumn.surname)
        if data['surname']:
            alumn.surname = data['surname']
            session.add(alumn)
            session.commit()

        data['name'] = safe_prompt(session, "Name: [%s]" % alumn.name)
        if data['name']:
            alumn.name = data['name']
            session.add(alumn)
            session.commit()

        data['dsa'] = True if safe_prompt(session, "dsa: [%s]" % alumn.dsa) in ("Y",'y','Yes','yes') else False
        if data['dsa']:
            alumn.dsa = data['dsa']
            session.add(alumn)
            session.commit()

        print alumn
        print 'Assign to a class'
        cls = select_class(session)
        alumn.belongs = cls
        session.add(alumn)
        session.commit()
