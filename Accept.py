# -*- coding: iso-8859-15 -*-
# Localizer, Zope product that provides internationalization services
# Copyright (C) 2001-2002 J. David Ibáñez <j-david@noos.fr>
# Authors:
# J. David Ibáñez <j-david@noos.fr>
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
This module implements the Accept-Charset and Accept-Language request
headers of the HTTP protocol.

This module follows the references:
RFC 2616 - Hypertext Transfer Protocol -- HTTP/1.1
RFC 3282 - Content Language Headers

The public interface is provided by the classes AcceptCharset and
AcceptLanguage. The other classes shouldn't be used directly.
"""

DEFAULT_CHARSET = 'ISO-8859-1'

class Node:
    """
    Base class that represents a node in a tree.
    """

    def __init__(self):
        self.quality = None
        self.children = {}

    # Mapping interface, and other Python standard methods
    def __setitem__(self, key, quality):
        """
        Sets the quality for a language. If the language doesn't exists
        it's added.
        """
        node = self._getnode(key)
        node.quality = quality

    def __str__(self):
        d = {}
        for key, value in self.children.items():
            d[key] = str(value)

        return "%s %s" % (self.get_quality(), d)

    def get_quality(self):
        """
        Returns the quality of this node.
        """
        if self.quality is None:
            return max([ x.get_quality() for x in self.children.values() ])

        return self.quality


class Root(Node):
    """
    Base class that represents the root of a tree.
    """

    # Hack to let access from Zope restricted code (Zope sucks).
    __allow_access_to_unprotected_subobjects__ = 1


    def __init__(self, accept):
        Node.__init__(self)

        self.quality = 0.0
        # It is needed to keep the order of the passed keys as recommended
        # by RFC3282 :
        # If no Q values are given, the language-ranges are given in priority
        # order, with the leftmost language-range being the most preferred
        # language; this is an extension to the HTTP/1.1 rules, but matches
        # current practice.
        self._ordered_keys = []
        self._parse(accept)

    def _parse(self, accept):
        """
        From a string formatted as specified in the RFC2616, it builds a data
        structure which provides a high level interface to implement language
        negotiation.
        """
        # Parse the accept string and initialize the tree.
        # parsed_accept is of the following form:
        # [(id1, id1-quality), (id2, id2-quality), etc.]
        accept_parsed = []
        for x in accept.split(','):
            x = x.strip()
            x = x.split(';')

            if len(x) == 2:
                # There is a quality value
                quality = x[1]            # Get the quality
                quality = quality.strip()
                quality = quality[2:]     # Get the quality number (remove "q=")
                quality = float(quality)  # Change it to float
            else:
                # There isn't any quality value,
                # so the quality value defaults to "q=1" as specified by RFC2616
                quality = 1.0

            accept_parsed.append((x[0], quality))

        for (key, quality) in accept_parsed:
            self._ordered_keys.append(key)
            self[key] = quality

    def __str__(self):
        d = {}
        for key, value in self.children.items():
            d[key] = str(value)

        return "%s %s" % (self.quality, d)

    # Public interface
    def getOrderedKeys(self):
        return self._ordered_keys

    def get_quality(self, key):
        """
        Returns the quality of the given node
        """
        try:
            node = self[key]
        except KeyError:
            return self.quality

        return node.get_quality()

    def set(self, key, quality):
        """
        Sets the quality for a language, only if the current quality is
        not bigger. If the language doesn't exists it's added.
        """
        node = self._getnode(key)
        if quality > node.quality:
            node.quality = quality


class CharsetNode(Node):
    """
    Implements the node of a Accept-Charset tree.
    """

    def __getitem__(self, key):
        """
        Traverses the tree to get the object.
        """
        return self.children[key]


class LanguageNode(Node):
    """
    Implements a node of a Accept-Language tree.
    """

    def _getnode(self, key):
        """
        Returns the required node. If it doesn't exists it's created.
        """
        if isinstance(key, str):
            if key == '*':
                key = []
            else:
                key = key.split('-')

        if len(key) == 0:
            return self
        else:
            accept = self.children.setdefault(key[0], LanguageNode())
            return accept._getnode(key[1:])

    def __getitem__(self, key):
        """
        Traverses the tree to get the object.
        """
        key = key.split('-', 1)
        x = key[0]

        try:
            y = key[1]
        except IndexError:
            return self.children[x]
        else:
            return self.children[x][y]


class AcceptCharset(Root, CharsetNode):
    """
    Implements the Accept-Charset tree.
    """

    def _parse(self, accept):
        Root._parse(self, accept)
        if '*' not in self._ordered_keys and DEFAULT_CHARSET not in self._ordered_keys:
            self._ordered_keys.append(DEFAULT_CHARSET)
            self[DEFAULT_CHARSET] = 1.0

    def _getnode(self, key):
        """
        Behaves like a simple dictionary, only one level.
        """
        if key == '*':
            return self
        return self.children.setdefault(key, CharsetNode())


class AcceptLanguage(Root, LanguageNode):
    """
    Implements the Accept-Language tree.
    """

    def select_language(self, languages):
        """
        This is the selection language algorithm, it returns the user
        prefered language for the given list of available languages,
        if the intersection is void returns None.
        """
        language, quality = None, 0.0

        ordered_languages = set(self.getOrderedKeys()).intersection(languages)
        for lang in languages:
            ordered_languages.add(lang)
        for lang in ordered_languages:
            q = self.get_quality(lang)
            if q > quality:
                language, quality = lang, q

        return language

