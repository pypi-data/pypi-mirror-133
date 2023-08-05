from typing import Any

from .. import mqtt as mqtt

def multiple(
    msgs,
    hostname: str = ...,
    port: int = ...,
    client_id: str = ...,
    keepalive: int = ...,
    will: Any | None = ...,
    auth: Any | None = ...,
    tls: Any | None = ...,
    protocol=...,
    transport: str = ...,
    proxy_args: Any | None = ...,
) -> None: ...
def single(
    topic,
    payload: Any | None = ...,
    qos: int = ...,
    retain: bool = ...,
    hostname: str = ...,
    port: int = ...,
    client_id: str = ...,
    keepalive: int = ...,
    will: Any | None = ...,
    auth: Any | None = ...,
    tls: Any | None = ...,
    protocol=...,
    transport: str = ...,
    proxy_args: Any | None = ...,
) -> None: ...
