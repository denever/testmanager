from sqlalchemy.orm import sessionmaker
from model import engine, Topic, Question, Answer, safe_prompt
from print_questions import print_questions, select_questions
import re
import sys

match_command = re.compile('(?P<command>\w)(?P<ans_id>\d+)(-(?P<ans2_id>\d+)){0,1}(:(?P<q_id>\d+)){0,1}')

try:
    from termcolor import colored
except ImportError:
    print 'Please install termcolor module'

def print_question(question):
    if question.answers_count % 2 == 1 or question.answers_count == 0:
        try:
            print colored(question.id, 'red'), question
        except NameError:
            print '>>>>>>', question.id, question, '<<<<<<'
    else:
        print question.id, question
    last_id = int(0)
    for answer in question.answers:
        print '\t',answer.id, answer
        last_id = answer.id
    return last_id

def print_available_answers(session, id_answ):
    answers_noassoc = session.query(Answer).filter(Answer.question == None).filter(Answer.id <= id_answ).all()
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
    questions = list()
    try:
        start_id = sys.argv[1]
        questions = session.query(Question).filter(Question.id >= start_id)
    except:
        questions = session.query(Question).all()



    for question in questions:
        last_id = print_question(question)
        if safe_prompt(session, "Edit this question? ") in ("Y",'y','Yes','yes'):
            while True:
                print_available_answers(session, last_id)
                command = re.match(match_command, safe_prompt(session, "Command: "))
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
                if command.group('command') == 'A':
                    ans_id = int(command.group('ans_id'))
                    ans2_id = int(command.group('ans2_id'))
                    q_id = int(command.group('q_id'))
                    print ans_id, ans2_id, q_id
                    selected = session.query(Question).filter(Question.id == q_id).first()
                    answers = session.query(Answer).filter(Answer.id >= ans_id).filter(Answer.id <= ans2_id)
                    for answer in answers:
                        print answer
                        answer.question = selected
                        session.add(answer)
                        session.commit()
                if command.group('command') == 'p':
                    ans_id = int(command.group('ans_id'))
                    print_available_answers(session, ans_id)
                if command.group('command') == 'U':
                    ans_id = int(command.group('ans_id'))
                    ans2_id = int(command.group('ans2_id'))
                    answers = session.query(Answer).filter(Answer.id >= ans_id).filter(Answer.id <= ans2_id)
                    for answer in answers:
                        print answer
                        answer.question = None
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
