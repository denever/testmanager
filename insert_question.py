from sqlalchemy.orm import sessionmaker
from model import engine, Alumn, AlumnClass, Question

if __name__ == '__main__':
    Session = sessionmaker(bind=engine)
    session = Session()
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
                print data['answers']
                answer_id += 1
        qa = Question(**data)
        session.add(qa)
        session.commit()
