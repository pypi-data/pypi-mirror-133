# fixtures

import pytest


@pytest.fixture
def encoded_url():
    # flake8: noqa: E501
    return (
        "https://linkprotect.cudasvc.com/url?"
        "a=http%3a%2f%2fdeviating.net%2fcontests%2factivate"
        "%2fNjE4OA%2fMw%2f5x5-b8b540205906bef48878%2f&c=E,1,"
        "SZc_GZpWxQ4B8rMJR4emVbg4Xxg7IqZAhevRMWpoAN8AAIY9aZ_7zfPexh"
        "eg5lcCqPJX6-OL79pdEKEfORapm3r8k7E917xh6yCywpcejAbs&typo=1"
    )


@pytest.fixture
def decoded_url():
    return "http://deviating.net/contests/activate/NjE4OA/Mw/5x5-b8b540205906bef48878/"
