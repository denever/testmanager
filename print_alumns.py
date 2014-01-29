from sqlalchemy.orm import sessionmaker
from model import engine
from utils import select_class, print_alumns
import sys

if __name__ == '__main__':
    Session = sessionmaker(bind=engine, autoflush=False, autocommit=False)
    session = Session()

    loop = True
    while loop:
        cls = select_class(session)
        if not cls: continue
        loop = print_alumns(session, cls)
#        loop = False if safe_prompt("Continue? ") in ("N",'n','No','no') else print_alumns()
