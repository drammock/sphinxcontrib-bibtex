# -*- coding: utf-8 -*-
"""
    test_citationnotfound
    ~~~~~~~~~~~~~~~~~~~~~

    Citation not found check.
"""

import pytest


@pytest.mark.sphinx('html', testroot='citationnotfound')
def test_citationnotfound(app, warning):
    app.builder.build_all()
    assert 'could not find bibtex key nosuchkey1' in warning.getvalue()
    assert 'could not find bibtex key nosuchkey2' in warning.getvalue()
