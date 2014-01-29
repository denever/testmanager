import readline
from sqlalchemy.orm import sessionmaker
from model import engine, Topic, Question, Answer
from utils import print_question, print_questions, select_question, safe_prompt

def print_answers_not_associated(session, id_answ):
    answers_noassoc = session.query(Answer).filter(Answer.question == None).filter(Answer.id < id_answ)
    for answer in answers_noassoc:
        print answer.id, answer
    return True
    
def select_answers(session):
    id_selected = safe_prompt(session, "Select answer: ")
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
            if safe_prompt(session, "Assign all this answers? ") in ("N",'n','No','no'):
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
            if safe_prompt(session, "Continue? ") in ("N",'n','No','no'):
                break
            else:
                continue
