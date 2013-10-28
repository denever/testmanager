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
        print question.id, question.question
    return True

def select_questions(session):
    id_selected = raw_input("Select question: ")
    if not id_selected:
        return False
    id_selected = int(id_selected)
    question = session.query(Question).filter(Question.id == id_selected).first()
    return question

if __name__ == '__main__':
    Session = sessionmaker(bind=engine)
    session = Session()

    loop = True
    while loop:
        loop = print_questions(session)
        if not loop: continue
        loop = select_questions(session)
        if not loop: continue
        print loop
        print loop.answers
#        loop = False if raw_input("Continue? ") in ("N",'n','No','no') else print_questions()
