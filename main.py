import random
from sqlalchemy.orm import sessionmaker
from model import engine, Alumn, AlumnClass, Question, Topic

def create_test():
    print 'Print test for a class'
    for cls in session.query(AlumnClass).order_by(AlumnClass.id):
        print '\t', cls.id, cls.name

    cls_id = raw_input('Select a class id: ')

    if not cls_id: return False

    cls = session.query(AlumnClass).filter(AlumnClass.id == cls_id).first()

    if not cls: return False

    loop = True
    topic_sequence = list()
    topic_ids = list()
    while loop:
        for topic in session.query(Topic).order_by(Topic.id):
            print '\t', topic.id, topic.title, topic.did_unit

        topic_id = raw_input('Select topics sequence [%s]: ' % ','.join(topic_ids))
        if not topic_id: break

        topic = session.query(Topic).filter(Topic.id == int(topic_id)).first()

        if not topic: continue

        topic_sequence.append(topic)
        topic_ids.append(topic_id)

    for alumn in cls.alumns:
        for topic in topic_sequence:
            questions = topic.questions
            if alumn.dsa:
                questions = [ question for question in topic.questions if question.qtype != 'OC' ]
            test = list()
            loop = True
            while len(test) < len(topic_sequence):
                random_choice = random.choice(questions)
                if random_choice not in test:
                    test.append(random_choice)
            print test
    return True


if __name__ == '__main__':
    Session = sessionmaker(bind=engine)
    session = Session()

    loop = True
    while loop:
        loop = create_test()
#        loop = False if raw_input("Continue? ") in ("N",'n','No','no') else print_alumns()
