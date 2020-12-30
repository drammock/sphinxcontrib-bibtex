"""Test warnings on duplicate labels/keys."""

import common
import pytest


@pytest.mark.sphinx('html', testroot='duplicate_label')
def test_duplicate_label(app, warning):
    # see github issue 14
    app.build()
    assert "duplicate label 1 for keys Test,Test2" in warning.getvalue()
    output = (app.outdir / "doc1.html").read_text()
    output2 = (app.outdir / "doc2.html").read_text()
    assert common.html_citations(label="1").search(output)
    assert common.html_citations(label="1").search(output2)


@pytest.mark.sphinx('html', testroot='duplicate_citation')
def test_duplicate_citation(app, warning):
    app.build()
    warning.seek(0)
    warnings = list(warning.readlines())
    assert len(warnings) == 1
    assert "duplicate citation for key Test" in warnings[0]
    # assure distinct citation ids
    output = (app.outdir / "index.html").read_text()
    ids = [match.group('id_')
           for match in common.html_citations().finditer(output)]
    assert len(ids) == 2  # just to check ids are found
    assert len(set(ids)) == 2, "citation ids not unique"


@pytest.mark.sphinx('html', testroot='duplicate_nearly_identical_entries')
def test_duplicate_nearly_identical_entries(app, warning):
    app.build()
    assert not warning.getvalue()
    output = (app.outdir / "index.html").read_text()
    cits = list(common.html_citations().finditer(output))
    cit_refs = list(common.html_citation_refs().finditer(output))
    assert len(cits) == len(cit_refs) == 2
    assert ({cit.group('label') for cit in cits}
            == {cit_ref.group('label') for cit_ref in cit_refs}
            == {'xyz19a', 'xyz19b'})


@pytest.mark.sphinx('html', testroot='duplicate_nearly_identical_keys')
def test_duplicate_nearly_identical_keys(app, warning):
    app.build()
    assert not warning.getvalue()
    output = (app.outdir / "index.html").read_text()
    # assure both citations and citation references are present
    assert common.html_citation_refs(label='Smi').search(output)
    assert common.html_citation_refs(label='Pop').search(output)
    assert common.html_citation_refs(label='Ein').search(output)
    assert common.html_citations(label='Smi').search(output)
    assert common.html_citations(label='Pop').search(output)
    assert common.html_citations(label='Ein').search(output)
    # assure distinct ids for citations
    ids = {match.group('id_')
           for match in common.html_citations().finditer(output)}
    refids = {match.group('refid')
              for match in common.html_citation_refs().finditer(output)}
    assert None not in ids
    assert len(ids) == 3
    assert ids == refids


# this test "accidentally" includes a user provided id which
# clashes with a bibtex generated citation id
@pytest.mark.sphinx('html', testroot='duplicate_citation_id')
def test_duplicate_citation_id(app, warning):
    app.build()
    assert not warning.getvalue()
    output = (app.outdir / "index.html").read_text()
    user_ids = {'id1', 'id2', 'id3'}
    ids = {match.group('id_')
           for match in common.html_citations().finditer(output)}
    refids = {match.group('refid')
              for match in common.html_citation_refs().finditer(output)}
    assert ids == refids
    assert len(ids) == 1
    assert not (user_ids & ids)