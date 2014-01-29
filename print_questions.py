from sqlalchemy.orm import sessionmaker
from model import engine
from utils import print_questions, select_question, print_question

if __name__ == '__main__':
    Session = sessionmaker(bind=engine)
    session = Session()

    loop = True
    while loop:
        loop = print_questions(session)
        if not loop: continue
        loop = select_question(session)
        if not loop: continue
        print_question(loop)
#        loop = False if safe_prompt("Continue? ") in ("N",'n','No','no') else print_questions()
