from sqlalchemy.orm import sessionmaker
from model import engine
from utils import select_subject

if __name__ == '__main__':
    Session = sessionmaker(bind=engine)
    session = Session()

    data = dict()
    loop = True
    while loop:
        subject = select_subject(session)
        if not subject: continue
        print 'Deleting subject %s' % subject
        session.delete(subject)
        session.commit()
