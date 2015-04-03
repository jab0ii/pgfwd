"""
Utility functions.
"""


class ObjectDoesNotExist(Exception):
    pass


class ErrorCode:
    HIER_EXHAUSTED = 0


class StatusCode:
    """
    Status code enum.
    """
    INACTIVE = 0
    ACTIVE = 1
    ACKED = 2
    PAGESENT = 3
    EVENTCREATED = 4
    EVENTESCALATED = 5
    NOEVENT = 6


def createErrorDict(**kwargs):
    """
    Creates an Error dict for use in JSON object construction.

    Args:
        kwargs: title, details, and errorCode. Defaulted to None.
    """
    result = {}
    keys = ['title', 'details', 'errorCode']

    for key in keys:
        if key in kwargs:
            result[key] = kwargs[key]
        else:
            result[key] = None

    return result
