from sqlalchemy.orm import sessionmaker
from model import engine, Topic, Question, Answer
from print_questions import print_questions, select_questions

try:
    from termcolor import colored
except ImportError:
    print 'Please install termcolor module'

def print_question(question):
    last_id = int(0)
    print question.id, question
    for answer in question.answers:
        print '\t',answer.id, answer
        last_id = answer.id
    return last_id

def print_answers_not_associated(session, id_answ):
    answers_noassoc = session.query(Answer).filter(Answer.question == None).filter(Answer.id < id_answ)
    for answer in answers_noassoc:
        print answer.id, answer
    return True
    
def select_answers(session):
    id_selected = raw_input("Select answer: ")
    if not id_selected:
        return False
    id_selected = int(id_selected)
    answer = session.query(Answer).filter(Answer.id == id_selected).first()
    return answer

if __name__ == '__main__':
    Session = sessionmaker(bind=engine)
    session = Session()

    questions = session.query(Question).all()
    for question in questions:
        if question.answers_count % 2 == 1:
            print_question(question)
            last_id = question.answers[-1].id
            print 'last_id', last_id
            answers_noassoc = session.query(Answer).filter(Answer.question == None).filter(Answer.id < last_id).all()
            for answer in answers_noassoc:
                print answer.id, answer
            if raw_input("Assign all this answers? ") in ("N",'n','No','no'):
                answer = select_answers(session)
                if not answer: break
                answer.question = question
                session.add(answer)
                session.commit()
            else:
                for answer in answers_noassoc:
                    answer.question = question
                    session.add(answer)
                    session.commit()
            print_question(question)
            if raw_input("Continue? ") in ("N",'n','No','no'):
                break
            else:
                continue
