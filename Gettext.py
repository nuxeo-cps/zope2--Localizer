# -*- coding: iso-8859-15 -*-

# Localizer, Zope product that provides internationalization services
# Copyright (C) 2000-2002  Juan David Ib��ez Palomar <j-david@noos.fr>

# This program is free software; you can redistribute it and/or
# modify it under the terms of the GNU General Public License
# as published by the Free Software Foundation; either version 2
# of the License, or (at your option) any later version.

# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.

# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 59 Temple Place - Suite 330, Boston, MA  02111-1307, USA.


"""
Localizer

"""

__version__ = "$Revision$"


# Zope
from Globals import package_home

# Localizer
from LocalFiles import gettext



class translation:
    def __init__(self, namespace):
        self.locale = package_home(namespace) + '/locale/'

    __call__ = gettext


def dummy(message, language=None):
    """
    Used to markup a string for translation but without translating it,
    this is known as deferred translations.
    """
    return message
