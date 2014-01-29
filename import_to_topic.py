import sys
import sqlite3 as lite

from sqlalchemy.orm import sessionmaker
from model import engine, Topic, Question, Answer, AlumnClass, Alumn
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

    subject = select_subject(session)
    selected_topic = select_topic(session, subject)

    print "Importing question in to this topic...", selected_topic
    con.row_factory = lite.Row
    cur = con.cursor()
    cur.execute("Select id, question, qtype from questions")
    rows = cur.fetchall()

    for row in rows:
        qa = Question(row['qtype'], row['question'])
        qa.topic = selected_topic
        session.add(qa)
        session.commit()
        
        con.row_factory = lite.Row
        cur2 = con.cursor()
        cur2.execute("Select answer_text, correct from answers where question_id=%d" % row['id'])

        for answer in cur2.fetchall():
            answ = Answer(answer['answer_text'], answer['correct'])
            answ.question = qa
            session.add(answ)
        session.add(qa)
        session.commit()
