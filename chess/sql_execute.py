def execute_script(mycursor, filename):
    fd = open(filename, 'r')
    sqlFile = fd.read()
    fd.close()
    sqlCommands = sqlFile.split(';')

    for command in sqlCommands:
        try:
            if command.strip() != '':
                mycursor.execute(command)
        except IOError:
            print("Command skipped: ")

