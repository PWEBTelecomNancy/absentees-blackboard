__author__ = 'Mael Beuget, Pierre Monnin & Thibaut Smith'

from google.appengine.ext import db
import hashlib
import random
import string


cookie_secret = "FrogidelPWEBMASTEROFTHEADEWORLD"


class Accounts(db.Model):
    login = db.StringProperty(required=True)
    password = db.StringProperty(required=True)
    is_admin = db.BooleanProperty(required=True)
    is_teacher = db.BooleanProperty(required=True)
    email_address = db.StringProperty(required=True)


def salt_generation():
    return ''.join(random.choice(string.letters) for i in range(5))


def id_cookie_generation(id):
    return str(id) + "|" + str(hashlib.sha256(str(id) + cookie_secret).hexdigest())


def check_cookie(cookie_id):
    user_id = cookie_id.split('|')

    if user_id[1] == str(hashlib.sha256(str(user_id[0] + cookie_secret)).hexdigest()):
        return True
    else:
        return False


def get_username_from_id(user_id):
    result = Accounts.get_by_id(int(user_id))
    if result:
        return result.login
    else:
        return None


def get_is_teacher_from_id(user_id):
    result = Accounts.get_by_id(int(user_id))
    if result:
        return result.is_teacher
    else:
        return None


def get_is_admin_from_id(user_id):
    result = Accounts.get_by_id(int(user_id))
    if result:
        return result.is_admin
    else:
        return None


def used_username(username):
    result = db.GqlQuery("SELECT * FROM Accounts WHERE login=:username", username=username)
    print result.count()
    return result.count() != 0


#Returns the user is if connexion is correct, None else
def user_connexion(username, password):
    result = db.GqlQuery("SELECT * FROM Accounts WHERE login=:username", username=username)

    if result.count() == 1:
        data = result.fetch(1)[0]
        db_password = data.password.split('|')[0]
        db_salt = data.password.split('|')[1]

        print db_password
        print db_salt

        if str(hashlib.sha256(password + db_salt).hexdigest()) == db_password:
            return data.key().id()
        else:
            return None

    else:
        return None


def password_hash(password):
    salt = salt_generation()
    return str(hashlib.sha256(password + salt).hexdigest()) + '|' + salt