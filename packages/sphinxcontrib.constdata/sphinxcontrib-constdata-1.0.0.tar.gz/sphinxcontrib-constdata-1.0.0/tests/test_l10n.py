from pathlib import Path

import pytest
from sphinx.application import Sphinx

from tests.conftest import assert_file_contains_fragment


@pytest.mark.xfail(reason="Locally passes, on GitLab CI failed with 'assert 0 == 1'")
@pytest.mark.sphinx("gettext", testroot="l10n")
def test_pot_generation(app: Sphinx, status, warning):
    """Properly extract translatable from all flatfiles messages to .pot, not only those used in documents"""
    app.build()

    assert_file_contains_fragment(
        Path(app.outdir, "constdata.pot"),
        Path(app.srcdir, "expected_pot_fragment.pot"),
    )


@pytest.mark.xfail(
    reason="""Sometimes causes
            sphinx.errors.SphinxError: This environment is incompatible with the selected builder, please choose another doctree directory.
        Sometimes not. Asked in sphinx-dev
        https://groups.google.com/u/1/g/sphinx-dev/c/ybAgTEl4GyU, but still not sure how to fix it.
    """
)
@pytest.mark.sphinx("html", testroot="l10n", confoverrides={"language": "cs"})
def test_translation(app: Sphinx, status, warning):
    """Translation works. Test that translatable CSV/JSON/YAML table/link/label produce the same output."""
    app.build()

    assert_file_contains_fragment(
        Path(app.outdir, "index.html"), Path(app.srcdir, "expected_html_tables.html")
    )

    assert_file_contains_fragment(
        Path(app.outdir, "index.html"),
        Path(app.srcdir, "expected_html_links.html"),
    )

    assert_file_contains_fragment(
        Path(app.outdir, "index.html"),
        Path(app.srcdir, "expected_html_labels.html"),
    )
