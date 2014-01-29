from sqlalchemy.orm import sessionmaker
from model import engine
from utils import select_class, select_alumn

if __name__ == '__main__':
    Session = sessionmaker(bind=engine)
    session = Session()

    data = dict()
    loop = True
    while loop:
        cls = select_class(session)
        if not cls: continue
        alumn = select_alumn(session, cls)
        if not alumn: continue
        print 'Deleting alumn %s' % alumn
        session.delete(alumn)
        session.commit()
