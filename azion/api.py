from azion.client import Azion


def login(token):
    azion = Azion(token)
    return azion


def authorize(username, password):
    azion = Azion()
    return azion.authorize(username, password)
