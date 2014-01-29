# encoding: utf-8
import sys
from sqlalchemy.orm import sessionmaker
from model import engine, Topic, Question, Answer
from utils import select_topic, select_subject, safe_prompt

if __name__ == '__main__':
    Session = sessionmaker(bind=engine)
    session = Session()

    current_topic = None
    while True:
        subject = select_subject(session)
        current_topic = select_topic(session, subject)
        if not current_topic: continue
        break
    
    data = dict()
    loop = True
    while loop:
        data['qtype'] = safe_prompt(session, "Type ('BC', 'SC', 'MC', 'OC'): ")
        if not data['qtype']:
            loop = False if safe_prompt(session, "Continue? ") in ("N",'n','No','no') else True
            continue

        data['question'] = safe_prompt(session, "Question: ")
        if not data['question']:
            loop = False if safe_prompt(session, "Continue? ") in ("N",'n','No','no') else True
            continue

        qa = Question(**data)
        qa.topic = current_topic
        session.add(qa)
        session.commit()
        
        if data['qtype'] in ('BC','bc','b'):
            true = Answer('Vero')
            true.question = qa
            false = Answer('Falso')
            false.question = qa
            session.add(true)
            session.add(false)
        else:
            subloop = True
            answer_id = 1            
            while subloop:
                answer = safe_prompt(session, 'Answer %s: ' % answer_id)
                if not answer: break
                answ = Answer(answer)
                answ.question = qa
                session.add(answ)
                answer_id += 1
        session.add(qa)
        session.commit()
#        loop = False if safe_prompt(session, "Continue? ") in ("N",'n','No','no') else True
