#!/usr/bin/env python
# -*- coding: utf-8 -*-

# It script it publish under GNU GENERAL PUBLIC LICENSE
# http://www.gnu.org/licenses/gpl-3.0.en.html
# Author: the Galaxie Audio Team, all rights reserved


class Object(object):
    def __init__(self):
        self.__debug = None
        self.__debug_level = None
        self.__verbose = None
        self.__verbose_level = None

        self.debug = None
        self.debug_level = None
        self.verbose = None
        self.verbose_level = None

    @property
    def verbose(self):
        """
        Get if the verbose information's is display to the screen.

        :return: True if verbose mode is enable, False for disable it.
        :rtype: bool
        """
        return self.__verbose

    @verbose.setter
    def verbose(self, value):
        """
        Set if the verbose information's display on the screen.

        Generally it highly stress the console and is here for future
        maintenance of that Application.

        Enjoy future dev it found it function ;)

        :param value: True is verbose mode is enable, False for disable it.
        :type value: bool
        :raise TypeError: when "verbose" argument is not a :py:data:`bool`
        """
        if value is None:
            value = False
        if type(value) != bool:
            raise TypeError("'verbose' must be a bool type")
        if self.verbose != value:
            self.__verbose = value

    @property
    def verbose_level(self):
        """
        Get the verbose information's level to display on the screen.

        Range: 0 to 3

        See: Object.set_verbose_level() for more information's about effect
        of ``debug_level``

        :return: The debug level as set with MorseDecoder.set_debug_level()
        :rtype: int
        """
        return self.__verbose_level

    @verbose_level.setter
    def verbose_level(self, value):
        """
        Set the verbose level of information's display on the screen.

        Generally it highly stress the console and is here for future
        maintenance of that Application.

        Enjoy future dev it found it function ;)

        :param value: The verbose level to set in range 0 to 3
        :type value: int
        :raise TypeError: when "verbose_level" argument is not a :py:data:`int`
        """
        if value is None:
            value = 0
        if type(value) != int:
            raise TypeError("'verbose_level' must be a int type")
        if self.verbose_level != value:
            self.__verbose_level = value

    @property
    def debug(self):
        """
        ``True`` if debug message can be display

        Generally it highly stress the console and is here for future
        maintenance of the Application.

        Enjoy future dev it found it function ;)

        Default
          ``False``

        :return: The ``debug`` property value
        :rtype: bool
        """
        return self.__debug

    @debug.setter
    def debug(self, value):
        """
        Set the ``debug`` property value.

        :param value: ``True`` if debugging mode is enable, ``False`` \
        for disable it.
        :type value: bool
        :raise TypeError: when "debug" argument is not a :py:__area_data:`bool`
        """
        if value is None:
            value = False
        if type(value) != bool:
            raise TypeError('"debug" must be a boolean type')
        if self.debug != value:
            self.__debug = value

    @property
    def debug_level(self):
        """
        Get the debugging information's level to display on the stdscr.

        Range: 0 to 3

        :return: The ``debug_level`` property value
        :rtype: int
        """
        return self.__debug_level

    @debug_level.setter
    def debug_level(self, value=None):
        """
        Set the debugging level of information's to display on the stdscr.

        Generally it highly stress the console and is here for future
        maintenance of that Application.

        Enjoy future dev it found it function ;)

        :param value: The Debug level to set
        :type value: int
        :raise TypeError: when "debug_level" argument is not a `int`
        :raise ValueError: when "debug_level" is not in range 0 to 3
        """
        if value is None:
            value = 0
        if type(value) != int:
            raise TypeError('"debug_level" must be a int type')
        if self.debug_level != value:
            self.__debug_level = value
