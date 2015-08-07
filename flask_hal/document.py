#!/usr/bin/env python
# encoding: utf-8

"""
flask_hal.document
==================

Module for constructing ``HAL`` documents.

Example:
    >>> from flask_hal.document import Document
    >>> d = Document()
    >>> d.to_dict()
"""

# Standard Libs
import json

# First Party Libs
from flask_hal import link


class BaseDocument(object):
    """Constructs a ``HAL`` document.
    """

    def __init__(self, data=None, links=None, embedded=None):
        """Base ``HAL`` Document. If no arguments are provided a minimal viable
        ``HAL`` Document is created.

        Keyword Args:
            data (dict): Data for the document
            links (flask_hal.link.Collection): A collection of ``HAL`` links
            embedded: TBC

        Raises:
            TypeError: If ``links`` is not a :class:`flask_hal.link.Collection`
        """

        self.data = data
        self.embedded = embedded or {}
        self.links = links or link.Collection()

    @property
    def links(self):
        return self._links

    @links.setter
    def links(self, value):
        if not isinstance(value, link.Collection):
            raise TypeError('links must be a {} instance'.format(link.Collection))
        self._links = value

    def to_dict(self):
        """Converts the ``Document`` instance into an appropriate data
        structure for HAL formatted documents.

        Returns:
            dict: The ``HAL`` document data structure
        """

        document = {}

        # Add Data to the Document
        if isinstance(self.data, dict):
            document.update(self.data)

        # Add Links
        if self.links:
            document.update(self.links.to_dict())

        # Add Embedded TODO: Embedded API TBC
        if self.embedded:
            document.update({
                '_embedded': {n: v.to_dict() for n, v in self.embedded.iteritems()}
            })

        return document

    def to_json(self):
        """Converts :class:`.Document` to a ``JSON`` data structure.

        Returns:
            str: ``JSON`` document
        """

        return json.dumps(self.to_dict())


class Document(BaseDocument):
    """Constructs a ``HAL`` document.
    """

    def __init__(self, data=None, links=None, embedded=None):
        """Initialises a new ``HAL`` Document instance. If no arguments are
        provided a minimal viable ``HAL`` Document is created.

        Keyword Args:
            data (dict): Data for the document
            links (flask_hal.link.Collection): A collection of ``HAL`` links
            embedded: TBC

        Raises:
            TypeError: If ``links`` is not a :class:`flask_hal.link.Collection`
        """
        super(Document, self).__init__(data, links, embedded)
        self.links.append(link.Self())


class Embedded(BaseDocument):
    """Constructs a ``HAL`` embedded.
    """
    pass
