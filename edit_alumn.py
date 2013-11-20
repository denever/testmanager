from sqlalchemy.orm import sessionmaker
from model import engine, Alumn, AlumnClass, Question
from print_alumns import print_alumns, select_class

if __name__ == '__main__':
    Session = sessionmaker(bind=engine)
    session = Session()

    data = dict()
    loop = True
    while loop:
        cls_id = select_class(session)
        if not cls_id: continue
        loop = print_alumns(session, cls_id)

        id_to_edit = raw_input("Id to edit: ")
        if not id_to_edit:
            break
        id_to_edit = int(id_to_edit)
        alumn = session.query(Alumn).filter(Alumn.id == id_to_edit).first()
        data['surname'] = raw_input("Surname: [%s]" % alumn.surname)
        if data['surname']:
            alumn.surname = data['surname']
            session.add(alumn)
            session.commit()
            
        data['name'] = raw_input("Name: [%s]" % alumn.name)
        if data['name']:
            alumn.name = data['name']
            session.add(alumn)
            session.commit()
            
        data['dsa'] = True if raw_input("dsa: [%s]" % alumn.dsa) in ("Y",'y','Yes','yes') else False
        if data['dsa']:
            alumn.dsa = data['dsa']
            session.add(alumn)
            session.commit()
            
        print alumn
        print 'Assign to a class'
        for cls in session.query(AlumnClass).order_by(AlumnClass.id):
            print '\t', cls.id, cls.name

        cls_id = raw_input('Select a class id: ')
        alumn.belongs = session.query(AlumnClass).filter(AlumnClass.id == cls_id).first()
        session.add(alumn)
        session.commit()
        loop = False if raw_input("Continue? ") in ("N",'n','No','no') else True

