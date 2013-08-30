# -*- coding: utf-8 -*-
"""
    Cached Information
    ~~~~~~~~~~~~~~~~~~

    Classes and methods to maintain any information that is stored
    outside the doctree.

    .. autoclass:: Cache
        :members:

    .. autoclass:: BibfileCache
        :members:

    .. autoclass:: BibliographyCache
        :members:
"""

import collections
from oset import oset
import pybtex.database


class Cache:

    """Global bibtex extension information cache. Stored in
    ``app.env.bibtex_cache``, so must be picklable.

    .. attribute:: bibfiles

        A :class:`dict` mapping .bib file names (relative to the top
        source folder) to :class:`BibfileCache` instances.

    .. attribute:: _bibliographies

        Each bibliography directive is assigned an id of the form
        bibtex-bibliography-xxx. This :class:`dict` maps each docname
        to another :class:`dict` which maps each id
        to information about the bibliography directive,
        :class:`BibliographyCache`. We need to store this extra
        information separately because it cannot be stored in the
        :class:`~sphinxcontrib.bibtex.nodes.bibliography` nodes
        themselves.

    .. attribute:: _cited

        A :class:`dict` mapping each docname to a :class:`set` of
        citation keys.

    .. attribute:: _enum_count

        A :class:`dict` mapping each docname to an :class:`int`
        representing the current bibliography enumeration counter.

    """

    def __init__(self):

        self.bibfiles = {}
        self._bibliographies = collections.defaultdict(dict)
        self._cited = collections.defaultdict(oset)
        self._enum_count = {}

    def purge(self, docname):
        """Remove  all information related to *docname*.

        :param docname: The document name.
        :type docname: :class:`str`
        """
        self._bibliographies.pop(docname, None)
        self._cited.pop(docname, None)
        self._enum_count.pop(docname, None)

    def inc_enum_count(self, docname):
        """Increment enumeration list counter for document *docname*."""
        self._enum_count[docname] += 1

    def set_enum_count(self, docname, value):
        """Set enumeration list counter for document *docname* to *value*."""
        self._enum_count[docname] = value

    def get_enum_count(self, docname):
        """Get enumeration list counter for document *docname*."""
        return self._enum_count[docname]

    def add_cited(self, key, docname):
        """Add the given *key* to the set of cited keys for
        *docname*.

        :param key: The citation key.
        :type key: :class:`str`
        :param docname: The document name.
        :type docname: :class:`str`
        """
        self._cited[docname].add(key)

    def is_cited(self, key):
        """Return whether the given key is cited in any document.

        :param key: The citation key.
        :type key: :class:`str`
        """
        for keys in self._cited.itervalues():
            if key in keys:
                return True
        return False

    def get_label_from_key(self, key):
        """Return label for the given key."""
        for info in self.get_all_bibliography_caches():
            if key in info.labels:
                return info.labels[key]
        else:
            raise KeyError("%s not found" % key)

    def get_all_cited_keys(self):
        """Yield all citation keys, sorted first by document
        (alphabetical), then by citation order in the document.
        """
        for docname in sorted(self._cited):
            for key in self._cited[docname]:
                yield key

    def set_bibliography_cache(self, docname, id_, bibcache):
        """Register *bibcache* (:class:`BibliographyCache`)
        with id *id_* for document *docname*.
        """
        assert id_ not in self._bibliographies[docname]
        self._bibliographies[docname][id_] = bibcache

    def get_bibliography_cache(self, docname, id_):
        """Return :class:`BibliographyCache` with id *id_* in
        document *docname*.
        """
        return self._bibliographies[docname][id_]

    def get_all_bibliography_caches(self):
        """Return all bibliography caches."""
        for bibcaches in self._bibliographies.itervalues():
            for bibcache in bibcaches.itervalues():
                yield bibcache

class BibfileCache:

    """Contains information about a parsed .bib file.

    .. attribute:: mtime

        A :class:`float` representing the modification time of the .bib
        file when it was last parsed.

    .. attribute:: data

        A :class:`pybtex.database.BibliographyData` containing the
        parsed .bib file.

    """

    def __init__(self, mtime=None, data=None):
        self.mtime = mtime if mtime is not None else -float("inf")
        self.data = (data if data is not None
                     else pybtex.database.BibliographyData())


class BibliographyCache:

    """Contains information about a bibliography directive.

    .. attribute:: bibfiles

        A :class:`list` of :class:`str`\\ s containing the .bib file
        names (relative to the top source folder) that contain the
        references.

    .. attribute:: style

        The bibtex style.

    .. attribute:: list_

        The list type.

    .. attribute:: enumtype

        The sequence type (only used for enumerated lists).

    .. attribute:: start

        The first ordinal of the sequence (only used for enumerated lists).

    .. attribute:: labels

        Maps citation keys to their final labels.

    .. attribute:: labelprefix

        This bibliography's string prefix for pybtex generated labels.

    .. attribute:: filter_

        An :class:`ast.AST` node, containing the parsed filter expression.
    """

    def __init__(self, bibfiles=None,
                 style=None,
                 list_="citation", enumtype="arabic", start=1,
                 labels=None,
                 encoding=None,
                 curly_bracket_strip=True,
                 labelprefix="",
                 filter_=None,
                 ):
        self.bibfiles = bibfiles if bibfiles is not None else []
        self.filter_ = filter_
        self.style = style
        self.list_ = list_
        self.enumtype = enumtype
        self.start = start
        self.encoding = encoding
        self.curly_bracket_strip = curly_bracket_strip
        self.labels = labels if labels is not None else {}
        self.labelprefix = labelprefix
