"""
From:
https://stackoverflow.com/questions/7160737/how-to-validate-a-url-in-python-malformed-or-not
and
https://stackoverflow.com/questions/319279/how-to-validate-ip-address-in-python/319293#319293
"""
import re
import socket
from urllib.parse import urlparse


# Check https://regex101.com/r/A326u1/5 for reference
DOMAIN_FORMAT = re.compile(
    r"(?:^(\w{1,255}):(.{1,255})@|^)" # http basic authentication [optional]
    r"(?:(?:(?=\S{0,253}(?:$|:))" # check full domain length to be less than or equal to 253 (starting after http basic auth, stopping before port)
    r"((?:[a-z0-9](?:[a-z0-9-]{0,61}[a-z0-9])?\.)+" # check for at least one subdomain (maximum length per subdomain: 63 characters), dashes in between allowed
    r"(?:[a-z0-9]{1,63})))" # check for top level domain, no dashes allowed
    r"|localhost)" # accept also "localhost" only
    r"(:\d{1,5})?", # port [optional]
    re.IGNORECASE
)
SCHEME_FORMAT = re.compile(
    r"^(http|hxxp|ftp|fxp)s?$", # scheme: http(s) or ftp(s)
    re.IGNORECASE
)


def is_valid_ipv4_address(address: str) -> bool:
    try:
        socket.inet_pton(socket.AF_INET, address)
    except AttributeError:  # no inet_pton here, sorry
        try:
            socket.inet_aton(address)
        except socket.error:
            return False
        return address.count('.') == 3
    except socket.error:  # not a valid address
        return False
    return True


def is_valid_ipv6_address(address: str) -> bool:
    try:
        socket.inet_pton(socket.AF_INET6, address)
    except socket.error:  # not a valid address
        return False
    return True


def validate_url(url: str):
    # На будущее нужно:
    # Определение IP адреса
    # Внедрить проверку IPv4 и IPv6
    url = url.strip()
    if not url:
        raise Exception("No URL specified")
    if len(url) > 2048:
        raise Exception("URL exceeds its maximum length of 2048 characters (given length={})".format(len(url)))
    result = urlparse(url)
    scheme = result.scheme
    domain = result.netloc
    if not scheme:
        raise Exception("No URL scheme specified")
    if not re.fullmatch(SCHEME_FORMAT, scheme):
        raise Exception("URL scheme must either be http(s) or ftp(s) (given scheme={})".format(scheme))
    if not domain:
        raise Exception("No URL domain specified")
    if not re.fullmatch(DOMAIN_FORMAT, domain):
        raise Exception("URL domain malformed (domain={})".format(domain))
    return url
