'''
    tarpy - a Python TAR Archive utility
'''
import sys
import pkgutil

from tarpy.logger import LOGGER, CONSOLE_HANDLER


# Enable verbosity
if '-v' in sys.argv or '--verbose' in sys.argv:
    LOGGER.addHandler(CONSOLE_HANDLER)

# Handle Version
__version__ = (pkgutil.get_data(__package__, 'VERSION') or b'').decode('ascii').strip()

del pkgutil
