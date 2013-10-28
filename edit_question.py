from sqlalchemy.orm import sessionmaker
from model import engine, Alumn, AlumnClass, Question
from print_questions import print_questions, select_questions

if __name__ == '__main__':
    Session = sessionmaker(bind=engine)
    session = Session()

    loop = True
    while loop:
        loop = print_questions(session)
        if not loop: continue
        question = select_questions(session)
        if not question: continue

        datain = raw_input("Question type [%s]: " % question.qtype)
        if datain:
            question.qtype = datain
            session.add(question)
            session.commit()

        print question.question
        datain = raw_input("Question: ")
        if datain:
            question.question = datain
            session.add(question)
            session.commit()

        print question.answers
        loop = False if raw_input("Continue? ") in ("N",'n','No','no') else True
