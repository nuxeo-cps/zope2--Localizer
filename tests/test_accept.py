# -*- coding: iso-8859-15 -*-
# Localizer, Zope product that provides internationalization services
# Copyright (C) 2001, 2002 J. David Ib��ez <j-david@noos.fr>
# Authors:
# J. David Ib��ez <j-david@noos.fr>
# M.-A. Darche <madarche@nuxeo.com>
#
# This program is free software; you can redistribute it and/or
# modify it under the terms of the GNU General Public License
# as published by the Free Software Foundation; either version 2
# of the License, or (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 59 Temple Place - Suite 330, Boston, MA  02111-1307, USA.
#
# $Id$
"""
Test suite for the language negotiation stuff.
"""

__version__ = "$Revision$"

# Python unit test
import unittest
from unittest import TestCase

# Add the Localizer product directory to the path
import os, sys
sys.path.append(os.path.join(sys.path[0], '../'))

# Localizer modules
from Accept import AcceptCharset, AcceptLanguage


class AcceptCharsetTestCase(TestCase):
    def test_case1(self):
        accept = AcceptCharset("ISO-8859-1, utf-8;q=0.66, *;q=0.66")
        self.assertEquals(accept.get_quality('utf-8'), 0.66)

    def test_case2(self):
        accept = AcceptCharset("ISO-8859-1, utf-8;q=0.66, *;q=0.66")
        self.assertEquals(accept.get_quality('ISO-8859-1'), 1.0)

    def test_case3(self):
        accept = AcceptCharset("utf-8, *;q=0.66")
        self.assertEquals(accept.get_quality('ISO-8859-1'), 0.66)

    def test_case4(self):
        accept = AcceptCharset("utf-8")
        self.assertEquals(accept.get_quality('ISO-8859-1'), 1.0)


class QualityAcceptLanguageTestCase(TestCase):
    def setUp(self):
        self.al = AcceptLanguage("da, en-gb;q=0.8")

    def test_da(self):
        self.assertEquals(self.al.get_quality('da'), 1.0)

    def test_en_gb(self):
        self.assertEquals(self.al.get_quality('en-gb'), 0.8)

    def test_en(self):
        self.assertEquals(self.al.get_quality('en'), 0.8)

    def test_en_us(self):
        self.assertEquals(self.al.get_quality('en-us'), 0.0)


class SelectLanguageAcceptLanguageTestCase(TestCase):
    def setUp(self):
        self.al = AcceptLanguage("da, en-gb;q=0.8")

    def testNone(self):
        """When none of the languages is acceptable."""

        self.assertEquals(self.al.select_language(['en-us', 'es']), None)

    def testImplicit(self):
        """When the preferred language is not explictly set."""

        self.assertEquals(self.al.select_language(['en-us', 'en']), 'en')

    def testSeveral(self):
        """When there're several accepted languages."""

        self.assertEquals(self.al.select_language(['en-us', 'en', 'da']), 'da')


class SelectLanguageAcceptLanguageWithoutQualityTestCase(TestCase):
    def setUp(self):
        self.al = AcceptLanguage('fr, en')

# TODO: Shouldn't it be working too?
##     def testImplicit(self):
##         """When the preferred language is not explictly set."""

##         self.assertEquals(self.al.select_language(['fr-fr', 'de']), 'fr')

    def testSeveral(self):
        """When there is no specified quality the order matters."""

        self.assertEquals(self.al.select_language(['en', 'fr', 'es']), 'fr')


class ChangeAcceptLanguageTestCase(TestCase):
    def setUp(self):
        self.al = AcceptLanguage("da, en-gb;q=0.8")

    def testChange(self):
        al = AcceptLanguage("da, en-gb;q=0.8")
        al['es'] = 5.0

        self.assertEquals(al.get_quality('es'), 5.0)


if __name__ == '__main__':
    unittest.main()
