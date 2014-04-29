__author__ = 'videl'

from model.ADECommunicator import *
import logging

def get_lessons_of_groups(groups, all_lessons = ADECommunicator().get_lessons()):
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

def get_groups_of_a_user(username, all_groups = ADECommunicator().get_students_groups()):
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
    Someone in the "2A IL 2" group is also in the "2A IL" group.
    """
    user_groups = get_groups_of_a_user(groups)
    real_groups = list()
    for group in user_groups:
        if len(group.split(' ')) == 3:
            real_groups.append(group[:-2])
        elif len(group.split(' ')) == 2:
            real_groups.append(group[:-1])
        else:
            real_groups.append(group)

    return real_groups