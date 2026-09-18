from __future__ import annotations

from scripts import vendor_utopia_fonts as vendor


def test_vendored_utopia_archives_have_expected_structure() -> None:
    info = vendor.inspect_archives()

    assert info["missing_expected_utopia_files"] == []
    assert info["psnfss_has_freenfss_zip"] is True
    assert info["psnfss_has_psfonts_ins"] is True
    assert info["psnfss_has_psfonts_dtx"] is True
    assert info["psnfss_has_utopia_map"] is True
    assert info["psnfss_has_8r_enc"] is True
    assert info["mathastext_dtx_present"] is True
