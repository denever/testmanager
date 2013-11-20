from sqlalchemy.orm import sessionmaker
from model import engine, Subject

if __name__ == '__main__':
    Session = sessionmaker(bind=engine)
    session = Session()

    loop = True
    data = dict()
    while loop:
        data['name'] = raw_input("Subject name: ")
        if not data['name']: break
        subject = Subject(**data)
        session.add(subject)
        session.commit()
        print 'Subject %(name)s created.' % data
        loop = False if raw_input('Create another subject? ') in ("N",'n','No','no') else True

    for subject in session.query(Subject).order_by(Subject.id):
        print '\t', subject.id, subject.name
