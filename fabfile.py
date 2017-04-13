from fabric.api import local, settings, abort
from fabric.contrib.console import confirm

def test():
    local("nosetests -v")

def commit():
    message = raw_input("Enter a git comment message: ")
    local("git add . && git commit -am '{}'".format(message))

def push():
    local("git push origin master")

def prepare():
    test()
    commit()
    push()


def pull():
    local("git pull origin master")

def heroku():
    local("git push heroku master")

def heroku_test():
    local("heroku run nosetests -v")

def deploy():
    pull()
    test()
    commit()
    heroku()
    heroku_test()

def rollback():
    local("heroku rollback")

