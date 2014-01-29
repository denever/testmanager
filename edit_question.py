from sqlalchemy.orm import sessionmaker
from model import engine, Alumn, AlumnClass, Question
from utils import select_question, print_answers, safe_prompt

if __name__ == '__main__':
    Session = sessionmaker(bind=engine)
    session = Session()

    loop = True
    while loop:
        question = select_question(session)
        if not question: continue

        datain = safe_prompt(session, "Question type [%s]: " % question.qtype)
        if datain:
            question.qtype = datain
            session.add(question)
            session.commit()

        print question.question
        datain = safe_prompt(session, "Question: [%s]" % question.question)
        if datain:
            question.question = datain
            session.add(question)
            session.commit()

        print_answers(session, question)
