import os

def compilemessages(data):
    if data['workingdir'] != data['reporoot']:
        return
    os.chdir("mds")
    os.system("../manage.py compilemessages")

