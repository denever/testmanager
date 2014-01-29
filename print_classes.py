from sqlalchemy.orm import sessionmaker
from model import engine
from utils import print_classes
import sys

try:
    from termcolor import colored
except ImportError:
    print 'Please install termcolor module'
    def colored(color, string):
        return string

if __name__ == '__main__':
    Session = sessionmaker(bind=engine)
    session = Session()

    print_classes(session)
