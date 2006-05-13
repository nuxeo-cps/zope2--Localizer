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
This module is for backwards compatibility only, since the features it
provided are now implemented in the LocalFiles module.

This change happened after the 0.8 version.
"""

__version__ = "$Revision$"


from LocalFiles import LocalDTMLFile, LocalPageTemplateFile, gettext



