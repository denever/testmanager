from sqlalchemy.orm import sessionmaker
from model import engine, Topic, Question, Answer
from print_questions import print_questions, select_questions
import re

match_command = re.compile('(?P<command>\w)(?P<ans_id>\d+):(?P<q_id>\d+)')

try:
    from termcolor import colored
except ImportError:
    print 'Please install termcolor module'

def print_question(question):
    if question.answers_count % 2 == 1:
        print colored(question.id, 'red'), question
    else:
        print question.id, question
    for answer in question.answers:
        print '\t',answer.id, answer

# def print_answers(session):
#     answers_noassoc = session.query(Answer).filter(Answer.id < id_answ)
#     for answer in answers_noassoc:
#         print answer.id, answer
#     return True

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
        print_question(question)
        if raw_input("Edit this question? ") in ("Y",'y','Yes','yes'):
            while True:
                command = re.match(match_command, raw_input("Command: "))
                print '#',command,'#'
                if not command: break
                if command.group('command') == 'u':
                    id_selected = int(command.group('ans_id'))
                    answer = session.query(Answer).filter(Answer.id == id_selected).first()
                    answer.question = None
                    session.add(answer)
                    session.commit()
                if command.group('command') == 'a':
                    ans_id = int(command.group('ans_id'))
                    q_id = int(command.group('q_id'))
                    answer = session.query(Answer).filter(Answer.id == ans_id).first()
                    answer.question = session.query(Question).filter(Question.id == q_id).first()
                    session.add(answer)
                    session.commit()
                print_question(question)
    # loop = True
    # while loop:
    #     loop = print_questions(session)
    #     if not loop: continue
    #     loop = select_questions(session)
    #     if not loop: continue
    #     selected_question = loop
    #     last_id = print_question(loop)
    #     while loop:
    #         print_answers_not_associated(session)
    #         answer = select_answers(session)
    #         if not answer: break
    #         answer.question = selected_question
    #         session.add(answer)
    #         session.commit()
    #         print_question(loop)
