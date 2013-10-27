import random
from datetime import datetime
from sqlalchemy.orm import sessionmaker
from model import engine, Alumn, AlumnClass, Question, Topic, Test, TestQuestionAssoc

def create_test():
    print 'Create test for a class...'
    title = raw_input('Test title: ')
    if not title: return False

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
        current_test = Test(title=title, date=datetime.today(), alumn=alumn)
        question_selected = list()
        while len(question_selected) < len(topic_sequence):
            for topic in topic_sequence:
                questions = topic.questions
                if alumn.dsa:
                    questions = [ question for question in topic.questions if question.qtype != 'OC' ]
                random_choice = random.choice(questions)
                if random_choice not in question_selected:
                    question_selected.append(random_choice)
        for pos, question in enumerate(question_selected):
            print pos, question.id
            a = TestQuestionAssoc(position=pos)
            a.question = question
            current_test.questions.append(a)
        session.add(current_test)
        session.commit()
    return True


if __name__ == '__main__':
    Session = sessionmaker(bind=engine)
    session = Session()

    loop = True
    while loop:
        loop = create_test()
