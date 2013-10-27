from sqlalchemy.orm import sessionmaker
from model import engine, Alumn, AlumnClass, Question

if __name__ == '__main__':
    Session = sessionmaker(bind=engine)
    session = Session()

    data = dict()
    loop = True
    while loop:
        for alumn in session.query(Alumn).order_by(Alumn.surname):
            print '\t', alumn.id, alumn.surname, alumn.name, alumn.dsa, alumn.belongs

        id_to_delete = raw_input("Id to delete: ")
        if not id_to_delete:
            break
        id_to_delete = int(id_to_delete)
        alumn = session.query(Alumn).filter(Alumn.id == id_to_delete).first()
        session.delete(alumn)
        session.commit()
