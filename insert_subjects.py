from sqlalchemy.orm import sessionmaker
from model import engine, Subject
from utils import print_subjects, safe_prompt

if __name__ == '__main__':
    Session = sessionmaker(bind=engine)
    session = Session()

    loop = True
    data = dict()
    while loop:
        data['name'] = safe_prompt(session, "Subject name: ")
        if not data['name']: break
        subject = Subject(**data)
        session.add(subject)
        session.commit()
        print 'Subject %(name)s created.' % data
        print_subjects(session)
            
