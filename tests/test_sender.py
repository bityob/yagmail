
def _send_message(**kwargs):
    from tests.test_dkim import _send_msg_with_dkim
    return _send_msg_with_dkim(**kwargs)


def test_sender_verify_line_ending_with_crlf_with_local_smtp_server():
    from smtpdfix.handlers import AuthMessage
    from smtpdfix import SMTPDFix

    class AuthMessageWithRawContent(AuthMessage):
        def prepare_message(self, session, envelope):
            msg = super().prepare_message(session, envelope)
            # Add the received raw content to the message object, so we can verify it later
            msg._raw_content = envelope.content
            return msg
    
    import smtpdfix.controller
    smtpdfix.controller.AuthMessage = AuthMessageWithRawContent

    hostname, port = "127.0.0.1", 8025

    with SMTPDFix(hostname, port) as smtpd:
        _send_message(
            preview_only=False,
            login_mock=False,
            smtp_skip_login=True,
            host=smtpd.hostname,
            port=smtpd.port,
            smtp_ssl=False,
            smtp_starttls=False,
        )

        assert smtpd.messages
        assert len(smtpd.messages) == 1

        received_message = smtpd.messages[0]

        # Verify line ending is `\r\n` and not only `\n` for support with office365
        raw = received_message._raw_content

        import re
        # Assert no line ending with `\r` (CRLF only)
        assert not re.findall(b"[^\r]\n", raw), "Message contains line ending with only '\\n` char"
