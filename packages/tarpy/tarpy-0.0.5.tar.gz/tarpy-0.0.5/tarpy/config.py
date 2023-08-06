''' Config

Config Variables for tarpy Package.
'''

import configparser
import os
from datetime import datetime
from pathlib import Path


# Define Static Variables
SYSTEM = os.uname().sysname
SYSTEMNAME = os.uname().release
MACHINE = os.uname().machine
HOST = os.uname().nodename
ARCHITECTURE = os.uname().machine
OWNDIR = os.path.dirname(os.path.realpath(__file__))
TODAY = datetime.today().strftime('%Y-%m-%d')

HOMEPATH = Path().home()

# The Config File
CONFIG_DIR = HOMEPATH / '.config/tarpy'
CONFIG_FILE = Path(CONFIG_DIR / 'conf.ini')
LOG_DIR = Path(CONFIG_DIR / 'logs')
LOG_FILE = Path(LOG_DIR / 'tarpy.log')

# Let us make configurations more flexible
# and customable.
#
class ConfigHandler:

    ''' Handle Configurations

    Handles all configurations and belonging
    operations of tarpy.

    Attributes
    ----------
    configs : configparser.ConfigParser
        Inits the ConfigParser.
    settings : str
        Defaults for CONFIG_FILE.
    '''

    configs = configparser.ConfigParser(allow_no_value=True)
    settings = f'''
    [SETTINGS]
        config-path = {str(CONFIG_DIR)}
        config-file = {str(CONFIG_FILE)}
        logs-path = {str(LOG_DIR)}
        logs-file = {str(LOG_FILE)}

    [BACKUP]
        root =
        target =
        compression =
        exclude-file =
        archive_name =

    [TIMER]
        enabled =
        set =
    '''

    def __init__(self):
        ''' Initialization

        Check and solve some dependencies,
        essential for tarpy.
        '''
        # Check for config directory
        # and logs subdirectory.
        if not os.path.exists(CONFIG_DIR):
            os.mkdir(CONFIG_DIR)
            os.mkdir(LOG_DIR)

        if not os.path.exists(CONFIG_FILE):
            self.conf_creator()
        else:
            self.conf_reader()

    def conf_creator(self) -> None:
        ''' Write Config File

        Writes the self.settings to the
        CONFIG_FILE.
        '''
        self.configs.read_string(self.settings)
        with open(CONFIG_FILE, 'w') as conf_f:
            self.configs.write(conf_f)

    def conf_reader(self) -> None:
        ''' Read Config File

        Reads in the configurations defined
        in CONFIG_FILE.
        '''
        self.configs.read(CONFIG_FILE)
        return self.configs.items('BACKUP')

    def add_options(self, options: dict[str:list[str]]) -> None:
        ''' Add Options

        The given options are set and the
        cfg.ini file written again. options
        needs to be a nested dictionary with
        the following structure:
            > { SECTION : [ OPTION, FIELD ] }
        e.g.:
            > {'BACKUP' : ['compression' : 'gz']}

        Parameters
        ----------
        options : dict
            The options to set.
        '''
        for section, entry in options.items():
            self.configs.set(section, entry[0], entry[1])

        with open(CONFIG_FILE, 'w') as conf_f:
            self.configs.write(conf_f)


SETTINGS = ConfigHandler().configs
