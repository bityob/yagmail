import logging
from pathlib import Path
import re

import dkim

from yagmail.message import prepare_message


def test_prepare_message_hello_world_without_formatting():
    user = "username@domain.com"
    useralias = "John Doe"
    addresses = {
        "To": "dest@other.domain.com",
    }
    subject = "fake-subject"
    contents = "Hello World"
    attachments = None
    headers = None
    encoding = "utf-8"

    msg = prepare_message(
        user,
        useralias,
        addresses,
        subject,
        contents,
        attachments,
        headers,
        encoding,
        text_only_without_formatting=True,
    )

    expected_output = Path("message_hello_world_without_formatting.txt").read_text()

    # Remove random boundary value
    message_without_random_boundary_value = re.sub("\d{19}", "", str(msg))

    assert expected_output == message_without_random_boundary_value


def test_prepare_message_hello_world_with_formatting():
    user = "username@domain.com"
    useralias = "John Doe"
    addresses = {
        "To": "dest@other.domain.com",
    }
    subject = "fake-subject"
    contents = "Hello World"
    attachments = None
    headers = {
        "Date": "Thu, 13 Jan 2022 19:28:36 -0000",
    }
    encoding = "utf-8"

    msg = prepare_message(
        user,
        useralias,
        addresses,
        subject,
        contents,
        attachments,
        headers,
        encoding,
        text_only_without_formatting=False,
    )

    expected_output = Path("message_hello_world_with_formatting.txt").read_text()

    # Remove random boundary value
    message_without_random_boundary_value = re.sub("\d{19}", "", str(msg))

    assert expected_output == message_without_random_boundary_value


def test_prepare_message_html_file_without_formatting():
    user = "username@domain.com"
    useralias = "John Doe"
    addresses = {
        "To": "dest@other.domain.com",
    }
    subject = "fake-subject"
    contents = Path("example.html").read_text()
    attachments = None
    headers = None
    encoding = "utf-8"

    msg = prepare_message(
        user,
        useralias,
        addresses,
        subject,
        contents,
        attachments,
        headers,
        encoding,
        text_only_without_formatting=True,
    )

    expected_output = Path("message_html_file_without_formatting.txt").read_text()

    # Remove random boundary value
    message_without_random_boundary_value = re.sub("\d{19}", "", str(msg))

    assert expected_output == message_without_random_boundary_value


def test_prepare_message_html_file_with_formatting():
    user = "username@domain.com"
    useralias = "John Doe"
    addresses = {
        "To": "dest@other.domain.com",
    }
    subject = "fake-subject"
    contents = Path("example.html").read_text()
    attachments = None
    headers = {
        "Date": "Thu, 13 Jan 2022 19:43:22 -0000",
    }
    encoding = "utf-8"

    msg = prepare_message(
        user,
        useralias,
        addresses,
        subject,
        contents,
        attachments,
        headers,
        encoding,
        text_only_without_formatting=False,
        # prettify html causes a lot of errors, ignore this usage when using formatting with html
        prettify_html=False,
    )

    expected_output = Path("message_html_file_with_formatting.txt").read_text()

    # Remove random boundary value
    message_without_random_boundary_value = re.sub("\d{19}", "", str(msg))

    assert expected_output == message_without_random_boundary_value


def test_prepare_message_html_file_without_formatting_and_dkim():
    user = "username@domain.com"
    useralias = "John Doe"
    addresses = {
        "To": "dest@other.domain.com",
    }
    subject = "fake-subject"
    contents = Path("example.html").read_text()
    attachments = None
    headers = None
    encoding = "utf-8"

    from yagmail.dkim import DKIM

    private_key_path = Path(__file__).parent / "privkey.pem"

    private_key = private_key_path.read_bytes()

    dkim_obj = DKIM(
        domain=b"a.com",
        selector=b"selector",
        private_key=private_key,
        include_headers=[b"To", b"From", b"Subject"]
    )

    msg = prepare_message(
        user,
        useralias,
        addresses,
        subject,
        contents,
        attachments,
        headers,
        encoding,
        text_only_without_formatting=True,
        dkim=dkim_obj,
    )

    expected_output = Path("message_html_file_without_formatting_and_dkim.txt").read_text()

    # Remove random boundary value
    msg_without_random_data = re.sub("\d{19}", "", str(msg))

    msg_without_random_data = re.sub("t=\d{10}", "t=1642107621", msg_without_random_data)

    pattern = re.compile("bh=.*?--=================", re.MULTILINE | re.DOTALL)

    msg_without_random_data = pattern.sub("\n--=================", msg_without_random_data)

    assert expected_output == msg_without_random_data

    msg_string = str(msg)

    from test_dkim import get_txt_from_test_file

    assert dkim.verify(
        message=msg_string.encode("utf8"),
        logger=logging.getLogger(),
        dnsfunc=get_txt_from_test_file
    )
