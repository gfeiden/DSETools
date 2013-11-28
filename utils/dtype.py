#
#

def checkTuple(data):
    """ Check that data is of type tuple or list. """
    if type(data) is tuple:
        pass
    elif type(data) is list:
        pass
    else:
        data = (data, None)
    return data
