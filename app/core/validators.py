import ipaddress
import re
import socket
from urllib.parse import urlparse

from app.core.config import settings
from app.core.exceptions import InvalidURLException


def validate_media_url(url: str) -> str:
    try:
        parsed = urlparse(url)
    except Exception:
        raise InvalidURLException("Invalid URL format.")

    if parsed.scheme not in ("http", "https"):
        raise InvalidURLException("Only http and https URLs are allowed.")

    hostname = parsed.hostname
    if not hostname:
        raise InvalidURLException("URL has no valid hostname.")

    _check_allowlist(parsed.netloc)
    _check_host(hostname)

    return url


def _check_allowlist(netloc: str) -> None:
    domain = re.sub(r"^www\.", "", netloc.lower())
    allowed = [re.sub(r"^www\.", "", h.lower()) for h in settings.ALLOWED_HOSTS]

    if not any(domain == h or domain.endswith(f".{h}") for h in allowed):
        raise InvalidURLException(
            f"Domain '{netloc}' is not in the list of allowed domains."
        )


def _check_host(hostname: str) -> None:
    try:
        _assert_public_ip(ipaddress.ip_address(hostname))
        return
    except ValueError:
        pass

    try:
        results = socket.getaddrinfo(hostname, None)
    except socket.gaierror:
        raise InvalidURLException(f"Could not resolve domain '{hostname}'.")

    for *_, sockaddr in results:
        _assert_public_ip(ipaddress.ip_address(sockaddr[0]))


def _assert_public_ip(addr: ipaddress.IPv4Address | ipaddress.IPv6Address) -> None:
    if (
        addr.is_private
        or addr.is_loopback
        or addr.is_link_local
        or addr.is_reserved
        or addr.is_unspecified
    ):
        raise InvalidURLException(
            "URLs pointing to private or reserved IP addresses are not allowed."
        )