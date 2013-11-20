import sys
import sqlite3 as lite

from sqlalchemy.orm import sessionmaker
from model import engine, Topic, Question, Answer
from print_subjects import select_subject, select_topic

if __name__ == '__main__':
    Session = sessionmaker(bind=engine)
    session = Session()
    con = None

    try:
        filename = sys.argv[1]
        con = lite.connect(filename)
    except lite.Error, e:
        print "Error %s" % e.args[0]
    except Exception, e:
        print "Error %s" % e

    print "Importing question in which topic?"
    sbj = select_subject(session)
    if not sbj:
        sys.exit(1)
    current_topic = select_topic(session, sbj)
    if not current_topic:
        sys.exit(1)

    con.row_factory = lite.Row
    cur = con.cursor()
    cur.execute("Select question, qtype, answers from questions")
    rows = cur.fetchall()

    for row in rows:
        qa = Question(row['qtype'], row['question'])
        qa.topic = current_topic
        for answer in row['answers'].split('\n'):
            print answer
            if answer:
                answ = Answer(answer[6:])
                answ.question = qa
                session.add(answ)
        session.add(qa)
        session.commit()

    print "Importing alumns in which ?"
