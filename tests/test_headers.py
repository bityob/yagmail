import yagmail
from yagmail.headers import make_addr_alias_user

import pytest


@pytest.mark.parametrize("user_input, email_output, name_output", [
    ("a@a.com", "a@a.com", "a@a.com"),
    ("A B <a@a.com>", "a@a.com", "A B"),
    ("C D <aaa.com>", None, None),
    ("bla-bla", None, None),
    ({}, None, None),
    ([], None, None),
])
def test_make_addr_alias_user(user_input, email_output, name_output):
    if not email_output or not name_output:
        with pytest.raises(yagmail.YagAddressError):
            make_addr_alias_user(user_input)
    else:
        assert make_addr_alias_user(user_input) == (email_output, name_output)

