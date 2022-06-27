from sys import platform


def get_os_slash():
    """
    function that returns specific slash for OS
    :return: slash
    :rtype: str
    """
    if platform == "win32":
        return "\\"
    return "/"


OS_SLASH = get_os_slash()