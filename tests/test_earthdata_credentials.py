from hantavirus_predictor.ingest.earthdata import _extract_value


def test_extract_earthdata_credential_values():
    text = "username: test_user\npassword = s3cret\n"

    assert _extract_value(text, ("username", "user")) == "test_user"
    assert _extract_value(text, ("password", "pass")) == "s3cret"
