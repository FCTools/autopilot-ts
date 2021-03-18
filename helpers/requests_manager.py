# Copyright © 2020-2021 Filthy Claws Tools - All Rights Reserved
#
# This file is part of autopilot.autopilot-ts.
#
# Unauthorized copying of this file, via any medium is strictly prohibited
# Proprietary and confidential
# Author: German Yakimov <german13yakimov@gmail.com>

import requests


def catch_network_errors(method):
    """
    Decorator for network errors catching.
    """

    def inner(*args, **kwargs):
        try:
            return method(*args, **kwargs)
        except (
                requests.exceptions.HTTPError,
                requests.exceptions.ConnectTimeout,
                requests.exceptions.Timeout,
                requests.exceptions.ConnectionError,
                requests.exceptions.RequestException,
                Exception,
        ) as network_error:
            return network_error

    return inner


@catch_network_errors
def get(session, *args, **kwargs):
    """
    Make safe GET request using given session and arguments.

    :param session: session for response making
    :type session: requests.Session
    :return: response if success, else catch error
    :rtype: Union[requests.Response, Exception]
    """

    return session.get(*args, **kwargs)


@catch_network_errors
def post(session, *args, **kwargs):
    """
    Make safe POST request using given session and arguments.

    :param session: session for response making
    :type session: requests.Session
    :return: response if success, else catch error
    :rtype: Union[requests.Response, Exception]
    """

    return session.post(*args, **kwargs)


@catch_network_errors
def put(session, *args, **kwargs):
    """
    Make safe PUT request using given session and arguments.

    :param session: session for response making
    :type session: requests.Session
    :return: response if success, else catch error
    :rtype: Union[requests.Response, Exception]
    """

    return session.put(*args, **kwargs)


@catch_network_errors
def patch(session, *args, **kwargs):
    """
    Make safe PATCH request using given session and arguments.

    :param session: session for response making
    :type session: requests.Session
    :return: response if success, else catch error
    :rtype: Union[requests.Response, Exception]
    """

    return session.patch(*args, **kwargs)
