''' Logger

Some logging Operations for Tarpy.
To use the Logger of this Module,
you can import LOGGER from here.

The following Log-Handlers are available:
    - Console Handler
    - File Handler
'''

import logging
import logging.config
import sys

from tarpy.config import SETTINGS

# Some Colors
DEFAULT = '\033[0m'
BLACK = '\033[30m'
RED = '\033[31m'
GREEN = '\033[32m'
YELLOW = '\033[33m'
BLUE = '\033[34m'
PURPLE = '\033[35m'
CYAN = '\033[36m'
BOLD = '\033[1m'


class CustomFormatter(logging.Formatter):

    ''' Custom Formatter

    Let's make the Logs colorful!

    Attributes
    ----------
    format : str
        Template for Log Messages.
    date_format : str
        How to display Date and Time.
    FORMATS : dict
        How Log Messages should be formatted.
    '''

    custom_format = (
        f'{BLUE}%(asctime)s{DEFAULT} - '\
        f'{PURPLE}{BOLD}%(module)s{DEFAULT}, '\
        f'{PURPLE}%(funcName)s{DEFAULT} - '\
        f'{CYAN}%(message)s{DEFAULT}'
        )
    date_format = '%d/%m/%Y, %H:%M:%S'
    levelname = '[%(levelname)s] '
    FORMATS = {
            logging.DEBUG: GREEN + levelname + custom_format,
            logging.INFO: GREEN + levelname + custom_format,
            logging.WARNING: YELLOW + levelname + custom_format,
            logging.ERROR: RED + levelname + custom_format,
            logging.CRITICAL: RED + BOLD + levelname + custom_format
            }

    def format(self, record) -> logging.LogRecord:
        ''' format

        Returns a formatted Log.

        Parameters
        ----------
        record : logging.LogRecord
            The Log to format.
        '''
        log_fmt = self.FORMATS.get(record.levelno)
        formatter = logging.Formatter(log_fmt)
        # Custom datefmt
        formatter.datefmt = self.date_format
        return formatter.format(record)


LOGGER = logging.getLogger(__name__)
LOGGER.setLevel(logging.DEBUG)
CONSOLE_HANDLER = logging.StreamHandler(sys.stdout)
CONSOLE_HANDLER.setFormatter(CustomFormatter())
# Let add CONSOLE_HANDLER inside of .cli/run/cli,
# so that verbosity is optional for the User.
# Uncomment if another behavior is wished.
#
# LOGGER.addHandler(CONSOLE_HANDLER)


# Logging to File as default setting:
#
#
# Uncomment following lines to use logging.FileHandler instead:
#
# FILE_HANDLER = logging.FileHandler(config.LOG_FILE, encoding='utf-8')
# FILE_HANDLER.setFormatter(CustomFormatter())
# LOGGER.addHandler(FILE_HANDLER)
#
#
# Using a RotatingFileHandler to prevent creating to huge log files.
#
# Max Size: 10 MB
# Max Number of Logs: 10
# After it is started from the beginnging again.
#
ROTATE_HANDLER = logging.handlers.RotatingFileHandler(
        SETTINGS['SETTINGS']['logs-file'],
        maxBytes=10000000,
        backupCount=10,
        encoding='utf-8'
        )
ROTATE_HANDLER.setFormatter(CustomFormatter())
LOGGER.addHandler(ROTATE_HANDLER)
