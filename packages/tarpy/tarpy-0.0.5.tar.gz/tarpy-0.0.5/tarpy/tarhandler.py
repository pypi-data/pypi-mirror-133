#!/usr/bin/python3
# -*- coding: utf-8 -*-

''' TAR Archive

All TAR - Operations are made
with this module.
'''

from __future__ import annotations


import os
import tarfile
import traceback
from datetime import datetime
from typing import Any, Tuple

# Internal Imports
from tarpy.config import SETTINGS
from tarpy.utils import real_path
from tarpy.filters import filtered_walk
from tarpy.logger import LOGGER


class TarpyOptions:
    ''' Set Tar Settings

    This class will take parameters
    from the CLI and set them inside
    of Tarpy.
    If a variable wasn't assigned with
    an variable, it will be set to
    None.
    This class provides us the flexbility
    that we can define here how and which
    variables will be set, without a need
    to think about it in :module: cli.run
    or in :class: Tarpy
    
    Notes
    -----
    In fact, it will either used the config
    file, or either cli parameters.

    Arguments
    ---------
    possible_vars : list
        Name of variables
        which can be given
        as parameter to
        TarHandler.

    Parameters
    ----------
    **kwargs :
        See Arguments section.
    '''
    possible_vars: list[str] = [
            'root',
            'target',
            'exclude_file',
            'compression',
            'archive_name'
    ]
    __slots__ = possible_vars

    def __init__(self, **kwargs: Any) -> None:
        # Dynamically set variables.
        for var in self.possible_vars:
            if var in kwargs:
                setattr(self, var, kwargs.get(var))
                LOGGER.debug(f'[#] Variable "{var}" set.')
            else:
                setattr(self, var, None)
                LOGGER.debug(f'[#] Variable "{var}" set to None.')


class Tarpy(TarpyOptions):
    ''' TAR Archive

    Attributes
    ----------
    EXCLUSIONS : list
        A list of strings for extra exclusions.

    Parameters
    ----------
    mode : str
        Which Operation on Tar Archive;
        private.
    '''
    # EXCLUSIONS = []

    def __init__(self, mode: str, **kwargs: Any) -> None:
        super().__init__(**kwargs)

        self._mode = mode

        # The ending of the archive name is changing
        # if and depending on the compression method
        # set.
        if not self.archive_name:
            self.archive_name = f'{str(real_path(self.target))}/TARpy_{datetime.today().strftime("%Y%m%d")}.tar'
        if self.compression:
            self.archive_name += f'.{self.compression}'

        self._exclusions = self.set_exclusions()

    def set_exclusions(self, *excludes: Tuple[str]) -> list[str]:
        ''' Set own Exclusions

        There have to be some program related
        exclusions (e.g. the directory of this
        script) independently from the user
        defined exclusions from the file.

        Parameters
        ----------
        *excludes : tuple
            A Tuple containing exclusions re-
            presented by strings.

        Returns
        -------
        _exclusions :list
            A List of Exclusions.
        '''
        exclusions = []

        if excludes:
            for elem in excludes:
                exclusions.append(elem)

        # If there is a Blacklist file:
        if self.exclude_file:
            print('why??')
            try:
                with open(self.exclude_file, 'r') as ex_f:
                    for exclude in ex_f.readlines():
                        if exclude != '\n':
                            exclusions.append(exclude.strip('\n'))
            except Exception as unknown_error:
                LOGGER.error(f'[!] [UNKNOWN] {traceback.format_exc()}')

        return exclusions

    def tar_writer(self) -> None:
        ''' Write TAR Archive

        Method for writing the archive.
        '''        
        with tarfile.open(
                self.archive_name,
                f'w:{self.compression if self.compression else ""}'
        ) as tar_f:

            for path in filtered_walk(real_path(self.root), self._exclusions):
                # The recursive option
                # should be set to False.
                # Catch Errors
                try:
                    LOGGER.info(f'[+] {path}')
                    tar_f.add(path, recursive=False)
                except FileNotFoundError as error_msg:
                    LOGGER.error(error_msg)
                    pass
                except PermissionError as error_msg:
                    LOGGER.error(error_msg)
                    pass
                except Exception as unknown_error:
                    LOGGER.error(f'[!] [UNKNOWN] {traceback.format_exc()}')
        LOGGER.info(f'[SUCCESS] Archive written to "{self.target}".')

    def tar_extractor(self) -> None:
        ''' Extract TAR Archive

        Method for extracting the archive.
        '''
        if self.target_dir:
            LOGGER.debug('Jump to %s' % self.target)
            os.chdir(self.target)
        with tarfile.open(
                self.root,
                'r'
        ) as tar_f:
            try:
                LOGGER.info('Extraction started.')
                tar_f.extractall()
            except PermissionError as permission_error:
                LOGGER.error(permission_error)
            except UnicodeEncodeError as unicode_error:
                LOGGER.error(unicode_error)
                pass
        LOGGER.info(f'[SUCCESS] Archive extracted to "{self.target}".')

    def __repr__(self) -> str:
        return (f'Class: {self.__class__.__name__!r}\n'
                f'Start from: {str(self.root)!r}\n'
                f'Target Directory: {str(self.target)!r}\n'
                f'Compression: {self.compression!r}\n'
                f'Exclude File: {str(self.exclude_file)!r}\n'
                f'Mode: {self._mode!r}\n'
                )

    def __str__(self) -> str:
        return (f'\n\tSource: {str(self.root)}\n'
                f'\tTarget: {str(self.target)}\n'
                f'\tCompression: {self.compression}\n'
                f'\tExclusions: {len(self._exclusions)}\n'
                f'\tExclude File: {self.exclude_file}'
                f'\tMode: {self._mode}'
                )

    def __call__(self) -> Tarpy:
        ''' Make this class callable

        Just call your created instance of Tarpy
        like a function::
            call_tar = Tarpy(...)
            call_tar()
        '''
        LOGGER.info(self.__str__())
        if self._mode == 'w':
            self.tar_writer()
        elif self._mode == 'e':
            self.tar_extractor()
        LOGGER.info('Finished.')
