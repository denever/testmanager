from sqlalchemy.orm import sessionmaker
from model import engine, Alumn, AlumnClass, Question

if __name__ == '__main__':
    Session = sessionmaker(bind=engine)
    session = Session()

    loop = True
    data = dict()
    while loop:
        data['name'] = raw_input("Class name: ")
        if not data['name']: break
        ac = AlumnClass(name=data['name'])
        print ac
        session.add(ac)
        session.commit()
        print 'Class %(name)s created.' % data
        loop = False if raw_input('Create another class? ') in ("N",'n','No','no') else True

    data = dict()
    loop = True
    while loop:
        data['name'] = raw_input("Name: ")
        data['surname'] = raw_input("Surname: ")
        data['dsa'] = True if raw_input("dsa: ") in ("Y",'y','Yes','yes') else False
        alumn = Alumn(**data)
        print 'Alumn %(surname)s %(name)s %(dsa)s created.' % data
        print alumn
        alumn.belongs = session.query(AlumnClass).first()
        session.add(alumn)
        session.commit()
        loop = False if raw_input("Continue? ") in ("N",'n','No','no') else True

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
