from sqlalchemy.orm import sessionmaker
from model import engine, Topic, Subject, Question
import sys

try:
    from termcolor import colored
except ImportError:
    print 'Please install termcolor module'
    def colored(color, string):
        return string

def select_subject(session):
    print 'Subject available'
    for sbj in session.query(Subject).order_by(Subject.id):
        print '\t', sbj.id, sbj.name

    sbj_id = raw_input('Select a subject id: ')

    if not sbj_id: return False

    return session.query(Subject).filter(Subject.id == sbj_id).first()

def print_topics(session, sbj):
    if not sbj: return False

    for topic in sbj.topics:
        print '\t', topic
    return True


if __name__ == '__main__':
    Session = sessionmaker(bind=engine)
    session = Session()

    loop = True
    while loop:
        sbj = select_subject(session)
        if not sbj: break
        loop = print_topics(session, sbj)
#        loop = False if raw_input("Continue? ") in ("N",'n','No','no') else print_alumns()
