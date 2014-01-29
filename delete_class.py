from sqlalchemy.orm import sessionmaker
from model import engine
from utils import select_class

if __name__ == '__main__':
    Session = sessionmaker(bind=engine)
    session = Session()

    data = dict()
    loop = True
    while loop:
        cls = select_class(session)
        if not cls: continue
        print 'Deleting class %s' % cls
        session.delete(cls)
        session.commit()
