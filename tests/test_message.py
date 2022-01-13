from pathlib import Path
import re


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
