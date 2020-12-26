"""Test back references."""

import common
import pytest


@pytest.mark.sphinx('html', testroot='backrefs')
def test_backrefs(app, warning):
    app.build()
    output = (app.outdir / "index.html").read_text()
    match = common.html_citations(name="test0").search(output)
    assert match
    assert match.group('backref') is None
    assert match.group('backref1') is None
    assert match.group('backref2') is None
    assert match.group('backref3') is None
    match = common.html_citations(name="test1").search(output)
    assert match
    assert match.group('backref') is not None
    assert match.group('backref1') is None
    assert match.group('backref2') is None
    assert match.group('backref3') is None
    match = common.html_citations(name="test2").search(output)
    assert match
    assert match.group('backref') is None
    assert match.group('backref1') is not None
    assert match.group('backref2') is not None
    assert match.group('backref3') is None
    match = common.html_citations(name="test3").search(output)
    assert match
    assert match.group('backref') is None
    assert match.group('backref1') is not None
    assert match.group('backref2') is not None
    assert match.group('backref3') is not None
