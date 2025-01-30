import pytest as pytest

from app.util.name_sanitizer import sanitize_name

test_names_and_results = [
    (
        "\u00E3\u00EF\u00EA", "coj"
    ),
    (
        "yeti", "yeti"
    ),
    (
        "BLooD_DoG(D_P)", "BLooD_DoG(D_P)"
    ),
    (
        "\u00C2ull\u00C4\u0012zer", "BullD0zer"
    ),
    (
        "chris' son", "chris son"
    ),
]


@pytest.mark.parametrize("name, expected_result", test_names_and_results)
def test_sanitize_name(name: str, expected_result: str) -> None:
    assert sanitize_name(name) == expected_result
