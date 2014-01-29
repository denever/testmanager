from sqlalchemy.orm import sessionmaker
from model import engine
from utils import select_subject, select_topic

if __name__ == '__main__':
    Session = sessionmaker(bind=engine, autoflush=False, autocommit=False)
    session = Session()

    loop = True
    while loop:
        sbj = select_subject(session)
        if not sbj: break
#        loop = print_topics(session, sbj)
        loop = select_topic(session, sbj)
#        loop = False if safe_prompt(session, "Continue? ") in ("N",'n','No','no') else print_alumns()
