"""Main module."""

from requests.utils import unquote, urlparse

"""known keys in query section of encoded URL"""
QUERY_KEYS = ["a", "c", "typo"]


class URL:
    def __init__(self, encoded_url=None):
        self.url = self.decode(encoded_url)

    def __str__(self):
        return self.decode()

    def decode(self, encoded_url=None):
        self.encoded = encoded_url or self.encoded
        query = _decode(self.encoded)
        self.url = query["a"]
        self.cookie = query["c"]
        self.typo_flag = query["typo"]
        return self.url


def _decode(encoded_url):
    parsed = urlparse(encoded_url)
    try:
        message = "URL does not appear to be LinkProtect encoded"
        assert parsed.scheme == "https", message
        assert parsed.netloc == "linkprotect.cudasvc.com", message
        assert parsed.path == "/url", message
        assert parsed.params == "", message
        query = {}
        for el in parsed.query.split("&"):
            assert el.count("=") == 1, "query element not in key=value format"
            key, value = el.split("=")
            assert key in QUERY_KEYS, f"unknown query key: {key}"
            query[key] = unquote(value)
    except AssertionError as e:
        raise ValueError(e.args[0]) from e
    return query


def decode(encoded_url: str) -> str:
    """decode a linkprotect url

    Args:
      encoded_url: a linkprotect-encoded URL

    Returns:
      The original URL from the message source

    Raises:
      ValueError: if encoded_url has an unexpected format or parsing fails
    """
    return _decode(encoded_url)["a"]
