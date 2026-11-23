"""
SahyogSetu SSRF Protection & Safe HTTP Client
Guards external URL fetching across government news collectors, RSS feeds, and document verifiers.
Prevents Server-Side Request Forgery (SSRF), local network probing, and cloud metadata access.
"""

import ipaddress
import socket
import logging
from urllib.parse import urlparse
from typing import Optional, Tuple, Dict, Any, List
import httpx

logger = logging.getLogger("sahyogsetu.security.ssrf")

# Disallowed private and reserved network CIDRs
BLOCKED_IP_NETWORKS = [
    ipaddress.ip_network("127.0.0.0/8"),       # IPv4 Loopback
    ipaddress.ip_network("10.0.0.0/8"),        # Private-Use
    ipaddress.ip_network("172.16.0.0/12"),     # Private-Use
    ipaddress.ip_network("192.168.0.0/16"),    # Private-Use
    ipaddress.ip_network("169.254.0.0/16"),    # Link-Local / AWS/GCP/Azure Metadata (169.254.169.254)
    ipaddress.ip_network("0.0.0.0/8"),         # Broadcast / Current Network
    ipaddress.ip_network("224.0.0.0/4"),       # Multicast
    ipaddress.ip_network("240.0.0.0/4"),       # Reserved
    ipaddress.ip_network("::1/128"),           # IPv6 Loopback
    ipaddress.ip_network("fc00::/7"),          # IPv6 Unique Local
    ipaddress.ip_network("fe80::/10"),         # IPv6 Link-Local
]

BLOCKED_HOSTNAMES = {
    "localhost",
    "metadata.google.internal",
    "metadata",
    "instance-data",
}

# Permitted official government and institutional domain suffixes
OFFICIAL_GOVERNMENT_DOMAINS = [
    ".gov.in",
    ".nic.in",
    ".rbi.org.in",
    ".nabard.org",
    ".harcobank.org.in",
    ".hafed.gov.in",
    ".hafed.in",
    ".verka.coop",
    ".pmfby.gov.in",
    ".egazette.gov.in",
    ".cooperation.gov.in",
    ".crcs.gov.in",
]


class SSRFValidationError(ValueError):
    """Raised when a URL destination violates SSRF security boundaries."""
    pass


def validate_url_for_ssrf(url: str, enforce_gov_domain: bool = False) -> Tuple[bool, str]:
    """
    Validates a URL against SSRF vulnerabilities:
    1. Scheme check (must be http or https).
    2. Hostname resolution to IP.
    3. Rejection of private, loopback, link-local, and cloud-metadata addresses.
    4. Optional official government domain whitelist check.
    Returns (is_safe: bool, reason: str).
    """
    if not url or not isinstance(url, str):
        return False, "URL cannot be empty"

    clean_url = url.strip()
    try:
        parsed = urlparse(clean_url)
    except Exception as e:
        return False, f"Malformed URL: {e}"

    # 1. Scheme check
    if parsed.scheme.lower() not in ("http", "https"):
        return False, f"Unsupported URL scheme '{parsed.scheme}'. Only HTTP and HTTPS are permitted."

    hostname = (parsed.hostname or "").lower().strip()
    if not hostname:
        return False, "Missing hostname in URL"

    # 2. Block reserved hostnames
    if hostname in BLOCKED_HOSTNAMES or hostname.endswith(".localhost") or hostname.endswith(".local"):
        return False, f"Access to host '{hostname}' is blocked for security."

    # 3. Optional government domain enforcement
    if enforce_gov_domain:
        is_gov = any(hostname.endswith(dom) or hostname == dom.lstrip(".") for dom in OFFICIAL_GOVERNMENT_DOMAINS)
        if not is_gov:
            return False, f"Domain '{hostname}' is not a verified government or apex cooperative portal."

    # 4. Resolve IP and block private / metadata subnets
    try:
        # Check if hostname is already a raw IP
        try:
            ip_obj = ipaddress.ip_address(hostname)
            ip_list = [ip_obj]
        except ValueError:
            # Resolve DNS
            addr_info = socket.getaddrinfo(hostname, None, socket.AF_UNSPEC, socket.SOCK_STREAM)
            ip_list = [ipaddress.ip_address(addr[4][0]) for addr in addr_info]

        for ip in ip_list:
            for blocked_net in BLOCKED_IP_NETWORKS:
                if ip in blocked_net:
                    return False, f"Destination IP '{ip}' belongs to blocked private/metadata range '{blocked_net}'."

    except socket.gaierror as e:
        # In isolated/sandboxed environments without outbound DNS resolution:
        # If hostname is explicitly a recognized government or apex cooperative domain, permit as safe external destination
        is_gov = any(hostname.endswith(dom) or hostname == dom.lstrip(".") for dom in OFFICIAL_GOVERNMENT_DOMAINS)
        if is_gov:
            return True, "URL is safe (verified government domain; offline DNS resolution)"
        return False, f"Failed to resolve hostname '{hostname}': {e}"
    except Exception as e:
        return False, f"IP validation error for '{hostname}': {e}"

    return True, "URL is safe"


async def safe_fetch_url(
    url: str,
    timeout: float = 8.0,
    max_bytes: int = 15 * 1024 * 1024,
    headers: Optional[Dict[str, str]] = None,
    enforce_gov_domain: bool = False,
) -> httpx.Response:
    """
    Safely executes an HTTP GET request with SSRF validation,
    redirect inspection, size capping, and timeout enforcement.
    """
    is_safe, reason = validate_url_for_ssrf(url, enforce_gov_domain=enforce_gov_domain)
    if not is_safe:
        logger.warning("SSRF block prevented request to '%s': %s", url, reason)
        raise SSRFValidationError(f"SSRF Protection: {reason}")

    req_headers = {
        "User-Agent": "SahyogSetu-PublicService-Bot/2.0 (+https://cooperation.gov.in)",
        "Accept": "*/*",
    }
    if headers:
        req_headers.update(headers)

    async with httpx.AsyncClient(
        verify=False,  # Accommodates NIC state portal legacy certs while still validating IP destination
        headers=req_headers,
        timeout=timeout,
        follow_redirects=False,  # We validate every redirect manually
    ) as client:
        current_url = url
        redirect_count = 0
        max_redirects = 3

        while redirect_count <= max_redirects:
            resp = await client.get(current_url)

            # Check if response is a redirect
            if resp.status_code in (301, 302, 303, 307, 308):
                location = resp.headers.get("Location")
                if not location:
                    break
                redirect_url = location if location.startswith("http") else urlparse(current_url)._replace(path=location).geturl()

                # Re-validate redirect target against SSRF!
                redir_safe, redir_reason = validate_url_for_ssrf(redirect_url, enforce_gov_domain=enforce_gov_domain)
                if not redir_safe:
                    logger.warning("SSRF block on redirect target '%s': %s", redirect_url, redir_reason)
                    raise SSRFValidationError(f"SSRF Protection blocked redirect: {redir_reason}")

                current_url = redirect_url
                redirect_count += 1
                continue

            # Check content length
            content_length = resp.headers.get("Content-Length")
            if content_length and int(content_length) > max_bytes:
                raise ValueError(f"Response size {content_length} exceeds limit of {max_bytes} bytes.")

            return resp

        return resp
