from NoSuchParameterException import NoSuchParameterException

__author__ = 'Mael Beuget, Pierre Monnin & Thibaut Smith'

from google.appengine.ext import ndb
import logging


class Parameters(ndb.Model):
    name = ndb.StringProperty(required=True)
    value = ndb.StringProperty(required=True)


def get_parameter(key):
    """
    If the key given in argument has been found, you will find:
        {'key': key, 'value': value}

    And if not found, you will have:
        False
    """

    try:
        value = Parameters.query(Parameters.name == key).fetch(1)[0].value

        #logging.error(key)
        #logging.error(value)

        if value is not None:
            return {'key': key, 'value': value.encode('utf-8')}
        else:
            return False
    except IndexError:
        raise NoSuchParameterException(key)