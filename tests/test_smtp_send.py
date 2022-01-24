""" Testing module for yagmail """
import itertools

import pytest

from yagmail import SMTP
from yagmail import raw

user_name = "a@a.com"


def get_combinations():
    """ Creates permutations of possible inputs """
    tos = (
        None,
        (user_name),
        [user_name, user_name],
        {user_name: '"me" <{}>'.format(user_name),
         user_name + '1': '"me" <{}>'.format(user_name)},
    )
    subjects = ('subj', ['subj'], ['subj', 'subj1'])
    contents = (
        None,
        ['body'],
        ['body', 'body1', '<h2><center>Text</center></h2>', u"<h1>\u2013</h1>"],
        [raw("body")],
        [{"a": 1}],
    )
    results = []
    for row in itertools.product(tos, subjects, contents):
        options = {y: z for y, z in zip(['to', 'subject', 'contents'], row)}
        options['preview_only'] = True
        results.append(options)

    return results


@pytest.mark.parametrize("combination", get_combinations())
def test_send(combination, smtpd):
    yag = SMTP(
        host=smtpd.hostname,
        port=smtpd.port,
        smtp_skip_login=True,
        soft_email_validation=False,
        smtp_ssl=False,
        smtp_starttls=False,
    )

    print(yag.send(
        **combination
    ))
