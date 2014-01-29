from sqlalchemy.orm import sessionmaker
from model import engine
from utils import print_classes
import sys

if __name__ == '__main__':
    Session = sessionmaker(bind=engine, autoflush=False, autocommit=False)
    session = Session()

    print_classes(session)
