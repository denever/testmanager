from sqlalchemy.orm import sessionmaker
from model import engine, Topic, Question
from print_questions import print_questions

if __name__ == '__main__':
    Session = sessionmaker(bind=engine)
    session = Session()

    data = dict()
    loop = True
    while loop:
        print_questions(session)

        id_to_delete = raw_input("Id to delete: ")
        if not id_to_delete:
            break
        id_to_delete = int(id_to_delete)
        alumn = session.query(Question).filter(Question.id == id_to_delete).first()
        session.delete(alumn)
        session.commit()
