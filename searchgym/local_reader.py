"""Fail closed unless the fetch server has a reachable local Jina Reader."""
from __future__ import annotations

import http.client
import ipaddress
import json
import os
from urllib.parse import urlsplit

_LOCAL_NETS = tuple(ipaddress.ip_network(n) for n in (
    "127.0.0.0/8", "10.0.0.0/8", "172.16.0.0/12", "192.168.0.0/16",
    "100.64.0.0/10", "::1/128", "fc00::/7",
))
# A self-hosted Reader on a RunPod pod, reached through RunPod's HTTPS proxy
# (https://<pod-id>-<port>.proxy.runpod.net). Still our own Reader, not hosted Jina.
RUNPOD_PROXY_SUFFIX = ".proxy.runpod.net"


def _is_runpod_proxy(parsed) -> bool:
    host = parsed.hostname or ""
    return (parsed.scheme == "https" and host.endswith(RUNPOD_PROXY_SUFFIX)
            and len(host) > len(RUNPOD_PROXY_SUFFIX) and parsed.port in (None, 443))


def reader_uses_post(base_url: str) -> bool:
    """RunPod's proxy turns '/https://x' into '/https:/x' with a 307 redirect, so the
    target URL goes in a JSON body there. Local Readers keep the original GET form."""
    return _is_runpod_proxy(urlsplit(base_url))


def local_reader_url(value: str) -> str:
    """Require an explicit loopback/LAN/Tailscale address or our RunPod pod; never hosted."""
    value = (value or "").strip().rstrip("/")
    try:
        parsed = urlsplit(value)
        host = parsed.hostname
        parsed.port  # Reject malformed ports before starting a run.
        local = host == "localhost" or _is_runpod_proxy(parsed)
        if not local and host:
            address = ipaddress.ip_address(host)
            local = any(address in net for net in _LOCAL_NETS)
        if (not local or parsed.scheme not in ("http", "https") or
                parsed.username is not None or parsed.password is not None or
                parsed.query or parsed.fragment):
            raise ValueError("not a local Reader URL")
    except ValueError:
        raise RuntimeError(
            "Local Jina is required. Set JINA_BASE_URL to the Reader's explicit "
            "localhost, LAN or Tailscale IP URL, or https://<pod-id>-<port>.proxy.runpod.net. "
            "Missing/public addresses are blocked."
        ) from None
    return value


def decision_server_url(value: str) -> str:
    """Our self-hosted decision server: a local URL as above. With
    DECISION_ALLOW_PUBLIC_IP=1 in .env, also a RunPod TCP port (http://<public-ip>:<port>).
    Off by default so machines that must stay local keep failing closed."""
    value = (value or "").strip().rstrip("/")
    from .paths import load_env
    load_env()
    if os.getenv("DECISION_ALLOW_PUBLIC_IP", "").strip() != "1":
        try:
            return local_reader_url(value)
        except RuntimeError:
            raise RuntimeError(
                f"jev_base_url {value!r} is not local/LAN/Tailscale or a RunPod HTTPS proxy. "
                "For a RunPod TCP port (http://<public-ip>:<port>) set DECISION_ALLOW_PUBLIC_IP=1 in .env."
            ) from None
    try:
        return local_reader_url(value)
    except RuntimeError:
        pass
    try:
        parsed = urlsplit(value)
        ipaddress.ip_address(parsed.hostname or "")
        if (parsed.scheme not in ("http", "https") or parsed.port is None or
                parsed.username is not None or parsed.password is not None or
                parsed.query or parsed.fragment or parsed.path):
            raise ValueError
    except ValueError:
        raise RuntimeError("jev_base_url must be http://<ip>:<port> (local, LAN, Tailscale or a RunPod TCP port) "
                           "or https://<pod-id>-<port>.proxy.runpod.net") from None
    return value


def probe_local_reader(base_url: str) -> None:
    """Check Jina's root metadata without fetching a website or following redirects."""
    base_url = local_reader_url(base_url)
    parsed = urlsplit(base_url)
    cls = http.client.HTTPConnection if parsed.scheme == "http" else http.client.HTTPSConnection
    conn = cls(parsed.netloc, timeout=8)
    try:
        conn.request("GET", (parsed.path.rstrip("/") or "") + "/",
                     headers={"Accept": "application/json"})
        response = conn.getresponse()
        if response.status != 200:
            raise ValueError(f"HTTP {response.status}")
        payload = json.loads(response.read(65537))
        data = payload.get("data") if isinstance(payload, dict) else None
        if (payload.get("code") != 200 or not isinstance(data, dict) or
                data.get("homepage", "").rstrip("/") != "https://jina.ai/reader"):
            raise ValueError("response is not Jina Reader metadata")
    except (OSError, ValueError, AttributeError, http.client.HTTPException) as exc:
        raise RuntimeError(f"Local Jina preflight failed at {base_url}: {exc}. Run blocked.") from exc
    finally:
        conn.close()
