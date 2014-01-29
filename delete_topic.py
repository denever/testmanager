from sqlalchemy.orm import sessionmaker
from model import engine
from utils import select_topic, select_subject

if __name__ == '__main__':
    Session = sessionmaker(bind=engine)
    session = Session()

    data = dict()
    loop = True
    while loop:
        subject = select_subject(session)
        topic = select_topic(session, subject)
        if not topic: continue
        print 'Deleting topic %s' % topic
        session.delete(topic)
        session.commit()
