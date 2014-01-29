from sqlalchemy.orm import sessionmaker
from model import engine, Topic, Subject
from utils import select_subject, print_topics, safe_prompt

if __name__ == '__main__':
    Session = sessionmaker(bind=engine)
    session = Session()

    loop = True
    data = dict()

    current_subject = None
    while True:
        current_subject = select_subject(session)
        if not current_subject: continue
        break

    while loop:
        data['did_unit'] = safe_prompt(session, "Didactic Unit: ")
        if not data['did_unit']: break
        data['title'] = safe_prompt(session, "Topic Title: ")
        if not data['title']: break
        topic = Topic(**data)
        print topic
        topic.subject = current_subject
        session.add(topic)
        session.commit()
        print 'Topic %(title)s created.' % data
        print_topics(session, current_subject)
