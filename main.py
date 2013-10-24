if __name__ == '__main__':
    Session = sessionmaker(bind=engine)
    session = Session()

    loop = True
    data = dict()
    while loop:
        data['name'] = raw_input("Class name: ")
        if not data['name']: break
        ac = AlumnClass(name=data['name'])
        print ac
        session.add(ac)
        session.commit()
        print 'Class %(name)s created.' % data
        loop = False if raw_input('Create another class? ') in ("N",'n','No','no') else True

    data = dict()
    loop = True
    while loop:
        data['name'] = raw_input("Name: ")
        data['surname'] = raw_input("Surname: ")
        data['dsa'] = True if raw_input("dsa: ") in ("Y",'y','Yes','yes') else False
        alumn = Alumn(**data)
        print 'Alumn %(surname)s %(name)s %(dsa)s created.' % data
        print alumn
        alumn.belongs = session.query(AlumnClass).first()
        session.add(alumn)
        session.commit()
        loop = False if raw_input("Continue? ") in ("N",'n','No','no') else True
