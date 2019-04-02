import os


def compilemessages(data):
    try:
        if data['workingdir'] != data['reporoot']:
            raise EnvironmentError('Working dir is not the root one')
        os.chdir("mds")
        os.system("../manage.py compilemessages")
    except Exception as error:
        print('Error occured while compilemessages')
        print('Working Dir: ' + data['workingdir'])
        print(error)
