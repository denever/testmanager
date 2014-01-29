from sqlalchemy.orm import sessionmaker
from model import engine
from utils import print_questions, select_question, print_question

if __name__ == '__main__':
    Session = sessionmaker(bind=engine, autoflush=False, autocommit=False)
    session = Session()

    while True:
        question = select_question(session)
        if not question: continue
        print_question(question)
