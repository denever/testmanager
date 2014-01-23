from sqlalchemy.orm import sessionmaker
from model import engine, Alumn, AlumnClass, Question, Topic, Test, TestQuestionAssoc
import sys
from string import Template
from random import shuffle


DOCUMENT ="""
\\documentclass[a4paper]{article}
\\usepackage[italian]{babel}
\\usepackage[utf8]{inputenc}
\\usepackage{enumitem}
\\setlength{\parindent}{0pt} % No paragraph indentation everywhere, except for specific paragraphs %
\\usepackage[cm]{fullpage} % use smaller margins %
\\usepackage{stmaryrd} % needed for boxempty itemize bullet, sudo apt-get install texlive-math-extra %
\\renewcommand{\\labelitemi}{$\\boxempty$} % change itemize bullet in a empty square box %

\\begin{document}
\\newenvironment{question}[1]{{\\bfseries #1} \\begin{itemize}[itemsep=0.2em]}{\\end{itemize}}
"""

header_tmpl = Template("""
\\begin{flushright}
Cognome: {\\bfseries $surname}

Nome: {\\bfseries $name}


Classe: {\\bfseries $classname}

Data: {\\bfseries $date}

\\end{flushright}

\\section*{$title}
""")

quest_tmpl = Template("""
\\begin{question}{$pos $question}
  $answers
\\end{question}
""")

END_DOCUMENT = "\end{document}"

if __name__ == '__main__':
    Session = sessionmaker(bind=engine)
    session = Session()

    for cls in session.query(AlumnClass).order_by(AlumnClass.id):
        print '\t', cls.id, cls.name

    cls_id = raw_input('Select a class id: ')

    if not cls_id: sys.exit(1)

    cls = session.query(AlumnClass).filter(AlumnClass.id == cls_id).first()

    if not cls: sys.exit(1)

    for test in session.query(Test).filter(Test.printed == False):
        if test.alumn.belongs == cls:
            texfile = open('%s_%s.tex' % (test.title, test.alumn), 'w')
            texfile.write(DOCUMENT)
            texfile.write(header_tmpl.substitute(surname=test.alumn.surname,
                                                 name=test.alumn.name,
                                                 date=test.date,
                                                 title=test.title,
                                                 classname=test.alumn.belongs
                                             ))
            sorted_questions = sorted([ (question.position, question.question) for question in test.questions],
                                      key = lambda question: question[0])
            for pos, question in sorted_questions:
                answers = question.answers
                shuffle(answers)
                text_answers = '\n'.join(str(answer) for answer in answers)
                texfile.write(quest_tmpl.substitute(pos=pos, question=question, answers=text_answers))
            texfile.write(END_DOCUMENT)
            texfile.close()
            test.printed = True
            session.add(test)
            session.commit()
