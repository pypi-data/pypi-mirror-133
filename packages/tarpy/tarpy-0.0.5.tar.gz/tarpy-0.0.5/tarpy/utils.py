''' Utils

Module of tarpy.
'''

import os
import pathlib
from tarpy.logger import LOGGER


def real_path(path: str) -> pathlib.PosixPath[str]:
    ''' Real Paths

    Makes sure to get a real Path.
    '''
    try:
        return pathlib.Path(path).resolve()
    except TypeError as error_msg:
        LOGGER.error(error_msg)
        pass

def check_existence(to_check: str) -> bool:
    ''' Check if File / Directory
        exists or not
    '''
    if not os.path.exists(to_check):
        LOGGER.warning(f'[-] "{to_check}" does not exist.')
        return False
    return True

def check_symlink(to_check: str) -> bool:
    ''' Check if File is a Symlink
    '''
    return pathlib.Path(to_check).is_symlink()

def delete_paths(path: str) -> None:
    ''' Delete given Path
    '''
    LOGGER.info(f'[-] {path}')
    if os.path.isdir(path):
        os.rmdir(path)
    elif os.path.isfile(path):
        os.remove(path)
