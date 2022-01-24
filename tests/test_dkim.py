import base64
import logging
from pathlib import Path
from unittest.mock import Mock

import dkim as dkimpy


to = "b@b.com"


def get_txt_from_test_file(*args, **kwargs):
    dns_data_file = Path(__file__).parent / "domainkey-dns.txt"

    return Path(dns_data_file).read_bytes()


def _send_msg_with_dkim(preview_only: bool,
                        login_mock: bool = True,
                        smtp_skip_login: bool = False,
                        host: str = "smtp.blabla.com",
                        port: int = 25,
                        smtp_ssl: bool = False,
                        smtp_starttls: bool = True,
                        ):
    from yagmail import SMTP
    from yagmail.dkim import DKIM

    private_key_path = Path(__file__).parent / "privkey.pem"
    private_key = private_key_path.read_bytes()

    dkim_obj = DKIM(
        domain=b"a.com",
        selector=b"selector",
        private_key=private_key,
        include_headers=[b"To", b"From", b"Subject"]
    )

    yag = SMTP(
        user="a@a.com",
        host=host,
        port=port,
        dkim=dkim_obj,
        smtp_skip_login=smtp_skip_login,
        smtp_ssl=smtp_ssl,
        smtp_starttls=smtp_starttls,
    )

    if login_mock:
        yag.login = Mock()

    return yag.send(
        to=to,
        subject="hello from tests",
        contents="important message",
        preview_only=preview_only,
    )


def test_msg_with_dkim():
    recipients, msg = _send_msg_with_dkim(preview_only=True, login_mock=True, smtp_skip_login=False)

    msg_string = msg.as_string()

    assert recipients == [to]
    assert "Subject: hello from tests" in msg_string

    text_b64 = base64.b64encode(b"important message").decode("utf8")
    assert text_b64 in msg_string

    dkim_string1 = "DKIM-Signature: v=1; a=rsa-sha256; c=relaxed/simple; d=a.com; i=@a.com;\n " \
                   "q=dns/txt; s=selector; t="
    assert dkim_string1 in msg_string

    dkim_string2 = "h=to : from : subject;"
    assert dkim_string2 in msg_string

    l = logging.getLogger()
    l.setLevel(level=logging.DEBUG)
    logging.basicConfig(level=logging.DEBUG)

    assert dkimpy.verify(
        message=msg.as_bytes(),
        logger=l,
        dnsfunc=get_txt_from_test_file
    )
