from sqlalchemy.orm import sessionmaker
from model import engine
from utils import select_question

if __name__ == '__main__':
    Session = sessionmaker(bind=engine)
    session = Session()

    data = dict()
    loop = True
    while loop:
        question = select_question(session)
        if not question: continue
        print 'Deleting question %s' % question
        session.delete(question)
        session.commit()
