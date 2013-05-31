import sys
import traceback


def get_exception_str(request=None):
    exc_type, exc_value, exc_traceback = sys.exc_info()
    tb = traceback.format_tb(exc_traceback, limit=20)
    s = "%s - %s\n%s" % (exc_type, exc_value, ''.join(tb))
    if request:
        path = request.get_full_path()
        s = "Path: " + str(path) + "\n" + s
    return s 