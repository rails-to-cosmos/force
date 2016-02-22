from fabric.api import local, settings


def push(cm):
    with settings(warn_only=True):
        local('git commit -am\'{cm}\''.format(cm=cm))
        local('git push')


def deploy():
    with settings(warn_only=True):
        local('git push origin heroku')
