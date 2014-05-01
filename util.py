__author__ = 'videl'

from model.ADECommunicator import *
import logging
import re

def get_lessons_of_groups(groups, all_lessons):
    """
    Get the lessons that a list of groups have.
    """
    ade = ADECommunicator()

    users_lessons = dict()
    # Filter all the lessons of one user
    for lesson in all_lessons:
        #logging.error(lesson)
        #logging.error(all_lessons[lesson])
        for one_class in all_lessons[lesson]:
            for one_group in groups:
                if one_group in one_class['trainee']:
                    if lesson not in users_lessons.keys():
                        users_lessons[lesson] = list()
                    users_lessons[lesson].append(one_class)

    return users_lessons

def get_groups_of_a_user(username, all_groups):
    """
    Get the groups of one user.

    Output contains strings like:
    [u'2A G42', u'2A IL 2']

    Possible enhancement: the groups fetched need to not contain
    """
    users_groups = list()

    for group in all_groups:
        members = all_groups[group]

        for member in members:
            if username in member['name']:
                users_groups.append(group)

    return users_groups

def get_extended_groups_of_a_user(groups):
    """
    Gets the list of the groups the user is really into.
    Someone in the "2A IL 2" group is also in the "2A IL" group, and in 2A.
    """
    real_groups = list()
    for group in groups:
        real_groups.append(group)

        # Add the main class, "1A", "2A", "3A"..
        group_to_add = group.split(' ')[0]
        if not real_groups.__contains__(group_to_add):
            real_groups.append(group_to_add)

        if len(group.split(' ')) == 3:
            group_to_add = group[:-2]
            real_groups.append(group_to_add)
        elif len(group.split(' ')) == 2:
            group_to_add = group[:-1]
            real_groups.append(group_to_add)
        else:
            real_groups.append(group)

    return real_groups


def valid_username(username):
    """
    Checks if a username is valid.
    """
    user_regexp = re.compile(r"^[a-zA-Z0-9_-]{3,20}$")
    return user_regexp.match(username)


def valid_password(password):
    """
    Check if a password is valid.
    """
    password_regexp = re.compile(r"^.{3,40}$")
    return password_regexp.match(password)


def valid_email(email):
    """
    Check if an email is valid.
    """
    email_regexp = re.compile(r"^[\S]+@(etu\.)?univ-lorraine\.fr$")
    return email_regexp.match(email)


def valid_name(name):
    check = True
    if check is None:
        check = False

    if len(name.split(' ')) != 2:
        check = False

    return check