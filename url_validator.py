"""
URL validation utilities to prevent SSRF attacks.
"""
from urllib.parse import urlparse
import ipaddress
import socket
from typing import Tuple


def is_safe_url(url: str) -> Tuple[bool, str]:
    """
    Validate URL to prevent SSRF attacks.

    Args:
        url: The URL to validate

    Returns:
        Tuple of (is_valid, error_message)
    """
    try:
        parsed = urlparse(url)

        # Check scheme
        if parsed.scheme not in ['http', 'https']:
            return False, "Only HTTP and HTTPS protocols are allowed"

        # Check if hostname exists
        if not parsed.netloc:
            return False, "Invalid URL: no hostname found"

        # Extract hostname (remove port if present)
        hostname = parsed.netloc.split(':')[0]

        # Resolve hostname to IP
        try:
            ip = socket.gethostbyname(hostname)
        except socket.gaierror:
            return False, f"Cannot resolve hostname: {hostname}"

        # Check if IP is private/internal
        try:
            ip_obj = ipaddress.ip_address(ip)
            if ip_obj.is_private or ip_obj.is_loopback or ip_obj.is_link_local:
                return False, "Access to private/internal IP addresses is not allowed"
        except ValueError:
            return False, "Invalid IP address"

        return True, ""

    except Exception as e:
        return False, f"Invalid URL: {str(e)}"
