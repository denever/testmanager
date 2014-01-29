import sys
from model import *

try:
    from termcolor import colored
except ImportError:
    print 'Please install termcolor module'
    def colored(string, color):
        return '>>>>>', string, '<<<<'

def safe_prompt(session, message):
    try:
        return raw_input(message)
    except KeyboardInterrupt:
        if raw_input("\n\tSave changes? ") in ("Y",'y','Yes','yes'):
            session.commit()
            session.close()
        sys.exit(0)
    except EOFError:
        if raw_input("\n\tSave changes? ") in ("Y",'y','Yes','yes'):
            session.commit()
            session.close()
        sys.exit(0)

def select_subject(session):
    print 'Subject available'
    for sbj in session.query(Subject).order_by(Subject.id):
        print '\t', sbj.id, sbj.name

    sbj_id = safe_prompt(session, 'Select a subject id: ')

    if not sbj_id: return False

    return session.query(Subject).filter(Subject.id == sbj_id).first()

def select_topic(session, sbj):
    print 'Topics available in %s' % sbj
    for tpc in session.query(Topic).filter(Topic.subject == sbj).order_by(Topic.id):
        print '\t', tpc.id, tpc

    tpc_id = safe_prompt(session, 'Select a topic id: ')

    if not tpc_id: return False

    return session.query(Topic).filter(Topic.id == tpc_id).first()

def select_class(session):
    print 'Select a class:'
    for cls in session.query(AlumnClass).order_by(AlumnClass.id):
        print '\t', cls.id, cls.name

    cls_id = safe_prompt(session, 'Select a class id: ')

    if not cls_id: return False

    return session.query(AlumnClass).filter(AlumnClass.id == cls_id).first()

def select_alumn(session, cls):
    print 'Select alumn:'
    print_alumns(session, cls)
    alumn_id = safe_prompt(session, 'Select an alumn id: ')

    if not alumn_id: return False

    return session.query(Alumn).filter(Alumn.id == alumn_id).first()

def print_classes(session):
    print 'Classes'
    for cls in session.query(AlumnClass).order_by(AlumnClass.id):
        print '\t', cls.id, cls.name, cls.subject
    return True

def print_topics(session, sbj):
    if not sbj: return False
    print 'Topics available in %s' % sbj
    for topic in sbj.topics:
        print '\t', topic
    return True

def print_questions(session):
    subject = select_subject(session)
    topic = select_topic(session, subject)
    for question in topic.questions:
        print question.id, question.question, question.answers_count
    return True

def select_question(session):
    print_questions(session)
    id_selected = safe_prompt(session, "Select question: ")
    if not id_selected:
        return False
    id_selected = int(id_selected)
    question = session.query(Question).filter(Question.id == id_selected).first()
    return question

def print_question(question):
    if question.answers_count % 2 == 1 or question.answers_count == 0:
        print colored(question.id, 'red'), question
    else:
        print question.id, question
    last_id = int(0)
    for answer in question.answers:
        print '\t',answer.id, answer
        last_id = answer.id
    return last_id

def print_alumns(session, cls):
    if not cls: return False

    for alumn in cls.alumns:
        print '\t', alumn.id, alumn.surname, alumn.name, 'DSA:', colored('Yes', 'yellow') if alumn.dsa else 'No'
    print 'Total alumns:', len(cls.alumns)
    return True

def print_answers(session, question):
    for answer in question.answers:
        print '\t', answer.id, answer
    return True

def select_answers(session, question):
    print_answers(session, question)
    id_selected = safe_prompt(session, "Select answer: ")
    if not id_selected:
        return False
    id_selected = int(id_selected)
    answer = session.query(Answer).filter(Answer.id == id_selected).first()
    return answer

def print_subjects(session):
    print 'Subjects'
    for subject in session.query(Subject).order_by(Subject.id):
        print '\t', subject.id, subject.name
    return True
