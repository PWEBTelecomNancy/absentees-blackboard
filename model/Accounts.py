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
    name = db.StringProperty(required=True)


def salt_generation():
    return ''.join(random.choice(string.letters) for i in range(5))


def id_cookie_generation(id):
    return str(id) + "|" + str(hashlib.sha256(str(id) + cookie_secret).hexdigest())


def check_cookie(cookie_id):
    user_id = cookie_id.split('|')

    if user_id[1] == str(hashlib.sha256(str(user_id[0] + cookie_secret)).hexdigest()) \
            and get_username_from_id(user_id[0]) is not None:
        return True
    else:
        return False


def get_connected_user(cookie_id):
    if cookie_id:
        if check_cookie(cookie_id):
            username = get_username_from_id(cookie_id.split('|')[0])
            result = db.GqlQuery("SELECT * FROM Accounts WHERE login=:username", username=username).fetch(1)
            if len(result) == 1:
                return result[0]
            else:
                return None
        else:
            return None
    else:
        return None


def get_username_from_id(user_id):
    result = Accounts.get_by_id(int(user_id))
    if result:
        return result.login
    else:
        return None


def get_account_from_id(user_id):
    result = Accounts.get_by_id(int(user_id))
    if result:
        return result
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
    return result.count() != 0


#Returns the user is if connexion is correct, None else
def user_connexion(username, password):
    result = db.GqlQuery("SELECT * FROM Accounts WHERE login=:username", username=username)

    if result.count() == 1:
        data = result.fetch(1)[0]
        db_password = data.password.split('|')[0]
        db_salt = data.password.split('|')[1]

        if str(hashlib.sha256(password + db_salt).hexdigest()) == db_password:
            return data.key().id()
        else:
            return None

    else:
        return None


def password_hash(password):
    salt = salt_generation()
    return str(hashlib.sha256(password + salt).hexdigest()) + '|' + salt


def delete_user_from_login(login):
    result = db.GqlQuery("SELECT * FROM Accounts WHERE login=:login", login=login)

    if result.count() == 1:
        Accounts.delete(result.fetch(1)[0])
        return True

    else:
        return False


def grant_admin_from_login(login):
    result = db.GqlQuery("SELECT * FROM Accounts WHERE login=:login", login=login)

    if result.count() == 1:
        account = result.fetch(1)[0]

        account.is_admin = True
        account.put()

        return True

    else:
        return False


def remove_admin_from_login(login):
    result = db.GqlQuery("SELECT * FROM Accounts WHERE login=:login", login=login)

    if result.count() == 1:
        account = result.fetch(1)[0]

        account.is_admin = False
        account.put()

        return True

    else:
        return False


def grant_teacher_from_login(login):
    result = db.GqlQuery("SELECT * FROM Accounts WHERE login=:login", login=login)

    if result.count() == 1:
        account = result.fetch(1)[0]

        account.is_teacher = True
        account.put()

        return True

    else:
        return False


def remove_teacher_from_login(login):
    result = db.GqlQuery("SELECT * FROM Accounts WHERE login=:login", login=login)

    if result.count() == 1:
        account = result.fetch(1)[0]

        account.is_teacher = False
        account.put()

        return True

    else:
        return False


def get_all_accounts():
    query = Accounts.all()
    accounts = query.fetch(limit=None)
    return accounts


def get_accounts_corresponding_login(login):
    query = db.GqlQuery("SELECT * FROM Accounts WHERE login=:login", login=login)
    accounts = query.fetch(limit=None)
    return accounts


def get_accounts_corresponding_email(email):
    query = db.GqlQuery("SELECT * FROM Accounts WHERE email_address=:email", email=email)
    accounts = query.fetch(limit=None)
    return accounts


def get_accounts_corresponding_ade_name(ade_name):
    query = db.GqlQuery("SELECT * FROM Accounts WHERE name=:ade_name", ade_name=ade_name)
    accounts = query.fetch(limit=None)
    return accounts