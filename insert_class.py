from sqlalchemy.orm import sessionmaker
from model import engine, Alumn, AlumnClass, Question
from utils import print_classes, select_subject, safe_prompt

if __name__ == '__main__':
    Session = sessionmaker(bind=engine)
    session = Session()

    loop = True
    data = dict()
    while loop:
        data['name'] = safe_prompt(session, "Class name: ")
        if not data['name']: break
        ac = AlumnClass(name=data['name'])
        print ac
        ac.subject = select_subject(session)
        session.add(ac)
        session.commit()
        print 'Class %(name)s created.' % data
        loop = False if safe_prompt(session, 'Create another class? ') in ("N",'n','No','no') else True

    print_classes(session)
