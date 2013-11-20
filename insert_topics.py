from sqlalchemy.orm import sessionmaker
from model import engine, Topic, Subject

if __name__ == '__main__':
    Session = sessionmaker(bind=engine)
    session = Session()

    loop = True
    data = dict()

    for subject in session.query(Subject).order_by(Subject.id):
        print '\t', subject.id, subject.name

    subject_id = raw_input("Select subject to add topics: ")
    if not subject_id:
        sys.exit(1)
    subject_id = int(subject_id)
    current_subject = session.query(Subject).filter(Subject.id == subject_id).first()

    while loop:
        data['did_unit'] = raw_input("Didactic Unit: ")
        if not data['did_unit']: break
        data['title'] = raw_input("Topic Title: ")
        if not data['title']: break
        topic = Topic(**data)
        print topic
        topic.subject = current_subject
        session.add(topic)
        session.commit()
        print 'Topic %(title)s created.' % data
        loop = False if raw_input('Create another topic? ') in ("N",'n','No','no') else True

    for topic in session.query(Topic).order_by(Topic.id):
        print '\t', topic.id, topic.title, topic.did_unit
