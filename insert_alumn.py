from sqlalchemy.orm import sessionmaker
from model import engine, Alumn, AlumnClass, Question

if __name__ == '__main__':
    Session = sessionmaker(bind=engine)
    session = Session()

    data = dict()
    loop = True
    while loop:
        data['name'] = raw_input("Name: ")
        data['surname'] = raw_input("Surname: ")
        data['dsa'] = True if raw_input("dsa: ") in ("Y",'y','Yes','yes') else False
        alumn = Alumn(**data)
        print 'Alumn %(surname)s %(name)s %(dsa)s created.' % data
        print alumn
        print 'Assign to a class'
        for cls in session.query(AlumnClass).order_by(AlumnClass.id):
            print '\t', cls.id, cls.name

        cls_id = raw_input('Select a class id: ')
        alumn.belongs = session.query(AlumnClass).filter(AlumnClass.id == cls_id).first()
        session.add(alumn)
        session.commit()
        loop = False if raw_input("Continue? ") in ("N",'n','No','no') else True
