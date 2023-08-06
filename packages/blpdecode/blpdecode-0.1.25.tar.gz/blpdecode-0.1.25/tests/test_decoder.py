# decoder test

from blpdecode import decode


def test_decode(encoded_url, decoded_url):
    url = decode(encoded_url)
    assert url == decoded_url
