import sys

from string import Template
from random import shuffle
from sqlalchemy.orm import sessionmaker
from model import engine, Alumn, AlumnClass, Question, Topic, Test, TestQuestionAssoc
from utils import select_class, safe_prompt

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

answ_tmpl = Template("""
\\item $answer
""")

END_DOCUMENT = "\end{document}"

if __name__ == '__main__':
    Session = sessionmaker(bind=engine)
    session = Session()

    cls = None
    while True:
        cls = select_class(session)
        if not cls: continue
        break

    for test in session.query(Test).filter(Test.printed == False):
        if test.alumn.belongs == cls:
            file_name = '%s_%s.tex' % (test.title, test.alumn)
            file_name = file_name.replace(' ','_')
            texfile = open(file_name, 'w')
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
                text_answers = '\n'.join(answ_tmpl.substitute(answer=answer) for answer in answers)
                texfile.write(quest_tmpl.substitute(pos=pos, question=question, answers=text_answers))
            texfile.write(END_DOCUMENT)
            texfile.close()
            session.rollback()
            test.printed = True
            session.add(test)
            session.commit()
