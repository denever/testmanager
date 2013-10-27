import sys
from sqlalchemy.orm import sessionmaker
from model import engine, Topic, Question

if __name__ == '__main__':
    Session = sessionmaker(bind=engine)
    session = Session()

    for topic in session.query(Topic).order_by(Topic.id):
        print '\t', topic.id, topic.title, topic.did_unit

    topic_id = raw_input("Select topic to add questions: ")
    if not topic_id:
        sys.exit(1)
    topic_id = int(topic_id)
    current_topic = session.query(Topic).filter(Topic.id == topic_id).first()

    data = dict()
    loop = True
    while loop:
        data['qtype'] = raw_input("Type: ")
        data['question'] = raw_input("Question: ")
        if data['qtype'] in ('BC','bc','b'):
            data['answers'] = '\\item Vero\n\\item Falso'
        else:
            subloop = True
            answer_id = 1
            data['answers'] = str()
            while subloop:
                answer = raw_input('Answer %s:' % answer_id)
                if not answer: break
                data['answers'] += '\\item %s\n' % answer
                answer_id += 1
        qa = Question(**data)
        qa.topic = current_topic
        session.add(qa)
        session.commit()
        loop = False if raw_input("Continue? ") in ("N",'n','No','no') else True
