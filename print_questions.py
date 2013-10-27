from sqlalchemy.orm import sessionmaker
from model import engine, Topic, Question

try:
    from termcolor import colored
except ImportError:
    print 'Please install termcolor module'

def print_questions(session):
    print 'Questions in a topic'
    for topic in session.query(Topic).order_by(Topic.id):
        print '\t', topic.id, topic.title, topic.did_unit

    topic_id = raw_input('Select a topic id: ')

    if not topic_id: return False

    topic = session.query(Topic).filter(Topic.id == topic_id).first()
    for question in topic.questions:
        print str(question)
    return True

if __name__ == '__main__':
    Session = sessionmaker(bind=engine)
    session = Session()

    loop = True
    while loop:
        loop = print_questions(session)
#        loop = False if raw_input("Continue? ") in ("N",'n','No','no') else print_questions()
