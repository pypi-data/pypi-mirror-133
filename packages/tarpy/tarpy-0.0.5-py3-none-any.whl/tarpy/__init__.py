'''
    tarpy - a Python TAR Archive utility
'''
import sys
import pkgutil

from tarpy.logger import LOGGER, CONSOLE_HANDLER


# Enable verbosity
if '-v' in sys.argv or '--verbose' in sys.argv:
    LOGGER.addHandler(CONSOLE_HANDLER)

del pkgutil
