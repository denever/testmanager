import random
from sqlalchemy.orm import sessionmaker
from model import engine, Alumn, AlumnClass, Question

def create_test():
    print 'Print test for a class'
    for cls in session.query(AlumnClass).order_by(AlumnClass.id):
        print '\t', cls.id, cls.name

    cls_id = raw_input('Select a class id: ')

    if not cls_id: return False

    cls = session.query(AlumnClass).filter(AlumnClass.id == cls_id).first()

    if not cls: return False

    test_size = int(raw_input('Numero di domande? '))

    for alumn in cls.alumns:
        query = session.query(Question)
        if alumn.dsa:
            query = query.filter(Question.qtype != 'OC')
        qs = query.all()
        test = list()
        loop = True
        while len(test) < test_size:
            random_choice = random.choice(qs)
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
